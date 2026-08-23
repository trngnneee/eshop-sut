# Stage 3 — Human-found state transitions the AI missed

**Per FR:** 5 SUP cases each (15 total). **Source:** Human. **Category:** StateTransition.

Oracles follow Stage 2: no invented HTTP codes; concurrency outcomes recorded not assumed.

---

## Summary by gap type

| Gap | Cases | Why AI missed (theme) |
|-----|-------|------------------------|
| Concurrency / race | PROFILE 001, 003 · CART 002, 005 · ADMIN 002, 005 | Checklist §2 concurrency never in prompt; AI emitted sequential chains only |
| Illegal / failed transition | PROFILE 002, 004 · CART 003 | Auth/checkout failures left to domain TCs or happy-path only |
| Missing legal transition | CART 001, 004 · PROFILE 005 | 1×1 bias to id=1 merge / name→phone partial order |
| Terminal / session state | ADMIN 003, 004 | Delete lifecycle without probing old JWT or live session |
| Unspecified admin transition | ADMIN 001 | FR-19 self-rule only; delete-other-admin absent from ST suite |

---

## FR-04 — `PUT /api/users/me` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-PROFILE-ST-SUP-001 | **Race** — two PUTs different names before GET | **Prompt quality** — ST generator sequential-only; concurrency in checklist §2 not requested |
| TC-PROFILE-ST-SUP-002 | **Illegal** — PUT without token mid-flow | **Model limitation** — auth off-points in domain TC-029..032; no state-transition framing |
| TC-PROFILE-ST-SUP-003 | **Race** — concurrent PUT name vs phone (different fields) | **Model limitation** — SUP-001 raced same field only; multi-attribute torn read not considered |
| TC-PROFILE-ST-SUP-004 | **Illegal** — malformed JWT PUT after P1 established | **Model limitation** — domain TC-031 one-shot; no mid-flow guard that P1 must not advance |
| TC-PROFILE-ST-SUP-005 | **Partial chain** — address-only then name-only | **Prompt quality** — ST-002 name→phone; address-first 2-of-3 path never split |

---

## FR-07 — `POST /api/cart` (+ checkout) (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-CART-ST-SUP-001 | Merge on **line 2** in 3-line cart | **Prompt quality** — merge always on product id=1 |
| TC-CART-ST-SUP-002 | **Race** — parallel POST same id from empty | **API characteristic** — in-memory cart may duplicate lines; spec silent on locking |
| TC-CART-ST-SUP-003 | **Failed checkout** — C_MULTI unchanged | **Prompt quality** — ST-011 only FR-08 happy path |
| TC-CART-ST-SUP-004 | Merge on **line 3** in 3-line cart | **Prompt quality** — merge matrix incomplete after SUP-001 (line 2) |
| TC-CART-ST-SUP-005 | **Race** — POST /api/cart ∥ POST /api/checkout | **API characteristic** — FR-08 vs add-in-flight undefined |

---

## FR-19 — `DELETE /api/admin/users/:id` (5)

| TC ID | What was missing | Why the AI missed it |
|-------|------------------|----------------------|
| TC-ADMINUSERS-ST-SUP-001 | Delete **another admin** (A-ID-10 lifecycle) | **API characteristic** — FR-19 silent beyond self-delete |
| TC-ADMINUSERS-ST-SUP-002 | **Race** — parallel DELETE same id | **Model limitation** — sequential multi-delete only (ST-005) |
| TC-ADMINUSERS-ST-SUP-003 | **Terminal** — old JWT GET /api/users/me after delete | **API characteristic** — ST-011 login only; token invalidation unspecified |
| TC-ADMINUSERS-ST-SUP-004 | Delete user **with active session** (D token probe) | **Prompt quality** — lifecycle register→delete without victim JWT timing |
| TC-ADMINUSERS-ST-SUP-005 | **Race** — DELETE ∥ GET /api/admin/users | **Model limitation** — ST-004 sequential GET→DELETE→GET only |

---

## Totals

| Sheet | AI ST | Human ST-SUP | Combined ST |
|-------|------:|-------------:|------------:|
| `state-transitions.csv` | 42 | 15 | **57** |

**Files:** `tests/test-cases/{profile,cart,admin-users}/TC-*-ST-SUP-*.md`
