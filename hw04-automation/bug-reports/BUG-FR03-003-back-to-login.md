# BUG-FR03-003 — Missing “Quay lại đăng nhập” control

| Field | Value |
| --- | --- |
| Feature | FR-03 |
| Severity | Medium |
| Environment | frontend-web · localhost:5173 |
| Found by | TC-FORGOT-012 |
| Date | 2026-08-07 |

## Spec

FR-03 Step 1: provide a **Quay lại đăng nhập** control that returns to the login page.

## Steps

1. Open `/forgot-password`.
2. Look for a control labeled exactly “Quay lại đăng nhập”.
3. Activate it and observe navigation.

## Expected

Control exists and navigates to `/login`.

## Actual

No such control. Step 2 only has “← Quay lại”, which returns to step 1 (does not go to login).

## Evidence

TC-FORGOT-012 failure screenshots in `test-results/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/374
