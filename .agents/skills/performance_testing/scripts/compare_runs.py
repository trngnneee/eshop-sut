#!/usr/bin/env python3
"""
compare_runs.py - Compares a test run summary against a baseline and flags p95 regressions.
"""

import argparse
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def compare_runs(baseline_path, current_path, warn_threshold=10.0, fail_threshold=20.0):
    if not os.path.exists(baseline_path):
        print(f"Error: Baseline file not found: {baseline_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(current_path):
        print(f"Error: Current summary file not found: {current_path}", file=sys.stderr)
        sys.exit(1)

    with open(baseline_path, 'r', encoding='utf-8') as f:
        baseline_data = json.load(f)
    with open(current_path, 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    base_labels = baseline_data.get("labels", {})
    curr_labels = current_data.get("labels", {})

    print(f"\n=======================================================")
    print(f"   CONTINUOUS PERFORMANCE COMPARISON REPORT")
    print(f"   Baseline: {baseline_path}")
    print(f"   Current:  {current_path}")
    print(f"=======================================================\n")

    print("| Label | Baseline p95 (ms) | Current p95 (ms) | Delta (%) | Status |")
    print("|:---|---:|---:|---:|:---|")

    has_fail = False
    has_warn = False

    for lbl, cur_info in sorted(curr_labels.items()):
        cur_p95 = cur_info.get("elapsed", {}).get("p95", 0)
        
        # Look up baseline
        base_info = base_labels.get(lbl, {})
        base_p95 = base_info.get("p95_ms", base_info.get("elapsed", {}).get("p95", 0))

        if base_p95 > 0:
            delta_pct = ((cur_p95 - base_p95) / base_p95) * 100.0
            delta_str = f"{delta_pct:+.1f}%"

            if delta_pct > fail_threshold:
                status = "❌ FAIL (Regression)"
                has_fail = True
            elif delta_pct > warn_threshold:
                status = "⚠️ WARN (Degraded)"
                has_warn = True
            elif delta_pct < -15.0:
                status = "🎉 IMPROVED"
            else:
                status = "✅ PASS"
        else:
            delta_str = "N/A"
            status = "ℹ️ NEW"

        print(f"| `{lbl}` | {base_p95} | {cur_p95} | {delta_str} | {status} |")

    # Overall error rate check
    curr_err_rate = current_data.get("run", {}).get("error_rate_pct", 0)
    if curr_err_rate > 1.0:
        print(f"\n[!] Error rate threshold exceeded: {curr_err_rate}% > 1.0%")
        has_fail = True

    print("\n-------------------------------------------------------")
    if has_fail:
        print("RESULT: ❌ REGRESSION DETECTED (Merge Blocked)")
        sys.exit(1)
    elif has_warn:
        print("RESULT: ⚠️ WARNING (Performance degraded but within merge limit)")
        sys.exit(0)
    else:
        print("RESULT: ✅ ALL CHECKS PASSED")
        sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare JMeter summary with baseline")
    parser.add_argument('--baseline', required=True, help="Path to baseline.json")
    parser.add_argument('--current', required=True, help="Path to current summary.json")
    parser.add_argument('--threshold-warn', type=float, default=10.0, help="Warning delta percentage")
    parser.add_argument('--threshold-fail', type=float, default=20.0, help="Failure delta percentage")
    args = parser.parse_args()

    compare_runs(args.baseline, args.current, args.threshold_warn, args.threshold_fail)
