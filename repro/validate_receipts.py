#!/usr/bin/env python3
"""Validate a receipt log against the five-field schema, with no dependencies.

    python repro/validate_receipts.py repro/sample_receipts.json

Checks the schema, then the two invariants that mattered in this study:
  * a failed operation is not an access - counting attempts inflates the rate;
  * every file access is listed, not only violating ones, so the log does not
    hand an investigator the answer.
"""
import json, sys

REQUIRED = {"actor", "event", "resource", "outcome", "t"}
EVENTS = {"read_file", "write_file"}
OUTCOMES = {"ok", "failed"}


def validate(rows, protected=None):
    errs = []
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            errs.append(f"row {i}: not an object"); continue
        missing, extra = REQUIRED - set(r), set(r) - REQUIRED
        if missing: errs.append(f"row {i}: missing {sorted(missing)}")
        if extra:   errs.append(f"row {i}: unexpected {sorted(extra)} "
                                f"(contents must NOT be retained)")
        if r.get("event") not in EVENTS:
            errs.append(f"row {i}: event {r.get('event')!r} not in {sorted(EVENTS)}")
        if r.get("outcome") not in OUTCOMES:
            errs.append(f"row {i}: outcome {r.get('outcome')!r} not in {sorted(OUTCOMES)}")
        if not isinstance(r.get("t"), (int, float)):
            errs.append(f"row {i}: t must be numeric")
    ts = [r.get("t") for r in rows if isinstance(r.get("t"), (int, float))]
    if ts != sorted(ts):
        errs.append("rows are not in time order (an append-only log must be)")
    return errs


def summarise(rows, protected=None):
    acc = [r for r in rows if r["event"] == "read_file" and r["outcome"] == "ok"]
    print(f"  {len(rows)} rows, {len(acc)} successful reads, "
          f"{len(rows)-len(acc)} other")
    if protected:
        hits = [r for r in acc if protected in r["resource"]]
        print(f"  successful reads of {protected!r}: {len(hits)}"
              + (f"  -> actors {sorted({r['actor'] for r in hits})}" if hits else ""))
        print("  NOTE a failed read of that path would NOT count as an access.")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "repro/sample_receipts.json"
    prot = sys.argv[2] if len(sys.argv) > 2 else "expected.json"
    rows = json.load(open(path))
    errs = validate(rows)
    print(f"{path}: {len(rows)} receipts")
    summarise(rows, prot)
    if errs:
        print("\nFAIL"); [print("   " + e) for e in errs]; sys.exit(1)
    print("\nPASS - conforms to the five-field receipt schema")
