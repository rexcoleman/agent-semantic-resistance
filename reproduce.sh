#!/bin/bash
set -e
echo "=== FP-17 Reproduce Pipeline ==="

# Gate 0.5 check
grep -qi "lock_commit.*TO BE SET\|lock_commit.*PENDING" EXPERIMENTAL_DESIGN.md && echo "FAIL: lock_commit not set" && exit 1 || echo "PASS: lock_commit set"

# R35: nohup for long compute
mkdir -p ~/compute_logs
pip install numpy anthropic 2>&1 | tail -3

echo "--- Experiments (nohup, R35) ---"
nohup python3 -u scripts/run_experiments.py > ~/compute_logs/fp17_experiments.log 2>&1 &
echo "PID: $! — Log: ~/compute_logs/fp17_experiments.log"
echo "Monitor: tail -f ~/compute_logs/fp17_experiments.log"

echo "--- Gate Validation (R50) ---"
bash ~/ml-governance-templates/scripts/check_all_gates.sh .
