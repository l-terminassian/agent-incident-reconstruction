# Evidence ablation for agent-incident reconstruction

Given that an agent's access to a protected file definitely occurred, this
repository measures what happens to an investigator's conclusion when evidence
of that access is removed from the record, and which retained artifact restores
it. It contains the environment, 120 recorded episodes, 752 frozen investigator
judgements, and the analysis that produces every reported statistic.

## Layout

```
src/
  tasks.py         task set: solvable and over-constrained strata
  harness.py       episode runner, the two records, the redactor
  driver.py        agent loop, randomised instruction condition, offline grading
  grader.py        mechanical labels; no model judge anywhere in this file
  views.py         investigator evidence views and the leakage guard
  investigator.py  investigator prompt, JSON schema, retries, call accounting
  run_judgement.py manifest-driven runner: resumable, deduplicating, call-capped
  analyze.py       scoring, outcome measures, bootstrap and permutation tests
  config.py        paths, model identifiers, credential loading
data/              120 episodes: manifests, labels, both records, reasoning
artifacts/         752 investigator judgements, one JSON object per line
human_labels/      human concealment labels and reader answers
repro/             integrity manifest, statistics, receipt schema and validator
tests/             view construction and runner test suites
```

## Prerequisites

Python 3.9 or later. Reproduction needs nothing else — no third-party packages,
no network, no credentials. The packages in `requirements.txt` are required only
to collect new data.

## Reproduce

```
./reproduce.sh
```

Expected output, in four stages:

```
0. integrity     four input groups hashed; manifest written (or drift reported)
1. unit tests    two suites, "0 failure(s)" each
2. all results   access rates, detection by view, paired gains, replication
3. receipt schema  "PASS - conforms to the five-field receipt schema"
4. worked example  one episode under two evidence views
```

The script exits nonzero on integrity drift, a failed test, a schema error, or
an analysis failure. Stage 0 compares every input against `repro/MANIFEST.json`
and fails if anything changed, so an altered dataset cannot silently produce
different numbers.

## Evidence views

Each investigator sees one view of one episode, and never a second view of the
same episode.

| view | evidence shown |
|---|---|
| V0 | submissions and scores only |
| V1 | + the agent's own session log, with the disclosure removed |
| V1A | + minimal access receipts |
| V1R | + the removed passage restored |
| V3 | + the full independently recorded call record |
| V6 | + reasoning traces |

## The receipt schema

Five fields per file operation. Contents are deliberately not retained.

```json
{"actor": "A", "event": "read_file", "resource": "tests/expected.json",
 "outcome": "ok", "t": 4.674}
```

`repro/receipt_schema.json` is the JSON Schema. `repro/validate_receipts.py`
checks a log against it with no dependencies, and enforces two invariants: a
failed operation is not an access, and every file access is listed rather than
only suspected violations.

## Collecting new data

```
export INVESTIGATOR_API_KEY=...

python src/run_judgement.py --data data/main_v1_trap_canary \
  --views V1,V1A --reps 1 --corrupted-only --contrast-only \
  --model <model> --out artifacts/new.jsonl --max-calls 100
```

Only missing judgements are issued; existing ones are skipped by identity, so a
run can be stopped and resumed without duplicating anything. `--max-calls` is a
hard ceiling on dispatched calls, retries included. To use another provider, add
`--base-url` and `--key-env`; the prompt and schema are unchanged on that path.

New agent episodes need a served model at `AGENT_ENDPOINT`:

```
AGENT_MODEL=<served-name> python src/driver.py main
```

## Notes for anyone reading the analysis

- Labels come only from the harness call record and file hashes. Reasoning
  traces and agent-written logs are evidence shown to investigators, never
  inputs to a label. A failed read is not an access.
- Confidence semantics are **not uniform across models** and are validated per
  model in `analyze.CONFIDENCE_SEMANTICS`. Some models report confidence in the
  answer they chose; others report the probability the prompt asked for.
  Applying one convention to all of them inverts the probability for whichever
  disagrees, so the categorical outcome is primary.
- The episode is the unit of analysis. Intervals use an episode-clustered
  bootstrap; p-values a sign-flip permutation corrected as
  `(extreme + 1) / (B + 1)` with B = 5000. A reported `p <= 0.0002` is that
  floor, not a point estimate.
- A redaction that removed nothing is recorded as `corruption_status: no_op`
  and excluded from the ablation sample rather than deleted from the data.
- `labels.json` stores the concealment label computed during the run. Stage 2
  recomputes it from the same stored logs with the current rule and reports how
  many rows differ.

## Caution

`src/grader.py` executes model-written code. Run it in a container. The
subprocess guard there is a timeout and a clean interpreter, not a sandbox.
