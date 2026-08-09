# BUG-FR03-004 — Email field uses type=text instead of type=email

| Field | Value |
| --- | --- |
| Feature | FR-22 (applies on FR-03 form) |
| Severity | Medium |
| Environment | frontend-web `ForgotPassword.jsx` |
| Found by | TC-FORGOT-013 |
| Date | 2026-08-07 |

## Spec

FR-22: email fields must use `type="email"` for HTML5 format validation.

## Steps

1. Open `/forgot-password`.
2. Inspect the email input attribute `type`.

## Expected

`type="email"`.

## Actual

`type="text"` (no HTML5 email validation).

## Evidence

TC-FORGOT-013 failure (expected `email`, received `text`).

## GitHub Issue

TBD — attach screenshot when filing.
