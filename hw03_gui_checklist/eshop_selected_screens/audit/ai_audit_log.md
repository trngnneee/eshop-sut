# AI Audit Report

**Declaration:** I use AI tools for the following tasks: GUI checklist drafting, GUI checklist gap review, and AI audit logging for Task 1.

(If no AI was used for a particular deliverable, state explicitly: "I do not use any AI help in this exercise for <deliverable>.")

**Tools used:** Codex (GPT-5, this session)

---

<!-- Entries appended below by scripts/log_ai_interaction.py â€” do not hand-edit the numbering, but DO fill in "Human Review Notes" for each entry. -->
### Interaction #1
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-01 General UI standards, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web, and Product Detail Mobile of EShop, generate concrete GUI checklist items for IA-01 General UI standards: visual consistency, typography, image handling, money formatting, responsive layout, and Vietnamese UI standards. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia01_output_excerpt.md)

```
# IA-01 General UI standards output excerpt

Generated checklist items for visual consistency, layout, typography, image handling, money formatting, responsive behavior, and Vietnamese UI standards across Product Detail Web, Cart Web, Product Management Admin Web, and Product Detail Mobile.

Rows in checklist.csv: GUI-001 to GUI-016, plus gap-review rows GUI-057, GUI-058, GUI-061.

```
- **Human Review Notes:** Pending human review by student: mark each row Keep/Edit/Reject before execution.

### Interaction #2
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-02 Forms, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web, and Product Detail Mobile of EShop, generate concrete GUI checklist items for IA-02 Forms: quantity validation, product CRUD form validation, required markers, CSV import input handling, labels, tab order, and mobile touch/input behavior. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia02_output_excerpt.md)

```
# IA-02 Forms output excerpt

Generated checklist items for quantity inputs, admin product form validation, required markers, CSV import input handling, mobile numeric input behavior, tab order, and touch targets.

Rows in checklist.csv: GUI-017 to GUI-032, plus gap-review row GUI-059.

```
- **Human Review Notes:** Pending human review by student: mark each row Keep/Edit/Reject before execution.

### Interaction #3
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-03 Navigation, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web, and Product Detail Mobile of EShop, generate concrete GUI checklist items for IA-03 Navigation: breadcrumb, navbar/cart badge, checkout redirect, admin sidebar active state, logout, access control navigation, and mobile home/back/cart routes. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia03_output_excerpt.md)

```
# IA-03 Navigation output excerpt

Generated checklist items for breadcrumb behavior, navbar/cart badge, checkout redirect when unauthenticated, admin sidebar active state, admin logout, access control navigation, and mobile back/home/cart routes.

Rows in checklist.csv: GUI-033 to GUI-044, plus gap-review row GUI-060.

```
- **Human Review Notes:** Pending human review by student: mark each row Keep/Edit/Reject before execution.

### Interaction #4
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-04 Feedback/state, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web, and Product Detail Mobile of EShop, generate concrete GUI checklist items for IA-04 Feedback/state: loading, empty/error states, add-to-cart feedback, invalid quantity feedback, delete confirmation, cart total updates, admin save/import feedback, and mobile network failure states. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia04_output_excerpt.md)

```
# IA-04 Feedback and state output excerpt

Generated checklist items for loading states, product-not-found states, add-to-cart feedback, invalid quantity feedback, cart empty state, delete confirmation, total/badge updates, admin save/import feedback, and mobile network/API failure states.

Rows in checklist.csv: GUI-045 to GUI-056, plus gap-review row GUI-062.

```
- **Human Review Notes:** Pending human review by student: mark each row Keep/Edit/Reject before execution.

### Interaction #5
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist gap review - selected EShop screens
- **Prompt:**
  > Critique the generated GUI checklist for commonly missed categories: accessibility/screen reader labels, keyboard-only navigation, contrast, encoding/localization, long text, and slow-network/error states. Add only applicable gap items and explain why the initial generation likely missed each one.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\gap_output_excerpt.md)

```
# Gap review output excerpt

Generated six additional AI-gap-review checklist items covering encoding, contrast, screen reader labels, keyboard-only navigation, long text/localization risk, and mobile slow-network/error recovery.

Full explanation is in checklist/gap_review.md.

```
- **Human Review Notes:** Pending human review by student: accept, edit, or reject each AI-gap-review item and keep the reason if retained.