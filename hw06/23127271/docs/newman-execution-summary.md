# Newman execution summary — manual bug triage

**Run:** `reports/newman-run.log` · **Student:** 23127271  
**Collection:** 343 requests · **Duration:** 31.4s

## Newman automated result

| Metric | Value |
|--------|------:|
| Requests executed | 343 |
| Assertions | 1019 |
| **Assertion failures** | **0** |

Postman test scripts are **observe-only** (record status, JSON parseable, response time). Zero Newman failures does **not** mean the SUT passed all oracles — manual comparison against `ExpectedResult` is required.

## Manual triage outcome

| Result | Count | Notes |
|--------|------:|-------|
| **Product bugs filed** | **8** | See `docs/bug-reports-summary.md` |
| Inconclusive / collection defect | 1 | `TC-ADMINUSERS-SEC-002` DELETE URL malformed (`<3>`) — privilege gap still confirmed in code |
| Observe-only / no spec violation | remainder | e.g. client-supplied cart price (FR-08 checkout scope) |

## High-signal log findings

| TC ID | HTTP | Oracle violation |
|-------|------|------------------|
| `TC-ADMINUSERS-SEC-SUP-002` | GET `/api/admin/users` **200** with user JWT | SEC-03 / FR-12 — non-admin must not list users |
| `TC-ADMINUSERS-SEC-002` | DELETE `/api/admin/users/<3>` **200** with user JWT | SEC-03 — non-admin must not delete |
| `TC-PROFILE-SEC-007` | PUT `/api/users/me` **200** with `role=admin` | SEC-06 — role must stay `user` |
| `TC-PROFILE-SCH-SUP-003` | GET `/api/users/me` **200**, 446B body | SEC-01 — password hash must not be exposed |
| `TC-ADMINUSERS-SEC-003` | DELETE `/api/admin/users/1` **200** (admin self) | FR-19 — admin must not delete self |
| `TC-PROFILE-SEC-SUP-004` | PUT `/api/users/me` **500** (`Content-Type: text/plain`) | SEC-02 — must not crash; reject safely |
| `TC-CART-SEC-SUP-002` | POST `/api/cart` **200** with `quantity: -1` | Integrity — corrupt cart state risk |
| `TC-ADMINUSERS-SCH-SUP-001` | GET list **200** | Schema — extra DB columns in list response |

## Human-found (Stage 3) bugs

These were missed by AI generation and caught via SUP cases:

- **BUG-001** — `TC-ADMINUSERS-SEC-SUP-002`
- **BUG-004** — `TC-PROFILE-SCH-SUP-003`
- **BUG-006** — `TC-PROFILE-SEC-SUP-004`
- **BUG-007** — `TC-CART-SEC-SUP-002`
- **BUG-008** — `TC-ADMINUSERS-SCH-SUP-001`

## Next steps

1. Record `PassFail` / `ActualResult` / `BugRef` in `sheets/all-test-cases.csv` for executed rows.
2. Attach redacted response screenshots to each bug under `bugs/evidence/` (optional).
3. Re-run Newman after SUT fixes with stricter assertions on SEC-03 / SEC-06 / SEC-01 cases.
