# AI Critique (HW04 §10) — 200–300 words

**Student:** Vo Ngoc Bich Tram (23127271)  
**Feature:** A — FR-03 Forgot Password (Web)  
**Date:** 2026-08-09  

---

Working with Cursor on HW04 Feature A showed that AI is strong at *structured* automation scaffolding but weak when the SUT disagrees with the specification. After I insisted on a step-by-step flow (analyze → design → data model → map → generate → verify), the agent produced a solid data-driven Playwright package: external JSON, a journey/assertion vocabulary, Chromium/Firefox/WebKit projects, and HTML reports stamped `Run by: 23127271` with ISO timestamps. That satisfied the mechanical Task 1 checklist quickly.

Where the AI went wrong was subtler. It first shipped a one-case “slice,” which would have failed the ≥12 rule. Early selectors treated any “đăng nhập” text as the FR-03 “Quay lại đăng nhập” control, creating a false Pass. For weak passwords, it waited for dialogs *after* `click()`, deadlocking on the SUT’s synchronous `alert()`. It also wanted end-of-test assertions that still looked for step-1 buttons after navigation to `/login`. Most dangerously, it was biased toward making tests green by matching the defective UI (4-digit OTP, missing confirm field) instead of keeping README oracles — which would have hidden real bugs. Those mistakes came from prompt shortcuts, generic Playwright patterns, and the model’s preference for passing demos over adversarial oracles.

The principle I take away: use AI as a disciplined assistant through each automation stage, then **audit selectors, dialog timing, and expected results yourself** against the SRS before trusting any matrix report.
