"""Manifest-driven judgement runner: resumable, deduplicating, spend-capped.

Every call is identified by a stable cell id:

    (episode_id, view, model, rep)

The runner reads every existing result file first, builds the set of cells that
already hold a VALID parsed answer, and issues calls only for cells that do not.
That makes it safe to stop at any point and safe to relaunch: nothing already
paid for is bought twice, and nothing already collected is overwritten.

Guards, each added for a failure that actually happened in this project:

  * `save()` appends, so re-running into a live file silently mixed two runs.
    Cells are now deduplicated by id on load, and a resumed run skips them.
  * A schema error made every call 400 before it was billed - 20 calls x 3
    attempts. A canary of the first N calls runs sequentially and must validate
    before the batch fans out. Canary results are KEPT; they are not extra.
  * A cache write costs 1.25x and only pays off on a later read, so k=1 runs
    were paying a 25% surcharge for nothing. Caching is gated on reps > 1.
  * The call cap counts DISPATCHED calls, including retries, not completed
    ones, so a run cannot overshoot while failures retry.
"""
from __future__ import annotations
import argparse, json, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import views as V
from investigator import CallTracker, run_package, missingness


def existing_cells(paths: list[Path]) -> dict[tuple, dict]:
    """Valid judgements already collected, keyed by cell id. Malformed ignored."""
    out = {}
    for p in paths:
        if not p.exists():
            continue
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if not r.get("answers"):
                continue                      # malformed: stays missing, not valid
            out[(r["episode_id"], r["view"], r["model"], r["rep"])] = r
    return out


def select(data: Path, contrast_only: bool, corrupted_only: bool) -> list[Path]:
    eps = []
    for ep in sorted(data.glob("*")):
        mf = ep / "manifest.json"
        if not mf.exists():
            continue
        m = json.loads(mf.read_text())
        if corrupted_only and not any(g.get("corrupted") for g in m["agents"].values()):
            continue
        if contrast_only:
            try:
                if V.build_package(ep, "V1").text == V.build_package(ep, "V1R").text:
                    continue                  # corruption was a no-op: nothing to repair
            except Exception as exc:                                 # noqa: BLE001
                # An episode that cannot be rendered must not vanish from the
                # manifest without a word, or the run would silently cover
                # fewer episodes than requested.
                print(f"  skipping {ep.name}: package build failed "
                      f"({type(exc).__name__}: {exc})")
                continue
        eps.append(ep)
    return eps


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--views", required=True)
    p.add_argument("--reps", type=int, default=1)
    p.add_argument("--model", default="claude-sonnet-5")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--also-read", nargs="*", default=[],
                   help="other result files to count as already-collected")
    p.add_argument("--episodes", type=int, default=10_000)
    p.add_argument("--contrast-only", action="store_true")
    p.add_argument("--corrupted-only", action="store_true")
    p.add_argument("--concurrency", type=int, default=8)
    p.add_argument("--max-calls", type=int, required=True,
                   help="hard ceiling on dispatched calls, retries included")
    p.add_argument("--canary", type=int, default=5)
    p.add_argument("--base-url", default=None,
                   help="OpenAI-compatible endpoint for a cross-family replication; "
                        "omit for Anthropic")
    p.add_argument("--key-env", default=None,
                   help="env var holding the key for --base-url")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    views_ = [v.strip() for v in a.views.split(",") if v.strip()]
    eps = select(a.data, a.contrast_only, a.corrupted_only)[: a.episodes]
    have = existing_cells([a.out] + [Path(x) for x in a.also_read])

    # ---- manifest: exactly the missing cells, grouped per package
    manifest, skipped = [], 0
    for ep in eps:
        m = json.loads((ep / "manifest.json").read_text())
        for v in views_:
            need = [r for r in range(a.reps)
                    if (ep.name, v, a.model, r) not in have]
            skipped += a.reps - len(need)
            if need:
                manifest.append((ep, sorted(m["agents"]), v, need))
    n_calls = sum(len(x[3]) for x in manifest)

    print(f"episodes={len(eps)} views={views_} reps={a.reps}")
    print(f"already collected : {skipped} cells (skipped)")
    print(f"to issue          : {n_calls} calls across {len(manifest)} packages")
    for ep, _, v, need in manifest[:3]:
        print(f"   e.g. {ep.name} {v} reps={need}")

    if n_calls > a.max_calls:
        print(f"REFUSING: {n_calls} calls exceeds the --max-calls ceiling of "
              f"{a.max_calls}. Narrow the scope or raise the ceiling.")
        raise SystemExit(2)
    if a.dry_run or not n_calls:
        return

    if a.base_url:
        # Provider SDKs are imported here, not at module scope: the offline
        # reproduction imports this module for `existing_cells` and must not
        # require either package to be installed.
        import os
        from openai import OpenAI
        key = os.environ.get(a.key_env or "", "")
        if not key:
            print(f"REFUSING: --base-url given but {a.key_env} is unset.")
            raise SystemExit(2)

        def client():
            return OpenAI(base_url=a.base_url, api_key=key)
    else:
        from config import anthropic_key
        import anthropic

        def client():
            return anthropic.Anthropic(api_key=anthropic_key())

    tracker = CallTracker()
    lock = threading.Lock()
    done = 0
    dispatched = 0
    stop = threading.Event()

    def flush(rs):
        with lock:
            with a.out.open("a") as f:
                for r in rs:
                    f.write(json.dumps(asdict(r)) + "\n")

    def one(job):
        nonlocal done, dispatched
        ep, agent_ids, v, need = job
        if stop.is_set():
            return []
        with lock:
            dispatched += len(need)
        pkg = V.build_package(ep, v)                 # re-asserts no leakage
        rs = run_package(client(), a.model, ep.name, v, pkg.text,
                         agent_ids, a.reps, tracker, reps=need)
        flush(rs)
        with lock:
            done += 1
            bad = sum(1 for r in rs if not r.answers)
            print(f"[{done}/{len(manifest)} calls={tracker.calls:<4}] {ep.name} {v:<4} "
                  f"ok={len(rs)-bad}/{len(rs)}", flush=True)
        return rs

    # ---- canary: first N calls sequential; results are kept, not discarded
    t0 = time.time()
    head, tail = manifest[:max(1, a.canary)], manifest[max(1, a.canary):]
    got = []
    for job in head:
        got += one(job)
    ok = sum(1 for r in got if r.answers)
    print(f"\ncanary: {ok}/{len(got)} valid")
    if ok == 0:
        print("CANARY FAILED - every call malformed. Not dispatching the batch.")
        raise SystemExit(3)

    with ThreadPoolExecutor(max_workers=a.concurrency) as pool:
        for fut in as_completed([pool.submit(one, j) for j in tail]):
            try:
                got += fut.result()
            except Exception as e:                                   # noqa: BLE001
                print(f"  job failed: {type(e).__name__}: {e}", flush=True)

    print(f"\n{len(got)} responses in {(time.time()-t0)/60:.1f}m "
          f"({dispatched} calls dispatched)")
    for k, r in sorted(missingness(got).items()):
        print(f"  missing {k[0]}/{k[1]}: {r:.0%}" + ("  <-- INCONCLUSIVE" if r > .10 else ""))

    # ---- completion check against the manifest
    have2 = existing_cells([a.out] + [Path(x) for x in a.also_read])
    want = {(ep.name, v, a.model, r) for ep, _, v, need in manifest for r in need}
    miss = want - set(have2)
    print(f"  manifest completion: {len(want)-len(miss)}/{len(want)}"
          + (f"  MISSING {len(miss)}" if miss else "  complete"))


if __name__ == "__main__":
    main()
