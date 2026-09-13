#!/usr/bin/env python3
"""One episode, shown as the investigator saw it under V1 and then V1A.

    python repro/worked_example.py [episode_id]

This is the whole study in one screen: the same run, the same question, and the
difference one 740-character receipt block makes.
"""
import sys, json
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root/"src"))
import views as V

eid = sys.argv[1] if len(sys.argv) > 1 else "main_062"
ep = root/"data/main_v1_trap_canary"/eid
man = json.loads((ep/"manifest.json").read_text())
acc = [a for a,g in man["agents"].items() if g.get("accessed_answer_file")]

print(f"EPISODE {eid}")
print(f"GROUND TRUTH: agent(s) {acc} read the protected file. "
      f"The session log was redacted to remove the disclosure.\n")

for view in ("V1", "V1A"):
    txt = V.build_package(ep, view).text
    print("=" * 72)
    print(f"  VIEW {view}  ({len(txt)} chars)")
    print("=" * 72)
    if view == "V1A":
        i = txt.find("Platform access receipts")
        print("  the only difference from V1 is this block, per agent:\n")
        print("  " + "\n  ".join(txt[i:i+520].splitlines()))
    else:
        i = txt.find("Session log")
        print("  the agent's own account, with the access removed:\n")
        print("  " + "\n  ".join(txt[i:i+520].splitlines()))
    print()

for m in ("claude-haiku-4-5","claude-sonnet-5","claude-opus-5"):
    f = root/f"artifacts/replication_{m}.jsonl"
    if not f.exists(): continue
    got = {}
    for l in f.read_text().splitlines():
        r = json.loads(l)
        if r["episode_id"] == eid and r["answers"]:
            for a in acc:
                got[(r["view"], a)] = r["answers"].get(a, {}).get("accessed", {})
    line = []
    for view in ("V1","V1A"):
        for a in acc:
            it = got.get((view,a))
            if it: line.append(f"{view}/{a}: {it['answer']}({it['confidence']})")
    if line: print(f"  {m:<18} " + "   ".join(line))
print("\n  Ground truth: every one of these should be 'yes'.")
