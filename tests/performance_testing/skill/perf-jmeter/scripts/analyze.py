#!/usr/bin/env python3
"""
perf-jmeter skill — tính metric ground-truth từ file .jtl thô (JMeter CSV) và
đề xuất performance threshold theo baseline. Percentile tính trực tiếp từ log,
KHÔNG tin dashboard (dùng để bắt AI/dashboard diễn giải sai).

Usage:
    python3 analyze.py <file1.jtl> [file2.jtl ...] [--md report.md]

Xuất: bảng metric per-scenario + per-endpoint ra stdout; nếu có --md thì ghi
thêm báo cáo Markdown kèm bảng threshold đề xuất (regression-based).
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
    rows = list(csv.DictReader(open(path, newline="")))
    if not rows:
        return None
    ts = [int(r["timeStamp"]) for r in rows]
    elapsed = sorted(int(r["elapsed"]) for r in rows)
    ok = sum(1 for r in rows if r["success"] == "true")
    err = len(rows) - ok
    wall = (max(int(r["timeStamp"]) + int(r["elapsed"]) for r in rows) - min(ts)) / 1000.0
    by_label = defaultdict(list)
    err_codes = defaultdict(int)
    for r in rows:
        by_label[r["label"]].append(int(r["elapsed"]))
        if r["success"] != "true":
            err_codes[f'{r["label"]} -> {r["responseCode"]} {r["responseMessage"][:30]}'] += 1
    per = {}
    for lbl in sorted(by_label):
        v = sorted(by_label[lbl])
        per[lbl] = {"n": len(v), "mean": sum(v) / len(v), "p95": pct(v, 95), "max": v[-1]}
    return {
        "path": path,
        "samples": len(rows),
        "ok": ok, "err": err, "err_pct": 100 * err / len(rows),
        "wall": wall, "rps": len(rows) / wall if wall else 0,
        "min": elapsed[0], "mean": sum(elapsed) / len(elapsed),
        "median": pct(elapsed, 50), "p90": pct(elapsed, 90),
        "p95": pct(elapsed, 95), "p99": pct(elapsed, 99), "max": elapsed[-1],
        "per": per, "err_codes": dict(err_codes),
    }


def print_console(m):
    print(f"\n===== {m['path']} =====")
    print(f"Samples: {m['samples']} | OK: {m['ok']} | Error: {m['err']} ({m['err_pct']:.2f}%)")
    print(f"Wall: {m['wall']:.1f}s | Throughput: {m['rps']:.2f} req/s")
    print(f"Latency ms — min {m['min']} | mean {m['mean']:.1f} | median {m['median']:.0f} "
          f"| p90 {m['p90']:.0f} | p95 {m['p95']:.0f} | p99 {m['p99']:.0f} | max {m['max']}")
    print("Per-endpoint (label | n | mean | p95 | max ms):")
    for lbl, s in m["per"].items():
        print(f"  {lbl:32s} n={s['n']:6d} mean={s['mean']:7.1f} p95={s['p95']:7.0f} max={s['max']:6d}")
    if m["err_codes"]:
        print("Error breakdown:")
        for k, c in sorted(m["err_codes"].items(), key=lambda x: -x[1]):
            print(f"  {c:5d} x {k}")


def thresholds(m):
    """Đề xuất threshold theo baseline đo được (regression-based, không tuyệt đối)."""
    p95 = m["p95"]
    return {
        "p95_alert_ms": max(round(p95 * 3), round(p95) + 10),   # ~3x baseline
        "error_max_pct": 0.5,
        "throughput_floor_rps": round(m["rps"] * 0.8, 1),        # regression nếu tụt >20%
        "note_bottleneck": max(m["per"].items(), key=lambda kv: kv[1]["mean"])[0],
    }


def write_md(metrics, out):
    lines = ["# Performance report (perf-jmeter skill)\n",
             "> Ground truth tính trực tiếp từ `.jtl` thô — percentile, không lấy từ dashboard.\n",
             "## Tổng hợp\n",
             "| File | Samples | Error % | Throughput | p95 (ms) | p99 (ms) | max (ms) |",
             "|---|---|---|---|---|---|---|"]
    for m in metrics:
        lines.append(f"| `{m['path'].split('/')[-1]}` | {m['samples']} | {m['err_pct']:.2f}% | "
                     f"{m['rps']:.2f} req/s | {m['p95']:.0f} | {m['p99']:.0f} | {m['max']} |")
    for m in metrics:
        t = thresholds(m)
        lines += [f"\n## `{m['path'].split('/')[-1]}` — per-endpoint\n",
                  "| Endpoint | n | mean (ms) | p95 (ms) | max (ms) |",
                  "|---|---|---|---|---|"]
        for lbl, s in m["per"].items():
            lines.append(f"| {lbl} | {s['n']} | {s['mean']:.1f} | {s['p95']:.0f} | {s['max']} |")
        lines += [f"\n**Endpoint nặng nhất (canary):** `{t['note_bottleneck']}`\n",
                  "**Threshold đề xuất (regression-based):**\n",
                  f"- p95 alert: **> {t['p95_alert_ms']} ms** (~3× baseline {m['p95']:.0f} ms)",
                  f"- error rate: **< {t['error_max_pct']}%** (baseline {m['err_pct']:.2f}%)",
                  f"- throughput floor: **≥ {t['throughput_floor_rps']} req/s** (regression nếu tụt > 20% so với {m['rps']:.1f})"]
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"\n[markdown] wrote {out}")


def main():
    args = sys.argv[1:]
    md = None
    if "--md" in args:
        i = args.index("--md")
        md = args[i + 1]
        args = args[:i] + args[i + 2:]
    if not args:
        print(__doc__)
        sys.exit(1)
    metrics = [m for m in (analyze(p) for p in args) if m]
    for m in metrics:
        print_console(m)
    if md and metrics:
        write_md(metrics, md)


if __name__ == "__main__":
    main()
