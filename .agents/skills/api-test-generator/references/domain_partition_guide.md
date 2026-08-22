# Stage A — Domain Partition & Boundary Value Guide

Goal: for **every** input the endpoint accepts (path params, query params,
body fields, relevant headers), derive equivalence classes and boundary
values instead of guessing a handful of ad-hoc inputs.

## Procedure

For each parameter:

1. Identify its declared type/format from the spec (string, email, enum,
   integer, price/decimal, date, password, free text, etc.) and any stated
   constraints (min/max length, regex, allowed values, required/optional).
2. Enumerate classes using the table below (skip rows that don't apply).
3. Write one test case per class that is meaningfully distinct — don't emit
   near-duplicate cases (e.g. two different "too long" strings of similar
   length is one class, not two).
4. Mark whether the class is expected to pass (2xx) or fail validation
   (4xx) in `expected.status`, based on the spec's stated constraints.

## Class checklist by type

| Type | Classes to cover |
|---|---|
| **email** | valid format; missing `@`; missing domain; consecutive dots; leading/trailing space; unicode/local-part edge cases; empty string; missing field; duplicate (already registered, if relevant); max-length boundary |
| **password** | meets policy exactly; one below min length; one above max length (if capped); missing uppercase/lowercase/digit/symbol per policy; only whitespace; empty; missing field |
| **price / money** | typical valid value; `0`; negative; extremely large; non-numeric string; float precision edge (e.g. `19.999`); missing field |
| **integer (qty, page, limit)** | valid mid-range; `0`; negative; non-integer (`1.5`); above stated max; below stated min; missing; string instead of number |
| **enum / status** | each declared valid value; an unknown value; case-mismatched value (`Pending` vs `pending`); empty; missing |
| **string (name, title, address)** | typical valid; empty; whitespace-only; at max length; one over max length; contains HTML/script fragment (also feeds Stage C); missing |
| **date / datetime** | valid ISO format; invalid format; past date where future required (or vice versa); far-future/far-past boundary; missing |
| **id / foreign key (path or body)** | existing valid id; well-formed but non-existent id; malformed id (wrong type/format); id belonging to another user (also feeds Stage C as IDOR); missing |
| **pagination (page/limit)** | default when omitted; `limit=0`; `limit` above server cap; negative page; non-numeric |
| **array / list body field** | empty array where ≥1 required; single item; max allowed items; over max; duplicate items where uniqueness implied |

## Combination cases

After single-parameter classes, add a small number of **combined** cases
where two boundary/invalid classes interact (e.g. invalid email + weak
password in one registration request) — real bugs often hide in the
interaction, and the assignment's audit step expects you to reason about
completeness, not just single-field coverage.

## Output

Each case goes into `test_cases.json` with `"stage": "domain_partition"`,
`"category"` set to the class name from the table (or your own precise
label), and `"fr_ref"` set to the functional requirement this parameter
belongs to.
