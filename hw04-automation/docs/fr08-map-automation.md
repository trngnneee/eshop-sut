# Feature B — FR-08 · Map automation

**Student ID:** 23127271  
**Date:** 2026-08-09  

---

## 1. Runtime

Web `5173` · API `3000` · FR-03 freeze must stay locked.

---

## 2. Page objects (`pages/CheckoutPage.js`)

Exports: `CheckoutPage`, `CartPage`, `HomePage` (+ `LoginPage` as needed).

| Area | Strategy |
| --- | --- |
| Cart CTA | Tiến hành thanh toán |
| Checkout lines | row / text filters by product name |
| Total | label / input near Tổng — assert readonly |
| Confirm | button xác nhận / thanh toán |
| Auth | register/login helpers; inject token like SPA pattern |

---

## 3. Setup notes (critical)

SPA cart is **in-memory**: seed cart **then** navigate without full reload that drops cart. Prefer in-app clicks after API/UI seed.

| Setup | Action |
| --- | --- |
| Guest | clear storage / no token |
| User + items | `registerUser` / login → add products → open checkout |
| Empty cart | login with empty cart |
| Tamper | intercept or API POST with forged `total_amount` |
| API unauth | `checkoutApi` without JWT |

---

## 4. Journey → actions (sketch)

| Journey | Flow |
| --- | --- |
| `guestCartCheckout` | cart CTA as guest → expect login gate |
| `guestDirectCheckout` | goto `/checkout` logged out |
| `emptyCartCheckout` | login, empty, attempt checkout |
| `fullCheckout` | login, seed, confirm pay |
| `inspectCheckout` | seed → open checkout → assert UI |
| `tamperTotalCheckout` | checkout with tampered total → verify stored total |
| `apiCheckoutUnauthorized` | API only |

---

## 5. Generate file list

- `test-data/fr08-checkout.json`
- `pages/CheckoutPage.js`
- `tests/fr08-checkout.spec.js`
- loader allow-lists for FR-08 journeys/assertions
- `bug-reports/BUG-FR08-001`…`005`

## Next

**Generate** → **Verify** (`fr08-verify-chromium.md`).
