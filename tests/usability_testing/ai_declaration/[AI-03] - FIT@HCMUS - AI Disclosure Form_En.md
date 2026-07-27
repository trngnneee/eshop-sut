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
| Assignment ID: | HW03 — Task 2 |
| Assignment Title: | Usability Evaluation on EShopSut |
| AI Use Category (1–5): | Category |
| Date: | 27/07/2026 |
| Student name: | Dang Truong Nguyen |
| Student ID: | 23127438 |

## 2. Disclosure Questions

### 1. AI tool(s) used:

- Claude Code (Claude Fable 5)

### 2. Stage(s) of the assignment where AI was used:

Tick all that apply: [x] brainstorming  [x] outlining  [x] drafting  [x] feedback  [x] revision  [x] coding  [x] data analysis  [ ] visual design  [ ] other (specify).

AI drafted the study instruments (research-objective candidates, task scenario, Vietnamese SUS form, probe questions, session kit), wrote the SUS scoring script (`sus_score.py`), produced the findings-synthesis draft, and formatted/posted the GitHub issue comments. I recruited the 7 participants, moderated every session, and recorded all observation notes and SUS responses myself without AI; I selected the final research objectives, corrected the AI's aggregate counts against the raw notes, and made all severity decisions.

### 3. Main prompts or tasks given to the AI:

Paste the 2–3 most impactful prompts verbatim. For the full transcript, attach Appendix A (prompt_log.md).

The full prompt set (Prompt #1–#6) is in `plan/PLAN-TASK2.md` and pasted verbatim in the AI Audit Report (Section 3). The 3 most impactful:

1. **Prompt #2 — task scenario**

   ROLE: You are a UX researcher writing a task scenario for a moderated usability session, in Vietnamese. CONTEXT: EShop; flow Register → search → detail → add to cart (≥ 300,000₫) → checkout with coupon SAVE10 → confirm in order history; real seeded products pasted in. TASK: write ONE 5–8-sentence scenario that gives a realistic GOAL and motivation, NOT instructions; naturally forces every step; NEVER names any UI element (forbidden words: nút, menu, biểu tượng, trang, tab, click, nhấn vào); states what "done" means from the USER's point of view. Then output a moderator-only mapping table: scenario element → flow step it triggers.

2. **Prompt #6 — findings synthesis**

   ROLE: You are helping a researcher synthesise moderated usability findings. You must not invent observations. INPUT: my typed raw notes from 7 sessions + SUS scores. TASK: (1) extract every friction event with its trace (participant, step, what happened, quote) — ambiguous notes go to an "AMBIGUOUS — researcher must recheck recording" list instead of being interpreted; (2) affinity-group into themes with DISTINCT-participant counts (x/7) and a bug-vs-design suggestion marked "candidate — needs researcher confirmation"; (3) propose severity (Blocker/Major/Minor/Cosmetic) justified by participant count and outcome, not adjectives; (4) answer each research objective in 1–2 sentences based ONLY on the data.

3. **Prompt #5 — SUS scoring script**

   TASK: Write a small self-contained Python script `sus_score.py` that reads `sus_responses.csv` (columns participant,q1..q10, values 1–5); validates every value and fails loudly on any invalid/missing value (no silent skip); computes each participant's SUS with the standard formula (odd items score−1, even items 5−score, sum × 2.5); prints per-participant scores, mean, median, min–max and the Bangor et al. adjective band; standard library only.

### 4. Specific parts of the work AI contributed to:

Be specific. Example: 'AI generated TC01–TC15 in Section 3.2; I rewrote TC04 and TC11; AI did NOT contribute to Sections 1, 2, 4, or the AI Critique.'

Claude Code generated the objective candidates (O1–O6), `task-scenario-draft.md`, the three instrument files under `template/` (SUS-vi, probe questions, session kit), `result/sus_score.py` + the CSV transcription, the `findings.md` synthesis draft, and the 7 GitHub evidence comments (+ severity edits on #204/#240, which I decided). I chose the 3 final objectives with written rationale, verified the scenario contains no UI-leading words, verified the SUS translation item-by-item, and corrected 3 aggregate counts in the synthesis after re-checking the raw notes. AI did NOT contribute to: the participant list (`participants.md` — compiled manually, contacts masked), the 7 session observation notes, the SUS responses, or the AI Critique.

### 5. How I reviewed, revised, or verified the AI output:

Describe your verification method (ran the test, checked the spec, asked the TA, looked up RFC, cross-checked with the ISTQB syllabus, etc.).

- For the findings synthesis, I re-derived every x/7 count line-by-line from the raw `session-P*.md` notes — this caught 3 miscounts in the AI draft, which I corrected before accepting. The SUS script's output was cross-checked against my hand-scored paper forms (7/7 match). Both severity re-triages on GitHub (#204 → Blocker, #240 → Major) were my decisions, made in `findings.md` before the AI executed them, and I verified the public comments contain participant codes only (P1–P7), no personal data.
- For the instruments, I verified the SUS translation item-by-item against the Brooke originals (positive/negative polarity preserved) and checked the task scenario for UI-leading words before running the sessions.

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
| Date: | 27/07/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
