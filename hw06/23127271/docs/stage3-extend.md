# Stage 3 — Human-found domain partitions the AI missed

**Per FR:** 5 SUP cases each (15 total). **Source:** Human. **Category:** DomainPartition.

Oracles follow Stage 2: no invented required fields or HTTP status codes.

---

## FR-04 — `PUT /api/users/me` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-PROFILE-SUP-001 | Positive **partial update** — phone only | **Prompt quality.** Example triple treated as only valid shape; omit-name was reject-only. |
| TC-PROFILE-SUP-002 | **Fullwidth Unicode** phone digits | **Model limitation.** ASCII-only phone partitions. |
| TC-PROFILE-SUP-003 | **Duplicate JSON key** `phone` | **API (JSON parser) + model limitation.** LLMs emit unique keys. |
| TC-PROFILE-SUP-004 | **Name-only** partial update | **Prompt quality.** Only phone-only partial added in first SUP batch; name field not split. |
| TC-PROFILE-SUP-005 | **Two-field** partial (name + phone, no address) | **Prompt quality.** Valid 2-of-3 combinations not enumerated. |

---

## FR-07 — `POST /api/cart` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-CART-SUP-001 | Merge **same id, different name** (identity key) | **API characteristic.** “Cùng một sản phẩm” undefined. |
| TC-CART-SUP-002 | Merge **unequal qty** (2+3) | **Prompt quality / 1×1.** Only 1+1 covered. |
| TC-CART-SUP-003 | Merge when **second add has different price** | **API characteristic.** Price mismatch + merge never combined. |
| TC-CART-SUP-004 | **Minimal body** `{id, quantity}` only | **Prompt quality.** No positive minimal-body after Stage 2. |
| TC-CART-SUP-005 | Merge when cart **already has two products** | **Prompt quality / state.** Multi-line cart + merge not combined. |

---

## FR-19 — `DELETE /api/admin/users/:id` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-ADMINUSERS-SUP-001 | **Single** percent-encoded path id | **Model limitation.** Literal decimal paths only. |
| TC-ADMINUSERS-SUP-002 | Path with **trailing slash** | **Model limitation.** URI normalisation not in spec. |
| TC-ADMINUSERS-SUP-003 | Delete **seed user id=2** | **Prompt quality.** Always “register disposable” vs seed partition. |
| TC-ADMINUSERS-SUP-004 | **Mixed alphanumeric** path `12abc` | **Model limitation.** Not split from `abc` vs `1.5`. |
| TC-ADMINUSERS-SUP-005 | **Double** percent-encoding | **API/HTTP characteristic.** Encoding depth beyond SUP-001. |

---

## Files

- `tests/test-cases/profile/TC-PROFILE-SUP-001.md` … `005.md`
- `tests/test-cases/cart/TC-CART-SUP-001.md` … `005.md`
- `tests/test-cases/admin-users/TC-ADMINUSERS-SUP-001.md` … `005.md`
- Rows in `sheets/domain-partitions.csv` (`Source=Human`)

**Sheet total:** 99 AI + 15 Human = **114** domain-partition cases.
