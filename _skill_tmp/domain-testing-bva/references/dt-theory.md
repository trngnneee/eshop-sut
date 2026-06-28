# Domain Testing Theory Reference

## What is Domain Testing?

Domain Testing (DT) is a black-box test design technique that divides the
**input space** of a program into **domains** (equivalence classes) such
that all values in a class are expected to trigger the same program behaviour.
Testing one representative from each class is sufficient to expose any
defect that the class would reveal.

It combines two sub-techniques:
1. **Equivalence Partitioning (EP)** — divides inputs into valid and invalid
   classes.
2. **Boundary Value Analysis (BVA)** — targets the edges of each class where
   defects cluster.

---

## Equivalence Partitioning (EP) — Full Theory

### Definitions

| Term | Definition |
|------|-----------|
| **Partition / class** | A set of input values expected to be processed identically |
| **Valid partition** | Values the system should accept and process correctly |
| **Invalid partition** | Values the system should reject (error / warning) |
| **Representative value** | The single concrete value chosen to stand for the class |

### How to Identify Classes

For each input variable, consider:

1. **Range constraints** (e.g., age 18–65)
   - Valid: [18, 65]
   - Invalid: < 18, > 65

2. **Set membership** (e.g., country ∈ {VN, US, SG})
   - Valid: any listed member
   - Invalid: any value not in the set

3. **Format / pattern** (e.g., email must match RFC 5322)
   - Valid: conforms to pattern
   - Invalid: missing @, multiple @, missing domain, etc.

4. **Required vs optional**
   - Valid: non-empty (required field)
   - Invalid: empty string, null, whitespace only

5. **Type** (e.g., must be integer)
   - Valid: integer
   - Invalid: float, string, special character

### Equivalence Class Table Template

```markdown
## EP Table — <Variable Name>

| Class ID | Description | Type | Representative Value |
|----------|-------------|------|---------------------|
| EC-01 | Typical valid value | Valid | alice@example.com |
| EC-02 | Valid minimum length | Valid | a@b.co |
| EC-03 | Valid maximum length | Valid | (254-char email) |
| EC-04 | Missing @ symbol | Invalid | aliceexample.com |
| EC-05 | Missing domain | Invalid | alice@ |
| EC-06 | Empty string | Invalid | "" |
| EC-07 | Whitespace only | Invalid | "   " |
| EC-08 | Already registered | Invalid | existing@user.com |
```

### Rules

- Classes must be **non-overlapping** (mutually exclusive)
- The union of all classes should cover the **entire input space**
  (collectively exhaustive) — or at least the meaningful portions
- **Do not** test more than one invalid class per test case unless you are
  specifically testing interaction effects; isolate one defect at a time

---

## Worked Example: FR-01 Account Registration

### Feature: User Registration Form
Fields: `email`, `password`, `confirm_password`, `full_name`, `phone`

### Step 1 — Input Variables

| # | Variable | Type | Known Constraints |
|---|----------|------|------------------|
| 1 | email | string | required, RFC 5322, ≤ 254 chars, unique in DB |
| 2 | password | string | required, 8–32 chars, ≥1 upper, ≥1 digit |
| 3 | confirm_password | string | required, must equal password |
| 4 | full_name | string | required, 2–100 chars, letters/spaces only |
| 5 | phone | string | optional, 10–11 digits, Vietnam format |

### Step 2 — Equivalence Classes (password)

| Class ID | Description | Type | Representative |
|----------|-------------|------|---------------|
| EC-PW-01 | Valid: 8–32 chars, 1 upper, 1 digit | Valid | `Abcdef1!` |
| EC-PW-02 | Too short: < 8 chars | Invalid | `Ab1!` |
| EC-PW-03 | Too long: > 32 chars | Invalid | `Abcdef1!` × 5 (40 chars) |
| EC-PW-04 | No uppercase | Invalid | `abcdef1!` |
| EC-PW-05 | No digit | Invalid | `Abcdefg!` |
| EC-PW-06 | Empty | Invalid | `""` |

### Step 3 — Test Cases (Domain Testing)

| TC ID | Description | Input | Expected |
|-------|-------------|-------|----------|
| TC-FR01-DT-001 | Valid registration, all typical | email=alice@example.com, pw=Abcdef1! | Account created, redirect to login |
| TC-FR01-DT-002 | Password too short | pw=Ab1! | Error: "Password must be at least 8 characters" |
| TC-FR01-DT-003 | Password no uppercase | pw=abcdef1! | Error: "Password must contain uppercase letter" |
| TC-FR01-DT-004 | Email missing @ | email=aliceexample.com | Error: "Invalid email format" |
| TC-FR01-DT-005 | Empty email | email="" | Error: "Email is required" |

---

## Common Pitfalls

1. **Forgetting the empty/null class** — Always add EC for empty string on
   required fields.
2. **Overlapping classes** — "< 8" and "exactly 7" are the same class.
3. **Using abstract values** — Write `alice@example.com`, not "a valid email".
4. **One test for all invalid classes** — Mixing multiple invalid values in
   one test makes it impossible to diagnose which constraint failed.
5. **Ignoring interaction between fields** — `confirm_password ≠ password`
   is a cross-field class; add it explicitly.
