# Traceability Matrix — FR02: Đăng nhập & Khóa tài khoản

| Requirement | Decision Rule | Pairwise Case | Test Case | Result | Bug Issue | Status |
|---|---|---|---|---|---|---|
| FR02 | R001 | PW001 | TC-WEB-DT-PW-001 | **Pass** | None | Executed |
| FR02 | R002 | PW002 | TC-WEB-DT-PW-002 | **Pass** | None | Executed |
| FR02 | R021 | PW003 | TC-WEB-DT-PW-003 | **Fail(Bug)** | BUG-FR02-001 | Executed |
| FR02 | R022 | PW004 | TC-WEB-DT-PW-004 | **Fail(Bug)** | BUG-FR02-001 | Executed |
| FR02 | R009 | PW005 | TC-WEB-DT-PW-005 | **Pass** | None | Executed |
| FR02 | R010 | PW006 | TC-WEB-DT-PW-006 | **Pass** | None | Executed |
| FR02 | R027 | PW007 | TC-WEB-DT-PW-007 | **Pass** | None | Executed |
| FR02 | R037 | PW008 | TC-WEB-DT-PW-008 | **Pass** | None | Executed |
| FR02 | R003 | PW009 | TC-WEB-DT-PW-009 | **Pass** | None | Executed |
| FR02 | R019 | PW010 | TC-WEB-DT-PW-010 | **Fail(Bug)** | BUG-FR02-001 | Executed |
| FR02 | R020 | PW011 | TC-WEB-DT-PW-011 | **Fail(Bug)** | BUG-FR02-001 | Executed |
| FR02 | R015 | PW012 | TC-WEB-DT-PW-012 | **Pass** | None | Executed |
| FR02 | R033 | PW013 | TC-WEB-DT-PW-013 | **Fail(Bug)** | BUG-FR02-001 | Executed |
| FR02 | R016 | PW014 | TC-WEB-DT-PW-014 | **Pass** | None | Executed |
| FR02 | R011, R029 | PW015 | TC-WEB-DT-PW-015 | **Pass** | None | Executed |
| FR02 | R023 | PW016 | TC-WEB-DT-PW-016 | **Fail(Bug)** | BUG-FR02-001 | Executed |
| FR02 | R017 | PW017 | TC-WEB-DT-PW-017 | **Pass** | None | Executed |
| FR02 | R028 | PW018 | TC-WEB-DT-PW-018 | **Pass** | None | Executed |

---

## Rules Removed (Impossible / Redundant) — Not Traced to Test Cases

| Rule ID | Reason |
|---|---|
| R006 | Impossible: attempts>=2 + UL với bug +2 |
| R007, R008 | Impossible: attempts=0 không thể bị locked |
| R013, R014 | Impossible: attempts=0 không thể có expired lock |
| R024 | Impossible với bug +2 |
| R025, R026 | Impossible: attempts=0 locked |
| R031, R032 | Impossible: attempts=0 expired lock |
| R038 | Redundant với R037 |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Total Requirements | 1 (FR02) |
| Total Decision Rules (valid) | 27 |
| Rules with Pairwise Cases | 21 |
| Total Pairwise Cases | 18 |
| Total Test Cases | 18 |
| Bug Reports Linked | 1 (BUG-FR02-001) |
| Test Cases Linked to Bug | 6 |
