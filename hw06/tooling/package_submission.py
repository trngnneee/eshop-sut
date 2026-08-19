#!/usr/bin/env python3
"""Export HW06 reports to PDF and build the submission ZIP.

The script intentionally fails closed when HUMAN-only evidence is absent. It
never creates, edits, or substitutes screenshots or the student-drawn diagram.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPO_ROOT = Path(__file__).resolve().parents[2]
HW06_ROOT = REPO_ROOT / "hw06"
DOCS_ROOT = REPO_ROOT / "docs" / "hw06"

HUMAN_ONLY_FILES = (
    Path("test-generator/diagram.png"),
    Path("evidence/screenshots/01-x-student-id-console.png"),
    Path("evidence/screenshots/04-ci-pass.png"),
    Path("evidence/screenshots/05-ci-fail.png"),
)

REQUIRED_HW06_FILES = (
    Path("README.md"),
    Path("report/main-report.md"),
    Path("report/ai-audit-report.md"),
    Path("report/ai-critique.md"),
    Path("report/bug-report.md"),
    Path("report/cicd-report.md"),
    Path("report/git-commit-log.txt"),
    Path("postman/EShop-HW06-23127207.postman_collection.json"),
    Path("postman/postman-features.md"),
    Path("newman/reports/00-full-suite.html"),
    Path("newman/reports/01-ddt-login.html"),
    Path("newman/reports/02-ddt-checkout.html"),
    Path("newman/reports/03-ddt-order-status.html"),
    Path("excel/test-cases.xlsx"),
    Path("excel/test-summary.xlsx"),
    Path("test-generator/design.md"),
    Path("test-generator/generator.py"),
)

REPORT_EXPORTS = (
    (Path("report/main-report.md"), "main-report.pdf"),
    (Path("report/ai-audit-report.md"), "ai-audit-report.pdf"),
    (Path("report/ai-critique.md"), "ai-critique.pdf"),
)

SUBMISSION_DIRS = (
    Path("api-01-login"),
    Path("api-02-checkout"),
    Path("api-03-admin-order-status"),
    Path("excel"),
    Path("evidence"),
    Path("newman"),
    Path("openapi"),
    Path("postman"),
    Path("report"),
)


class PackagingError(RuntimeError):
    """A submission gate or packaging operation failed."""


@contextmanager
def staging_workspace(output_dir: Path):
    """Create an exact, self-owned stage without tempfile's Windows ACL issue."""
    output_dir = output_dir.resolve()
    workspace = output_dir / (
        f".hw06-submission-stage-{os.getpid()}-{uuid.uuid4().hex}"
    )
    if workspace.exists():
        raise PackagingError(f"Unexpected staging collision: {workspace}")
    workspace.mkdir()
    stage = workspace / "submission"
    stage.mkdir()
    try:
        yield stage
    finally:
        resolved = workspace.resolve()
        if (
            resolved.parent != output_dir
            or not resolved.name.startswith(".hw06-submission-stage-")
        ):
            raise PackagingError(f"Refusing unsafe staging cleanup: {resolved}")
        shutil.rmtree(resolved)


def validate_grade(value: str) -> str:
    """Require the three-digit grade format mandated by the checklist."""
    if not re.fullmatch(r"\d{3}", value) or not 0 <= int(value) <= 100:
        raise argparse.ArgumentTypeError(
            "grade must be exactly three digits in [000, 100], for example 080"
        )
    return value


