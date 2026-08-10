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
| Assignment ID: | HW04 — Task 1 |
| Assignment Title: | Automation Testing on EShopSut (FR-02, FR-09, FR-14) |
| AI Use Category (1–5): | Category |
| Date: | 10/08/2026 |
| Student name: | Dang Truong Nguyen |
| Student ID: | 23127438 |

## 2. Disclosure Questions

### 1. AI tool(s) used:

- Claude Code (Claude Fable 5)

### 2. Stage(s) of the assignment where AI was used:

Tick all that apply: [x] brainstorming  [x] outlining  [x] drafting  [x] feedback  [x] revision  [x] coding  [x] data analysis  [ ] visual design  [ ] other (specify).

AI was used to write the Task-1 work plan, design the 40 test cases and their data files, generate the Playwright Page Objects / spec files / multi-browser configuration, triage the multi-browser execution results, draft the summary report (`REPORT.md`), draft the 9 GitHub bug reports, and write the Cloudinary evidence-upload script. I directed every step, reviewed and corrected each artifact, verified all runs, and recorded the demo video myself.

### 3. Main prompts or tasks given to the AI:

Paste the 2–3 most impactful prompts verbatim. For the full transcript, attach Appendix A (prompt_log.md).

The full prompt-by-prompt trail (with outputs, verdicts and my fixes) is in the AI Audit Report (Section 3). The 3 most impactful:

1. **Prompt — Task-1 work plan**

   hãy viết plan cho task 1 vào folder plan trước, sau đó t sẽ đọc theo plan và cần biết làm gì

2. **Prompt — environment setup + Playwright scripts for the 3 chosen features**

   lấy FR 2, 9 14, hãy setup môi trường và viết code playwright cho 3 feat đó đi

   (The AI was then driven step-by-step per the plan: read the SRS sections for FR-02/09/14 → read the real frontend/backend source to derive selectors and seeded data → design ≥12 test cases per feature → emit separate JSON data files → generate Page Objects and data-driven specs → run on Chromium/Firefox/WebKit and fix script defects.)

3. **Prompt — summary report + templated bug reports filed as GitHub issues**

   t push lên git r, giờ hãy viết 1 file report md tổng hợp từ các result trước, sau đó viết bug report theo chuẩn template rổi đẩy lên github issue sử dụng gh

### 4. Specific parts of the work AI contributed to:

Be specific. Example: 'AI generated TC01–TC15 in Section 3.2; I rewrote TC04 and TC11; AI did NOT contribute to Sections 1, 2, 4, or the AI Critique.'

Claude Code generated `plan/task1-plan.md`, the 3 data files (40 test cases), the 3 Page Objects, the 3 spec files, `playwright.config.ts`, `REPORT.md`, the 9 GitHub issue bodies (#390–398), and `scripts/upload-screenshots-cloudinary.mjs`. I chose the 3 features, drove the step-by-step workflow, redesigned test isolation (fresh API-seeded users for lockout/coupon-usage, category snapshot + cleanup), replaced the non-working `getByLabel()` locators, added the API-level 401/403 oracle, diagnosed the port-3000 conflict that broke the first run, caught and repaired the title/body mismatch in the first batch of GitHub issues, verified "Run by: 23127438" inside all 4 HTML report payloads, and confirmed each of the 13 consistently-failing test cases traces to a real spec violation (9 defects). AI did NOT produce the HTML report execution evidence (real runs), the demo video, or the final wording of the AI Critique.

### 5. How I reviewed, revised, or verified the AI output:

Describe your verification method (ran the test, checked the spec, asked the TA, looked up RFC, cross-checked with the ISTQB syllabus, etc.).

- Executed the full suite on all 3 browsers (120 test executions) and required cross-browser consistency before accepting any failure as a defect: the same 13 test cases fail on Chromium, Firefox and WebKit — zero flaky, browser-specific failures.
- Cross-checked every failing assertion against the SRS (README spec of FR-02/FR-09/FR-14) and against the backend/frontend source to confirm the root cause (e.g., `login_attempts + 2` in `backend/server.js`, `total × (1 − value)` percent formula, strict `>` threshold, missing `authenticateToken` on `/api/apply-coupon`).
- Verified the anti-cheat requirement by decoding the base64-embedded `report.json` of all 4 HTML reports and confirming `options.title` / `metadata` carry "Run by: 23127438" + ISO timestamp.
- Spot-checked the filed GitHub issues (content, labels, template sections) and the Cloudinary-hosted screenshots (HTTP 200) after the link rewrite.

### 6. Citation (if required by course style guide):

Software Testing uses the IEEE style. Example: Anthropic. (2026). AI Tool (e.g., ChatGPT, Claude, Gemini) [Large language model]. https://claude.ai

1. Anthropic. (2026). Claude (Claude Fable 5) [Large language model]. https://claude.ai

## 3. Statement of Honesty

By signing below, I confirm that the disclosure above is accurate and complete. I understand that undisclosed or false disclosure of AI use is treated as academic misconduct and may result in a 0 grade for the assignment and disciplinary referral.

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 10/08/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
