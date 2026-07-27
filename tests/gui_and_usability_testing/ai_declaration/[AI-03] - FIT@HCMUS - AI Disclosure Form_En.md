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
| Assignment ID: | HW03 — Task 1 |
| Assignment Title: | GUI Checklist & Usability Testing on EShopSut |
| AI Use Category (1–5): | Category |
| Date: | 25/07/2026 |
| Student name: | Dang Truong Nguyen |
| Student ID: | 23127438 |

## 2. Disclosure Questions

### 1. AI tool(s) used:

- Claude Code (Claude Opus 4.8)

### 2. Stage(s) of the assignment where AI was used:

Tick all that apply: [x] brainstorming  [x] outlining  [x] drafting  [x] feedback  [ ] revision  [ ] coding  [x] data analysis  [ ] visual design  [ ] other (specify).

AI was used to build the UI element inventory, draft the GUI checklist per Interface Aspect (IA-01→IA-04 against FR-21→FR-24), diagnose coverage gaps, consolidate the final 66-item checklist, and draft the bug reports. I executed every checklist item on the running SUT myself and wrote the gap analysis and AI Critique.

### 3. Main prompts or tasks given to the AI:

Paste the 2–3 most impactful prompts verbatim. For the full transcript, attach Appendix A (prompt_log.md).

The full prompt set (Prompt #1, #2a–#2d, #3, #4, #6) is in `plan/PLAN.md` and pasted verbatim in the AI Audit Report (Section 3). The 3 most impactful:

1. **Prompt #1 — UI element inventory**

   ROLE: You are helping build a UI element inventory for GUI testing (not generating checklist items yet). You have read access to the eshop-sut repository. CONTEXT: EShop is a Vietnamese e-commerce demo app. Screen in scope: "<<screen name>>", corresponding to FR-<<0X>>. STEPS: search `frontend-web/src/` for the file(s) implementing the screen; read the full component tree incl. every conditional-rendering branch; cross-check against the running app; build an exhaustive UI element inventory for THIS SCREEN ONLY. OUTPUT: a markdown table with a `Source file:line` column so every row traces to the code.

2. **Prompt #2a — GUI checklist per Interface Aspect** (run 4×, for IA-01→IA-04 with FR-21→FR-24)

   ROLE: You are a senior QA engineer creating a requirements-based GUI checklist. CONTEXT: EShop Frontend Web; the Phase-1 inventory; the official FR-21 (General UI Standards) verbatim from README §8. TASK: generate GUI checklist items for IA-01 ONLY. RULES: each item = one objective testable Pass/Fail statement; each must reference a specific screen/element from the inventory; verify each FR-21 rule plus best-practice items; merge items shared across screens; produce ≥12 items. OUTPUT: a table `| ID | Screen(s) | Checklist Item | Expected Result | Traced to |`.

3. **Prompt #6 — bug report / GitHub issue draft**

   I found a UI bug while executing GUI checklist item <<ID>>. Raw details (all provided by me — do not add anything I have not stated): Screen, Steps, Expected (per checklist / FR-XX), Actual observed, Environment. TASK: draft a GitHub issue using exactly this structure (Title / Description / Steps to Reproduce / Expected / Actual / Environment / Related checklist item / Severity [Blocker/Major/Minor/Cosmetic] / Screenshot). Do not invent, assume, or embellish any detail beyond what I gave you.

### 4. Specific parts of the work AI contributed to:

Be specific. Example: 'AI generated TC01–TC15 in Section 3.2; I rewrote TC04 and TC11; AI did NOT contribute to Sections 1, 2, 4, or the AI Critique.'

Claude Code generated the UI element inventory (9 files), the four Interface-Aspect checklist drafts (65 items across IA-01→IA-04), the gap-analysis diagnosis, the consolidated 66-item checklist, and the 48 GitHub-issue drafts. I decided the final screen scope, added 4 manual GUI-GAP items (including two accessibility defects — `html lang="en"` and missing `htmlFor` — that the AI missed even though it proposed the accessibility dimension), confirmed every defect severity, and executed all 66 checklist items myself on the running SUT. AI did NOT write the gap-analysis reasoning, the AI Critique, or this disclosure form.

### 5. How I reviewed, revised, or verified the AI output:

Describe your verification method (ran the test, checked the spec, asked the TA, looked up RFC, cross-checked with the ISTQB syllabus, etc.).

- For the checklist drafts, I cross-checked every item against the SUT requirements FR-21→FR-24 (README §8, pasted into the prompts verbatim) and against each element's `Source file:line` in the React source, so that each item is grounded in the real UI and the actual requirement.
- I executed all 66 checklist items myself on the running SUT (Frontend Web at `localhost:5173`, Google Chrome), comparing each observed result against the item's Expected Result, and captured a screenshot for every Failed item.
- For the AI-drafted bug reports, I grouped the 57 failed items into 48 distinct defects, personally confirmed each severity (Blocker/Major/Minor) against reproduction, attached the real screenshot per bug, and filed them as GitHub issues #194–241 — cross-referencing each issue back to its checklist ID.

### 6. Citation (if required by course style guide):

Software Testing uses the IEEE style. Example: Anthropic. (2026). AI Tool (e.g., ChatGPT, Claude, Gemini) [Large language model]. https://claude.ai

1. Anthropic. (2026). Claude (Claude Opus 4.8) [Large language model]. https://claude.ai

## 3. Statement of Honesty

By signing below, I confirm that the disclosure above is accurate and complete. I understand that undisclosed or false disclosure of AI use is treated as academic misconduct and may result in a 0 grade for the assignment and disciplinary referral.

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 25/07/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
