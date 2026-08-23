# Stage 3 — Human extensions the AI missed (summary)

**Student:** 23127271 · **SUT:** EShop FR-04 / FR-07 / FR-19  
**Requirement:** ≥5 human-found cases with *why the AI missed them* — emphasis on **security** and **state transitions**.

Oracles follow Stage 2: no invented HTTP status codes unless written in spec.

---

## Totals

| Category | AI | Human SUP | Combined | Doc |
|----------|---:|----------:|---------:|-----|
| Domain partitions | 99 | 15 | 114 | `docs/stage3-extend.md` |
| State transitions | 42 | **15** | 57 | `docs/stage3-extend-state-transitions.md` |
| Security | 37 | **15** | 52 | `docs/stage3-extend-security.md` |
| Schema validation | 42 | 15 | 57 | `docs/stage3-extend-schema.md` |
| **Human total** | — | **60** | — | 5 per FR × 4 categories |

### Human SUP audit (Stage 3)

| Label | Count |
|-------|------:|
| VALID | 49 |
| INVALID | 1 |
| INCOMPLETE | 10 |

Full per-case labels and corrected oracles: [`docs/stage3-audit-human.md`](stage3-audit-human.md). Applied via `scripts/apply_stage3_audit_human.py`.

---

## State transitions — 5 per FR (15)

| Gap theme | Examples | Why AI missed |
|-----------|----------|---------------|
| **Concurrency / race** | PROFILE-ST-SUP-001/003 · CART-ST-SUP-002/005 · ADMIN-ST-SUP-002/005 | Prompt never asked for parallel transitions; AI emitted sequential PUT→GET chains only |
| **Illegal mid-flow auth** | PROFILE-ST-SUP-002/004 | Auth failures lived in domain TCs as one-shots, not state-transition “P0 must not advance” framing |
| **Missing legal paths** | CART-ST-SUP-001/004 (merge line 2/3) · PROFILE-ST-SUP-005 (address-first partial) | 1×1 bias toward id=1 merge and name→phone order |
| **Terminal session** | ADMIN-ST-SUP-003/004 (JWT after delete) | FR-19 lifecycle silent on token invalidation |
| **Unspecified admin rule** | ADMIN-ST-SUP-001 (delete other admin) | FR-19 only forbids self-delete |

Full tables: [`docs/stage3-extend-state-transitions.md`](stage3-extend-state-transitions.md)

---

## Security — 5 per FR (15)

| Gap theme | Examples | Why AI missed |
|-----------|----------|---------------|
| **Concurrency / race** | PROFILE-SEC-SUP-001/005 · CART-SEC-SUP-001/003 · ADMIN-SEC-SUP-003 | Security generator one-shot; checklist §2 concurrency omitted |
| **Privilege / integrity** | PROFILE-SEC-SUP-002 · CART-SEC-SUP-002/005 · ADMIN-SEC-SUP-001/002/004 | SEC-03 mapped to DELETE only; negative qty and list-endpoint auth gaps |
| **Encoding / parser bypass** | PROFILE-SEC-SUP-003/004 · CART-SEC-SUP-004 · ADMIN-SEC-SUP-005 | ASCII SQLi/XSS defaults; no null-byte, Content-Type, Unicode-escape, or path-encoding probes |

Full tables: [`docs/stage3-extend-security.md`](stage3-extend-security.md)

---

## Cross-cutting lesson (for AI audit report)

1. **Prompt quality:** Stating SEC-01..07 or “generate security tests” without **concurrency**, **list-endpoint SEC-03**, or **malformed envelopes** yields sequential happy-path + classic injection only.
2. **Model limitation:** LLMs mirror spec example JSON (flat objects, literal XSS, numeric path ids) and miss duplicate keys, nested bodies, and cross-field races.
3. **API characteristic:** In-memory cart, `SELECT *` profile/list, and undocumented DELETE bodies create races and schema leaks invisible from spec text alone.

---

## Scripts (idempotent append)

| Script | Sheet |
|--------|-------|
| `scripts/append_stage3_sup_cases.py` | `domain-partitions.csv` |
| `scripts/append_stage3_st_sup_cases.py` | `state-transitions.csv` |
| `scripts/append_stage3_sec_sup_cases.py` | `security-tests.csv` |
| `scripts/append_stage3_sch_sup_cases.py` | `schema-validation.csv` |
