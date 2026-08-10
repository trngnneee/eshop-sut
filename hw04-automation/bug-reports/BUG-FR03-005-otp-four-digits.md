# BUG-FR03-005 — OTP is 4 digits instead of 6

| Field | Value |
| --- | --- |
| Feature | FR-03 / SEC-07 |
| Severity | High |
| Environment | backend `POST /api/forgot-password` + web UI |
| Found by | TC-FORGOT-014 |
| Date | 2026-08-07 |

## Spec

FR-03 / SEC-07: system generates a **6-digit** random OTP (demo may display it on screen).

## Steps

1. Register/request OTP for a valid user via UI.
2. Read the demo OTP banner (“Mã OTP của bạn là: …”).
3. Count digits; note UI label “Mã OTP (4 số)”.

## Expected

OTP length = 6.

## Actual

Backend generates `1000–9999` (4 digits). UI labels the field as 4 digits.

## Evidence

TC-FORGOT-014: Expected 6, Received 4. Screenshots in `test-results/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/376
