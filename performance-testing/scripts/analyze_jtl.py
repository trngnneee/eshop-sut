#!/usr/bin/env python3
"""
analyze_jtl.py - Analyze JMeter CSV .jtl logs and produce summary.json + summary.md.
Follows nearest-rank ISO 80000-2 percentile specification to match JMeter HTML reports.
"""

import argparse
import csv
import datetime
import json
import math
import os
import sys

def percentile_nearest_rank(sorted_values, p):
    n = len(sorted_values)
    if n == 0:
        return 0
    rank = math.ceil(p / 100.0 * n)
    return sorted_values[max(0, rank - 1)]

def analyze_jtl(jtl_path, out_dir=None, scenario_name=None, slice_sec=60, resource_csv=None):
    if not os.path.exists(jtl_path):
        print(f"Error: JTL file not found: {jtl_path}", file=sys.stderr)
        sys.exit(1)

    if out_dir is None:
        out_dir = os.path.dirname(jtl_path)
    os.makedirs(out_dir, exist_ok=True)

    if scenario_name is None:
        base = os.path.basename(jtl_path)
        parts = base.split('_')
        if len(parts) >= 2:
            scenario_name = parts[1]
        else:
            scenario_name = "Performance"

    # Data structures
    samples_by_label = {}
    latencies_by_label = {}
    bytes_by_label = {}
    errors_by_label = {}
    response_codes_count = {}
    
    all_timestamps = []
    all_elapsed = []
    all_threads_list = []
    total_samples = 0
    total_errors = 0
    corrupted_lines = 0

    # Slices
    slice_data = {}

    # Open with utf-8, fallback utf-8-sig
    encoding = 'utf-8'
    try:
        with open(jtl_path, 'r', encoding=encoding) as f:
            f.readline()
    except UnicodeDecodeError:
        encoding = 'utf-8-sig'

    with open(jtl_path, 'r', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = int(row['timeStamp'])
                elapsed = int(row['elapsed'])
                label = row['label']
                success_str = row['success'].strip().lower()
                success = (success_str == 'true')
                resp_code = row.get('responseCode', 'UNKNOWN')
                byte_count = int(row.get('bytes', 0))
                latency = int(row.get('Latency', 0))
                all_threads = int(row.get('allThreads', 0))
            except (ValueError, KeyError):
                corrupted_lines += 1
                continue

            total_samples += 1
            if not success:
                total_errors += 1

            all_timestamps.append(ts)
            all_elapsed.append(elapsed)
            all_threads_list.append(all_threads)

            response_codes_count[resp_code] = response_codes_count.get(resp_code, 0) + 1

            if label not in samples_by_label:
                samples_by_label[label] = []
                latencies_by_label[label] = []
                bytes_by_label[label] = []
                errors_by_label[label] = 0

            samples_by_label[label].append(elapsed)
            latencies_by_label[label].append(latency)
            bytes_by_label[label].append(byte_count)
            if not success:
                errors_by_label[label] += 1

    if total_samples == 0:
        print(f"Warning: No valid samples found in {jtl_path}", file=sys.stderr)
        return

    min_ts = min(all_timestamps)
    max_ts = max(t + e for t, e in zip(all_timestamps, all_elapsed))
    duration_sec = max(1.0, (max_ts - min_ts) / 1000.0)
    throughput_rps = round(total_samples / duration_sec, 2)
    overall_err_pct = round((total_errors / total_samples) * 100, 3)
    max_threads = max(all_threads_list) if all_threads_list else 0

    # Calculate time slices
    num_slices = max(1, math.ceil(duration_sec / slice_sec))
    for s_idx in range(num_slices):
        slice_label = f"{s_idx * slice_sec}-{(s_idx + 1) * slice_sec}s"
        slice_data[slice_label] = {'elapsed': [], 'errors': 0, 'threads': []}

    for t, e, s, ath in zip(all_timestamps, all_elapsed, [r == 'true' for r in [str(x) for x in range(len(all_timestamps))]], all_threads_list):
        offset_sec = (t - min_ts) / 1000.0
        s_idx = min(num_slices - 1, int(offset_sec // slice_sec))
        slice_label = f"{s_idx * slice_sec}-{(s_idx + 1) * slice_sec}s"
        slice_data[slice_label]['elapsed'].append(e)
        slice_data[slice_label]['threads'].append(ath)

    # Label statistics
    labels_summary = {}
    for label, el_list in samples_by_label.items():
        el_sorted = sorted(el_list)
        cnt = len(el_sorted)
        errs = errors_by_label[label]
        err_pct = round((errs / cnt) * 100, 3)
        lat_list = latencies_by_label[label]
        lat_sorted = sorted(lat_list)
        b_list = bytes_by_label[label]

        labels_summary[label] = {
            "count": cnt,
            "errors": errs,
            "error_rate_pct": err_pct,
            "elapsed": {
                "min": el_sorted[0],
                "avg": round(sum(el_sorted) / cnt, 1),
                "max": el_sorted[-1],
                "p50": percentile_nearest_rank(el_sorted, 50),
                "p90": percentile_nearest_rank(el_sorted, 90),
                "p95": percentile_nearest_rank(el_sorted, 95),
                "p99": percentile_nearest_rank(el_sorted, 99)
            },
            "latency": {
                "avg": round(sum(lat_sorted) / cnt, 1),
                "p95": percentile_nearest_rank(lat_sorted, 95)
            },
            "bytes": {
                "avg": round(sum(b_list) / cnt, 1),
                "total": sum(b_list)
            },
            "throughput_rps": round(cnt / duration_sec, 2)
        }

    # Time slices list
    time_slices_summary = []
    for slice_label, s_info in slice_data.items():
        s_el = s_info['elapsed']
        s_cnt = len(s_el)
        if s_cnt > 0:
            s_sorted = sorted(s_el)
            avg_th = round(sum(s_info['threads']) / s_cnt, 1) if s_info['threads'] else 0
            p95_val = percentile_nearest_rank(s_sorted, 95)
            time_slices_summary.append({
                "slice": slice_label,
                "samples": s_cnt,
                "p95": p95_val,
                "avg_allThreads": avg_th
            })

    # Resource metrics integration (if resource CSV provided)
    resource_stats = None
    if resource_csv and os.path.exists(resource_csv):
        res_ws = []
        res_pm = []
        res_cpu = []
        with open(resource_csv, 'r', encoding='utf-8') as rf:
            r_reader = csv.DictReader(rf)
            for r_row in r_reader:
                try:
                    res_ws.append(float(r_row['working_set_mb']))
                    res_pm.append(float(r_row['private_mb']))
                    res_cpu.append(float(r_row['cpu_percent']))
                except (ValueError, KeyError):
                    continue
        if res_pm:
            init_pm = res_pm[0]
            final_pm = res_pm[-1]
            max_pm = max(res_pm)
            avg_cpu = round(sum(res_cpu) / len(res_cpu), 1) if res_cpu else 0
            max_cpu = max(res_cpu) if res_cpu else 0
            dur_mins = duration_sec / 60.0
            leak_rate = round((final_pm - init_pm) / max(0.1, dur_mins), 2)
            resource_stats = {
                "initial_private_mb": init_pm,
                "final_private_mb": final_pm,
                "max_private_mb": max_pm,
                "avg_cpu_percent": avg_cpu,
                "max_cpu_percent": max_cpu,
                "memory_leak_mb_per_min": leak_rate
            }

    all_sorted = sorted(all_elapsed) if all_elapsed else []
    overall_elapsed_stats = {
        "min": all_sorted[0] if all_sorted else 0,
        "avg": round(sum(all_sorted) / len(all_sorted), 1) if all_sorted else 0,
        "max": all_sorted[-1] if all_sorted else 0,
        "p50": percentile_nearest_rank(all_sorted, 50),
        "p90": percentile_nearest_rank(all_sorted, 90),
        "p95": percentile_nearest_rank(all_sorted, 95),
        "p99": percentile_nearest_rank(all_sorted, 99)
    }

    # Complete Summary JSON
    summary_obj = {
        "source_file": os.path.relpath(jtl_path, os.getcwd()).replace('\\', '/'),
        "generated_at": datetime.datetime.now().isoformat(),
        "corrupted_lines": corrupted_lines,
        "run": {
            "scenario": scenario_name,
            "start_ts": min_ts,
            "end_ts": max_ts,
            "duration_sec": round(duration_sec, 1),
            "total_samples": total_samples,
            "total_errors": total_errors,
            "error_rate_pct": overall_err_pct,
            "throughput_rps": throughput_rps,
            "max_concurrent_threads": max_threads,
            "overall_elapsed": overall_elapsed_stats
        },
        "labels": labels_summary,
        "errors_breakdown": response_codes_count,
        "time_slices": time_slices_summary
    }

    if resource_stats:
        summary_obj["resource_stats"] = resource_stats

    # Write summary.json
    json_path = os.path.join(out_dir, "summary.json")
    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump(summary_obj, jf, indent=2)
    print(f"[analyze] Wrote {json_path}")

    # Write summary.md
    md_path = os.path.join(out_dir, "summary.md")
    with open(md_path, 'w', encoding='utf-8') as mf:
        mf.write(f"### {scenario_name} — {os.path.basename(jtl_path)}\n\n")
        mf.write(f"**Tổng quan:** {total_samples:,} mẫu · {duration_sec:.1f} s · {throughput_rps} req/s · lỗi {overall_err_pct} % · tối đa {max_threads} threads\n\n")
        mf.write("| Label | Samples | Err% | Min | Avg | p50 | p90 | **p95** | p99 | Max | RPS | Avg Bytes |\n")
        mf.write("|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        
        # Sort labels 01_Login .. 05_Checkout
        sorted_labels = sorted(labels_summary.keys())
        for lbl in sorted_labels:
            info = labels_summary[lbl]
            el = info['elapsed']
            mf.write(f"| `{lbl}` | {info['count']} | {info['error_rate_pct']:.2f}% | {el['min']} | {el['avg']} | {el['p50']} | {el['p90']} | **{el['p95']}** | {el['p99']} | {el['max']} | {info['throughput_rps']} | {info['bytes']['avg']} |\n")

        if time_slices_summary:
            mf.write("\n#### Phân bố theo lát cắt thời gian\n\n")
            mf.write("| Khung thời gian | Số mẫu | **p95 (ms)** | Avg Threads |\n")
            mf.write("|:---|---:|---:|---:|\n")
            for sl in time_slices_summary:
                mf.write(f"| {sl['slice']} | {sl['samples']} | **{sl['p95']}** | {sl['avg_allThreads']} |\n")

        if resource_stats:
            mf.write("\n#### Thống kê tài nguyên hệ thống\n\n")
            mf.write(f"- **RAM Private bắt đầu:** {resource_stats['initial_private_mb']} MB\n")
            mf.write(f"- **RAM Private kết thúc:** {resource_stats['final_private_mb']} MB\n")
            mf.write(f"- **Trần RAM Private (Ceiling):** {resource_stats['max_private_mb']} MB\n")
            mf.write(f"- **Tốc độ tăng RAM:** {resource_stats['memory_leak_mb_per_min']} MB/phút\n")
            mf.write(f"- **CPU trung bình:** {resource_stats['avg_cpu_percent']} %\n")
            mf.write(f"- **CPU đỉnh:** {resource_stats['max_cpu_percent']} %\n")

    print(f"[analyze] Wrote {md_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze JMeter .jtl log files")
    parser.add_argument('--jtl', required=True, help="Path to raw .jtl CSV file")
    parser.add_argument('--out-dir', default=None, help="Directory to save summary files")
    parser.add_argument('--scenario', default=None, help="Scenario name (Load, Stress, Spike, Endurance)")
    parser.add_argument('--slice-sec', type=int, default=60, help="Time slice width in seconds")
    parser.add_argument('--resource-csv', default=None, help="Path to resource monitor CSV file")
    
    args = parser.parse_args()
    analyze_jtl(args.jtl, args.out_dir, args.scenario, args.slice_sec, args.resource_csv)
