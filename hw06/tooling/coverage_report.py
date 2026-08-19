#!/usr/bin/env python3
"""Reconcile the final HW06 test inventory with real Newman JSON evidence.

The report only considers a test case executed when its TC ID appears in a
Newman assertion name.  It never infers execution from a data-file row or from
the Postman collection source.  This keeps the coverage number auditable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from sanitize_public_artifacts import redact_text


ROOT = Path(__file__).resolve().parents[2]
HW06 = ROOT / "hw06"
REPORTS = HW06 / "newman" / "reports"
OUTPUT = REPORTS / "execution-coverage.md"

TC_RE = re.compile(r"TC-API-(?:LOGIN|CHECKOUT|ORDER-STATUS)-\d{3}")
TABLES = (
    HW06 / "api-01-login" / "test-cases.md",
    HW06 / "api-02-checkout" / "test-cases.md",
    HW06 / "api-03-admin-order-status" / "test-cases.md",
)

# These are deliberately explicit.  A missing assertion must never silently
# become "manual" just to improve the reported percentage.
NON_AUTOMATED: dict[str, tuple[str, str]] = {
    "TC-API-LOGIN-024": (
        "Blocked",
        "Tiền điều kiện yêu cầu TC-023 đăng nhập thành công sau hai lần sai, nhưng D-LOGIN-01 khóa tài khoản sớm nên không thể đi tới trạng thái reset cần kiểm thử.",
    ),
    "TC-API-LOGIN-041": (
        "Manual",
        "Phải chờ lock thực tế 180 giây rồi kiểm tra residual state; tách khỏi regression tự động để tránh một iteration kéo dài và dễ nhiễu thời gian.",
    ),
    "TC-API-LOGIN-042": (
        "Blocked",
        "Cần ký JWT bằng secret của SUT; không nhúng signing secret hoặc forged token vào collection/report công khai.",
    ),
    "TC-API-CHECKOUT-029": (
        "Blocked",
        "SUT phát JWT không có exp và không cung cấp signing fixture an toàn, nên không thể tạo token hợp lệ nhưng đã hết hạn mà không sao chép secret vào artifact.",
    ),
    "TC-API-ORDER-STATUS-041": (
        "Blocked",
        "SUT không có Dashboard/revenue API để quan sát hậu điều kiện doanh thu; transition canceled→delivered được phủ riêng bởi TC-024.",
    ),
}


@dataclass(frozen=True)
class AssertionEvidence:
    suite: str
    passed: bool
    assertion: str
    error: str = ""


def parse_inventory() -> tuple[list[str], dict[str, Path]]:
    ids: list[str] = []
    owners: dict[str, Path] = {}
    for path in TABLES:
        text = path.read_text(encoding="utf-8")
        found = []
        for line in text.splitlines():
            if not line.lstrip().startswith("|"):
                continue
            match = TC_RE.search(line)
            if match:
                found.append(match.group(0))
        if len(found) != len(set(found)):
            raise ValueError(f"Duplicate TC ID in {path}")
        for tc_id in found:
            if tc_id in owners:
                raise ValueError(f"Duplicate TC ID across tables: {tc_id}")
            owners[tc_id] = path
            ids.append(tc_id)
    return ids, owners


def error_text(value: object) -> str:
    if not value:
        return ""
    if isinstance(value, dict):
        text = str(value.get("message") or value.get("name") or "assertion failed")
    else:
        text = str(value)
    return redact_text(text)[0]


def read_newman_evidence() -> tuple[dict[str, list[AssertionEvidence]], list[str]]:
    evidence: dict[str, list[AssertionEvidence]] = defaultdict(list)
    parsed_suites: list[str] = []
    for path in sorted(REPORTS.glob("*.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot parse Newman JSON {path}: {exc}") from exc
        executions = document.get("run", {}).get("executions")
        if not isinstance(executions, list):
            continue
        suite = path.stem
        parsed_suites.append(suite)
        for execution in executions:
            for assertion in execution.get("assertions") or []:
                name = str(assertion.get("assertion") or "")
                matches = set(TC_RE.findall(name))
                # findall() on this regex returns only the non-capturing full
                # match in modern Python, but finditer is unambiguous and also
                # protects this code if the regex is extended later.
                matches = {match.group(0) for match in TC_RE.finditer(name)}
                err = error_text(assertion.get("error"))
                for tc_id in matches:
                    evidence[tc_id].append(
                        AssertionEvidence(
                            suite=suite,
                            passed=not bool(assertion.get("error")),
                            assertion=name,
                            error=err,
                        )
                    )
    return evidence, parsed_suites


def module_name(tc_id: str) -> str:
    if "ORDER-STATUS" in tc_id:
        return "API-3"
    if "CHECKOUT" in tc_id:
        return "API-2"
    return "API-1"


def cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def render_result(items: list[AssertionEvidence]) -> str:
    by_suite: dict[str, list[AssertionEvidence]] = defaultdict(list)
    for item in items:
        by_suite[item.suite].append(item)
    parts = []
    for suite in sorted(by_suite):
        suite_items = by_suite[suite]
        failed = [item for item in suite_items if not item.passed]
        if failed:
            message = failed[0].error or "assertion failed"
            parts.append(f"`{suite}`: FAIL — {cell(message)}")
        else:
            parts.append(f"`{suite}`: PASS")
    return "; ".join(parts)


def render_report(inventory: list[str], evidence: dict[str, list[AssertionEvidence]], suites: list[str]) -> str:
    executed = [tc_id for tc_id in inventory if evidence.get(tc_id)]
    manual = [tc_id for tc_id in inventory if not evidence.get(tc_id) and NON_AUTOMATED.get(tc_id, ("", ""))[0] == "Manual"]
    blocked = [tc_id for tc_id in inventory if not evidence.get(tc_id) and NON_AUTOMATED.get(tc_id, ("", ""))[0] == "Blocked"]
    unclassified = [tc_id for tc_id in inventory if not evidence.get(tc_id) and tc_id not in NON_AUTOMATED]
    percent = len(executed) * 100 / len(inventory) if inventory else 0.0

    lines = [
        "# HW06 Newman execution coverage",
        "",
        "> Nguồn duy nhất cho cột Executed là TC ID xuất hiện trong tên assertion của các file Newman JSON thật. Dòng có trong data file/collection nhưng không có assertion không được tính.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| :--- | ---: |",
        f"| Final test cases | {len(inventory)} |",
        f"| Executed by Newman assertion | {len(executed)} |",
        f"| Execution coverage | {percent:.1f}% |",
        f"| Manual | {len(manual)} |",
        f"| Blocked | {len(blocked)} |",
        f"| Unclassified gap | {len(unclassified)} |",
        "",
        "| API | Final | Executed | Coverage |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for module in ("API-1", "API-2", "API-3"):
        module_ids = [tc_id for tc_id in inventory if module_name(tc_id) == module]
        module_executed = [tc_id for tc_id in module_ids if evidence.get(tc_id)]
        module_percent = len(module_executed) * 100 / len(module_ids)
        lines.append(f"| {module} | {len(module_ids)} | {len(module_executed)} | {module_percent:.1f}% |")

    lines += [
        "",
        f"Parsed Newman suites ({len(suites)}): " + ", ".join(f"`{name}`" for name in sorted(suites)) + ".",
        "",
        "## Reconciliation",
        "",
        "| TC ID | Executed? | Suite | Assertion result |",
        "| :--- | :---: | :--- | :--- |",
    ]
    for tc_id in inventory:
        items = evidence.get(tc_id, [])
        if items:
            suite_names = ", ".join(f"`{name}`" for name in sorted({item.suite for item in items}))
            lines.append(f"| {tc_id} | Yes | {suite_names} | {render_result(items)} |")
        else:
            status, reason = NON_AUTOMATED.get(tc_id, ("Unclassified", "Không có assertion Newman và chưa được phân loại."))
            lines.append(f"| {tc_id} | No — {status} | — | {cell(reason)} |")
    return "\n".join(lines) + "\n"


def annotate_table(path: Path, evidence: dict[str, list[AssertionEvidence]]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: list[str] = []
    in_inventory_table = False
    headers: list[str] = []
    for line in lines:
        if line.startswith("| TC ID |"):
            headers = [part.strip() for part in line.strip().strip("|").split("|")]
            if "Execution" not in headers:
                headers += ["Execution", "Lý do"]
            result.append("| " + " | ".join(headers) + " |")
            in_inventory_table = True
            continue
        if in_inventory_table and line.startswith("| :---"):
            result.append("| " + " | ".join(":---" for _ in headers) + " |")
            continue
        match = TC_RE.search(line) if in_inventory_table and line.startswith("|") else None
        if match:
            cells = [part.strip() for part in line.strip().strip("|").split("|")]
            tc_id = match.group(0)
            if "Execution" in headers:
                base_count = len(headers) - 2
                cells = cells[:base_count]
            if evidence.get(tc_id):
                execution, reason = "Automated", "—"
            else:
                execution, reason = NON_AUTOMATED.get(tc_id, ("Blocked", "Không có assertion Newman; chưa phân loại nguyên nhân."))
            cells += [execution, cell(reason)]
            result.append("| " + " | ".join(cells) + " |")
            continue
        if in_inventory_table and line and not line.startswith("|"):
            in_inventory_table = False
        result.append(line)
    path.write_text("\n".join(result) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotate", action="store_true", help="Update Execution/Lý do columns in the three final test tables")
    parser.add_argument("--minimum", type=float, default=90.0, help="Required executed coverage percentage")
    args = parser.parse_args()

    inventory, _ = parse_inventory()
    evidence, suites = read_newman_evidence()
    unknown = sorted(tc_id for tc_id in evidence if tc_id not in set(inventory))
    if unknown:
        print("Warning: Newman assertions reference unknown TC IDs: " + ", ".join(unknown), file=sys.stderr)

    OUTPUT.write_text(render_report(inventory, evidence, suites), encoding="utf-8")
    if args.annotate:
        for path in TABLES:
            annotate_table(path, evidence)

    executed = sum(1 for tc_id in inventory if evidence.get(tc_id))
    coverage = executed * 100 / len(inventory)
    unclassified = [tc_id for tc_id in inventory if not evidence.get(tc_id) and tc_id not in NON_AUTOMATED]
    print(f"Executed {executed}/{len(inventory)} test cases ({coverage:.1f}%).")
    print(f"Report: {OUTPUT}")
    if unclassified:
        print("Unclassified gaps: " + ", ".join(unclassified), file=sys.stderr)
        return 3
    if coverage < args.minimum:
        print(f"Coverage {coverage:.1f}% is below required {args.minimum:.1f}%.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
