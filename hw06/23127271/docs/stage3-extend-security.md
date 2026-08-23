# Stage 3 — Human-found security cases the AI missed

**Per FR:** 5 SEC-SUP cases each (15 total). **Source:** Human. **Category:** Security.

Oracles follow Stage 2: no invented HTTP status codes; concurrency outcomes recorded not assumed.

---

## Summary by gap type

| Gap | Cases | Why AI missed (theme) |
|-----|-------|------------------------|
| Concurrency / race | PROFILE 001, 005 · CART 001, 003 · ADMIN 003 | Security generator was sequential one-shot; checklist §2 concurrency never in prompt |
| Illegal / privilege / integrity | PROFILE 002 · CART 002, 005 · ADMIN 001, 002, 004 | Model mapped SEC tags to obvious payloads; list-endpoint SEC-03 and numeric boundaries omitted |
| Encoding / parser bypass | PROFILE 003, 004 · CART 004 · ADMIN 005 | LLM default ASCII SQLi/XSS; no Content-Type, null-byte, Unicode-escape, or path-encoding probes |

---

## FR-04 — `PUT /api/users/me` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-PROFILE-SEC-SUP-001 | **Race** — parallel PUT with `role=admin` vs valid body | **Prompt quality** — SEC-06 tested only sequential role escalation (SEC-007); concurrency not requested |
| TC-PROFILE-SEC-SUP-002 | **Mass assignment** `id` field | **Model limitation** — SEC-06 mapped to role/password/email; primary-key swap not in spec example JSON |
| TC-PROFILE-SEC-SUP-003 | **Null-byte** in name | **Model limitation** — printable SQLi/XSS only; encoding-truncation absent |
| TC-PROFILE-SEC-SUP-004 | **Content-Type** `text/plain` + JSON body | **Prompt quality** — SEC-02 covered Authorization only, not media-type confusion |
| TC-PROFILE-SEC-SUP-005 | **Race** — concurrent XSS vs SQLi on name | **API characteristic** — last-write-wins under parallel malicious PUTs untested |

---

## FR-07 — `POST /api/cart` (+ GET verification) (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-CART-SEC-SUP-001 | **Race** — parallel POST price=1 vs catalogue price | **Prompt quality** — SEC-006 sequential; realistic tampering is concurrent |
| TC-CART-SEC-SUP-002 | **Negative quantity** integrity | **Model limitation** — auth/SQLi/XSS focus; qty sign not treated as security |
| TC-CART-SEC-SUP-003 | **Race** — GET cart ∥ POST add | **API characteristic** — IDOR tested sequentially; same-user stale read under race omitted |
| TC-CART-SEC-SUP-004 | **Unicode-escaped XSS** in name | **Model limitation** — literal `<script>` only (SEC-005); normalization bypass gap |
| TC-CART-SEC-SUP-005 | **Extreme quantity** overflow | **Prompt quality** — domain qty boundaries not reused as SEC-06 integrity/DoS probe |

---

## FR-19 — `DELETE /api/admin/users/:id` + `GET /api/admin/users` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-ADMINUSERS-SEC-SUP-001 | **Unauthenticated GET** admin list | **Prompt quality** — SEC-02 on DELETE only; FR-19 list endpoint left open |
| TC-ADMINUSERS-SEC-SUP-002 | **User JWT on GET** list (SEC-03) | **Model limitation** — SEC-03 mapped to DELETE; spec §6.1 pairs GET+DELETE under admin guard |
| TC-ADMINUSERS-SEC-SUP-003 | **Race** — parallel DELETE same id | **Prompt quality** — sequential delete probes; double-delete idempotency absent |
| TC-ADMINUSERS-SEC-SUP-004 | **Negative path id** `-1` | **Model limitation** — string SQLi paths only; numeric type-confusion boundary omitted |
| TC-ADMINUSERS-SEC-SUP-005 | **Path traversal** encoded slash `1%2f2` | **API characteristic** — HTTP routing confusion not visible from spec SQLi examples |

---

## Totals

| Sheet | AI SEC | Human SEC-SUP | Combined SEC |
|-------|-------:|--------------:|-------------:|
| `security-tests.csv` | 37 | 15 | **52** |

**Files:** `tests/test-cases/{profile,cart,admin-users}/TC-*-SEC-SUP-*.md`  
**Script:** `scripts/append_stage3_sec_sup_cases.py` (idempotent)

---

## Combined Stage-1 counts (domain + state + security, after SEC-SUP)

- FR-04: 40 + 12 + 14 + 5 = **71**
- FR-07: 39 + 15 + 11 + 5 = **70**
- FR-19: 20 + 15 + 12 + 5 = **52**
