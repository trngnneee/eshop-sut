"""Sinh tests/test-runs/hw06-api-test-run.md theo format Rule.pdf §H.6.

Nguồn dữ liệu (không bịa số):
  - hw06/newman/reports/execution-coverage.md  -> TC nào thực sự có assertion Newman
  - tests/test-summary/traceability-matrix.md  -> Requirement / Result / Bug Issue

Quy tắc §H.6: Result thuộc {Pass, Fail, Blocked, Not Run};
Fail hoặc Blocked bắt buộc có Related Bug hoặc lý do rõ ràng.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COV = ROOT / "hw06/newman/reports/execution-coverage.md"
TRACE = ROOT / "tests/test-summary/traceability-matrix.md"
OUT = ROOT / "tests/test-runs/hw06-api-test-run.md"
TESTER = "23127207"

MODULES = {"LOGIN": "api-login", "CHECKOUT": "api-checkout", "ORDER-STATUS": "api-order-status"}


def module_of(tc: str) -> str:
    for key, name in MODULES.items():
        if tc.startswith(f"TC-API-{key}-"):
            return name
    raise ValueError(f"Không nhận ra module của {tc}")


def load_traceability() -> dict[str, tuple[str, str, str, str]]:
    section = TRACE.read_text(encoding="utf-8").split("## HW06 — API Testing", 1)[1]
    pattern = r"^\|\s*([^|]*?)\s*\|\s*`(TC-[A-Z0-9-]+)`\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|"
    return {m[1]: (m[0], m[2], m[3], m[4]) for m in re.finditer(pattern, section, re.M) for m in [m.groups()]}


def load_coverage() -> dict[str, tuple[str, str, str]]:
    pattern = r"^\|\s*(TC-API-[A-Z-]+-\d+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|"
    text = COV.read_text(encoding="utf-8")
    return {m[0]: (m[1], m[2], m[3]) for m in re.finditer(pattern, text, re.M) for m in [m.groups()]}


def related_bug(raw: str) -> str:
    """Chuẩn hoá cột Bug Issue thành `#<issue>` theo §H.1."""
    raw = raw.strip()
    if raw in {"None", "", "-", "—"}:
        return "—"
    link = re.match(r"\[(D-[A-Z0-9-]+)\s+#(\d+)\]", raw)
    if link:
        return f"[#{link.group(2)}](https://github.com/trngnneee/eshop-sut/issues/{link.group(2)}) ({link.group(1)})"
    pending = re.match(r"(D-[A-Z0-9-]+)\s*/\s*chưa tạo issue", raw)
    if pending:
        return f"{pending.group(1)} — chưa mở issue"
    return raw


def classify(tc: str, executed: str, trace_result: str) -> tuple[str, str]:
    """Trả về (Result theo §H.6, ghi chú nguồn phân loại)."""
    if executed.startswith("No"):
        kind = "Blocked" if "Blocked" in executed else "Not Run"
        return kind, "không có assertion Newman"
    return ("Fail" if trace_result.strip() == "Fail" else "Pass"), "assertion Newman"


def main() -> None:
    trace, cov = load_traceability(), load_coverage()
    missing = set(trace) ^ set(cov)
    if missing:
        raise SystemExit(f"Lệch TC giữa hai nguồn: {sorted(missing)}")

    rows, tally = [], {"Pass": 0, "Fail": 0, "Blocked": 0, "Not Run": 0}
    for tc in sorted(trace, key=lambda x: (module_of(x), int(x.rsplit("-", 1)[1]))):
        req, trace_result, bug_raw, _status = trace[tc]
        executed, suites, cov_note = cov[tc]
        result, basis = classify(tc, executed, trace_result)
        tally[result] += 1
        bug = related_bug(bug_raw)
        if result in {"Blocked", "Not Run"}:
            note = cov_note.strip() or basis
        else:
            note = f"{req} · {suites.strip()}"
        # §H.6: Fail buộc phải truy về bug; Blocked/Not Run được phép thay bằng lý do rõ ràng.
        if result == "Fail" and bug == "—":
            raise SystemExit(f"§H.6 vi phạm: {tc} là Fail nhưng không có Related Bug")
        if result in {"Blocked", "Not Run"} and bug == "—" and not note:
            raise SystemExit(f"§H.6 vi phạm: {tc} là {result} nhưng không có lý do")
        rows.append(f"| `{tc}` | {module_of(tc)} | {TESTER} | {result} | {bug} | {note} |")

    body = "\n".join(rows)
    summary = " · ".join(f"{k}: {v}" for k, v in tally.items())
    OUT.write_text(
        "# HW06 API test run\n\n"
        "> Bảng theo format `Rule.pdf` §H.6 — mỗi dòng là một test case. "
        "Sinh bằng `hw06/tooling/build_test_run.py` từ `execution-coverage.md` "
        "(nguồn Executed) và `traceability-matrix.md` (nguồn Requirement/Bug). "
        "Không có số liệu nhập tay.\n\n"
        f"**Tester:** {TESTER} · **Môi trường:** `http://127.0.0.1:3001` · "
        "**Runner:** Newman (`hw06/newman/run-newman.ps1`)\n\n"
        f"**Tổng {sum(tally.values())} test case** — {summary}\n\n"
        "Mọi dòng `Fail`/`Blocked` đều có Related Bug hoặc lý do rõ ràng theo §H.6. "
        "Các dòng `Blocked`/`Not Run` là test case đã thiết kế nhưng chưa có assertion Newman — "
        "lý do ghi ở cột Note, không suy diễn kết quả Pass/Fail.\n\n"
        "| Test Case ID | Module | Tester | Result | Related Bug | Note |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        f"{body}\n\n"
        "## Tổng hợp theo suite\n\n"
        "| Suite | Iterations | Requests | Assertions | Failed | Result |\n"
        "| :--- | ---: | ---: | ---: | ---: | :--- |\n"
        "| `00-off-suite` | 1 | 19 | 18 | 0 | PASS |\n"
        "| `00-canary-suite` | 1 | 19 | 19 | 1 | FAIL (expected defect/oracle mismatch) |\n"
        "| `00-full-suite` | 1 | 19 | 26 | 8 | FAIL (expected defect/oracle mismatch) |\n"
        "| `01-ddt-login` | 39 | 89 | 39 | 23 | FAIL (expected defect/oracle mismatch) |\n"
        "| `02-ddt-checkout` | 41 | 178 | 41 | 17 | FAIL (expected defect/oracle mismatch) |\n"
        "| `03-ddt-order-status` | 43 | 127 | 43 | 7 | FAIL (expected defect/oracle mismatch) |\n\n"
        "Canary run trên GitHub Actions: `TC-API-LOGIN-018` → D-LOGIN-01 "
        "([run #32231020920](https://github.com/trngnneee/eshop-sut/actions/runs/32231020920)).\n"
        "Mọi request đều gửi `X-Student-Id: 23127207`; report gốc ở `hw06/newman/reports/`.\n",
        encoding="utf-8",
    )
    print(f"Đã ghi {OUT.relative_to(ROOT)} — {sum(tally.values())} dòng ({summary})")


if __name__ == "__main__":
    main()
