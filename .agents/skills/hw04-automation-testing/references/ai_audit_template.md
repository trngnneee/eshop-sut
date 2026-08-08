# AI Audit Report — HW04 Automation Testing

> If you did NOT use any AI in this exercise, delete everything below and write only:
> "I do not use any AI help in this exercise."
>
> Otherwise, keep the declaration line exactly as required, then log every interaction.

I use AI tools for the following tasks:

## Interaction Log

Append one entry per interaction, in chronological order, immediately after it happens.
Don't batch these at the end — you will forget details and it will show.

### Entry template

```
### [N] <short label, e.g. "FR-08 Checkout — page object scaffold">
- **Tool:** Claude / ChatGPT / Gemini / Copilot / Cursor (name the actual tool)
- **Date/time:** YYYY-MM-DD HH:MM (local time)
- **Prompt:**
  > exact prompt text used
- **Output:**
  Summary of what the AI produced (paste short outputs verbatim; for long code,
  summarize + link to the commit/diff instead of pasting hundreds of lines).
- **Accepted as-is / Modified:** state which, and if modified, one line on what changed
  and why (this feeds directly into the Task 1 "review and fix" write-up).
```

### Example entry

```
### [1] FR-08 Checkout — locator scaffold
- Tool: Claude (claude.ai)
- Date/time: 2026-08-08 14:20
- Prompt:
  > "Here is the checkout page DOM (pasted). Generate Playwright locators for the
  > shipping-address form, payment-method selector, and 'Place Order' button. Use
  > role-based or data-testid locators, not text matches."
- Output:
  Provided a `CheckoutPage` class with 6 locators, all role/data-testid based except
  one text-based locator for the "Place Order" button.
- Modified: swapped the text-based "Place Order" locator for
  `page.getByTestId('place-order-btn')` because the button text is
  locale-dependent (Vietnamese UI) and would break under localization.
```

## Tool declaration summary

| Tool | Used for | # of interactions |
|---|---|---|
| e.g. Claude | Test case design, script generation, review notes | e.g. 14 |

Fill this table in after logging is complete — it should match the interaction count
above exactly (a mismatch is an easy thing for a TA to catch).