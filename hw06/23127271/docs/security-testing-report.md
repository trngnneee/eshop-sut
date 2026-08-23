# Security Testing Report — FR-04, FR-07, FR-19

**Student:** 23127271 · **SUT:** EShop (`http://localhost:3000`)  
**Category:** Stage 1 — Security (API testing skill checklist section 3)  
**Sources:** `Repo/eshop-sut/README.md` (SEC-01..SEC-07), `api_specification.md`

---

## SEC requirement applicability

| SEC | Requirement | In-scope endpoints | Testable here? |
|-----|-------------|-------------------|----------------|
| SEC-01 | Password not plaintext in storage/responses | GET /api/admin/users, DELETE responses | Yes (FR-19) |
| SEC-02 | Protected APIs require valid JWT | PUT /me, POST /cart, GET /cart (IDOR), DELETE admin | Yes |
| SEC-03 | Admin APIs require role=admin | DELETE /api/admin/users/:id | Yes |
| SEC-04 | UI escape user input | Profile/cart string fields on in-scope PUT/POST | API stores literal; UI manual |
| SEC-05 | Parameterized queries | In-scope string/path inputs | Yes |
| SEC-06 | No privilege/integrity tampering via body | PUT /me, POST /cart | Yes |
| SEC-07 | OTP reset entropy/expiry | Forgot-password APIs | **Gap** — not in FR-04/07/19 scope |

## In-scope endpoints

| FR | Primary endpoints under test | Allowed verification only |
|----|------------------------------|---------------------------|
| FR-04 | `PUT /api/users/me` | `GET /api/users/me`; `POST /api/login` as password oracle |
| FR-07 | `POST /api/cart` | `GET /api/cart` for cart isolation/IDOR and POST side effects |
| FR-19 | `DELETE /api/admin/users/:id`, `GET /api/admin/users` | `GET /api/admin/users` after DELETE for SEC-01/SEC-03 checks |

Out of scope (no dedicated security TCs): checkout (FR-08), catalogue/products (FR-05), login/register (FR-02/03), forgot-password (SEC-07).

## Stage 2 audit (AI cases only)

| Label | Count |
|-------|------:|
| VALID | 31 |
| INVALID | 1 |
| INCOMPLETE | 5 |
| **AI SEC total** | **37** |

Full per-case table: `docs/stage2-audit-security.md`. Human SEC-SUP cases (15) are not re-audited (`Source=Human`).

**Notable fixes:** `TC-CART-SEC-006` (INVALID — FR-07 does not mandate cart price validation; FR-08 is checkout-only); SEC-06 mis-tags on password/user_id mass assignment; `TC-ADMINUSERS-SEC-003` reframed as FR-19 not SEC-03.

## SEC → test case map

| SEC | TC IDs |
|-----|--------|
| SEC-01 | TC-ADMINUSERS-SEC-006, TC-ADMINUSERS-SEC-007, TC-ADMINUSERS-SEC-013 |
| SEC-02 | TC-ADMINUSERS-SEC-001, TC-ADMINUSERS-SEC-010, TC-CART-SEC-001, TC-CART-SEC-002, TC-CART-SEC-007, TC-CART-SEC-011, TC-PROFILE-SEC-009, TC-PROFILE-SEC-010 |
| SEC-03 | TC-ADMINUSERS-SEC-002, TC-ADMINUSERS-SEC-003 |
| SEC-04 | TC-CART-SEC-005, TC-PROFILE-SEC-005, TC-PROFILE-SEC-006, TC-PROFILE-SEC-014 |
| SEC-05 | TC-ADMINUSERS-SEC-004, TC-ADMINUSERS-SEC-005, TC-ADMINUSERS-SEC-008, TC-ADMINUSERS-SEC-011, TC-ADMINUSERS-SEC-014, TC-CART-SEC-003, TC-CART-SEC-004, TC-CART-SEC-010, TC-CART-SEC-012, TC-PROFILE-SEC-001, TC-PROFILE-SEC-002, TC-PROFILE-SEC-003, TC-PROFILE-SEC-004, TC-PROFILE-SEC-013 |
| SEC-06 | TC-CART-SEC-006, TC-CART-SEC-008, TC-PROFILE-SEC-007, TC-PROFILE-SEC-008, TC-PROFILE-SEC-011, TC-PROFILE-SEC-012 |

---

## FR-04 — `PUT /api/users/me`

**Count:** 14 cases

