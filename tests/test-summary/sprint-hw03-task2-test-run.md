# HW03 Task 2 Supplemental Test Run — 2026-08-02

## Scope

Registration password policy only, using synthetic data and an isolated temporary database. No participant data was created or inferred.

## Result

| Test case | Controls | Expected | Actual | Status |
|---|---|---|---|---|
| TC-REGISTER-001 | Frontend EP/BVA matrix | 13 policy classifications match FR-01 | 13/13 matched | PASS control |
| TC-REGISTER-001 | Direct API, password missing allowed special character | Registration 4xx; login fails | Registration 200; login 200 | FAIL — defect reproduced |

## Defect linkage

- Local Task 2 ID: `BUG-REG-PASSWORD-POLICY-01`.
- Canonical existing issue: https://github.com/trngnneee/eshop-sut/issues/118.
- New duplicate issue created: No.
- Participant frequency contribution: None.
- Evidence: `task2-usability/evidence/github-issue-reproduction/result.json` and `BUG-REG-PASSWORD-POLICY-01-safe-reproduction.png`.

