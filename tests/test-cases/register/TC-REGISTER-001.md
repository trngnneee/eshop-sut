# TC-REGISTER-001: Reject registration password missing the FR-01 special-character class

## Requirement

- FR-01 — Account registration password must contain at least eight characters, one uppercase letter, one lowercase letter, one digit and one special character from `@`, `$`, `!`, `%`, `*`, `?`, `&`.

## Module / Test Type / Technique

- Module: Registration
- Test type: API functional validation with frontend control checks
- Technique: Equivalence Partitioning and Boundary Value Analysis

## Preconditions

- Backend API is running against an isolated temporary SQLite database.
- Frontend source regex is the current `frontend-web/src/pages/Register.jsx` implementation.
- Synthetic `example.com` data only; no participant data is used.

## Test Data

| Partition/boundary | Value | Expected |
|---|---|---|
| Invalid, length 7 | `Aa1!aaa` | Reject |
| Valid, minimum length 8 | `Aa1!aaaa` | Accept |
| Valid, minimum + 1 | `Aa1!aaaaa` | Accept |
| Invalid, missing allowed special character | `NoSpecial1` | Reject |
| Valid allowed-special controls | one case each using `@ $ ! % * ? &` | Accept |
| Invalid unsupported-only special character | `Aa1#aaaa` | Reject |

## Test Steps

1. Execute the frontend password regex against the EP/BVA control matrix.
2. Send `POST /api/register` using a unique synthetic email and `NoSpecial1`.
3. Verify registration returns a 4xx response and does not create the account.
4. Attempt `POST /api/login` with the same synthetic credentials.
5. Verify login fails.
6. Dispose of the isolated database.

## Expected Result

- Frontend controls classify every boundary and partition according to FR-01.
- The API rejects `NoSpecial1` with 4xx, creates no account, and the credentials cannot log in.

## Status / Related Bugs

- Status: `FAIL`
- Frontend control matrix: `PASS` — 13/13 checks.
- API observation on 2026-08-02: registration `200`; subsequent login `200`.
- Related local bug: `BUG-REG-PASSWORD-POLICY-01`.
- Canonical existing issue: https://github.com/trngnneee/eshop-sut/issues/118.
- Participant attribution: `NONE`; this technical test does not change P01–P07 frequency.

