#!/usr/bin/env bash
# run_tests.sh — local CI-style runner for the memory plugin's bin/ scripts.
#
# Executes every bin/test_*.sh in turn (currently test_measure_memory.sh and
# test_fixtures.sh), prints each one's output, and aggregates the result. Exits
# non-zero if any test file fails. Pure stdlib bash + Python 3; no network, no
# third-party deps.
#
# Run: bash memory/bin/run_tests.sh
set -uo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

failed=0
ran=0
for t in "$BIN_DIR"/test_*.sh; do
    [[ -e "$t" ]] || continue
    ran=$((ran + 1))
    name="$(basename "$t")"
    echo "######## $name ########"
    if bash "$t"; then
        echo "-------- PASS: $name"
    else
        rc=$?
        echo "-------- FAIL: $name (exit $rc)"
        failed=$((failed + 1))
    fi
    echo
done

if [[ "$ran" -eq 0 ]]; then
    echo "run_tests.sh: no test_*.sh files found in $BIN_DIR" >&2
    exit 1
fi

if [[ "$failed" -gt 0 ]]; then
    echo "CI: $failed/$ran test file(s) FAILED"
    exit 1
fi
echo "CI: all $ran test file(s) passed"
