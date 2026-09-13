#!/usr/bin/env bash
# Regenerate every reported result from the frozen judgements. No API calls.
#
#     ./reproduce.sh
#
# Add --with-api to re-issue the investigator calls instead of reusing them.
# Everything else is deterministic and runs offline.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
echo "=================== 0. integrity ==================="
$PY repro/check_integrity.py

echo; echo "=================== 1. unit tests ==================="
$PY tests/test_views.py | tail -3
$PY tests/audit_runner.py | tail -3

echo; echo "=================== 2. all results ==================="
cat artifacts/inv_pilot.jsonl artifacts/inv_v3.jsonl artifacts/inv_v1a.jsonl \
    artifacts/judge.jsonl artifacts/replication_claude-haiku-4-5.jsonl \
    artifacts/replication_claude-opus-5.jsonl > /tmp/all_judgements.jsonl
$PY repro/all_results.py /tmp/all_judgements.jsonl

echo; echo "=================== 3. receipt schema ==================="
$PY repro/validate_receipts.py repro/sample_receipts.json

echo; echo "=================== 4. worked example ==================="
$PY repro/worked_example.py
