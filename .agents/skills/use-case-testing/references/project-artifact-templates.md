# Project Artifact Templates For Use Case Testing

Read this reference before writing testcase, summary, test-run, traceability, or bug-report files for the EShop use-case workflow.

## Test Case File

Path: `tests/test-cases/<module_name>/<TC_ID>.md`

```markdown
# <TC_ID>: <Vietnamese test title>

## Requirement ID
FR-<NN>

## Module / Test type / Technique
<Module Display Name> / Functional / Use Case Testing

## Use case coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Use case ID | UC-<NN> |
| Actor | <primary actor/supporting actor> |
| Goal | <actor goal> |
| Flow type | Main success / Alternate / Exception |
| Covered flow | <UC-<NN>-MAIN/ALT/EXC item> |
| Covered requirement | <README/API bullet or section> |

## Preconditions
- <Required session/role/fixture/state>
- <Required data or UI/API context>

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | <user/admin/guest/system> |
| Interface | <web/admin/mobile/API> |
| Endpoint / UI flow | `<method path>` or `<screen/action>` |
| Input / Payload | `<payload or form values>` |
| Fixture | `<fixture/entity id/user/cart/order/etc.>` |

## Test steps
1. <Prepare the precondition or fixture.>
2. <Authenticate/open the correct interface as Actor.>
3. <Perform the use-case flow/action.>
4. <Observe response/UI/state/data after the action.>

## Expected result
- <Expected response/UI result.>
- <Expected postcondition or rejection behavior.>
- <Required invariant or side effect.>

## Status / Related bugs
Not Run / None
```

## Summary File

Path: `tests/test-summary/frNN-<module-name>-use-case-summary.md`

```markdown
# FR-<NN> - <Feature Title>

## Nguồn yêu cầu

<Source file and line range or section name.>

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | <Assumption> | <Reason from spec/code> |

## Use Case Model

| Use case ID | Actor | Goal | Trigger | Preconditions | Success postcondition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| UC-01 | <actor> | <goal> | <trigger> | <preconditions> | <postcondition> |

## Flow Inventory

| Flow ID | Use case ID | Flow type | Steps / Condition | Expected result | Requirement source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| UC-01-MAIN | UC-01 | Main success | <step summary> | <success result> | <README/API/code ref> |
| UC-01-ALT-01 | UC-01 | Alternate | <variation> | <accepted result> | <README/API/code ref> |
| UC-01-EXC-01 | UC-01 | Exception | <failure condition> | <rejection/result> | <README/API/code ref> |

## Generated Test Case Index

| TC ID | Use case | Flow ID | Actor | Technique | Expected Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FR<NN>-UC01-TC01 | UC-01 | UC-01-MAIN | <actor> | Use Case Testing | Accepted |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| Use cases | <n> | <TC IDs> | <covered>/<total> |
| Main flows | <n> | <TC IDs> | <covered>/<total> |
| Alternate flows | <n> | <TC IDs> | <covered>/<total> |
| Exception flows | <n> | <TC IDs> | <covered>/<total> |
| Actors / permission branches | <n> | <TC IDs> | <covered>/<total> |
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

| Nhóm kiểm thử | Main TC | Alternate TC | Exception TC | Tổng TC |
| :--- | ---: | ---: | ---: | ---: |
| <Use case/group> | <n> | <n> | <n> | <n> |
| **Tổng** | **<n>** | **<n>** | **<n>** | **<n>** |
```

## Test Run File

Path: `tests/test-runs/frNN-<module-name>-test-run.md`

```markdown
# Test Run - FR-<NN> <Feature Title>

__Ngày thực hiện__: [dd/mm/yyyy]  
__Người thực hiện__: [Tên người test]  
__Môi trường thử nghiệm__: [Local Web/API, backend http://localhost:3000, frontend/admin/mobile theo luồng kiểm thử]  

## Tổng quan kết quả

| Nhóm kiểm thử | Main TC | Alternate TC | Exception TC | Tổng TC | Pass | Fail | Blocked | Skipped |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| <Use case/group> | <n> | <n> | <n> | <n> | 0 | 0 | 0 | 0 |
| **Tổng** | **<n>** | **<n>** | **<n>** | **<n>** | **0** | **0** | **0** | **0** |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| Use cases | <n> | <TC IDs> | <covered>/<total> |
| Main flows | <n> | <TC IDs> | <covered>/<total> |
| Alternate flows | <n> | <TC IDs> | <covered>/<total> |
| Exception flows | <n> | <TC IDs> | <covered>/<total> |
| Requirement bullets | <n> | <TC IDs> | <covered>/<total> |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [<TC_ID>](../test-cases/<module_name>/<TC_ID>.md) | <Module - Use case/group> | [Tên người test] | Not Run | None | [Điền actual result / ghi chú sau khi chạy] |

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
4. <Observe the response/UI/state/data.>

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
- Technique: `Use Case Testing`.
- Coverage item: use case ID + flow ID.
- Result and related bug after execution.
