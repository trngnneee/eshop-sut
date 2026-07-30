---
name: gui-usability-testing
description: Guides a disciplined, step-by-step GUI checklist design/execution and a moderated usability evaluation (SUS or UEQ-S) for a web or mobile screen/flow, exactly as required by HW03 GUI & Usability. Every AI interaction performed while using this skill (checklist generation, item review, bug-report drafting, session-notes synthesis, etc.) is automatically logged to an AI Audit Report so the mandatory declaration in the assignment is produced with zero manual bookkeeping. Trigger this skill whenever the user mentions GUI checklist, usability testing or evaluation, SUS, UEQ-S, usability session, cross-browser/cross-platform testing prep, bug report for a screen, or HW03 / EShop / interface aspects IA-01 through IA-04 — even if they only ask for one sub-step (e.g. "generate a checklist for the Checkout page" or "help me write probe questions"), since that sub-step is part of this larger workflow and must still be logged. Reusable across any screen or end-to-end flow, not just the one used in the first run.
---

# GUI & Usability Testing Skill

This skill turns Claude into a **disciplined assistant, not a black box**, for two testing techniques:
1. **GUI Checklist** design + execution (Task 1)
2. **Moderated Usability Evaluation** with SUS/UEQ-S (Task 2)

...and produces the **AI Audit Report** (§9) and the raw material for the **AI Critique** (§10) as a side effect of normal use, so nothing has to be reconstructed after the fact.

**Core rule for Claude: never issue one generic prompt to itself and call it done.** Each task below is broken into small, guided sub-steps. Do them one at a time, show the user the intermediate result, and let them correct it before moving to the next sub-step. Every one of these sub-steps counts as a loggable "AI interaction" — see **AI Audit Logging** below, which is not optional.

## 0. Setup — one project per screen/flow

This skill is reusable: the user may run it multiple times for different screens or different flows. At the start of a session, ask (if not already clear from context):
- Is this a **new** screen/flow, or continuing an existing one?
- What is the target: a **screen** (for the GUI checklist) or an **end-to-end flow** (for the usability evaluation)?
- A short slug for it, e.g. `checkout`, `admin-dashboard`, `signup-to-checkout`.

Then initialize a working folder for that target using the skill's own directory (wherever it's installed, e.g. `/mnt/skills/.../gui-usability-testing/` or a user-uploaded copy):

```bash
bash <skill_dir>/scripts/init_project.sh <slug> <output_dir>
```

