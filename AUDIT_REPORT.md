# Audit report

## 1. Verdict

**PASS WITH MINOR ISSUES**

The offline reproduction completes, every recomputable value matches the
canonical results, integrity and schema checks pass, deliberate corruption is
detected, and no release-bound file contains a prohibited personal,
organizational, budget, license, or credential reference. Two informational
items remain, neither blocking; both are listed in section 4.

## 2. Checks performed

| Check | Command or method | Result |
|---|---|---|
| File inventory, including hidden files | `find`, `du` | 31 release files plus 120 episode directories |
| Prohibited identity and organization terms | case-insensitive `grep` over all text, filenames, data | none; two hits were the ordinary English word "apart" in model reasoning |
| Budget, price, billing, cost terms | `grep` over code, docs, scripts | present at audit start; removed (section 3) |
| License files and notices | `find`, `grep` for SPDX and copyright | none present, none removed |
| Secrets and secret-like values | pattern scan for key, token, bearer, PEM, cloud-id forms | none |
| Absolute local paths | `grep` over code and data | none in code; two data files contain a fictional path written by the model itself |
| Symlinks escaping the repository | `find -type l` | none |
| Ground truth is mechanical | read `grader.py`, `harness.py`, `analyze.load` | labels derive only from the call record and file hashes |
| Reasoning and narrative not used as labels | read `analyze.load`, `grader.py` | confirmed; both are evidence shown to investigators only |
| Failed reads not counted as access | read `_is_successful_access` | requires a successful call |
| No-op redaction retained but excluded | `corruption_status`, `analyze.load` | retained in data, excluded from the ablation sample |
| View definitions match documentation | read `views.build_package` | V1 altered record, V1A five receipt fields, V1R restored passage, V3 full call record |
| One view per investigator call | read `run_judgement`, `investigator.ask` | one view of one episode per call |
| Denominators distinguished | recomputation | 120 episodes, 240 agent rows, 66 accesses, 34 ablation episodes, 38 accessing rows, 752 judgements |
| Human and automated samples not pooled | separate files and code paths | `human_labels/` is never read by the statistics script |
| Statistical machinery matches the report | read `analyze.py` | episode-clustered bootstrap, sign-flip permutation, `(extreme + 1)/(B + 1)`, B = 5000, abstention 0.5 |
| Per-model confidence conversion | read `CONFIDENCE_SEMANTICS`, `to_prob_for` | per-model table; categorical outcome primary |
| Recomputation against canonical values | `./reproduce.sh` plus a 48-assertion comparison | 47 of 48 matched; one explained, see section 4 |
| Integrity manifest fails on drift | flipped a ground-truth label in a temporary copy | exit 1, drift reported |
| Integrity manifest fails on judgement loss | removed one judgement line in a temporary copy | exit 1 |
| Receipt invariants and schema | `repro/validate_receipts.py` | pass |
| Test suites | `tests/test_views.py`, `tests/audit_runner.py` | 0 failures each |
| Offline isolation | inspected imports and the reproduction path | no provider reference reachable; provider SDKs imported inside functions only |
| Dependency declaration | AST scan of all imports against `requirements.txt` | no undeclared, no unused, no stdlib listed |
| Python version | executed reproduction | runs on 3.9.6; README states 3.9+ |
| Encoding, newlines, permissions | `file`, `find -perm` | UTF-8, LF, only scripts executable |
| Debug markers, dead code | `grep` for TODO, FIXME, XXX, pdb, breakpoint | none |
| Broad exception handling | AST and manual review | six sites, all in retry or tolerance paths; one silent skip fixed |

## 3. Changes made

**Removed from the release surface**

| File or class | Count | Reason |
|---|---|---|
| `*/[AB]/_prompt_DO_NOT_SHIP.txt` | 240 | Contains the randomized instruction text. Not read by any release code; `views.py` uses the string only as a banned-metadata token in the leakage guard. |
| `*/sandbox_*/tmp*.py` | ~200 | Temporary subprocess scratch output. |
| `*/parse_failures.jsonl` | 186 | Development debugging output, not read by any release code. |
| `*.pyc`, `__pycache__/` | 120 | Build cache. |
| Unrelated development files | — | Not carried into this release. |

