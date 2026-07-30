# GUI Checklist Workflow (Task 1 detail)

Target: **> 40 items**, covering all four interface aspects (IA-01..IA-04), each item eventually marked Passed/Failed with Notes.

## Step-by-step (do NOT skip steps or merge them into one prompt)

### Step 1 — Scope
Ask the user which screen(s) they're checking (Home, Cart, Checkout, Admin Dashboard, a Mobile screen, etc.). Confirm the choice is written down before generating anything — the checklist should reference the actual screen, not be generic.

### Step 2 — Generate items per IA, one pass per aspect
Run four separate generation passes. For each pass, the prompt Claude uses internally should reference the *specific screen* and *specific aspect*, e.g.:

> "For the [Checkout] screen of an e-commerce app, list 10-15 GUI checklist items specific to IA-02 Forms: field validation, labels, error messages, input types, required-field marking, autofill, tab order. Be concrete to this screen, not generic."

Aspect scopes to use as a baseline (expand per screen):

- **IA-01 General UI standards**: visual consistency (spacing, alignment, color contrast), typography hierarchy, responsive layout/breakpoints, icon consistency, button states (hover/active/disabled), loading indicators, image alt text/broken-image handling.
- **IA-02 Forms**: label/placeholder correctness, inline validation, error message clarity and placement, required-field indication, input masking/formatting, autofill behavior, tab order, submit-button disabled state until valid.
- **IA-03 Navigation**: breadcrumb correctness, back-button behavior, active-state indication in menus, deep-link correctness, 404/empty-route handling, consistent placement of nav elements across pages, mobile hamburger behavior.
- **IA-04 Feedback / state**: success/error toasts, empty-state messaging, loading skeletons/spinners, optimistic UI vs. real state, session-timeout handling, confirmation dialogs for destructive actions, undo affordances.

Log each of the four passes via `scripts/log_ai_interaction.py`.

### Step 3 — Human review pass
Present the combined list back to the user item by item (or in batches per IA). Ask them to mark each as Keep / Edit / Reject. Apply their edits. This satisfies "Human review" in §2 — Claude must not silently keep AI items the user rejected.

### Step 4 — Gap-finding pass (critical, explicitly graded)
Ask Claude to critique its own list against categories AI commonly misses:
- Accessibility (screen-reader labels, focus order, ARIA roles, color-contrast ratios, keyboard-only operability)
- RTL layout readiness (even if the SUT is LTR-only, note whether layout would break)
- Dark mode / theme switching
- Localization/i18n (text truncation in Vietnamese vs. English, date/currency formats)
- Low-connectivity / slow-network states
- Edge-case empty states (zero search results, empty cart, empty order history)

For each gap item actually added, Claude must write a one-line reason **why the earlier generation pass missed it**. Plausible reasons (pick the one that actually applies, don't default to the same one every time):
- The initial prompt didn't mention the category, so the model had no signal to include it.
- The model tends to default to "happy path" / visible-desktop-Chrome assumptions unless explicitly asked about accessibility or edge devices.
- The category depends on inspecting rendered DOM/CSS (e.g., real contrast ratios, actual focus order) which a text-only description can't determine — it needed a live look at the screen.
- The screen's specific business logic (e.g., a Vietnamese-only marketplace) made a general checklist template not directly applicable without adaptation.

### Step 5 — Count and coverage check
Count items per IA. If any IA has fewer than ~10 items or total is ≤ 40, run a targeted follow-up generation pass for that IA only. Log it.

### Step 6 — Execution
This is manual QA by the user against the live SUT. Claude's job is to help structure results, not invent them:
- Ask the user, item by item or in batches, what they observed (Pass/Fail).
- For each Fail, ask for the specific reason (what happened vs. expected) to fill the Notes column.
- Remind them to capture a screenshot for every Failed item (not Passed ones).

### Step 7 — Bug report drafting
For every Failed item, draft an entry using `assets/bug_report_template.md`: title, screen, steps to reproduce, expected result, actual result, severity, screenshot placeholder. Output both as (a) rows for the Markdown report and (b) a ready-to-paste GitHub Issue body. Remind the user to actually attach the screenshot file when they create the GitHub issue — Claude cannot do that upload for them.

## Output format
`checklist.csv`