def relative_display(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def fail_for_missing(paths: list[Path], heading: str) -> None:
    if not paths:
        return
    details = "\n".join(f"  - {relative_display(path)}" for path in paths)
    raise PackagingError(
        f"{heading}\n{details}\n"
        "No PDF, fallback HTML, or ZIP was created. Do not replace HUMAN-only "
        "evidence with generated or simulated files."
    )


def validate_submission_inputs() -> None:
    """Run irreversible gates before creating any output directory or file."""
    missing_human = [
        HW06_ROOT / relative
        for relative in HUMAN_ONLY_FILES
        if not (HW06_ROOT / relative).is_file()
    ]
    fail_for_missing(
        missing_human,
        "HUMAN-only gate failed; the following required files are missing:",
    )

    missing_required = [
        HW06_ROOT / relative
        for relative in REQUIRED_HW06_FILES
        if not (HW06_ROOT / relative).is_file()
    ]
    missing_docs = []
    if not DOCS_ROOT.is_dir():
        missing_docs.append(DOCS_ROOT)
    else:
        expected_docs = [
            DOCS_ROOT / "01-requirements-analysis.md",
            DOCS_ROOT / "02-sut-defect-catalog.md",
            DOCS_ROOT / "03-execution-plan.md",
            DOCS_ROOT / "04-deliverables-checklist.md",
        ]
        missing_docs.extend(path for path in expected_docs if not path.is_file())
    fail_for_missing(
        missing_required + missing_docs,
        "Mandatory deliverables from checklist section 1 are missing:",
    )

    bug_screenshots = sorted(
        (HW06_ROOT / "evidence" / "screenshots").rglob("bug-*.png")
    )
    if len(bug_screenshots) < 15:
        raise PackagingError(
            "Bug evidence gate failed: expected at least 15 real bug screenshots "
            f"under hw06/evidence/screenshots, found {len(bug_screenshots)}."
        )

    critique = (HW06_ROOT / "report" / "ai-critique.md").read_text(encoding="utf-8")
    if "HUMAN-ONLY" in critique or "bản nháp" in critique.casefold():
        raise PackagingError(
            "Human authorship gate failed: hw06/report/ai-critique.md is still "
            "marked as a HUMAN-only draft. The student must rewrite and review it "
            "before packaging."
        )


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def valid_pdf(path: Path) -> bool:
    try:
        return path.is_file() and path.stat().st_size > 100 and path.read_bytes()[:4] == b"%PDF"
    except OSError:
        return False


def try_pandoc_pdf(source: Path, destination: Path) -> tuple[bool, str]:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return False, "pandoc not found"
    result = run_command(
        [
            pandoc,
            str(source),
            "--standalone",
            "--resource-path",
            str(source.parent),
            "--output",
            str(destination),
        ],
        source.parent,
    )
    if result.returncode == 0 and valid_pdf(destination):
        return True, "pandoc"
    destination.unlink(missing_ok=True)
    tail = result.stdout.strip().splitlines()[-1:] or ["unknown pandoc error"]
    return False, f"pandoc failed: {tail[0]}"


def render_print_html(source: Path, destination: Path) -> str:
    """Create a local, print-ready HTML fallback without network access."""
    markdown_text = source.read_text(encoding="utf-8")
    renderer = "escaped Markdown source"
    try:
        import markdown  # type: ignore[import-not-found]

        body = markdown.markdown(
            markdown_text,
            extensions=["extra", "tables", "fenced_code", "toc"],
        )
        renderer = "Python-Markdown"
    except (ImportError, ModuleNotFoundError):
        body = f'<pre class="markdown-source">{html.escape(markdown_text)}</pre>'

    document = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(source.stem)}</title>
  <style>
    @page {{ size: A4; margin: 18mm 16mm; }}
    body {{ color: #17202a; font: 11pt/1.5 Arial, sans-serif; max-width: 180mm; margin: 0 auto; }}
    h1, h2, h3 {{ color: #102a43; page-break-after: avoid; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 9pt; }}
    th, td {{ border: 1px solid #9aa5b1; padding: 5px; vertical-align: top; }}
    pre, code {{ font-family: Consolas, monospace; white-space: pre-wrap; overflow-wrap: anywhere; }}
    pre {{ background: #f5f7fa; border: 1px solid #d9e2ec; padding: 10px; }}
    img {{ max-width: 100%; }}
    a {{ color: #0b69a3; }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""
    destination.write_text(document, encoding="utf-8")
    return renderer


def browser_candidates() -> list[Path]:
    candidates: list[Path] = []
    for name in ("msedge", "msedge.exe", "chrome", "chrome.exe", "chromium"):
        located = shutil.which(name)
        if located:
            candidates.append(Path(located))

    for environment, relative in (
        ("PROGRAMFILES(X86)", Path("Microsoft/Edge/Application/msedge.exe")),
        ("PROGRAMFILES", Path("Microsoft/Edge/Application/msedge.exe")),
        ("PROGRAMFILES", Path("Google/Chrome/Application/chrome.exe")),
        ("PROGRAMFILES(X86)", Path("Google/Chrome/Application/chrome.exe")),
    ):
        base = os.environ.get(environment)
        if base:
            candidate = Path(base) / relative
            if candidate.is_file():
                candidates.append(candidate)

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate.resolve()).casefold()
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def try_browser_pdf(
    html_path: Path, destination: Path, browser_profile: Path
) -> tuple[bool, str]:
    attempts: list[str] = []
    for browser in browser_candidates():
        destination.unlink(missing_ok=True)
        result = run_command(
            [
                str(browser),
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--user-data-dir={browser_profile}",
                f"--print-to-pdf={destination}",
                html_path.resolve().as_uri(),
            ],
            html_path.parent,
        )
        if result.returncode == 0 and valid_pdf(destination):
            return True, browser.name
        attempts.append(f"{browser.name} exit={result.returncode}")
    return False, ", ".join(attempts) if attempts else "Chrome/Edge not found"


def copy_supplied_pdfs(pdf_dir: Path, destination_dir: Path) -> list[str]:
    methods: list[str] = []
    missing_or_invalid: list[Path] = []
    for _, pdf_name in REPORT_EXPORTS:
        supplied = pdf_dir / pdf_name
        if not valid_pdf(supplied):
            missing_or_invalid.append(supplied)
            continue
        shutil.copy2(supplied, destination_dir / pdf_name)
        methods.append(f"{pdf_name}: supplied PDF")
    if missing_or_invalid:
        fail_for_missing(
            missing_or_invalid,
            "--pdf-dir does not contain three valid PDF files:",
        )
    return methods


def export_pdfs(
    destination_dir: Path,
    output_dir: Path,
    pdf_dir: Path | None,
) -> list[str]:
    if pdf_dir is not None:
        return copy_supplied_pdfs(pdf_dir.resolve(), destination_dir)

    methods: list[str] = []
    fallback_html: list[Path] = []
    browser_profile = destination_dir / ".browser-profile"
    for source_relative, pdf_name in REPORT_EXPORTS:
        source = HW06_ROOT / source_relative
        pdf_destination = destination_dir / pdf_name
        success, detail = try_pandoc_pdf(source, pdf_destination)
        if success:
            methods.append(f"{pdf_name}: {detail}")
            continue

        html_destination = destination_dir / f"{Path(pdf_name).stem}-print.html"
        renderer = render_print_html(source, html_destination)
        browser_success, browser_detail = try_browser_pdf(
            html_destination, pdf_destination, browser_profile
        )
        if browser_success:
            methods.append(
                f"{pdf_name}: HTML ({renderer}) printed by {browser_detail}; {detail}"
            )
            html_destination.unlink(missing_ok=True)
            continue

        fallback_html.append(html_destination)
        methods.append(
            f"{pdf_name}: PDF failed ({detail}; {browser_detail}); HTML created"
        )

    shutil.rmtree(browser_profile, ignore_errors=True)
    if fallback_html:
        fallback_dir = output_dir / "hw06-pdf-fallback"
        if fallback_dir.exists():
            raise PackagingError(
                f"Refusing to overwrite existing fallback directory: {fallback_dir}"
            )
        fallback_dir.mkdir(parents=True)
        for html_file in fallback_html:
            shutil.copy2(html_file, fallback_dir / html_file.name)
        raise PackagingError(
            "No working PDF engine was available for every report. Print the HTML "
            f"files in {fallback_dir} to the three required PDF names, then rerun "
            "with --pdf-dir <directory-containing-those-pdfs>. ZIP creation stopped."
        )
    return methods


def copy_to_stage(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def collect_submission_files(stage: Path) -> None:
    """Copy checklist artifacts while excluding local dependencies and AI diagram notes."""
    copy_to_stage(HW06_ROOT / "README.md", stage / "README.md")

    for directory in SUBMISSION_DIRS:
        source_dir = HW06_ROOT / directory
        if not source_dir.is_dir():
            continue
        for source in sorted(path for path in source_dir.rglob("*") if path.is_file()):
            relative = source.relative_to(HW06_ROOT)
            if "node_modules" in relative.parts:
                continue
            if relative == Path("test-generator/_reference/diagram-notes.mmd"):
                continue
            copy_to_stage(source, stage / relative)

    for relative in (
        Path("test-generator/design.md"),
        Path("test-generator/DRAWING-BRIEF.md"),
        Path("test-generator/generator.py"),
        Path("test-generator/diagram.png"),
    ):
        source = HW06_ROOT / relative
        if source.is_file():
            copy_to_stage(source, stage / relative)

    for source in sorted(path for path in DOCS_ROOT.rglob("*") if path.is_file()):
        relative = source.relative_to(REPO_ROOT)
        copy_to_stage(source, stage / relative)

    for relative in (
        Path("tests/test-runs/hw06-api-test-run.md"),
        Path("tests/test-summary/traceability-matrix.md"),
    ):
        source = REPO_ROOT / relative
        if source.is_file():
            copy_to_stage(source, stage / relative)


def refresh_commit_log(stage: Path) -> None:
    result = run_command(
        [
            "git",
            "log",
            "--date=iso-strict",
            "--pretty=format:%H%x09%ad%x09%s",
            "--",
        ],
        REPO_ROOT,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise PackagingError("Could not generate the real Git commit log for the ZIP.")
    destination = stage / "report" / "git-commit-log.txt"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result.stdout.rstrip() + "\n", encoding="utf-8")


def write_manifest(stage: Path, grade: str, pdf_methods: list[str]) -> None:
    files = []
    for path in sorted(item for item in stage.rglob("*") if item.is_file()):
        files.append(
            {
                "path": path.relative_to(stage).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    manifest = {
        "student_id": "23127207",
        "self_assessed_grade": grade,
        "repository": "https://github.com/trngnneee/eshop-sut",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pdf_export": pdf_methods,
        "file_count_before_manifest": len(files),
        "files": files,
    }
    (stage / "submission-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def create_zip(stage: Path, destination: Path) -> None:
    if destination.exists():
        raise PackagingError(
            f"Refusing to overwrite existing submission archive: {destination}"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "x", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source in sorted(path for path in stage.rglob("*") if path.is_file()):
            archive.write(source, source.relative_to(stage).as_posix())


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export HW06 PDFs and build the checklist-complete submission ZIP."
    )
    parser.add_argument(
        "--grade",
        required=True,
        type=validate_grade,
        help="three-digit self-assessed grade in [000, 100], e.g. 080",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT,
        help="directory for the ZIP or fallback HTML (default: repository root)",
    )
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        help="reuse three manually printed PDFs if Pandoc/Chrome/Edge is unavailable",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate all submission gates without exporting or creating a ZIP",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_submission_inputs()
        if args.check_only:
            print("All HUMAN-only and checklist section 1 file gates passed.")
            return 0

        output_dir = args.output_dir.resolve()
        zip_path = output_dir / f"23127207_HW06_AI_API_{args.grade}.zip"
        if zip_path.exists():
            raise PackagingError(
                f"Refusing to overwrite existing submission archive: {zip_path}"
            )

        output_dir.mkdir(parents=True, exist_ok=True)
        with staging_workspace(output_dir) as stage:
            collect_submission_files(stage)
            refresh_commit_log(stage)
            pdf_methods = export_pdfs(stage, output_dir, args.pdf_dir)
            write_manifest(stage, args.grade, pdf_methods)
            create_zip(stage, zip_path)

        print(f"Created submission: {zip_path}")
        for method in pdf_methods:
            print(f"  - {method}")
        return 0
    except PackagingError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
