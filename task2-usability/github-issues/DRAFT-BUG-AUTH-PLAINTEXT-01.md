# [DRAFT] BUG-AUTH-PLAINTEXT-01 — Login password renders as plaintext

**Status:** `INDEPENDENTLY_REPRODUCED — DUPLICATE_FOUND — EXISTING_ISSUE_LINKED`
**GitHub action:** Reuse https://github.com/trngnneee/eshop-sut/issues/37; do not create a duplicate.

## Summary

Login password characters are readable on screen by default. No explicit reveal action is observed. This exposes credentials to shoulder surfing and screen recordings.

## Requirement/baseline

Password controls must mask credentials by default. If a reveal control exists, reveal must be explicit, accessible and reversible. Product owner should link the repository-specific requirement/security control before publication.

## Environment

- SUT: EShop Web Frontend.
- Page: login.
- SUT commit/build: NOT_RECORDED in participant videos.
- Devices/browsers: mixed desktop and mobile recordings; exact versions mostly NOT_OBSERVABLE.
- Reproduction credential: test-only; never use a participant password.

## Preconditions

1. Open login page.
2. Use a synthetic test account/password.
3. Ensure no reveal control has been activated.

## Steps to reproduce

1. Focus the login password field.
2. Enter test characters.
3. Observe whether characters appear as readable text or masked symbols.
4. Repeat in supported desktop/mobile browsers.
5. If reveal exists, verify default/active/remasked states and keyboard/autofill behavior.

## Expected result

- Characters are masked by default.
- Reveal occurs only after explicit user action.
- Remasking works reliably.
- Screen recording does not expose the test password in the default state.

## Actual result from participant evidence

Password characters are readable in five distinct participant recordings. No explicit reveal action is observed. Values are intentionally omitted from this draft.

## Participant evidence

- P01/D01 @ 00:00:19–00:00:33.
- P02/D02 @ 00:00:17–00:00:35.
- P04/D04 @ 00:01:01–00:01:39.
- P05/D05 @ 00:00:39–00:00:46.
- P07/D07 @ 00:00:29–00:00:48.
- Frequency: 5/7 distinct official participants.
- P06 not counted because the replacement recording never reaches login.
- Genuine quote/security concern: NOT_RECORDED; no emotional/trust impact is inferred.

## Impact

Credentials can be read by nearby people and captured in videos/screenshots. The issue does not visibly block login, but creates direct privacy/security exposure.

## Severity/priority

- Provisional severity: `S2`.
- Priority: SECURITY/PRODUCT OWNER TO ASSIGN.
- Rationale: Serious credential exposure across desktop and mobile evidence; participant verbal concern is unavailable.

## Suggested fix

- Render the field as a password input masked by default.
- Provide an accessible optional reveal button if required.
- Preserve safe autocomplete semantics.
- Review recording/screenshot handling and invalidate any exposed real credential outside this analysis if applicable.

## Retest acceptance criteria

- [ ] Masked by default in every supported browser/device.
- [ ] No reveal without explicit action.
- [ ] Reveal control has accessible name/state and remasks correctly.
- [ ] Copy/paste, keyboard and password-manager behaviors do not switch to plaintext unexpectedly.
- [ ] Automated UI assertion confirms password input semantics.
- [ ] Redacted evidence demonstrates behavior without a readable credential.

## Evidence handling

- Original frames contain plaintext credentials and adjacent PII; do not attach them unredacted.
- Fresh screenshot uses only the synthetic non-account value `NotARealCredential!42`.
- Safe screenshot: `../evidence/github-issue-reproduction/BUG-AUTH-PLAINTEXT-01-safe-reproduction.png`.
- Result log: `../evidence/github-issue-reproduction/result.json`.

## Potential duplicate

Duplicate search completed. Canonical existing issue is #37; related duplicates include #184 and #196.

## Publication gate

- [ ] Human verifies all timestamps and distinct-participant count.
- [x] Independent reproduction completed with synthetic credential.
- [ ] Supported-browser matrix checked.
- [x] Privacy-safe synthetic evidence created; SHA-256 recorded in the bug report.
- [x] Existing GitHub issues searched; canonical duplicate #37 selected.
- [x] Safe-reproduction evidence published to canonical issue on 2026-08-01.
- [ ] Security/product owner confirms requirement and severity.
- [ ] Reviewer explicitly approves publication.
- [x] Existing issue URL added to all traceability files.

**Published GitHub URL:** https://github.com/trngnneee/eshop-sut/issues/37

**Published evidence comment:** https://github.com/trngnneee/eshop-sut/issues/37#issuecomment-5149476796
