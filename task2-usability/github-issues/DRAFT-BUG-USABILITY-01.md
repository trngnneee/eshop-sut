# [DRAFT-BUG-USABILITY-01] Profile rejects valid Vietnamese phone number

**Status:** `PROVISIONAL_TECHNICAL_PREFLIGHT`
**GitHub action:** Do not publish until a genuine session exposes the issue and the researcher reproduces it again.

## Requirement

FR-04 requires a phone number to start with `0` and contain 10–11 digits.

## Preconditions

- EShop backend and web frontend are running.
- A normal user is authenticated.
- The user is on `/profile`.

## Steps to reproduce

1. Enter any non-empty display name.
2. Enter `0912345678` in the phone field.
3. Enter a non-empty shipping address.
4. Select **Cập nhật**.

## Expected result

The profile accepts `0912345678`, because it starts with `0` and contains 10 digits.

## Actual result

The browser shows: `Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số.` The same profile saves after changing the phone to `912345678`, which violates the required leading-zero rule.

## Technical-preflight evidence

- Result: `../evidence/technical-preflight/result.json`
- Valid-phone attempt: `../evidence/technical-preflight/03-after-valid-phone-attempt.png`
- Saved fallback and persistence: `../evidence/technical-preflight/04-profile-after-reload.png`
- Source: `frontend-web/src/pages/Profile.jsx`

## Impact and provisional severity

Potential S1/S2 impact for the selected Task 2 flow because a participant using an ordinary Vietnamese phone cannot independently finish the profile update. Final severity requires genuine participant evidence.

## Required publication gate

- [ ] Observed in at least one genuine official session or pilot and cited with timestamp.
- [ ] Reproduced independently after that session.
- [ ] Screenshot reviewed to exclude participant identity.
- [ ] Existing GitHub issues searched for a duplicate.
- [ ] GitHub repository/fork confirmed.
- [ ] Published issue URL added to the bug report, findings, summary, and evidence index.
