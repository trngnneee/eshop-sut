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
| Assignment ID: | HW05 — Task 1 & Task 2 |
| Assignment Title: | Performance Testing (Load / Stress / Spike) + AI Analysis & Misinterpretation Hunt on EShopSut |
| AI Use Category (1–5): | Category |
| Date: | 15/08/2026 |
| Student name: | Dang Truong Nguyen |
| Student ID: | 23127438 |

## 2. Disclosure Questions

### 1. AI tool(s) used:

- Claude Code (Claude Opus 4.8)

### 2. Stage(s) of the assignment where AI was used:

Tick all that apply: [x] brainstorming  [x] outlining  [x] drafting  [x] feedback  [ ] revision  [x] coding  [x] data analysis  [ ] visual design  [ ] other (specify).

AI was used to design the "Category-guided buy" end-to-end workflow, generate the four JMeter test plans (Load/Stress/Spike/Soak) via a script, build the data-driven CSV and user pool, write the resource-monitor and `.jtl`-analysis scripts, and draft the evidence documents (Task 1); and — for Task 2 — to analyse the results, propose performance thresholds, and suggest SUT optimizations. I chose the final load parameters, corrected the AI's mistakes (search keyword, lockout behaviour, timer placement, listener choice, assertions), executed all four scenarios on my own hardware, and wrote the human-review reasoning and AI Critique myself. For Task 2, the AI-misinterpretation hunt (8 corrections against the raw `.jtl`) and the feasible/hallucinated judgment on each optimization are entirely my own.

### 3. Main prompts or tasks given to the AI:

Paste the 2–3 most impactful prompts verbatim. For the full transcript, attach Appendix A (prompt_log.md).

Following the AI-first strategy, I did NOT use a single generic prompt. I decomposed the work into nine focused, verifiable prompts — P1–P7 for Task 1, P8–P9 for Task 2; all nine are pasted verbatim in the AI Audit Report (Section 3). The three most impactful:

1. **P1 — plan the assigned work (verbatim)**

   "đọc đề và README, phần việc của t là Đặng Trường Nguyên 23127438, viết 1 plan.md để mô tả các bước t cần làm gì"
   (Translation: read the assignment PDF and README; my part is Dang Truong Nguyen 23127438; write a plan.md describing the steps I need to do.)

2. **P4 — generate the four JMeter plans (verbatim)**

   "Write a Python generator that emits four JMeter 5.6 plans for this workflow: Load (20 VU, 60s ramp, 5 min, realistic think-time), Stress (step 50→100→200 VU over 7 min), Spike (10 VU baseline + 150 VU burst at t=90s), Soak (30 VU, 12 min). Each plan: recycling CSV Data Set, HTTP defaults localhost:3000, Bearer header from a JSON-extracted token, a CONTENT assertion per request (not status-only), and a DIFFERENT listener per plan (Summary / Aggregate / View Results Tree). Name them {StudentID}_{Scenario}_20260815.jmx."

3. **P5 — probe lockout + safe reset (verbatim)**

   "On a throwaway user, probe the REAL lockout behaviour (how many wrong logins trigger it, and for how long) and document a reset I can run between Stress/Spike runs WITHOUT restarting the server — check database.js first to confirm whether a restart would wipe the seeded data."

   The remaining prompts (P2 confirm payloads from source, P3 private user pool + data-driven CSV, P6 run + monitor, P7 analyse the raw `.jtl`) are in the AI Audit Report Section 3.

### 4. Specific parts of the work AI contributed to:

Be specific. Example: 'AI generated TC01–TC15 in Section 3.2; I rewrote TC04 and TC11; AI did NOT contribute to Sections 1, 2, 4, or the AI Critique.'

Claude Code generated `plan.md`, the four `.jmx` test plans (through `gen_jmx.py`), the 60-row `nguyen_users.csv` plus the registered user pool, the `monitor.sh` and `analyze_jtl.py` scripts, and the draft evidence docs (`test_design.md`, `bug_report.md`, `results_summary.md`, `lockout_probe.md`, `hardware_report.md`). I decided the final workflow scope (#3, no overlap with teammates) and load parameters, corrected six classes of AI error (empty-result keyword, spec-vs-real lockout, destructive DB reset, JMeter timer order, listener memory cost, status-only assertions), executed all four scenarios myself, and wrote the AI Audit conclusion and this disclosure form. AI did NOT produce the raw `.jtl` logs, the resource-monitor screenshots, the hardware report values, the demo video, or the AI Critique.

### 5. How I reviewed, revised, or verified the AI output:

Describe your verification method (ran the test, checked the spec, asked the TA, looked up RFC, cross-checked with the ISTQB syllabus, etc.).

- I read the SUT backend source (`server.js`, `database.js`) and confirmed every request payload and response field with curl smoke tests before trusting the generated plans — this is how I caught the `Laptop` keyword returning `[]`, the `+2`/180s lockout (vs the spec's ≥3/30s), and the HTTP-200-empty response for a missing product id.
- I validated every generated `.jmx` as well-formed XML and inspected each thread group, listener, and assertion; I ran a full end-to-end smoke test (login → categories → search → cart → checkout, orderId returned) before the load runs.
- I executed all four scenarios myself on my own hardware (Apple M4, macOS 15.5) with JMeter 5.6.3 non-GUI, kept the raw `.jtl` logs and HTML dashboards, and logged the backend process CPU/RSS every 5s.
- I re-computed p95/p99 directly from the raw `.jtl` with my own `analyze_jtl.py` (independent of JMeter's dashboard) to obtain a trusted ground truth, and reset the lockout with SQL between Stress/Spike runs rather than restarting the server (which would wipe the DB).

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
| Date: | 15/08/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
