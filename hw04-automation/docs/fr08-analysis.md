# Feature B — FR-08 Checkout · Analyze only

**Student ID:** 23127271  
**Stage:** Analyze · Design → `fr08-design.md`  
**Date:** 2026-08-09  
**Sources:** README FR-08, HW02 Feature B, HW04 PDF, prep `fr08-prep-ledger.md`  
**Tool:** Cursor Agent · skill `automation-testing`

> **Analyze only.** Do not overwrite FR-03 frozen evidence.

---

## 1. Contract

| Item | Value |
| --- | --- |
| Feature | B — FR-08 Checkout |
| Web | `http://localhost:5173` |
| API | `http://localhost:3000` |
| Evidence rule | `npm run test:matrix:fr08` only; verify FR-03 freeze before/after |

---

## 2. Actors

| Actor | Role |
| --- | --- |
| Logged-in user | May checkout with non-empty cart |
| Guest | Must be blocked from checkout |
| Backend | Recalculates total; must not trust client `total_amount` |

---

## 3. Preconditions

1. API + Web up; FR-03 evidence locked.
2. Unique registered user preferred for happy paths.
3. Cart seeded (SPA in-memory — seed then navigate carefully).

---

## 4. Acceptance criteria (README)

1. Only logged-in users may checkout.
2. Payment total computed from cart — **not user-editable**.
3. UI lists all ordered product lines.
4. Backend recalculates total; rejects trusting client total.
5. After success, **cart cleared**.

---

## 5. SUT observations (keep as failing oracles)

- `/checkout` reachable without auth (missing route guard).
- Empty cart checkout may succeed.
- Total input editable in UI.
- `POST /api/checkout` trusts client `total_amount`.
- Cart may remain after success.

---

## 6. Next

**Design** ≥12 cases (`docs/fr08-design.md`).
