# Prompt log (Appendix A) — HW04 Feature A FR-03

**Student:** 23127271 · **Tool:** Cursor Agent  
**Scope:** Feature A — FR-03 Forgot Password (Web)

Prompts are paraphrased in English from the Cursor session; outcomes match files under `HW4/23127271/`.

---

## Interaction 1 — 2026-08-07 · FR-03 Analyze only

**Prompt:** Use automation-testing skill for Feature A — FR-03 Forgot Password (Web). **Analyze only** — no Design case table, no JSON, no Playwright. Cross-check README + HW04 PDF.

**AI output:** Actors, two-step transitions, FR-01/FR-22/SEC-07 rules, SUT gaps (OTP 4 digits, missing confirm/indicator/back-to-login, email type=text). Stage file: `docs/fr03-analysis.md`.

**Student action:** Accept Analyze; next = Design ≥12 cases only.

---

## Interaction 2 — 2026-08-07 · FR-03 Design only

**Prompt:** Based on Analyze, propose ≥12 distinct TC-FORGOT IDs (pos/neg/boundary/UI). No JSON, no Playwright.

**AI output:** 14 cases TC-FORGOT-001…014 in `docs/fr03-design.md`.

**Student action:** Review coverage; next = Review (still no JSON/code).

---

## Interaction 3 — 2026-08-07 · FR-03 Review only

**Prompt:** Review case list — drop duplicates, map observable oracles, forecast SUT fails. Do not soften oracles. No code.

**AI output:** Keep all 14; oracle map; forecast fails 010–014 → `docs/fr03-review.md`.

**Student action:** Accept Review; next = Model data.

---

## Interaction 4 — 2026-08-07 · FR-03 Model data

**Prompt:** External JSON only — journeys/assertions vocabulary; map every Design ID to one record.

**AI output:** `test-data/fr03-forgot-password.json` + `docs/fr03-model-data.md`.

**Student action:** Next = Map automation.

---

## Interaction 5 — 2026-08-07 · FR-03 Map automation

**Prompt:** Map locators, setup/cleanup, journey→actions, expect vocabulary. Do not generate full suite yet.

**AI output:** `docs/fr03-map-automation.md` (ForgotPasswordPage plan, dialog `Promise.all` note).

**Student action:** Prompt Generate when ready.

---

## Interaction 6 — 2026-08-07 · FR-03 Generate

**Prompt:** Generate page object + data-driven `.spec.js` from JSON. Keep Review oracles; do not soften for fake green.

**AI output:** `ForgotPasswordPage.js`, loader/helpers, `fr03-forgot-password.spec.js`, matrix runner, conversion log.

**Student action:** Run Verify when SUT is up.

---

## Interaction 7 — 2026-08-07 · FR-03 Verify + repair

**Prompt:** List tests → Chromium → full 3-browser matrix; stamp `Run by: 23127271`. Fix automation bugs only; keep product fails.

**AI output:** 9 pass / 5 fail × 3; dialog deadlock fix; `docs/fr03-verify-chromium.md` + `fr03-bug-notes.md` + BUG-FR03-001…005.

**Student action:** Accepted product fails 010–014.

---

## Interaction 8 — 2026-08-09 · PDF gap check + AI reports

**Prompt:** Double-check FR-03 against the HW04 PDF for gaps; write the AI report.

**AI output:** `hw04-fr03-gap-analysis.md`; `ai-audit-report.md`; `ai-critique.md`; formal `bug-reports/`; README links.

**Student action:** Review wording; file GitHub Issues with screenshots before final Moodle zip; continue Features B/C later.

---

## Interaction 9 — 2026-08-09 · Prepare Feature B without overwriting A

**Prompt:** Prepare before Feature B — FR-08 Checkout. Make sure it does not overwrite Feature A evidence.

**AI output:** Freeze archive + EVIDENCE-LOCK; matrix filter `test:matrix:fr08`; merge-safe manifests; default report slug `adhoc`; `docs/fr08-prep-ledger.md`; `FR-08/README.md`.

**Student action:** Run `npm run evidence:verify-fr03` before/after B work; implement FR-08 only when ready.

---

## Interaction 10 — 2026-08-09 · FR-08 Analyze only

**Prompt:** Feature B FR-08 Checkout — **Analyze only**. Keep FR-03 freeze. No Design IDs yet.

**AI output:** Auth gate, readonly total, line items, server recalc, cart clear; SUT defect notes → `docs/fr08-analysis.md`.

**Student action:** Next = Design ≥12.

---

## Interaction 11 — 2026-08-09 · FR-08 Design only

**Prompt:** Design ≥12 TC-CHECKOUT IDs from Analyze. No JSON/code.

**AI output:** 14 cases in `docs/fr08-design.md`.

**Student action:** Next = Review.

---

## Interaction 12 — 2026-08-09 · FR-08 Review only

**Prompt:** Review FR-08 cases; keep oracles for known defects 002/003/007/008/009. No code.

**AI output:** `docs/fr08-review.md`.

**Student action:** Next = Model data.

---

## Interaction 13 — 2026-08-09 · FR-08 Model data

**Prompt:** External `fr08-checkout.json` + journey/assertion vocabulary only.

**AI output:** JSON + `docs/fr08-model-data.md`.