| TC ID | SEC | Threat |
|-------|-----|--------|
| TC-PROFILE-SEC-001 | SEC-05 | SQL injection in name |
| TC-PROFILE-SEC-002 | SEC-05 | SQL injection UNION in name |
| TC-PROFILE-SEC-003 | SEC-05 | SQL injection in shipping_address |
| TC-PROFILE-SEC-004 | SEC-05 | SQL injection in phone |
| TC-PROFILE-SEC-005 | SEC-04 | Stored XSS script in name |
| TC-PROFILE-SEC-006 | SEC-04 | Stored XSS event handler in address |
| TC-PROFILE-SEC-007 | SEC-06 | Role escalation role=admin |
| TC-PROFILE-SEC-008 | SEC-06 | Mass assignment password field |
| TC-PROFILE-SEC-009 | SEC-02 | Auth bypass — no JWT |
| TC-PROFILE-SEC-010 | SEC-02 | Auth bypass — invalid signature JWT |
| TC-PROFILE-SEC-011 | SEC-06 | Privilege — email change |
| TC-PROFILE-SEC-012 | SEC-06 | Mass assignment login_attempts / locked_until |
| TC-PROFILE-SEC-013 | SEC-05 | SQLi in Authorization header |
| TC-PROFILE-SEC-014 | SEC-04 | Template/polyglot injection in name |

---

## FR-07 — `POST /api/cart` (+ GET cart IDOR)

**Count:** 11 cases

| TC ID | SEC | Threat |
|-------|-----|--------|
| TC-CART-SEC-001 | SEC-02 | Auth bypass — no JWT |
| TC-CART-SEC-002 | SEC-02 | Auth bypass — malformed JWT |
| TC-CART-SEC-003 | SEC-05 | SQL injection in name |
| TC-CART-SEC-004 | SEC-05 | SQL injection numeric id as string |
| TC-CART-SEC-005 | SEC-04 | Stored XSS in cart name |
| TC-CART-SEC-006 | SEC-06 | Price tampering / integrity |
| TC-CART-SEC-007 | SEC-02 | IDOR — cross-user cart read |
| TC-CART-SEC-008 | SEC-06 | Mass assignment user_id |
| TC-CART-SEC-010 | SEC-05 | NoSQL-style operator in name |
| TC-CART-SEC-011 | SEC-02 | IDOR — POST to another user cart |
| TC-CART-SEC-012 | SEC-05 | SQLi in Authorization header |

---

## FR-19 — `DELETE /api/admin/users/:id` + `GET /api/admin/users`

**Count:** 12 cases

| TC ID | SEC | Threat |
|-------|-----|--------|
| TC-ADMINUSERS-SEC-001 | SEC-02 | Auth bypass — no JWT |
| TC-ADMINUSERS-SEC-002 | SEC-03 | Role escalation — user JWT |
| TC-ADMINUSERS-SEC-003 | SEC-03 | Admin self-delete bypass FR-19 |
| TC-ADMINUSERS-SEC-004 | SEC-05 | SQL injection in path id |
| TC-ADMINUSERS-SEC-005 | SEC-05 | SQL injection stacked in path |
| TC-ADMINUSERS-SEC-006 | SEC-01 | Password exposure in list response |
| TC-ADMINUSERS-SEC-007 | SEC-01 | Password in DELETE error response |
| TC-ADMINUSERS-SEC-008 | SEC-05 | SQLi in JSON DELETE body |
| TC-ADMINUSERS-SEC-010 | SEC-02 | Empty Bearer token |
| TC-ADMINUSERS-SEC-011 | SEC-05 | SQLi percent-encoded path |
| TC-ADMINUSERS-SEC-013 | SEC-01 | Data exposure after successful delete |
| TC-ADMINUSERS-SEC-014 | SEC-05 | SQLi in Authorization on DELETE |

---

## Combined Stage-1 counts (domain + state + security)

- FR-04: 40 + 12 + 14 + 5 = **71**
- FR-07: 39 + 15 + 11 + 5 = **70**
- FR-19: 20 + 15 + 12 + 5 = **52**

## Artifacts

| Artifact | Path |
|----------|------|
| This report | `docs/security-testing-report.md` |
| Per-TC files | `tests/test-cases/{profile,cart,admin-users}/TC-*-SEC-*.md` |
| Sheet | `sheets/security-tests.csv` |
| Generator | `scripts/generate_security_tests.py` |

**Total security cases:** 37 AI-generated + 15 human SEC-SUP = **52** total.

See `docs/stage3-extend-security.md` for human extensions (≥5 per FR) and why-AI-missed notes.
