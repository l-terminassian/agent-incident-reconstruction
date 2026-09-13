#!/usr/bin/env python3
"""Frozen manifest: hash every input the results depend on."""
import hashlib, json, glob, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

groups = {
 "episode data (120)": sorted(glob.glob(str(root/"data/main_v1_trap_canary/*/manifest.json"))),
 "judgements":         sorted(glob.glob(str(root/"artifacts/*.jsonl"))),
 "source":             sorted(glob.glob(str(root/"src/*.py"))),
 "human labels":       sorted(glob.glob(str(root/"human_labels/*.json"))),
}
man = {}
for name, files in groups.items():
    digest = hashlib.sha256("".join(h(f) for f in files).encode()).hexdigest()[:16]
    man[name] = {"files": len(files), "digest": digest}
    print(f"  {name:<20} {len(files):>4} files   digest {digest}")
out = root/"repro"/"MANIFEST.json"
prev = json.load(open(out)) if out.exists() else None
json.dump(man, open(out, "w"), indent=2)
if prev and prev != man:
    print("\n  WARNING: inputs changed since the last run:")
    for k in man:
        if prev.get(k) != man[k]: print(f"     {k}: {prev.get(k)} -> {man[k]}")
    sys.exit(1)
print(f"\n  manifest written to {out.relative_to(root)}")
