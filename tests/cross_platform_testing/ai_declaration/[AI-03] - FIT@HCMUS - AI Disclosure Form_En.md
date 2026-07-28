Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)

CS423 / CSC13003 – Software Testing (AI-augmented · 2026)

AI POLICY · TEMPLATES — 2026 v1.0

# AI Use Disclosure Form

Attach to assignments where AI was used in any permitted capacity.

Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC15003 Software Testing course.

## 1. Course & Student Info

| Field | Value |
| --- | --- |
| Course: | CS423 / CSC13003 – Software Testing |
| Assignment ID: | HW03 — Task 3 |
| Assignment Title: | Cross-Browser / Cross-Platform execution of the GUI checklist on EShopSut |
| AI Use Category (1–5): | Category |
| Date: | 28/07/2026 |
| Student name: | Dang Truong Nguyen |
| Student ID: | 23127438 |

## 2. Disclosure Questions

### 1. AI tool(s) used:

- Claude Code (Claude Opus 5) — acting as orchestrator
- Four parallel sub-agents of the same model, each given one Interface Aspect of the checklist (IA-01 … IA-04). The orchestrator authored those sub-agent prompts during the session; they are reproduced verbatim in the AI Audit Report (Section 3) and summarised in `plan/PLAN-TASK3.md` §5.

### 2. Stage(s) of the assignment where AI was used:

Tick all that apply: [x] brainstorming  [x] outlining  [x] drafting  [x] feedback  [x] revision  [x] coding  [x] data analysis  [ ] visual design  [ ] other (specify).

AI designed and wrote the whole measurement harness (`harness/`: platform definitions, evidence overlay, per-check context, runner, matrix builder, evidence gate, window-capture script), implemented all 66 checks by reading the 66 Task 1 test cases, executed them on the 3 required platforms (198 executions), and drafted the report/matrix/divergence documents. AI did **not** decide the platform matrix, did not choose which divergences count as bugs, and did not produce a single pixel of any screenshot: every image comes from a real browser run captured by the browser itself or by the macOS `screencapture` utility.

### 3. Main prompts or tasks given to the AI:

Paste the 2–3 most impactful prompts verbatim. For the full transcript, attach Appendix A (prompt_log.md).

The full prompt set is pasted verbatim in the AI Audit Report (Section 3) — P1–P6 are the working prompts and P3a–P3d the four parallel sub-agent prompts (identical skeleton, different ID list + DESIGN NOTES) — and the skeletons are mirrored in `plan/PLAN-TASK3.md` §5. `<<...>>` marks what was substituted at run time. The 3 most impactful:

1. **T3·GĐ1 — the platform-matrix decision exchange (verbatim, Vietnamese: my instruction and my decisions)**

   The question put back to me: "Task 3 yêu cầu chạy checklist Task 1 trên ≥3 platform, screenshot phải hiện tên browser/OS/device + URL localhost. Máy này chỉ có Safari.app; Playwright đã cài sẵn Chromium/Firefox/WebKit. Anh muốn đi hướng nào?" — with 4 options offered (Playwright 3 engines local / Playwright + real Safari via `safaridriver` / BrowserStack–LambdaTest with my own credentials / 3 engines + mobile emulation).

   My decisions: "Playwright 3 engine (local)" (BrowserStack/LambdaTest trial was unavailable and this machine has only Safari installed) · overlay identity = "dtnguyen23@clc.fitus.edu.vn" · later in the session "Bỏ 2 cái mobile web kia" → the two emulated mobile platforms were dropped from the evidence set.

2. **P2 — the check-module contract given to every sub-agent (excerpt, verbatim from `harness/checks/README.md`)**

   "1. **Observe, never assume.** A check must read the live DOM / computed style / behaviour. Do not hard-code the Task 1 verdict. 2. **Put every platform-visible raw value into `metrics`.** The matrix builder diffs `metrics` across platforms; that diff is the actual Task 3 finding (e.g. `thousandsSeparator: "," | "."`, `validationMessage` per engine). […] 8. `BLOCKED` is legitimate: e.g. a keyboard-only check on the emulated mobile platforms, or `alert()` behaviour that a platform genuinely cannot express. Explain why in `evidence`."

