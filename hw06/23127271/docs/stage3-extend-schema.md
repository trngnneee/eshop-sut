# Stage 3 — Human-found schema validation cases the AI missed

**Per FR:** 5 SCH-SUP cases each (15 total). **Source:** Human. **Category:** SchemaValidation.

Oracles follow Stage 2: no invented HTTP codes; observe undocumented response shapes.

---

## Summary by gap type

| Gap | Cases | Why AI missed (theme) |
|-----|-------|------------------------|
| Undocumented / over-exposed columns | PROFILE 001, 003 · ADMIN 001 | SUT SELECT *; AI checked only api_spec example fields |
| Malformed request envelope | PROFILE 002, 004 · CART 005 | Flat-object bias; nested/array/duplicate-key bodies omitted |
| Partial / polluted line schema | CART 001, 002, 003 | Four-field example treated as mandatory storage shape |
| List consistency / error envelope | ADMIN 002, 003, 004, 005 | Per-element type checks without key-set equality or DELETE leak |

---

## FR-04 — `GET/PUT /api/users/me` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-PROFILE-SCH-SUP-001 | **login_attempts / locked_until** on GET | **API characteristic** — SELECT * exposes lockout columns not in api_spec |
| TC-PROFILE-SCH-SUP-002 | **Nested** `{profile:{...}}` PUT body | **Prompt quality** — generator only flat api_spec example |
| TC-PROFILE-SCH-SUP-003 | Full **key inventory** for secret column names | **Model limitation** — SCH-007 checked password only, not alias keys |
| TC-PROFILE-SCH-SUP-004 | **Array root** PUT body | **Model limitation** — empty object tested, not array malformed root |
| TC-PROFILE-SCH-SUP-005 | **charset** on request Content-Type | **Prompt quality** — response Content-Type only on GET |

---

## FR-07 — `GET/POST /api/cart` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-CART-SCH-SUP-001 | **Partial** POST `{id, quantity}` stored shape | **Prompt quality** — domain minimal-body not reused in schema category |
| TC-CART-SCH-SUP-002 | **Extra keys** (user_id, role) persisted on line | **API characteristic** — SUT stores req.body verbatim |
| TC-CART-SCH-SUP-003 | **Heterogeneous** keys across two lines | **Model limitation** — per-line types checked in isolation |
| TC-CART-SCH-SUP-004 | **name:null** nullable probe | **Prompt quality** — required vs optional name not split |
| TC-CART-SCH-SUP-005 | **Duplicate quantity** key last-wins | **Model limitation** — domain duplicate-key on profile only |

---

## FR-19 — `GET/DELETE /api/admin/users` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-ADMINUSERS-SCH-SUP-001 | **shipping_address / lockout** columns on list | **API characteristic** — FR-19 lists users; SUT returns extra columns |
| TC-ADMINUSERS-SCH-SUP-002 | **Same key set** on every list element | **Prompt quality** — object type checked, not key-set equality |
| TC-ADMINUSERS-SCH-SUP-003 | **Non-numeric path** error JSON type | **Model limitation** — DELETE schema assumed valid id |
| TC-ADMINUSERS-SCH-SUP-004 | **New register** row schema in list | **Prompt quality** — seed users only in SCH-011 |
| TC-ADMINUSERS-SCH-SUP-005 | DELETE body must not **echo full user** | **API characteristic** — message-only vs PII echo not forbidden in spec |

---

## Totals

| Sheet | AI SCH | Human SCH-SUP | Combined |
|-------|-------:|--------------:|---------:|
| `schema-validation.csv` | 42 | 15 | **57** |

**Combined Stage-1 (all categories + human):** FR-04 **90** · FR-07 **89** · FR-19 **71**