(If the script isn't reachable, just create the folder structure by hand: `<output_dir>/<slug>/{checklist,usability,bugs,audit,screenshots}` and copy the templates from `assets/` into it.)

Copy the templates from `assets/` into the new project folder as a starting point (`checklist_template.csv`, `bug_report_template.md`, `usability_session_notes_template.md`, `participant_list_template.csv`, `ai_audit_log_template.md`).

Every AI-assisted step from here on writes into `<output_dir>/<slug>/audit/ai_audit_log.md` — see below.

## 1. AI Audit Logging (mandatory, do this throughout — not just at the end)

Read `references/ai_audit_logging.md` for the exact log format required by §9 of the assignment. In short: **every time Claude produces AI output that ends up in the deliverable** (a checklist draft, a set of probe questions, a synthesized bug list, session-notes clustering, etc.), append one entry to `ai_audit_log.md` with:
- Tool name (Claude, and the model if known)
- Date and time
- The exact prompt/instruction that produced the output (this is effectively the message the user sent, or the sub-step instruction Claude used internally — log both if they differ)
- The AI output (or a pointer to the file it was written to, if long)

Use `scripts/log_ai_interaction.py` to append entries programmatically so the format stays consistent — don't hand-roll the Markdown each time:

```bash
python3 scripts/log_ai_interaction.py \
  --log <output_dir>/<slug>/audit/ai_audit_log.md \
  --tool "Claude (this session)" \
  --prompt "Generate 15 GUI checklist items for IA-02 Forms on the Checkout page" \
  --output-file <path to the file containing the raw output>
```

Tell the user plainly, once, near the start: *"I'll log every AI-assisted step to the audit report automatically as we go — you don't need to copy-paste anything."* Do not narrate every single log-append after that; just do it.

At the end of the whole assignment, remind the user to fill in the **declaration line** (§9): if they used AI tools outside this skill too (e.g. a separate ChatGPT session), those need manual entries in the same log — the skill only captures what happened inside this conversation.

## 2. Task 1 — GUI Checklist

Follow `references/gui_checklist_workflow.md` step by step. Do **not** collapse this into a single "generate a GUI checklist" prompt — the assignment explicitly forbids that. The workflow is:

1. **Scope the screen(s)** with the user (which screen(s), why, confirm no duplication with groupmates if relevant).
2. **Generate items per interface aspect, one aspect at a time** (IA-01 General UI standards, IA-02 Forms, IA-03 Navigation, IA-04 Feedback/state) — four separate guided passes, not one bulk call. Log each pass.
3. **Human review pass**: present the AI-generated items back to the user and explicitly ask them to accept/reject/edit each one.
4. **Gap-finding pass**: prompt Claude to critique its own checklist for commonly-missed categories (accessibility/ARIA, RTL layout, dark mode, keyboard-only navigation, localization, offline/slow-network states, empty states) — but treat this as a starting list of *categories to check*, not a final answer; ask the user which gaps genuinely apply to their screen. For every item added this way, write a one-line explanation of *why the AI missed it initially* (prompt ambiguity, model limitation, interface-specific nuance) — this is graded explicitly.
5. **Verify item count** — must be **more than 40** and cover all four IAs. If short, do another targeted generation pass for the thinnest IA.
6. **Execution pass**: help the user record Pass/Fail + Notes (reason for failure) per item as they manually test the SUT. Claude should not fabricate pass/fail results — these come from the user actually operating the SUT.
7. **Bug report pass**: for each Failed item, draft a bug-report entry (title, steps to reproduce, expected vs actual, severity) using `assets/bug_report_template.md`, ready to paste into a GitHub Issue. Remind the user to attach the failure screenshot to both the Markdown report and the GitHub issue.

Save the running checklist to `<output_dir>/<slug>/checklist/checklist.csv` (columns: ID, IA, Item, Source[AI/Human/AI-gap-review], Pass/Fail, Notes). Tell the user to open it in Excel/Sheets for final formatting — this skill produces the content, not final `.xlsx` polish (use the `xlsx` skill separately if they want a formatted spreadsheet).

## 3. Task 2 — Usability Evaluation

Follow `references/usability_evaluation_workflow.md`. Phases map directly to §6 Task 2 of the assignment:

**Phase 1 — Plan**
1. Draft **objectives** with the user (what do they want to learn about the flow).
2. Turn the chosen end-to-end flow into a **goal-oriented task scenario** (never step-by-step instructions) — Claude proposes a draft, user edits.
3. Choose **SUS or UEQ-S** (or help justify a custom scale) and draft **probe questions** covering at minimum: clarity, error recovery, speed, trust. Use `assets/usability_session_notes_template.md`.
4. Remind the user participant recruiting and pilot session are **their responsibility** — Claude must never fabricate participant identities or contact details (see Anti-AI-Cheat note below).

**Phase 2 — Conduct** (human-run; Claude's role is prep and note-structuring)
- Provide a short moderator script/checklist (stage-setting line, think-aloud reminder, neutral-observation reminders) so sessions are consistent across all 7 participants.
- After each session, help the user structure raw notes into `usability_session_notes_template.md` (friction points, errors, hesitations, quotes) — Claude organizes what the user observed, it does not invent observations.

**Phase 3 — Analyse**
1. **Score** SUS/UEQ-S once the user supplies the 7 raw responses — use `scripts/score_sus.py` for SUS (0-100 per participant + average) or point to the standard UEQ-S data-analysis spreadsheet if they chose UEQ-S.
2. **Synthesize**: cluster the 7 sets of notes into pain-point themes, separating one-off bugs from systemic design issues. Claude proposes clusters; user confirms/edits.
3. **Prioritize by severity** (Blocker / Major / Minor) with a short rationale per item.
4. Draft bug entries for genuine bugs found during sessions, same template as Task 1, ready for GitHub Issues.

**Critical constraint — do not fabricate human data.** Claude must never invent participant names/contacts, session transcripts, SUS scores, or quotes. If the user asks Claude to "just make up 7 participants" or similar, refuse that specific request, explain why (§11 Anti-AI-Cheat Constraints — this is checked by TAs, including random participant calls), and offer to help with everything else (scenario design, instrument design, note structuring, analysis) once real data is available.

## 4. AI Critique material (§10)

Throughout the session, keep a short running note (in `audit/ai_critique_notes.md`) whenever Claude's output was wrong, incomplete, or needed real correction by the user — e.g. an IA category the AI's checklist pass missed, a leading probe question Claude drafted that had to be reworded, a bug severity Claude mis-rated. At the end, offer to turn these notes into a 200–300 word draft critique paragraph per §10 (where AI erred, why, and the lesson learned) — the user should personalize and finalize it, not submit it verbatim.

## 5. What this skill does NOT do

- Does not run BrowserStack/LambdaTest or take cross-platform screenshots (Task 3) — that requires real tools/devices per §6.
- Does not recruit or contact participants, run sessions, or verify identities.
- Does not fabricate Pass/Fail results, bug repros, screenshots, or survey data — all of that must come from the user actually operating the SUT and running real sessions.
- Does not replace the human review the assignment requires (§2 "Human review") — always present AI output as a draft for the user to correct.

## 6. Reference files

- `references/gui_checklist_workflow.md` — detailed IA-01..04 guidance, example items, common AI blind spots.
- `references/usability_evaluation_workflow.md` — SUS/UEQ-S detail, probe question bank, severity rubric.
- `references/ai_audit_logging.md` — exact log entry format for §9.
- `assets/checklist_template.csv`, `assets/bug_report_template.md`, `assets/usability_session_notes_template.md`, `assets/participant_list_template.csv`, `assets/ai_audit_log_template.md`