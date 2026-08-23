# State Transition Testing Report — FR-04, FR-07, FR-19

**Student:** 23127271 · **SUT:** EShop (`http://localhost:3000`)  
**Category:** Stage 1 — State Transitions (API testing skill checklist §2)  
**Sources:** `Repo/eshop-sut/README.md`, `api_specification.md`

---

## Scope

| FR | Endpoint | Resource state model |
|----|----------|----------------------|
| FR-04 | `PUT /api/users/me` | Profile field snapshot P0→P1→…; immutables email/role |
| FR-07 | `POST /api/cart` | Cart line-item states EMPTY/SINGLE/MERGED/MULTI; FR-08 clears cart |
| FR-19 | `DELETE /api/admin/users/:id` | User existence EXISTS/DELETED/SELF; admin list count |

---

## FR-04 — Profile state machine

```
P0 (seed profile)
  │ PUT valid (name/phone/address)
  ▼
P1 (updated snapshot)
  │ PUT again (full or partial — partial semantics unspecified)
  ▼
P2 … Pn

Constraints (no transition): email, role
```

**Count:** 12 cases (`TC-PROFILE-ST-001` … `TC-PROFILE-ST-012`)

| TC ID | Transition | Type |
|-------|------------|------|
| TC-PROFILE-ST-001 | P0 → P1 | Legal |
| TC-PROFILE-ST-002 | P0 → P1a → P1b | Legal / Unspecified |
| TC-PROFILE-ST-003 | P1 → P2 | Legal |
| TC-PROFILE-ST-004 | P1 → P1 | Legal (idempotency) |
| TC-PROFILE-ST-005 | session boundary | Legal |
| TC-PROFILE-ST-006 | immutable email | Legal constraint |
| TC-PROFILE-ST-007 | immutable role | Legal constraint |
| TC-PROFILE-ST-008 | admin P0→P1 | Legal |
| TC-PROFILE-ST-009 | multi partial chain | Legal / Unspecified |
| TC-PROFILE-ST-010 | invalid transition attempt | Illegal input / Unspecified |
| TC-PROFILE-ST-011 | cross-user isolation | Legal (isolation) |
| TC-PROFILE-ST-012 | no-op / reject | Illegal / no-op |

---

## FR-07 — Cart state machine

```
C_EMPTY
  │ POST product
  ▼
C_SINGLE ──POST same id──► C_MERGED (qty↑, one line)   [FR-07]
  │ POST different id
  ▼
C_MULTI ──POST checkout (FR-08)──► C_EMPTY
```

**Count:** 15 cases (`TC-CART-ST-001` … `TC-CART-ST-015`)

| TC ID | Transition | Type |
|-------|------------|------|
| TC-CART-ST-001 | C_EMPTY → C_SINGLE | Legal |
| TC-CART-ST-002 | C_SINGLE → C_MERGED | Legal |
| TC-CART-ST-003 | C_SINGLE → C_TWO | Legal |
| TC-CART-ST-004 | C_TWO → C_TWO' | Legal |
| TC-CART-ST-005 | C_TWO → C_THREE | Legal |
| TC-CART-ST-006 | C_EMPTY → C_MERGED | Legal |
| TC-CART-ST-007 | quantity accumulation | Legal |
| TC-CART-ST-008 | idempotent add | Legal |
| TC-CART-ST-009 | observable consistency | Legal |
| TC-CART-ST-010 | cross-user isolation | Legal (isolation) |
| TC-CART-ST-011 | C_MULTI → C_EMPTY | Legal (cross-endpoint FR-08) |
| TC-CART-ST-012 | post-checkout fresh add | Legal |
| TC-CART-ST-013 | illegal qty decrease via POST-only | Legal (monotonic add) |
| TC-CART-ST-014 | C_EMPTY → C_MERGED(5) | Legal |
| TC-CART-ST-015 | session boundary | Legal / Unspecified persistence |

---

## FR-19 — User existence state machine

```
U_EXISTS (in admin list)
  │ DELETE by admin (other user)
  ▼
U_DELETED (terminal — not in list, login fails)

U_SELF (admin own id)
  │ DELETE self
  ✗ blocked [FR-19]
```

**Count:** 15 cases (`TC-ADMINUSERS-ST-001` … `TC-ADMINUSERS-ST-015`)

| TC ID | Transition | Type |
|-------|------------|------|
| TC-ADMINUSERS-ST-001 | U_EXISTS → U_DELETED | Legal |
| TC-ADMINUSERS-ST-002 | illegal self-delete | Illegal |
| TC-ADMINUSERS-ST-003 | terminal / idempotency | Illegal repeat |
| TC-ADMINUSERS-ST-004 | list state | Legal |
| TC-ADMINUSERS-ST-005 | multi-delete chain | Legal |
| TC-ADMINUSERS-ST-006 | illegal role | Illegal |
| TC-ADMINUSERS-ST-007 | illegal unauthenticated | Illegal |
| TC-ADMINUSERS-ST-008 | lifecycle | Legal |
| TC-ADMINUSERS-ST-009 | U3→DELETED, U1/U2→EXISTS | Legal |
| TC-ADMINUSERS-ST-010 | illegal self + list stability | Illegal |
| TC-ADMINUSERS-ST-011 | cross-endpoint auth state | Legal consequence |
| TC-ADMINUSERS-ST-012 | cascade edge | Unspecified |
| TC-ADMINUSERS-ST-013 | path wins over body | Illegal / guard |
| TC-ADMINUSERS-ST-014 | seed user delete | Legal |
| TC-ADMINUSERS-ST-015 | delete missing user | Illegal |

---

## Step 5 — Review checklist

| Check | FR-04 | FR-07 | FR-19 |
|-------|-------|-------|-------|
| Legal transition covered | Yes | Yes | Yes |
| Illegal / terminal transition | Yes | Yes | Yes |
| Idempotency / repeat | Yes | Yes | Yes |
| Cross-session / isolation | Yes | Yes | Yes |
| Oracles spec-only (no invented HTTP codes) | Yes | Yes | Yes |

## Artifact index

| Artifact | Path |
|----------|------|
| This report | `docs/state-transition-report.md` |
| Per-TC files | `tests/test-cases/{profile,cart,admin-users}/TC-*-ST-*.md` |
| Sheet | `sheets/state-transitions.csv` |
| Generator | `scripts/generate_state_transitions.py` |

**Totals:** 12 PROFILE + 15 CART + 15 ADMINUSERS = **42** state-transition cases.

**Combined Stage-1 AI counts (domain + state):**
- FR-04: 40 + 12 = 52
- FR-07: 39 + 15 = 54
- FR-19: 20 + 15 = 35

**Stage 2 audit:** 33 VALID / 0 INVALID / 9 INCOMPLETE — see `docs/stage2-audit-state-transitions.md`. Corrected oracles applied in TC files and `sheets/state-transitions.csv`.

**Stage 3 human SUP:** 15 cases (5 per FR) — see `docs/stage3-extend-state-transitions.md`. Sheet total: 42 AI + 15 Human = **57** state-transition cases.
