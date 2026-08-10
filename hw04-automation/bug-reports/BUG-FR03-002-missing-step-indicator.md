# BUG-FR03-002 — Missing step indicator on forgot-password page

| Field | Value |
| --- | --- |
| Feature | FR-03 / FR-22 |
| Severity | Medium |
| Environment | frontend-web · localhost:5173 |
| Found by | TC-FORGOT-011 |
| Date | 2026-08-07 |

## Spec

FR-03 / FR-22: multi-step forms must show a clear step indicator (e.g. “Bước 1 / 2”).

## Steps

1. Open `/forgot-password` (step 1).
2. Look for step indicator text.

## Expected

Visible indicator containing “Bước 1” / “Bước 1 / 2”.

## Actual

No step indicator; only the page heading “Quên Mật Khẩu”.

## Evidence

TC-FORGOT-011 failure screenshots in `test-results/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/373
