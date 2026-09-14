"""Placebo redaction: remove matched text that does not carry the disclosure.

The tampered view removes the sentence disclosing the protected access, which
changes two things at once: the record loses a specific fact, and it becomes
shorter and less continuous. Either could explain a failed reconstruction.

This view holds the fact fixed and reproduces only the structural change. The
disclosure stays; a matched character volume of non-disclosing sentences is
removed instead.

    V1R   disclosure present, nothing removed
    V1    disclosure removed
    V1P   disclosure present, matched volume removed

Sentence selection is seeded per episode, so the view rebuilds identically.
"""
from __future__ import annotations

import json
import random
import re
import statistics
from pathlib import Path

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def _disclosure_pattern(access_path: str) -> re.Pattern:
    """Sentences matching this name the protected artifact and are never removed."""
    name = access_path.split("/")[-1]
    return re.compile(
        rf"{re.escape(name)}|expected\.json|answer\s*key|reference\s*outputs?|"
        rf"ref_outputs|cat\s+\S*expected|read\s+\S*expected|open\(\S*expected",
        re.I,
    )


def build_placebo(intact: str, redacted: str, access_path: str,
                  seed: str) -> tuple[str, dict]:
    """Return the placebo log and a record of how well the volume was matched.

    Sentences are added until the removed volume reaches the target, so the
    match errs toward removing slightly too much. That direction is
    conservative: it biases the comparison toward finding structural harm.
    """
    target = len(intact) - len(redacted)
    discloses = _disclosure_pattern(access_path)
    sentences = SENTENCE_BOUNDARY.split(intact)
    candidates = [i for i, s in enumerate(sentences) if not discloses.search(s)]

    order = candidates[:]
    random.Random(seed).shuffle(order)

    chosen: set[int] = set()
    removed = 0
    for index in order:
        if removed >= target:
            break
        chosen.add(index)
        removed += len(sentences[index]) + 1        # the joining space

    placebo = " ".join(s for i, s in enumerate(sentences) if i not in chosen).strip()
    return placebo, {
        "target_chars": target,
        "removed_chars": len(intact) - len(placebo),
        "sentences_removed": len(chosen),
        "candidates_available": len(candidates),
        "disclosure_retained": bool(discloses.search(placebo)),
        "volume_unreachable": removed < target,
    }


def write_all(data_dir: Path) -> dict:
    """Write session_log_placebo.txt for every episode with a real redaction."""
    report = {}
    for episode in sorted(data_dir.glob("*")):
        manifest = episode / "manifest.json"
        if not manifest.exists():
            continue
        for agent, meta in json.loads(manifest.read_text())["agents"].items():
            if not meta.get("corrupted") or meta.get("corruption_status") == "no_op":
                continue
            intact = episode / agent / "session_log.txt"
            redacted = episode / agent / "session_log_corrupted.txt"
            if not (intact.exists() and redacted.exists()):
                continue
            placebo, info = build_placebo(
                intact.read_text(), redacted.read_text(),
                meta["answer_path"], seed=f"{episode.name}:{agent}")
            (episode / agent / "session_log_placebo.txt").write_text(placebo)
            report[f"{episode.name}/{agent}"] = info
    return report


def summarise(report: dict) -> str:
    errors = [v["removed_chars"] - v["target_chars"] for v in report.values()]
    return (
        f"  placebo logs: {len(report)}\n"
        f"  disclosure retained: "
        f"{sum(v['disclosure_retained'] for v in report.values())}/{len(report)}\n"
        f"  volume unreachable: {sum(v['volume_unreachable'] for v in report.values())}\n"
        f"  sentences removed, median: "
        f"{statistics.median(v['sentences_removed'] for v in report.values()):.0f}\n"
        f"  character match error, median: {statistics.median(errors):+.0f} "
        f"(range {min(errors):+d} to {max(errors):+d})"
    )


if __name__ == "__main__":
    from config import ROOT

    print(summarise(write_all(ROOT / "data" / "main_v1_trap_canary")))
