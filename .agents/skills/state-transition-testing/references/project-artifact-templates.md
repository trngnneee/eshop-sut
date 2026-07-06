# Project Artifact Templates For State Transition Testing

Read this reference before writing testcase, summary, test-run, traceability, or bug-report files for the EShop state-transition workflow.

## Test Case File

Path: `tests/test-cases/<module_name>/<TC_ID>.md`

```markdown
# <TC_ID>: <Vietnamese test title>

## Requirement ID
FR-<NN>

## Module / Test type / Technique
<Module Display Name> / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | <S-VALID-01/S-INVALID-01> |
| State variable | `<status/session/etc.>` |
| Actor | <admin/user/guest/system> |
| Flow type | Valid transition / Invalid transition / Final-state rejection / Guard rejection |
| Covered guard/rule | <auth/role/ownership/business/final-state rule> |
| Covered requirement | <README/API bullet or section> |

## Preconditions
- <Initial state or setup data>
- <Actor/session/role condition>

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | <admin/user/guest/system> |
| Current state | `<state_before>` |
| Action / Event | <action name> |
| Requested state | `<state_after>` |
| Endpoint / UI flow | `<method path>` or `<screen/action>` |
| Body / Input | `<payload>` |
| Entity ID | `<id or fixture>` |

## Test steps
1. <Prepare the entity in Current state.>
2. <Authenticate or open the UI as Actor.>
3. <Perform Action / Event.>
4. <Reload/read the entity after the action.>

## Expected result
- <HTTP/UI result or error message expectation.>
- <Expected state after action, or unchanged state for invalid transition.>
- <Required side effect or invariant.>

## Status / Related bugs
Not Run / None
```

For invalid transitions, include an explicit unchanged-state expectation.

## Summary File

Path: `tests/test-summary/frNN-<module-name>-state-transition-summary.md`

```markdown
# FR-<NN> - <Feature Title>

## Nguồn yêu cầu

<Source file and line range or section name.>

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | <Assumption> | <Reason from spec/code> |

## State Model

| Element | Value |
| :--- | :--- |
| State variable | `<status/session/etc.>` |
| Initial state | `<state>` |
| Valid states | `<state list>` |
| Final states | `<state list>` |
| Actors | `<actor list>` |
| Interfaces | `<API/UI list>` |

## State Transition Table

| Transition ID | Actor | Current state | Action / Requested state | Expected next state | Expected status | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S-VALID-01 | <actor> | `<from>` | `<action/to>` | `<to>` | Accepted | <Reason> |
| S-INVALID-01 | <actor> | `<from>` | `<action/to>` | `<from>` | Rejected | <Reason> |

## Generated Test Case Index

| TC ID | Transition / Class | Actor | Technique | Expected Status |
| :--- | :--- | :--- | :--- | :--- |
| FR<NN>-S-TC01 | S-VALID-01 | <actor> | State Transition Testing | Accepted |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| State variables | <n> | <TC IDs> | <covered>/<total> |
| Valid transitions | <n> | <TC IDs> | <covered>/<total> |
| Invalid transitions | <n> | <TC IDs> | <covered>/<total> |
| Final-state rejections | <n> | <TC IDs> | <covered>/<total> |
| Actor / permission guards | <n> | <TC IDs> | <covered>/<total> |
| Requirement bullets | <n> | <TC IDs> | <covered>/<total> |

## TC Status

| Status | Count |
| :--- | ---: |
| Not Run | <n> |
| Passed | <n> |
| Failed | <n> |
| Blocked | <n> |
| Skipped | <n> |
| **Total TC** | **<n>** |

## Bug Coverage

| Metric | Count / Value |
| :--- | :--- |
| Bug Count | <n> |
| Failed TC | <n> |
| Failed TC with exactly one bug | <n>/<failed_tc_count> |
| Bug reports mapped to exactly one failed TC | <n>/<bug_count> |
| Unmapped failed TC | <TC IDs or None> |
| Bug without failed TC | <BUG IDs or None> |

## Generated Artifacts

| Artifact | Path |
| :--- | :--- |
| Test cases | `tests/test-cases/<module_name>/` |
| Test run | `tests/test-runs/frNN-<module-name>-test-run.md` |
| Traceability matrix | `tests/test-summary/traceability-matrix.md` |
| Bug reports | `tests/bug/FR-<NN>/` |

## Count Summary

| Nhóm kiểm thử | State TC | Tổng TC |
| :--- | ---: | ---: |
| <Group> | <n> | <n> |
| **Tổng** | **<n>** | **<n>** |
```

