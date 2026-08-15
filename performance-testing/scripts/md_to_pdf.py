#!/usr/bin/env python3
"""Chuyen file Markdown cua HW05 sang PDF de nop kem ban .md.

Quy trinh: Markdown -> HTML (thu vien `markdown`) -> PDF (Edge/Chrome headless).
Khong dung pandoc/wkhtmltopdf vi may khong co san.

Cach dung:
    python md_to_pdf.py <input.md> [input2.md ...]
    python md_to_pdf.py --all          # 3 file bat buoc theo checklist muc 1 & 8

PDF duoc ghi canh file .md goc, cung ten, doi duoi thanh .pdf.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

SCRIPT_DIR = Path(__file__).resolve().parent
PT_DIR = SCRIPT_DIR.parent

# 3 tai lieu bat buoc co ban PDF (checklist 12_REPORT_OUTLINE.md muc 1 va 8)
REQUIRED = [
    PT_DIR / "23127207_HW05_Report.md",
    PT_DIR / "deliverables" / "AI_CRITIQUE.md",
    PT_DIR / "deliverables" / "AI_AUDIT_REPORT.md",
]

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

# Cac ky hieu LaTeX that su xuat hien trong bo tai lieu nay.
# Chromium khong render MathJax offline nen doi sang Unicode cho doc duoc.
TEX_MAP = {
    r"\to": "\u2192",       # ->
    r"\le": "\u2264",       # <=
    r"\ge": "\u2265",       # >=
    r"\neq": "\u2260",
    r"\times": "\u00d7",
    r"\approx": "\u2248",
    r"\Delta": "\u0394",
    r"\%": "%",
    r"\,": " ",
}


def detex(md_text: str) -> str:
    """Go cac doan toan hoc inline `$...$` thanh van ban Unicode tuong duong."""

    def convert(match: re.Match) -> str:
        body = match.group(1)
        body = re.sub(r"\\text\{([^}]*)\}", r"\1", body)
        body = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", body)
        for tex, uni in TEX_MAP.items():
            body = body.replace(tex, uni)
        return body.strip()

    return re.sub(r"\$([^$\n]+)\$", convert, md_text)


CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body {
  font-family: "Segoe UI", "Times New Roman", sans-serif;
  font-size: 10.5pt; line-height: 1.55; color: #14161a; margin: 0;
}
h1, h2, h3, h4 { color: #0b2545; line-height: 1.25; page-break-after: avoid; }
h1 { font-size: 19pt; border-bottom: 2.5px solid #0b2545; padding-bottom: 6px; margin: 0 0 14px; }
h2 { font-size: 14pt; border-bottom: 1px solid #c8d3e0; padding-bottom: 4px; margin: 22px 0 10px; }
h3 { font-size: 11.5pt; margin: 16px 0 6px; }
h4 { font-size: 10.5pt; margin: 12px 0 4px; }
p, li { orphans: 3; widows: 3; }
ul, ol { padding-left: 22px; margin: 6px 0; }
li { margin: 2px 0; }
hr { border: 0; border-top: 1px solid #d6dde6; margin: 18px 0; }
table {
  border-collapse: collapse; width: 100%; margin: 10px 0;
  font-size: 9pt; page-break-inside: avoid;
}
th, td { border: 1px solid #b9c4d1; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #eef2f7; font-weight: 600; color: #0b2545; }
tr:nth-child(even) td { background: #fafbfd; }
code {
  font-family: Consolas, "Courier New", monospace; font-size: 9pt;
  background: #f1f3f6; padding: 1px 4px; border-radius: 3px; color: #9c1c3d;
}
pre {
  background: #f6f8fa; border: 1px solid #dde3ea; border-radius: 4px;
  padding: 9px 11px; overflow-x: auto; page-break-inside: avoid;
}
pre code { background: none; padding: 0; color: #14161a; }
blockquote {
  border-left: 3px solid #7f9bbd; margin: 10px 0; padding: 2px 0 2px 12px;
  color: #3c4a5c; background: #f7f9fc;
}
a { color: #0a4a8f; text-decoration: none; word-break: break-all; }
strong { color: #0b2545; }
"""

HTML_SHELL = """<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8"><title>{title}</title>
<style>{css}</style></head><body>{body}</body></html>
"""


def find_browser() -> str:
    for path in BROWSERS:
        if os.path.isfile(path):
            return path
    raise SystemExit(
        "Khong tim thay Microsoft Edge hoac Google Chrome de in PDF.\n"
        "Da tim o:\n  " + "\n  ".join(BROWSERS)
    )


def convert(md_path: Path, browser: str) -> Path:
    if not md_path.is_file():
        raise SystemExit(f"Khong co file: {md_path}")

    pdf_path = md_path.with_suffix(".pdf")
    text = detex(md_path.read_text(encoding="utf-8"))
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "nl2br"],
    )
    html = HTML_SHELL.format(title=md_path.stem, css=CSS, body=body)

    tmp_dir = Path(tempfile.mkdtemp(prefix="hw05pdf_"))
    try:
        html_path = tmp_dir / (md_path.stem + ".html")
        html_path.write_text(html, encoding="utf-8")

        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            f"--user-data-dir={tmp_dir / 'profile'}",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if not pdf_path.is_file():
            sys.stderr.write(result.stderr or "")
            raise SystemExit(f"[FAIL] Khong sinh duoc PDF cho {md_path.name}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    size_kb = pdf_path.stat().st_size / 1024
    print(f"[OK] {md_path.name:34s} -> {pdf_path.name:34s} ({size_kb:,.1f} KB)")
    return pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Markdown -> PDF cho bai nop HW05")
    parser.add_argument("files", nargs="*", help="Duong dan file .md")
    parser.add_argument(
        "--all", action="store_true", help="Chuyen 3 file bat buoc theo checklist"
    )
    args = parser.parse_args()

    targets = REQUIRED if args.all else [Path(f).resolve() for f in args.files]
    if not targets:
        parser.error("Can it nhat 1 file .md, hoac dung --all")

    browser = find_browser()
    print(f"Trinh duyet dung de in: {browser}\n")
    for md_path in targets:
        convert(md_path, browser)


if __name__ == "__main__":
    main()
