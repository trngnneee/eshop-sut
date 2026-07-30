# Usability Evaluation Workflow (Task 2 detail)

7 real participants, one moderated session each, single end-to-end flow. Claude's role is **prep + structuring + analysis**, never fabricating human data.

## Phase 1 — Plan & prepare

1. **Objectives.** Ask the user what they want to learn (e.g., "where do users hit navigation friction in the sign-up → cart → checkout flow", "how confident do users feel completing checkout with a coupon"). Write 2-4 concrete objectives.

2. **Task scenario.** Convert the chosen flow into ONE goal-oriented scenario. Bad: "Click Sign Up, fill in the form, click Submit, then go to Products…" (step-by-step — not allowed). Good: "You want a winter coat for under 500,000₫. Find one you like and complete your purchase using any discount coupon you can find." Draft 2-3 candidate scenario phrasings, let the user pick/edit.

3. **Instruments.**
   - **SUS** (10 items, 5-point Likert, alternating positive/negative wording) — standard, fast, produces a single 0-100 score. See `scripts/score_sus.py` for scoring.
   - **UEQ-S** (8 bipolar item pairs, pragmatic vs. hedonic quality) — use if the user cares about hedonic/emotional quality, not just efficiency.
   - Or a custom scale — only if the user gives a clear written justification for why SUS/UEQ-S don't fit.
   - **Probe questions** (open-ended, asked after the scale): must cover at minimum clarity, error recovery, speed, trust. Example bank (adapt to the scenario, don't just copy verbatim):
     - Clarity: "At any point were you unsure what to do next? Where?"
     - Error recovery: "Did you make any mistakes or take a wrong turn? How did you recover?"
     - Speed: "Did the process feel faster or slower than you expected? Why?"
     - Trust: "Was there any point where you hesitated to proceed, e.g., before entering payment info? What caused that?"

4. **Participants.** Claude does NOT generate or invent this list. Remind the user: 7 real people, outside the class, verifiable contact (Zalo/email/phone with middle 4 digits masked), non-IT preferred. Use `assets/participant_list_template.csv` purely as a fill-in-the-blanks structure.

5. **Pilot session.** Remind the user to run one pilot session first and note anything that needs fixing (unclear scenario wording, broken flow step, timing) before the real 7 sessions.

## Phase 2 — Conduct (human-run)

Provide the user a short **moderator script** to keep all 7 sessions consistent:
1. Stage-setting line: "We're testing the product, not you — there are no wrong answers. Please think out loud as you go."
2. Present the task scenario (read verbatim, don't add hints).
3. Observe neutrally — no leading hints, no explaining the UI; step in only if truly stuck.
4. After task completion/abandonment: administer SUS/UEQ-S, then ask the probe questions.

After each session, help the user transcribe raw notes into `assets/usability_session_notes_template.md`: friction points, errors, hesitations, verbalized frustration, timestamps if recorded. Claude organizes/tags what the user reports observing — it must not add observations the user didn't report.

## Phase 3 — Analyse & report

1. **Score.** Once the user has all 7 raw SUS (or UEQ-S) responses, run `scripts/score_sus.py` to get per-participant scores + the average + a benchmark interpretation (SUS: >68 is above average, 90+ excellent, <50 poor — standard published benchmarks).
2. **Synthesize.** Group similar pain points across the 7 sessions into themes. Separate one-off bugs (something objectively broken) from systemic design issues (something that works but confuses users). Claude proposes clusters from the notes provided; user confirms.
3. **Prioritize by severity**: Blocker (prevents task completion) > Major (causes significant friction/errors but recoverable) > Minor (cosmetic/annoyance only).
4. **Bug report.** For genuine bugs (not design opinions) found during sessions, draft entries with `assets/bug_report_template.md`, ready for the Markdown report and GitHub Issues. Screenshot attachment is the user's job.

## Reminders to give the user
- The TA may randomly call 2 participants to verify — never help fabricate a plausible-sounding fake participant or transcript.
- Keep a copy of raw session notes/recordings as evidence for the submission zip.