## Test Run File

Path: `tests/test-runs/frNN-<module-name>-test-run.md`

```markdown
# Test Run - FR-<NN> <Feature Title>

__Ngày thực hiện__: [dd/mm/yyyy]  
__Người thực hiện__: [Tên người test]  
__Môi trường thử nghiệm__: [Local Web/API, backend http://localhost:3000, frontend/admin/mobile theo luồng kiểm thử]  

## Tổng quan kết quả

| Nhóm kiểm thử | State TC | Tổng TC | Pass | Fail | Blocked | Skipped |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| <Group> | <n> | <n> | 0 | 0 | 0 | 0 |
| **Tổng** | **<n>** | **<n>** | **0** | **0** | **0** | **0** |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| State variables | <n> | <TC IDs> | <covered>/<total> |
| Valid transitions | <n> | <TC IDs> | <covered>/<total> |
| Invalid transitions | <n> | <TC IDs> | <covered>/<total> |
| Final-state rejections | <n> | <TC IDs> | <covered>/<total> |
| Actor / permission guards | <n> | <TC IDs> | <covered>/<total> |
| Requirement bullets | <n> | <TC IDs> | <covered>/<total> |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [<TC_ID>](../test-cases/<module_name>/<TC_ID>.md) | <Module - Group> | [Tên người test] | Not Run | None | [Điền actual result / ghi chú sau khi chạy] |

## TC Status

| Status | Count |
| :--- | ---: |
| Not Run | <n> |
| Passed | <n> |
| Failed | <n> |
| Blocked | <n> |
| Skipped | <n> |
| **Total TC** | **<n>** |

## Defect Log

Mỗi failed TC phải map sang đúng một bug report riêng.

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| <BUG-ID> | <TC_ID> | <Tóm tắt lỗi> | High/Medium/Low | Open | <Actual result / evidence> |

## Bug Coverage

| Metric | Count / Value |
| :--- | :--- |
| Bug Count | <n> |
| Failed TC | <n> |
| Failed TC with exactly one bug | <n>/<failed_tc_count> |
| Bug reports mapped to exactly one failed TC | <n>/<bug_count> |
| Unmapped failed TC | <TC IDs or None> |
| Bug without failed TC | <BUG IDs or None> |
```

## Bug Report File

Path: `tests/bug/FR-<NN>/<BUG-ID>.md`

```markdown
## <BUG-ID> - <Tóm tắt lỗi>

**GitHub issue title:** `[BUG][FR-<NN>][<Feature>] <Tóm tắt lỗi>`

**GitHub issue:** [TBD]

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `<TC_ID>`
- Path: `eshop-sut/tests/test-cases/<module_name>/<TC_ID>.md`

## Requirement liên quan

- `FR-<NN>`
- <Requirement bullet from README/spec>
- Source: `eshop-sut/README.md`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: [Browser/API client]
- **URL**: `<endpoint or UI URL>`
- **Build/Commit**:

## Steps to reproduce

1. <Use the exact TC setup step.>
2. <Use the exact TC actor/interface step.>
3. <Use the exact TC action step.>
4. <Reload/read the entity state.>

## Expected result

- <Expected result from the TC.>

## Actual result

- <Observed actual result.>

## Evidence

[Evidence bổ sung sau.]
```

Keep `Found by Test Case` to exactly one testcase for this skill.

## Traceability Matrix Row

Append or update rows in `tests/test-summary/traceability-matrix.md` using the existing table style. Each generated TC should trace to:

- Requirement ID.
- Test case ID and relative testcase path.
- Technique: `State Transition Testing`.
- Coverage item: transition/class ID and state/guard rule.
- Result and related bug after execution.
