# Usability Evaluation — Software Bug Report

**Current status:** `READY_FOR_FIELDWORK`
**Policy:** Reproduce every candidate independently, attach evidence, search Task 1 issues for duplicates, and create or update a GitHub Issue for every confirmed software bug.

## Confirmed bugs from official sessions

No participant-confirmed Task 2 bug has been entered yet.

| Bug ID | Requirement | Participant discovery evidence | Independent reproduction | Severity | Local evidence | GitHub issue URL | Duplicate disposition |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` |

## Provisional technical-preflight candidates

| Candidate | Observation | Current disposition | Required next action |
| :--- | :--- | :--- | :--- |
| PF-01 | Login title/label/input types/language are inconsistent; the password is visible. | Existing Task 1 BUG-GUI-01; do not open a duplicate. | Link the existing GitHub Issue URL after verifying its external state; cite P01–P07 only if genuinely observed. |
| PF-02 | Live preflight rejects valid `0912345678` but accepts invalid fallback `912345678`. | `PROVISIONAL`; technically reproduced, not participant-validated. Draft: `github-issues/DRAFT-BUG-USABILITY-01.md`. | Observe in a genuine session, reproduce again, redact evidence, search GitHub duplicates, then publish/update an issue. |
| PF-03 | The logout control and post-logout route may not clearly confirm a safe logout. | `PROVISIONAL`; may be usability issue, requirement defect, or bug. | Observe official sessions and compare with FR-23 before classification. |

## GitHub Issue quality checklist

- [ ] Concise title and unique bug ID.
- [ ] SUT commit, device, OS, browser, and URL.
- [ ] Preconditions and exact reproduction steps.
- [ ] Expected result tied to a requirement.
- [ ] Actual result without participant identity.
- [ ] Severity/priority rationale.
- [ ] Screenshot or clip attached.
- [ ] Existing issue search completed.
- [ ] GitHub URL copied into this report, findings, summary, and evidence index.

If seven sessions yield no genuine software bug, replace the placeholders with a reasoned `NO_SOFTWARE_BUGS_CONFIRMED` statement and evidence of the review. Do not use that statement while provisional candidates remain unresolved.
