# AI Critique (HW04 §10) — 200–300 words

**Student:** Vo Ngoc Bich Tram (23127271)  
**Features:** A FR-03 · B FR-08 · C FR-15  
**Date:** 2026-08-10  

---

Working with Cursor on HW04 showed that AI is strong at *structured* automation scaffolding but weak when the SUT disagrees with the specification. After I insisted on a step-by-step flow (analyze → design → data model → map → generate → verify) for each feature, the agent produced solid data-driven Playwright packages: external JSON, journey/assertion vocabularies, Chromium/Firefox/WebKit projects, and HTML reports stamped `Run by: 23127271`. That satisfied the mechanical Task 1 checklist across FR-03, FR-08, and FR-15.

Where the AI went wrong was subtler. On Feature A it first shipped a one-case “slice,” used over-broad “đăng nhập” locators, deadlocked on synchronous `alert()`, and preferred matching the defective 4-digit OTP UI instead of keeping README oracles. On Feature B it seeded the cart via storage the SPA ignored, producing false fails until the seed path matched React hydration. On Feature C it was tempted to accept HTTP 200 for empty names, zero/negative prices, invalid categories, and missing admin JWT — which would have hidden FR-15 validation and FR-12 authorization defects. Those mistakes came from prompt shortcuts, generic Playwright patterns, and the model’s preference for passing demos over adversarial oracles.

The principle I take away: use AI as a disciplined assistant through each automation stage, then **audit selectors, SPA state, dialog timing, and expected results yourself** against the SRS before trusting any matrix report.
