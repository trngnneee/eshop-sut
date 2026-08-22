#!/usr/bin/env python3
"""
consolidate.py — Stage 5 của api-test-generator skill (HW06 - API Testing).

Gom 4 file test case theo stage (domain partition / state transition /
security / schema validation) của MỘT api-slug thành 1 file CSV master,
đánh lại ID thống nhất, và báo cáo số lượng theo từng category so với
ngưỡng >=35 test case / API mà đề bài yêu cầu.

Usage:
    python3 consolidate.py --api-dir ./API-testing/<api-slug> [--slug LOGIN] [--min-total 35]

Input mong đợi trong --api-dir:
    01_domain_partitions.json
    02_state_transitions.json
    03_security.json
    04_schema_validation.json
(File nào không tồn tại sẽ được bỏ qua với cảnh báo, không làm script lỗi.)

Output:
    test_cases_master.csv  (ghi trong chính --api-dir)
    In ra terminal: bảng đếm theo category + tổng + cảnh báo nếu < min-total.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

STAGE_FILES = [
    ("01_domain_partitions.json", "DomainPartition", "DP"),
    ("02_state_transitions.json", "StateTransition", "ST"),
    ("03_security.json", "Security", "SEC"),
    ("04_schema_validation.json", "SchemaValidation", "SV"),
]

# Cột cuối cùng trong CSV (thứ tự cố định, dễ import Excel).
CSV_COLUMNS = [
    "id",
    "category",
    "endpoint",
    "related_requirement",
    "title",
    "preconditions",
    "request_method",
    "request_path",
    "request_headers",
    "request_params",
    "request_body",
    "expected_status",
    "expected_result",
    "priority",
    # category-specific
    "parameter",
    "partition_type",
    "from_state",
    "to_state",
    "action",
    "expected_allowed",
    "sec_id",
    "attack_vector",
    "schema_ref",
    "fields_checked",
    "notes",
]


def load_stage_file(path: Path):
    if not path.exists():
        print(f"  [!] Bỏ qua (không tìm thấy): {path.name}")
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  [!] Lỗi JSON trong {path.name}: {e}", file=sys.stderr)
        return []
    if not isinstance(data, list):
        print(f"  [!] {path.name} phải là 1 JSON array, bỏ qua.", file=sys.stderr)
        return []
    return data


def flatten(tc: dict, final_id: str) -> dict:
    req = tc.get("request", {}) or {}
    row = {col: "" for col in CSV_COLUMNS}
    row.update(
        {
            "id": final_id,
            "category": tc.get("category", ""),
            "endpoint": tc.get("endpoint", ""),
            "related_requirement": tc.get("related_requirement", ""),
            "title": tc.get("title", ""),
            "preconditions": tc.get("preconditions", ""),
            "request_method": req.get("method", ""),
            "request_path": req.get("path", ""),
            "request_headers": json.dumps(req.get("headers", {}), ensure_ascii=False) if req.get("headers") else "",
            "request_params": json.dumps(req.get("params", {}), ensure_ascii=False) if req.get("params") else "",
            "request_body": json.dumps(req.get("body", {}), ensure_ascii=False) if req.get("body") else "",
            "expected_status": tc.get("expected_status", ""),
            "expected_result": tc.get("expected_result", ""),
            "priority": tc.get("priority", ""),
            "parameter": tc.get("parameter", ""),
            "partition_type": tc.get("partition_type", ""),
            "from_state": tc.get("from_state", ""),
            "to_state": tc.get("to_state", ""),
            "action": tc.get("action", ""),
            "expected_allowed": tc.get("expected_allowed", ""),
            "sec_id": tc.get("sec_id", ""),
            "attack_vector": tc.get("attack_vector", ""),
            "schema_ref": tc.get("schema_ref", ""),
            "fields_checked": ", ".join(tc.get("fields_checked", [])) if tc.get("fields_checked") else "",
            "notes": tc.get("notes", ""),
        }
    )
    return row


def main():
    parser = argparse.ArgumentParser(description="Gộp 4 stage JSON thành 1 CSV master cho 1 API.")
    parser.add_argument("--api-dir", required=True, help="Thư mục ./API-testing/<api-slug>")
    parser.add_argument("--slug", default=None, help="API slug dùng trong ID (mặc định: tên thư mục, viết hoa)")
    parser.add_argument("--min-total", type=int, default=35, help="Ngưỡng tối thiểu tổng số test case (mặc định 35)")
    args = parser.parse_args()

    api_dir = Path(args.api_dir)
    if not api_dir.is_dir():
        print(f"Lỗi: không tìm thấy thư mục {api_dir}", file=sys.stderr)
        sys.exit(1)

    slug = (args.slug or api_dir.name).upper().replace(" ", "-")

    print(f"== Consolidate: {api_dir} (slug={slug}) ==")

    all_rows = []
    counts = {}
    for filename, category, prefix in STAGE_FILES:
        items = load_stage_file(api_dir / filename)
        counts[category] = len(items)
        for i, tc in enumerate(items, start=1):
            final_id = f"TC-{slug}-{prefix}-{i:03d}"
            all_rows.append(flatten(tc, final_id))
        print(f"  {filename:<28} -> {len(items):>3} test case(s)")

    out_path = api_dir / "test_cases_master.csv"
    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    total = len(all_rows)
    print(f"\n-- Tổng kết: {api_dir.name} --")
    for filename, category, prefix in STAGE_FILES:
        print(f"  {category:<16}: {counts.get(category, 0)}")
    print(f"  {'TOTAL':<16}: {total}")
    print(f"\nĐã ghi: {out_path}")

    if total < args.min_total:
        print(
            f"\n[CẢNH BÁO] Tổng {total} < ngưỡng yêu cầu {args.min_total}. "
            f"Quay lại đúng stage đang thiếu để bổ sung (đừng nhồi bừa vào 1 stage)."
        )
        sys.exit(2)
    else:
        print(f"\nĐạt ngưỡng >= {args.min_total} test case.")


if __name__ == "__main__":
    main()