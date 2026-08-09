# Prompt log (Appendix A) — HW04 Feature A FR-03

**Student:** 23127271 · **Tool:** Cursor Agent  
**Scope:** Feature A — FR-03 Forgot Password (Web)

Prompts are paraphrased in English from the Cursor session; outcomes match files under `HW4/23127271/`.

---

## Interaction 1 — 2026-08-07 · Analyze + contract

**Prompt:** In HW4/FR-03, use the automation testing skill for Feature A FR-03 Forgot Password (Web). Cross-check `eshop-sut/README.md` and `2026.HW04.Automation Testing_En.pdf`.

**AI output:** Requirement ledger; FR-03 two-step rules; SUT defect notes; plan for ≥12 cases, JSON data, 3 browsers, labeled HTML.

**Student action:** Confirmed Student ID 23127271; accepted Feature A-only scope for this slice.

---

## Interaction 2 — 2026-08-07 · Design + generate suite

**Prompt:** Expand beyond the prior 1-case slice to ≥12 data-driven Playwright cases with external JSON, page object, matrix runner.

**AI output:** 14 cases TC-FORGOT-001…014; `fr03-forgot-password.json`; loader; spec; `ForgotPasswordPage`; `run-matrix.js`; conversion log.

**Student action:** Kept spec oracles for UI contracts (010–014); reviewed categories mix.

---

## Interaction 3 — 2026-08-07 · Verify + repair

**Prompt:** Install browsers, list tests, run Chromium, then full 3-browser matrix; stamp `Run by: 23127271`.

**AI output:** Discovery 42 tests; first Chromium run exposed dialog deadlock and assertion lifecycle bugs; repairs; matrix 9 pass / 5 fail × 3; reports + manifest.

**Student action:** Accepted product fails 010–014; did not loosen expectations.

---

## Interaction 4 — 2026-08-09 · PDF gap check + AI reports

**Prompt:** Double-check FR-03 against the HW04 PDF for gaps; write the AI report.

**AI output:** `hw04-fr03-gap-analysis.md`; `ai-audit-report.md`; `ai-critique.md`; formal `bug-reports/`; README links.

**Student action:** Review wording; file GitHub Issues with screenshots before final Moodle zip; continue Features B/C later.

---

## Interaction 5 — 2026-08-09 · Prepare Feature B without overwriting A

**Prompt:** Prepare before Feature B — FR-08 Checkout. Make sure it does not overwrite Feature A evidence.

**AI output:** Freeze archive + EVIDENCE-LOCK; matrix filter `test:matrix:fr08`; merge-safe manifests; default report slug `adhoc`; `docs/fr08-prep-ledger.md`; `FR-08/README.md`.

**Student action:** Run `npm run evidence:verify-fr03` before/after B work; implement FR-08 only when ready.

---

## Interaction 6 — 2026-08-09 · Implement Feature B FR-08

**Prompt:** In HW4, use automation testing skill for Feature B — FR-08 Checkout; cross-check README + HW04 PDF; do not overwrite Feature A evidence.

**AI output:** 14 data-driven cases; SPA cart seeding fix; matrix 9/5 × 3 browsers; BUG-FR08-001…005; FR-03 freeze verified OK.

**Student action:** Review defects; optional AI Audit update for Feature B; Feature C next.
