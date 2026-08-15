#!/usr/bin/env python3
"""Tinh metric tu file .jtl (JMeter CSV) — ground truth cho Task 2.
Usage: python3 analyze_jtl.py <file.jtl> [label]
"""
import csv, sys
from collections import defaultdict

def pct(sorted_vals, p):
    if not sorted_vals:
        return 0
    k = (len(sorted_vals) - 1) * p / 100.0
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)

def analyze(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    if not rows:
        print("EMPTY:", path); return
    ts = [int(r["timeStamp"]) for r in rows]
    elapsed = [int(r["elapsed"]) for r in rows]
    ok = sum(1 for r in rows if r["success"] == "true")
    err = len(rows) - ok
    wall = (max(int(r["timeStamp"]) + int(r["elapsed"]) for r in rows) - min(ts)) / 1000.0
    by_label = defaultdict(list)
    err_codes = defaultdict(int)
    for r in rows:
        by_label[r["label"]].append(int(r["elapsed"]))
        if r["success"] != "true":
            err_codes[f'{r["label"]} -> {r["responseCode"]} {r["responseMessage"][:30]}'] += 1
    se = sorted(elapsed)
    print(f"\n===== {path} =====")
    print(f"Samples: {len(rows)} | OK: {ok} | Error: {err} ({100*err/len(rows):.2f}%)")
    print(f"Wall time: {wall:.1f}s | Throughput: {len(rows)/wall:.2f} req/s")
    print(f"Latency ms — min {se[0]} | mean {sum(se)/len(se):.1f} | median {pct(se,50):.0f} "
          f"| p90 {pct(se,90):.0f} | p95 {pct(se,95):.0f} | p99 {pct(se,99):.0f} | max {se[-1]}")
    print("\nPer-request (label | n | mean | p95 | max ms):")
    for lbl in sorted(by_label):
        v = sorted(by_label[lbl])
        print(f"  {lbl:30s} n={len(v):5d} mean={sum(v)/len(v):7.1f} p95={pct(v,95):7.0f} max={v[-1]:6d}")
    if err_codes:
        print("\nError breakdown:")
        for k, c in sorted(err_codes.items(), key=lambda x: -x[1]):
            print(f"  {c:5d} x {k}")

if __name__ == "__main__":
    analyze(sys.argv[1])
