"""Convert selected Markdown docs under docs/ to PDF via Chromium print."""
from __future__ import annotations

import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parent
DEFAULT_FILES = [
    "ai-audit-report.md",
    "ai-critique.md",
    "hw04-main-report.md",
]

CSS = """
@page { margin: 16mm 14mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11pt; line-height: 1.45; color: #111; }
h1 { font-size: 18pt; margin: 0 0 10px; }
h2 { font-size: 14pt; margin: 18px 0 8px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }
h3 { font-size: 12pt; margin: 14px 0 6px; }
p, li { margin: 4px 0; }
code, pre { font-family: Consolas, 'Courier New', monospace; font-size: 9.5pt; }
pre { background: #f5f5f5; border: 1px solid #e0e0e0; padding: 10px; white-space: pre-wrap; word-break: break-word; }
code { background: #f5f5f5; padding: 1px 4px; }
blockquote { margin: 8px 0; padding: 6px 12px; border-left: 3px solid #888; background: #fafafa; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9pt; }
th, td { border: 1px solid #ccc; padding: 5px 7px; vertical-align: top; text-align: left; }
th { background: #f0f0f0; }
hr { border: none; border-top: 1px solid #ddd; margin: 16px 0; }
"""


def convert(names: list[str]) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for name in names:
            md_path = DOCS / name
            if not md_path.exists():
                print("SKIP missing", md_path)
                continue
            html_body = markdown.markdown(
                md_path.read_text(encoding="utf-8"),
                extensions=["tables", "fenced_code", "nl2br"],
            )
            html = (
                "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
                f"<style>{CSS}</style></head><body>{html_body}</body></html>"
            )
            out_html = DOCS / f"{md_path.stem}.tmp.html"
            out_pdf = DOCS / f"{md_path.stem}.pdf"
            out_html.write_text(html, encoding="utf-8")
            page.goto(out_html.resolve().as_uri())
            page.pdf(
                path=str(out_pdf),
                format="A4",
                print_background=True,
                margin={
                    "top": "14mm",
                    "bottom": "14mm",
                    "left": "12mm",
                    "right": "12mm",
                },
            )
            out_html.unlink(missing_ok=True)
            print("OK", out_pdf, out_pdf.stat().st_size)
        browser.close()


if __name__ == "__main__":
    files = sys.argv[1:] or DEFAULT_FILES
    convert(files)
