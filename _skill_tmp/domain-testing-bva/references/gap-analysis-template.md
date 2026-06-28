# AI Gap Analysis Template

Use this template in your report after reviewing all AI-generated test cases.
The gap analysis is **mandatory** per HW02 requirements (Section 6.3).

---

## Section: AI Gap Analysis — <Feature ID> <Feature Name>

### Summary

| Metric | Count |
|--------|-------|
| Total test cases AI generated | |
| Test cases you added manually | |
| Test cases AI got wrong (corrected) | |
| Bugs AI failed to anticipate | |

---

### Missed Test Cases

For each test case the AI did not generate but you added:

#### GAP-<FR>-<seq>: <Short Description>

| Field | Value |
|-------|-------|
| TC ID added | TC-FRxx-DT-015 |
| Class / Point | EC-07 (whitespace-only input) / OFF lower boundary |
| Why AI missed it | *(choose one or more)* |

**Root cause options:**
- **Prompt quality**: The prompt did not mention this constraint explicitly
  (e.g., did not say "also consider whitespace-only inputs")
- **AI limitation**: The model tends to skip security-related or
  edge-case classes unless explicitly prompted
- **Feature complexity**: The interaction between two fields (e.g.,
  confirm_password ≠ password when both are non-empty) requires
  cross-field reasoning the AI did not apply
- **Specification gap**: The SUT's documentation does not mention this
  constraint, so neither the AI nor a human reading the spec alone would
  catch it

---

### Incorrect AI Outputs

For each test case the AI generated with a wrong expected result:

#### ERR-<FR>-<seq>: <Short Description>

**AI's version:**
```
TC-FRxx-DT-008 | Empty phone field | phone="" | Expected: Error "Phone required"
```

**Corrected version:**
```
TC-FRxx-DT-008 | Empty phone field | phone="" | Expected: Account created
               | (phone is optional per spec)
```

**Root cause:** The AI incorrectly assumed phone was required. This is a
hallucination / incorrect assumption because the spec was ambiguous and the
AI defaulted to treating all fields as required.

---

### Reflection Paragraph (include in AI Critique)

Use these prompts to write your 200–300 word AI Critique (Section 10):

1. **What did the AI get wrong?**
   - Wrong expected results (hallucinated constraints)?
   - Missing edge/boundary cases?
   - Incorrect TC IDs or duplicate IDs?

2. **Why did it fail?**
   - Insufficient context in the prompt?
   - The AI's general tendency to over- or under-generate?
   - Feature complexity that requires reading source code?

3. **What principle did you learn?**
   - "The AI is a fast first-drafter but a poor final reviewer."
   - "Prompting step-by-step (EP first, then BVA separately) gives better
     results than asking for everything at once."
   - "AI misses cross-field constraints unless the prompt explicitly names them."