**Student action:** Next = Map.

---

## Interaction 14 — 2026-08-09 · FR-08 Map automation

**Prompt:** Map Checkout/Cart/Home page objects, SPA cart seed navigation, expect vocabulary. No full spec yet.

**AI output:** `docs/fr08-map-automation.md`.

**Student action:** Prompt Generate.

---

## Interaction 15 — 2026-08-09 · FR-08 Generate + Verify

**Prompt:** Generate FR-08 suite; run matrix; do not overwrite FR-03; do not soften oracles.

**AI output:** `CheckoutPage.js`, `fr08-checkout.spec.js`, matrix 9/5 × 3; BUG-FR08-001…005; `docs/fr08-verify-chromium.md`; `evidence:verify-fr03` OK.

**Student action:** Review defects; Feature C next.

---

## Interaction 16 — 2026-08-10 · Stage-doc parity (FR-03/FR-08)

**Prompt:** Check FR-03/FR-08 for separate Analyze→Verify markdown like FR-15; reconstruct any missing stage files; do not change oracles.

**AI output:** Added `fr03-*.md` and `fr08-*.md` stage set (analysis/design/review/model-data/map/verify) under both submission package and `hw04-automation/docs/`; aligned this prompt log to one-stage-per-interaction.

**Student action:** Accept; commit gradually.

---

## Interaction 17 — 2026-08-10 · Feature C FR-15 Analyze only

**Prompt:** Use automation-testing skill for Feature C — FR-15 CRUD (Admin). Student ID 23127271. Analysis stage only — no Design cases, no code. Keep FR-03/FR-08 evidence. Write results under `SoftwareTesting-HW/HW4`.

**AI output:** `docs/fr15-analysis.md` (actors, preconditions, CRUD, Tên/Giá/Danh mục rules, FR-12 linkage, SUT gaps, ambiguities); `FR-15/README.md`; Analyze entry in `ai-conversion-log.md`; ledger marks C as Analysis-only.

**Student action:** Accept Analysis; next prompt = Design ≥12 cases only (still no Generate until Review/Data/Map).

---

## Interaction 18 — 2026-08-10 · Feature C FR-15 Design only

**Prompt:** Based on Analyze, propose >12 distinct test case IDs (positive CRUD + negative/boundary). No JSON, no Playwright.

**AI output:** 14 cases `TC-PRODUCT-001…014` in `docs/fr15-design.md` (CRUD 001–005, name/price/category validation 006–012, FR-12 auth 013–014); conversion log Design stage; FR-15 README case ledger.

**Student action:** Review coverage; next = Review stage (still no JSON/code).

---

## Interaction 19 — 2026-08-10 · Feature C FR-15 Review only

**Prompt:** Review test case list — drop semantic duplicates, map observable oracles, note cases likely to fail from SUT defects. No code generation.

**AI output:** `docs/fr15-review.md` — kept 14 IDs; narrowed 001/002; oracle map (UI/API/status); likely fail 004,006,008–010,012–014 (8); likely pass ~6. No JSON/Playwright.

**Student action:** Accept Review; next = Model data JSON only when ready.

---

## Interaction 20 — 2026-08-10 · Feature C FR-15 Model data

**Prompt:** Create JSON from reviewed test cases. Primitives only; no selectors/secrets in JSON.

**AI output:** `test-data/fr15-admin-product.json` (14 cases); `docs/fr15-model-data.md` schema/vocabulary; credentials via `authMode` only.

**Student action:** Next = Map automation / Generate when ready.

---

## Interaction 21 — 2026-08-10 · Feature C FR-15 Map automation

**Prompt:** Map automation — locators, admin setup/cleanup, action/expect vocabulary. Do not generate full spec if skill separates stages; or clearly mark Map done then Generate.

**AI output:** `docs/fr15-map-automation.md` (locators, setup/cleanup, journey→actions, expect vocabulary, per-case map, Generate file list). **No** `fr15-*.spec.js` yet — Generate is next separate stage.

**Student action:** Prompt Generate when ready to implement page object + loader + spec.

---

## Interaction 22 — 2026-08-10 · Feature C FR-15 Generate

**Prompt:** Generate — implement pages + data-driven `.spec.js` from JSON. Keep oracles; do not soften assertions for fake green.

**AI output:** `AdminProductPage.js`, `product-api.js`, FR-15 loader allow-lists, `fr15-admin-product.spec.js` (14 cases), matrix `BASE_URL=5174` for FR-15; discovery 42 tests. Spec oracles unchanged (expected product fails 004/006/008–010/012–014).

**Student action:** Run Verify (`npm run test:matrix:fr15` + `evidence:verify-fr03`) when SUT is up.

---

## Interaction 23 — 2026-08-10 · Feature C FR-15 Verify Chromium

**Prompt:** Verify — run FR-15 on Chromium; list failures; propose targeted fixes; do not change expected to match buggy UI.

**AI output:** Chromium **6 pass / 8 fail**; `docs/fr15-verify-chromium.md`. Failures = product defects (004 UI isolation, validation+FR-12 return 200). Optional clearer 004 row-index assert; no oracle softening.

**Student action:** Decide on optional 004 locator clarity; add BUG-FR15 reports; run full matrix when ready.