`data/` reduced from 29 MB to 20 MB. Recomputed results unchanged.

**Cost and price material removed**

| File | Change |
|---|---|
| `src/config.py` | Removed the per-token price table. |
| `src/investigator.py` | `CostTracker` replaced by `CallTracker`; counts calls and cache behaviour only. |
| `src/run_judgement.py` | `--max-spend` replaced by `--max-calls`, a hard ceiling on dispatched calls including retries. Same safety property, no monetary reference. |
| `tests/audit_runner.py`, `README.md` | Wording and example command updated to match. |

**Correctness and clarity**

| File | Change | Why |
|---|---|---|
| `src/run_judgement.py` | A package that fails to build now prints a warning instead of being skipped silently. | An episode could otherwise vanish from the manifest and the run would cover fewer episodes than requested, without a word. |
| `src/harness.py` | `re` and `grader` imports lifted to module scope; `import re` added. | They were hidden inside functions with no justification. |
| `src/investigator.py` | `defaultdict` lifted to module scope. | Same. |
| `src/config.py`, `src/run_judgement.py` | Provider SDK imports kept inside functions, with a comment stating why. | The offline reproduction must import these modules without either package installed. |
| `repro/all_results.py` | Added a concealment recomputation from the stored logs. | Makes the reported concealment count reproducible from primary data; see section 4. |
| `repro/all_results.py` | Output headings made self-describing instead of numbered cross-references. | Numbers referring to an external document are brittle. |
| `repro/check_integrity.py` | Corrected the human-label glob, which matched nothing. | The manifest silently covered zero files in that group. |
| `README.md` | Rewritten: added prerequisites and expected output, trimmed to the required structure. | |

## 4. Remaining issues

| Severity | File | Impact | Next action |
|---|---|---|---|
| Low, informational | `data/main_v1_trap_canary/*/labels.json` | The stored `concealment` field was computed during the run by a rule that has since been superseded, and reports 2 concealments where the current rule and the human labels both give 3. The single differing row is `main_043/A`. Primary data was deliberately not overwritten. | None required. Stage 2 of the reproduction recomputes the label from the same stored logs and prints how many rows differ, so the reported figure is reproducible from primary data. |
| Low, informational | repository root | This directory is not yet its own repository, so no independent history exists to scan for secrets or prohibited terms. | Initialise a fresh repository at this directory so the release starts with a clean history. |

## 5. Reproduction result

| Command | Exit | Outcome |
|---|---|---|
| `./reproduce.sh` | 0 | All four stages completed. No network access, no credentials. |
| `tests/test_views.py` | 0 | 0 failures |
| `tests/audit_runner.py` | 0 | 0 failures |
| `repro/validate_receipts.py` | 0 | Conforms to the five-field schema |
| `./reproduce.sh` on a copy with one ground-truth label flipped | 1 | Drift detected and reported |
| `./reproduce.sh` on a copy with one judgement removed | 1 | Drift detected and reported |

Recomputed values were compared against the canonical results on 48 assertions
covering episode and agent counts, condition sizes, access counts and rates by
condition and stratum, ablation sample sizes, judgement totals, malformed and
duplicate counts, per-view detection and false alarms, confidence summaries,
paired gains and intervals for three repairs, and per-model categorical results.
**47 matched exactly.** The single mismatch is the concealment label described
in section 4, which the reproduction now recomputes correctly from primary data.

Reruns are idempotent: repeated invocation regenerates the manifest and
reproduces identical values.

## 6. Release inventory

```
README.md
AUDIT_REPORT.md
reproduce.sh
requirements.txt
.gitignore
src/          9 modules
repro/        4 scripts, receipt schema, sample receipts, integrity manifest
tests/        2 suites
data/         120 episode directories
artifacts/    6 judgement files, 752 records
human_labels/ 2 files
```

Total 20 MB, of which `data/` is 20 MB.
