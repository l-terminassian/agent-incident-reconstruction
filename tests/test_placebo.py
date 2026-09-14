"""Invariants for the placebo redaction.

The placebo is only a valid control if it keeps the disclosure and removes at
least as much text as the redaction it mirrors. Both are asserted here against
the stored logs, along with determinism.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from placebo import _disclosure_pattern, build_placebo   # noqa: E402

failures = []


def check(name, condition, detail=""):
    print(f"  {'PASS' if condition else 'FAIL'}  {name}"
          + (f"  -- {detail}" if detail and not condition else ""))
    if not condition:
        failures.append(name)


def episodes():
    for manifest in sorted((ROOT / "data/main_v1_trap_canary").glob("*/manifest.json")):
        episode = manifest.parent
        for agent, meta in json.loads(manifest.read_text())["agents"].items():
            if not meta.get("corrupted") or meta.get("corruption_status") == "no_op":
                continue
            placebo = episode / agent / "session_log_placebo.txt"
            if placebo.exists():
                yield episode, agent, meta, placebo


def run():
    cases = list(episodes())
    check("placebo logs exist for every redacted episode", len(cases) == 34,
          f"found {len(cases)}")

    kept = short = 0
    for episode, agent, meta, placebo in cases:
        intact = (episode / agent / "session_log.txt").read_text()
        redacted = (episode / agent / "session_log_corrupted.txt").read_text()
        text = placebo.read_text()
        kept += bool(_disclosure_pattern(meta["answer_path"]).search(text))
        short += len(intact) - len(text) >= len(intact) - len(redacted)

    check("disclosure retained in every placebo log", kept == len(cases),
          f"{kept}/{len(cases)}")
    check("placebo removes at least as much text as the redaction",
          short == len(cases), f"{short}/{len(cases)}")

    episode, agent, meta, placebo = cases[0]
    intact = (episode / agent / "session_log.txt").read_text()
    redacted = (episode / agent / "session_log_corrupted.txt").read_text()
    seed = f"{episode.name}:{agent}"
    first, _ = build_placebo(intact, redacted, meta["answer_path"], seed)
    second, _ = build_placebo(intact, redacted, meta["answer_path"], seed)
    check("same seed gives the same log", first == second)
    check("stored log matches a fresh build", first == placebo.read_text())

    other, _ = build_placebo(intact, redacted, meta["answer_path"], seed + "x")
    check("a different seed selects different sentences", other != first)

    print(f"\n{len(failures)} failure(s)" + (": " + ", ".join(failures) if failures else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
