# BUG-REG-PASSWORD-POLICY-01 — Registration API accepts a password without the required special character

**Status:** `INDEPENDENTLY_REPRODUCED — EXISTING_ISSUE_REUSED — EVIDENCE_COMMENT_NOT_PUBLISHED`
**Canonical existing issue:** https://github.com/trngnneee/eshop-sut/issues/118
**Requirement:** FR-01
**Task 2 severity:** `S2` provisional; owner/security review required
**Participant evidence:** None. This is a supplemental technical reproduction and is not counted in P01–P07 frequencies.

## Description

FR-01 requires at least eight characters containing uppercase, lowercase, digit and one character from `@`, `$`, `!`, `%`, `*`, `?`, `&`. The web registration form enforces that rule, but `POST /api/register` inserts the supplied password without server-side validation. A caller can bypass the UI, create an account with no allowed special character, and then log in with that account.

This defect is distinct from `UF-REG-PASSWORD-RECOVERY-01`. P04/P06 recordings show repeated password-policy recovery, but their masked input does not reveal which policy condition failed. Those participants are therefore not attributed to this software bug.

## Preconditions

- Backend API is running against an isolated temporary SQLite database.
- Use only a unique `example.com` synthetic account.
- Do not use participant names, contacts or credentials.

## Test data

- Partition: invalid password missing the allowed-special-character class.
- Synthetic password: `NoSpecial1` (10 characters; uppercase, lowercase and digit present; no character from the FR-01 allowed set).
- Synthetic email pattern: `github.issue.password-policy.<run-id>@example.com`.

## Steps to reproduce

1. Send `POST /api/register` with a synthetic name/email and the test password above.
2. Record the HTTP status and response body.
3. Send `POST /api/login` with the newly submitted synthetic email/password.
4. Record the login status.
5. Dispose of the isolated test database after evidence capture.

## Expected result

- Registration returns a 4xx validation response.
- No account is created.
- A subsequent login with the rejected credentials fails.

## Actual result

- Registration returned HTTP `200` with `User registered successfully`.
- Login returned HTTP `200`; the invalid account was usable.
- Reproduction result: `FAIL_DEFECT_REPRODUCED` (1/1 isolated API run on 2026-08-02).

## Domain and boundary controls

| Control | Expected | Observed |
|---|---|---|
| Frontend regex, length 7 | Reject | Reject |
| Frontend regex, minimum length 8 | Accept when all classes present | Accept |
| Frontend regex, length 9 | Accept when all classes present | Accept |
| Frontend regex, each of `@ $ ! % * ? &` | Accept | All accepted |
| Frontend regex, `#` as the only special character | Reject | Reject |
| Direct API, missing allowed special character | Reject with 4xx | **Accepted with 200; login also 200** |

The frontend control matrix passed 13/13 checks. The failure is the missing backend enforcement, not an incorrect allowed-character set in `Register.jsx`.

## Evidence

- Machine-readable result: `../evidence/github-issue-reproduction/result.json`; SHA-256 `1cc19accd5eda2cd4e27b7046d919a290b7735b606de97ac5bbd5b89983abbcd`.
- Privacy-safe screenshot: `../evidence/github-issue-reproduction/BUG-REG-PASSWORD-POLICY-01-safe-reproduction.png`; SHA-256 `5c1e6d718f39f20dff7c5263c505a3789d96f6ddf196fae6167e8ce4f85d0537`.
- Test case: `../../tests/test-cases/register/TC-REGISTER-001.md`.
- Source trace: `backend/server.js` registration handler inserts `name`, `email`, `password` without validating FR-01; `frontend-web/src/pages/Register.jsx` contains the client-side regex.

## Duplicate disposition

GitHub Search API was checked on 2026-08-02 using `register password special`, `registration API password validation` and `FR-01 password`. Existing issue #118 describes the same backend bypass, including the missing-special-character case. Do not open a duplicate. The canonical issue remains https://github.com/trngnneee/eshop-sut/issues/118.

No new comment or attachment has been published for this Task 2 reproduction. Publication requires a human privacy review and explicit external action.

## Recommended fix

Enforce the complete FR-01 password policy inside `POST /api/register`, return a specific 4xx validation error, and share one policy definition between client and server. Never treat client-side validation as an authorization or integrity boundary.

## Acceptance criteria

1. Direct API and UI both reject passwords missing uppercase, lowercase, digit, allowed special character, or the eight-character minimum.
2. Each allowed character `@`, `$`, `!`, `%`, `*`, `?`, `&` is accepted when all other conditions are met.
3. Unsupported characters such as `#` do not satisfy the allowed-special-character condition.
4. A valid eight-character boundary value is accepted; a seven-character value is rejected.
5. Rejected registration data cannot subsequently authenticate.