3. **P3b — the IA-02 sub-agent prompt (excerpt, verbatim — the one that produced the headline finding `GUI-IA02-14`)**

   "DESIGN NOTES specific to IA-02 (forms) — this group is the richest source of genuine cross-engine differences, so instrument it carefully: IA02-14 (required-message language): submit an empty required field and record the raw `validationMessage` string per engine — Chromium/Firefox/WebKit word it differently and may localise differently. Judge PASS only if the message is Vietnamese. […] IA02-02 (`type="email"`), IA02-08 (OTP maxlength/pattern), IA02-09 (quantity min/max): besides reading the attributes, ACTUALLY type an invalid value, submit, and record `input.validationMessage` + `input.validity` flags in `metrics`. The native validation *message text* differs per engine and per UI language — that is exactly the kind of Task 3 finding we want. […] RULES: Every check OBSERVES the live app and returns PASS/FAIL/BLOCKED from what it sees — never hard-code the Task 1 verdict."

### 4. Specific parts of the work AI contributed to:

Be specific. Example: 'AI generated TC01–TC15 in Section 3.2; I rewrote TC04 and TC11; AI did NOT contribute to Sections 1, 2, 4, or the AI Critique.'

AI generated: `harness/lib/{platforms,overlay,ctx}.js`, `harness/run-audit.js`, `harness/checks/ia0{1,2,3,4}.js` (66 checks, 3.7 k lines), `harness/scripts/{build-matrix,capture-platform-proof,verify-evidence}.js`, `harness/run-all-platforms.sh`, and the first drafts of `platform-matrix.md`, `results-matrix.md`, `divergences.md`, `cross-platform-report.md`, `issues/XP-*.md` and `plan/PLAN-TASK3.md`. `results-matrix.md` and `divergences.md` are *generated files* — they are recomputed from `results/raw/*.json` by a script, not written by hand.

AI did NOT contribute to: the choice of platform matrix and the decision to substitute BrowserStack (mine, documented with its risk in `platform-matrix.md` §4–5), the final classification of each divergence as SUT bug vs. legitimate engine behaviour vs. measurement limitation, and the AI Critique.

### 5. How I reviewed, revised, or verified the AI output:

Describe your verification method (ran the test, checked the spec, asked the TA, looked up RFC, cross-checked with the ISTQB syllabus, etc.).

- **Every check was executed, not merely written.** The evidence gate (`verify-evidence.js`) refuses the deliverable if any of the 66 checklist IDs is missing on any platform, if any FAIL has no screenshot file on disk, or if any check ended in `ERROR` — so an unrunnable check cannot be silently reported as a finding.
- **Checks that disagreed with Task 1 were re-examined individually**, because a disagreement is either a better measurement or a broken check. Confirmed better measurements: `GUI-IA01-08` (Task 1 Passed — it only used the valid seed price; driving a non-numeric price through the UI renders `NaN ₫`), `GUI-IA01-15` (Task 1 Passed — at exactly 768 px Tailwind's `md:` breakpoint is already active so the grid is 3 columns, not the 2 the checklist demands), `GUI-IA04-12` (Task 1 Passed — both coupon branches do render, but the arithmetic the item also demands is wrong: a 10 % coupon shows `Tiết kiệm -270.000.000 ₫`).
- **I reversed one of the AI's own procedural decisions.** The first plan said not to restart the backend between platforms; the metrics proved the opposite was needed (`GUI-IA03-15.orderRows` drifted 7/3/5/9/11 with run order because checks place real orders), so the authoritative run re-seeds the SQLite fixture before every platform (`run-all-platforms.sh`).
- **Screenshots were opened and eyeballed**, not trusted: the window-capture path was corrected after the first attempt captured a different application window instead of the WebKit window.

### 6. Citation (if required by course style guide):

Software Testing uses the IEEE style. Example: Anthropic. (2026). AI Tool (e.g., ChatGPT, Claude, Gemini) [Large language model]. https://claude.ai

1. Anthropic. (2026). Claude (Claude Opus 5) [Large language model]. https://claude.ai
2. Microsoft. (2026). Playwright — cross-browser automation library (v1.56) [Software]. https://playwright.dev

## 3. Statement of Honesty

By signing below, I confirm that the disclosure above is accurate and complete. I understand that undisclosed or false disclosure of AI use is treated as academic misconduct and may result in a 0 grade for the assignment and disciplinary referral.

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 28/07/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
