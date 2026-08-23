# Prompt log — Stage 1 Domain partitions

**Student:** 23127271 · **Tool:** Cursor Grok 4.6  
**Scope:** FR-04 `PUT /api/users/me` · FR-07 `POST /api/cart` · FR-19 `DELETE /api/admin/users/:id`

Full machine log: `ai_audit_log.md`.

---

## Interaction 1 — 2026-08-22 · Stage 1 Domain partitions

**Prompt:** Design and generate all domain-partition test cases for FR-04 / FR-07 / FR-19 using the API testing skill and Skill-01-Domain-Testing, against `Repo/eshop-sut`.

**AI output:** 99 cases (40 PROFILE, 39 CART, 20 ADMINUSERS); domain-testing report Steps 1–5; per-TC markdown; `sheets/domain-partitions.csv` with `Category=DomainPartition` and blank `AuditStatus`.

**Student action:** Review oracles and ⚠️ assumptions in `docs/domain-testing-report.md` before Stage 2 audit.

---

## Interaction 2 — 2026-08-22 · Stage 2 Audit

**Prompt:** Label each AI-generated test case VALID / INVALID / INCOMPLETE with reasoning, and correct the invalid or incomplete ones. Do not assume anything; reason if the requirement was missing. Example: P-NAME-05 (omit name) was assumed required.

**AI output:** 16 VALID, 42 INVALID, 41 INCOMPLETE. P-NAME-05 / `TC-PROFILE-010` marked INVALID (name not specified as mandatory). Invented HTTP 400/401/403/404 and FR-06-on-cart-API oracles corrected in place. Artifacts: `docs/stage2-audit.md`, updated TC files and CSV.

**Student action:** Use corrected oracles as the final cases. Next = Stage 3 extend (≥5 human-found).

---

## Interaction 3 — 2026-08-22 · Stage 3 Extend (human-found domain partitions)

**Prompt:** Add at least five domain-partition test cases the AI missed; explain why (prompt quality, model limitation, or API characteristics).

**AI output:** 6 SUP cases + `docs/stage3-extend.md`; rows appended to `sheets/domain-partitions.csv` (`Source=Human`).

**Student action:** Execute SUP cases when running Newman; cite in HW06 report extend section.

---

## Interaction 4 — 2026-08-22 · Stage 3 Extend (≥5 per FR)

**Prompt:** Add at least five domain-partition cases **per FR** that the AI missed, with why missed.

**AI output:** 9 additional SUP cases (PROFILE 004–005, CART 003–005, ADMINUSERS 002–005) → **15 total** (5 per FR). Updated `docs/stage3-extend.md`, CSV, TC files.

---

## Interaction 5 — 2026-08-22 · Stage 1 State transitions

**Prompt:** Using API testing skill and state-transition method, generate all state-transition test cases for FR-04 / FR-07 / FR-19.

**AI output:** 42 cases (12 PROFILE-ST, 15 CART-ST, 15 ADMINUSERS-ST); `docs/state-transition-report.md`; `sheets/state-transitions.csv`. Combined domain+state AI counts: FR-04 **52**, FR-07 **54**, FR-19 **35**.

**Student action:** Audit state-transition oracles (Stage 2) before security/schema generation.

---

## Interaction 6 — 2026-08-22 · Stage 2 Audit (state transitions)

**Prompt:** Label each AI-generated state-transition case VALID / INVALID / INCOMPLETE; correct invalid/incomplete ones (same rule as domain audit).

**AI output:** 33 VALID, 0 INVALID, 9 INCOMPLETE. Corrected oracles in TC files + `sheets/state-transitions.csv`. Report: `docs/stage2-audit-state-transitions.md`.

---

## Interaction 7 — 2026-08-22 · Stage 3 Extend (state transitions, ≥5 per FR)

**Prompt:** Add at least five state-transition cases per API the AI missed (INVALID, concurrency/race, others); explain why missed.

**AI output:** 8 new ST-SUP cases (003–005 per module) added to existing 7 → **15 total** (5 per FR). Themes: concurrency (7), illegal/failed (4), missing legal paths (3), terminal session (2). `docs/stage3-extend-state-transitions.md`; CSV total **57**.

---

## Interaction 8 — 2026-08-23 · Stage 1 Security tests

**Prompt:** Use API testing skill to design and generate security test cases for FR-04 / FR-07 / FR-19.

**AI output:** 40 SEC-mapped cases (14 PROFILE-SEC, 12 CART-SEC, 14 ADMINUSERS-SEC). Covers SEC-01..06; SEC-07 noted as gap (OTP APIs out of scope). Artifacts: `docs/security-testing-report.md`, `sheets/security-tests.csv`.

---

## Interaction 9 — 2026-08-23 · Stage 3 Extend (security, ≥5 per FR)

**Prompt:** Add at least five security test cases per API that the AI missed (INVALID, concurrency/race, others); explain why missed.

**AI output:** 15 SEC-SUP cases (5 per FR). Themes: concurrency (5), illegal/integrity (5), encoding bypass (5). `docs/stage3-extend-security.md`; CSV total **52** (37 AI + 15 Human). Combined Stage-1: FR-04 **71**, FR-07 **70**, FR-19 **52**.

---

## Interaction 10 — 2026-08-23 · Stage 2 Audit (security)

**Prompt:** Label each AI-generated security case VALID / INVALID / INCOMPLETE; correct invalid/incomplete oracles.

**AI output:** 31 VALID, 1 INVALID, 5 INCOMPLETE (37 AI SEC). Report: `docs/stage2-audit-security.md`. Key fix: `TC-CART-SEC-006` dropped invented cart price-validation rule (FR-08 is checkout-only).

---

## Interaction 11 — 2026-08-23 · Stage 1 Schema validation

**Prompt:** Use API testing skill to design and generate schema validation test cases for FR-04 / FR-07 / FR-19.

**AI output:** 42 SCH cases (14 per FR): request/response JSON types, field presence/types from api_spec examples, SEC-01 forbidden fields, Content-Type, type-coercion and error-envelope observe where spec is silent. `docs/schema-validation-report.md`, `sheets/schema-validation.csv`. Combined Stage-1: FR-04 **85**, FR-07 **84**, FR-19 **66**.

---

## Interaction 12 — 2026-08-23 · Stage 3 Extend (human gaps — security & state focus)

**Prompt:** Add ≥5 own test cases the AI missed, especially security and state transitions; explain why missed.

**AI output:** **Already present:** 15 ST-SUP + 15 SEC-SUP (5/FR). **Added:** 15 SCH-SUP (schema gap) + `docs/stage3-extend-summary.md` master index. **60 human cases** total across four categories.


