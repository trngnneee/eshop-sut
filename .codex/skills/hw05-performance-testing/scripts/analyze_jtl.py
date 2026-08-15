#!/usr/bin/env python3
"""Summarize JMeter .jtl CSV or XML logs without external dependencies."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = (len(ordered) - 1) * pct
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (rank - low)


def parse_success(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "ok"}


def load_csv(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            elapsed = row.get("elapsed") or row.get("Elapsed") or row.get("t") or 0
            timestamp = row.get("timeStamp") or row.get("timestamp") or row.get("ts") or 0
            label = row.get("label") or row.get("Label") or row.get("lb") or "sample"
            success = row.get("success") or row.get("Success") or row.get("s") or ""
            code = row.get("responseCode") or row.get("response_code") or row.get("rc") or ""
            rows.append(
                {
                    "elapsed": float(elapsed or 0),
                    "timestamp": float(timestamp or 0),
                    "label": str(label),
                    "success": parse_success(success),
                    "code": str(code),
                }
            )
    return rows


def load_xml(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for _, elem in ET.iterparse(path, events=("end",)):
        if elem.tag in {"sample", "httpSample"}:
            rows.append(
                {
                    "elapsed": float(elem.attrib.get("t", 0)),
                    "timestamp": float(elem.attrib.get("ts", 0)),
                    "label": elem.attrib.get("lb", "sample"),
                    "success": parse_success(elem.attrib.get("s", "")),
                    "code": elem.attrib.get("rc", ""),
                }
            )
        elem.clear()
    return rows


def load_rows(path: Path) -> list[dict[str, object]]:
    prefix = path.read_text(encoding="utf-8-sig", errors="ignore")[:200].lstrip()
    if prefix.startswith("<"):
        return load_xml(path)
    return load_csv(path)


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "total": summarize_group(rows),
        "by_label": summarize_by_label(rows),
    }


def summarize_group(rows: list[dict[str, object]]) -> dict[str, object]:
    elapsed = [float(row["elapsed"]) for row in rows]
    failures = [row for row in rows if not bool(row["success"])]
    timestamps = [float(row["timestamp"]) for row in rows if float(row["timestamp"]) > 0]
    duration_s = 0.0
    if timestamps:
        duration_s = max((max(timestamps) - min(timestamps)) / 1000.0, 0.001)
    labels: dict[str, int] = {}
    codes: dict[str, int] = {}
    for row in rows:
        labels[str(row["label"])] = labels.get(str(row["label"]), 0) + 1
        code = str(row["code"])
        if code:
            codes[code] = codes.get(code, 0) + 1
    count = len(rows)
    return {
        "samples": count,
        "failures": len(failures),
        "error_rate_percent": round((len(failures) / count * 100.0) if count else 0.0, 3),
        "duration_seconds": round(duration_s, 3),
        "throughput_rps": round((count / duration_s) if duration_s else 0.0, 3),
        "elapsed_ms": {
            "min": round(min(elapsed), 3) if elapsed else 0.0,
            "avg": round(statistics.mean(elapsed), 3) if elapsed else 0.0,
            "median": round(statistics.median(elapsed), 3) if elapsed else 0.0,
            "p90": round(percentile(elapsed, 0.90), 3),
            "p95": round(percentile(elapsed, 0.95), 3),
            "p99": round(percentile(elapsed, 0.99), 3),
            "max": round(max(elapsed), 3) if elapsed else 0.0,
        },
        "labels": labels,
        "response_codes": codes,
    }


def summarize_by_label(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["label"]), []).append(row)
    return {
        label: summarize_group(label_rows)
        for label, label_rows in sorted(grouped.items())
    }


def print_markdown(path: Path, summary: dict[str, object]) -> None:
    total = summary["total"]
    assert isinstance(total, dict)
    elapsed = total["elapsed_ms"]
    assert isinstance(elapsed, dict)
    print(f"# JTL Summary: {path.name}")
    print()
    print("## Total Metrics")
    print()
    print(f"- Samples: {total['samples']}")
    print(f"- Failures: {total['failures']}")
    print(f"- Error rate: {total['error_rate_percent']}%")
    print(f"- Duration: {total['duration_seconds']} s")
    print(f"- Throughput: {total['throughput_rps']} req/s")
    print(f"- Latency p95: {elapsed['p95']} ms")
    print(f"- Latency p99: {elapsed['p99']} ms")
    print(f"- Latency avg: {elapsed['avg']} ms")
    print(f"- Latency max: {elapsed['max']} ms")
    print()
    print("## Per-Sampler Metrics")
    print()
    print("| Sampler / endpoint | Samples | Failures | Error % | Avg ms | p95 ms | p99 ms | Max ms | Throughput req/s |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    by_label = summary["by_label"]
    assert isinstance(by_label, dict)
    for label, label_summary in by_label.items():
        assert isinstance(label_summary, dict)
        label_elapsed = label_summary["elapsed_ms"]
        assert isinstance(label_elapsed, dict)
        print(
            f"| {label} | "
            f"{label_summary['samples']} | "
            f"{label_summary['failures']} | "
            f"{label_summary['error_rate_percent']} | "
            f"{label_elapsed['avg']} | "
            f"{label_elapsed['p95']} | "
            f"{label_elapsed['p99']} | "
            f"{label_elapsed['max']} | "
            f"{label_summary['throughput_rps']} |"
        )
    print()
    print("## Response Codes")
    for code, count in sorted(dict(total["response_codes"]).items()):
        print(f"- {code}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("jtl", type=Path)
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args()
    if not args.jtl.exists():
        print(f"File not found: {args.jtl}", file=sys.stderr)
        return 2
    summary = summarize(load_rows(args.jtl))
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_markdown(args.jtl, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
