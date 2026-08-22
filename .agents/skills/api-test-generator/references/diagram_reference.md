# Diagram Reference (for YOU to hand-draw — do not submit this file as-is)

The assignment's anti-cheat constraints explicitly require the Section 7
diagram to be **self-drawn, designed by you, not generated directly by an
AI**. This file only describes the boxes/arrows/labels so you can redraw
them yourself in draw.io, PowerPoint, Excalidraw, or on paper + photo.

## Boxes (in order, top to bottom)

1. **Input**: `API specification (api_specification.md)`
2. **Parser** (deterministic): `parse_spec.py` → `endpoint_model.json`
   (fields: method, path, params, auth/role, example responses, SEC refs,
   state hints)
3. **Four parallel generation stages** (draw as four boxes side by side,
   all fed by the endpoint model, all feeding into one "draft test cases"
   box):
   - Stage A: Domain Partition & Boundary
   - Stage B: State Transition
   - Stage C: Security (SEC-01–SEC-07)
   - Stage D: Schema Validation
4. **Draft test cases (JSON)** — the box all four stages converge into
5. **Audit loop** (draw as a box with a small loop-back arrow to itself,
   or a decision diamond): `AI drafts label -> human confirms/overrides ->
   corrected case`. Labels: VALID / INVALID / INCOMPLETE
6. **Extension** box: `Human + AI gap-hunting (>=5 cases)`, feeding into
   the same test case set
7. **Export** — draw as three output boxes fed by the final test case set:
   - `test_cases.xlsx` (Excel + summary)
   - `collection.json` (Postman v2.1, with pre-request script injecting
     `X-Student-Id`)
   - `ai_audit_log.md` (one entry per stage)
8. Optional final box: `Newman execution -> HTML report` (outside this
   skill's scope — dashed border/arrow to show it's a downstream, separate
   step you run manually against the live SUT)

## Arrows

- Spec → Parser → Endpoint model
- Endpoint model → each of the 4 stage boxes (fan-out)
- Each stage box → Draft test cases (fan-in)
- Draft test cases → Audit loop → (back into) test case set
- Test case set + gap-hunting prompts → Extension → (back into) test case set
- Final test case set → the 3 export boxes (fan-out)
- Postman export → (dashed) → Newman execution → HTML report

## Suggested layout

A simple top-to-bottom flow with the 4 stages drawn as a horizontal row in
the middle (fan-out/fan-in) reads clearly and matches how the pipeline
actually executes. Keep the "self-drawn" requirement in mind — hand
imperfection is fine and expected; the TAs are checking that you understand
the structure, not evaluating your draftsmanship.
