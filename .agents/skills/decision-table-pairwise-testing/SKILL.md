---
name: decision-table-pairwise-testing
description: Kỹ năng thiết kế test case cho một Feature/FR của EShop bằng Decision Table Testing, rút gọn tổ hợp bằng Pairwise khi có nhiều điều kiện hoặc nghi ngờ tương tác điều kiện, sinh mỗi test case thành một file Markdown theo template chuẩn, tạo thêm file test-run template để tester bắt đầu chạy test, và ghi lại các bước AI đã thực hiện trong file summary.
---

# Decision Table Pairwise Testing

## Mục tiêu

Sử dụng skill này khi cần phân tích một Feature/FR có nhiều điều kiện nghiệp vụ, actor, trạng thái, quyền truy cập, dữ liệu đầu vào, hoặc hành động đầu ra. Agent phải tạo bảng quyết định trước, rút gọn có kiểm soát, chỉ áp dụng Pairwise ở bước rút gọn khi cần, sinh từng test case thành file `.md` riêng, và tạo file test run để tester bắt đầu chạy test.

## Quy trình bắt buộc

### Bước 1: Thu thập phạm vi Feature

1. Xác định `Requirement ID`, tên feature, module, nền tảng liên quan, endpoint/UI flow, actor, precondition, dữ liệu hệ thống cần có, và expected behavior.
2. Đọc nguồn đặc tả trong repo nếu có: `README.md`, `api_specification.md`, UI/frontend, backend route/controller, test-run cũ, bug cũ.
3. Nếu thông tin còn thiếu nhưng vẫn có thể làm tiếp, nêu rõ giả định trong summary thay vì dừng lại.
4. Không ghi đè file test-run, bug, hoặc testcase đã có kết quả thật nếu người dùng không yêu cầu rõ.

### Bước 2: Xác định condition và action

Lập danh sách các biến quyết định:

| Condition ID | Condition | Values / Classes | Source / Evidence | Note |
| :--- | :--- | :--- | :--- | :--- |
| C1 | [actor/role/status/input] | [valid/invalid/classes] | [file/line or spec] | [assumption/risk] |

Lập danh sách action/expected result:

| Action ID | Action / Expected Result | HTTP/UI Expected Status | Note |
| :--- | :--- | :--- | :--- |
| A1 | [allow/reject/update/render] | [200/403/error/UI state] | [reason] |

### Bước 3: Tạo Decision Table đầy đủ

Tạo bảng quyết định ban đầu trước khi rút gọn. Mỗi rule là một tổ hợp điều kiện có expected action rõ ràng.

| Rule ID | C1 | C2 | C3 | Action | Expected Status | Risk | Keep? | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R01 | [value] | [value] | [value] | [A1] | [status] | [High/Medium/Low] | [Yes/No] | [why] |

Quy tắc bảo toàn:

1. Giữ mọi rule được đặc tả trực tiếp trong requirement.
2. Giữ mọi rule liên quan authorization, ownership, security, payment, order state, data exposure, destructive action, hoặc known bug.
3. Giữ ít nhất một rule cho mỗi action/expected status.
4. Loại bỏ rule impossible/duplicate/equivalent only khi đã ghi rõ lý do trong summary.

### Bước 4: Rút gọn bằng Pairwise khi nghi ngờ

Chỉ áp dụng Pairwise sau khi đã có Decision Table và danh sách rule bắt buộc giữ lại.

Một tổ hợp được xem là cần Pairwise khi có ít nhất một dấu hiệu:

1. Có từ 3 condition trở lên và mỗi condition có nhiều giá trị, khiến full matrix quá lớn.
2. Requirement mơ hồ hoặc có khả năng tương tác giữa các condition.
3. Điều kiện liên quan actor + trạng thái + quyền sở hữu + endpoint/action.
4. Có khác biệt giữa đặc tả và implementation.
5. Có rule hợp lệ cần giảm số lượng nhưng vẫn muốn bao phủ các cặp condition-value.

Không dùng Pairwise để loại bỏ:

1. Rule invalid riêng lẻ cần kiểm thử độc lập.
2. Rule security/authorization/data leak.
3. Rule có expected action khác biệt rõ ràng.
4. Rule đã có bug hoặc nghi ngờ regression cao.

Nếu cần sinh Pairwise thủ công, làm theo cách tham lam:

1. Liệt kê mọi cặp khả thi giữa các condition-value, sau khi loại impossible combo.
2. Seed trước bằng các rule bắt buộc giữ lại.
3. Tính các cặp còn chưa covered.
4. Chọn thêm rule hợp lệ cover nhiều cặp chưa covered nhất; khi hòa, ưu tiên risk cao hơn và expected action khác biệt hơn.
5. Lặp lại đến khi các cặp khả thi đều được covered hoặc phần chưa covered được giải thích.
6. Ghi bảng Pairwise Coverage trong summary.

### Bước 5: Sinh test case Markdown

Mỗi test case phải là một file `.md` riêng tại:

```text
tests/test-cases/[module_slug]/[TC_ID].md
```

Quy ước đặt mã:

1. `Requirement ID` dùng dạng `FR-18`.
2. `TC_ID` dùng dạng `FR18-[GROUP]-TC[NN]`.
3. `[GROUP]` là mã nhóm ngắn theo nghiệp vụ, ví dụ `A` = Authorization, `S` = Status, `O` = Ownership, `PW` = Pairwise mixed rule.
4. Tên file phải trùng `TC_ID`, ví dụ `FR18-A-TC01.md`.
5. Module slug dùng `snake_case`, ví dụ `admin_order_management`.

Template bắt buộc cho từng file:

```markdown
# [TC_ID]: [Tên test case]

## Requirement ID

[FR-XX]

## Module / Test type / Technique

[Module] / Functional / Decision Table / [Pairwise nếu có]

## Preconditions

- [Precondition 1]
- [Precondition 2]

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| [Parameter] | [Value] |

## Test steps

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected result

- [Expected result 1]
- [Expected result 2]

## Status / Related bugs

Not Run / None
```

Chỉ điền `Failed / BUG-...` hoặc trạng thái khác khi người dùng đã cung cấp kết quả chạy test hoặc bug ID thật. Không tự bịa bug ID cho testcase chưa chạy.

### Bước 6: Sinh file test run

Sau khi sinh testcase, tạo thêm file test run tại:

```text
tests/test-runs/[fr]-[module-kebab]-test-run.md
```

Ví dụ:

```text
tests/test-runs/fr09-coupon-application-test-run.md
```

Nếu file test run đã tồn tại và có kết quả thật (`Passed`, `Failed`, bug ID, tester thật, hoặc note actual result), không ghi đè mặc định. Chỉ ghi đè khi người dùng yêu cầu rõ.

Template bắt buộc:

```markdown
# Test Run - [FR-XX] [Feature]

__Ngày thực hiện__: [dd/mm/yyyy]  
__Người thực hiện__: [Tên người test]  
__Môi trường thử nghiệm__: [Môi trường thử nghiệm]  

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| [Nhóm kiểm thử] | [Số Decision Table TC] | 0 | [Tổng TC] | 0 | 0 |
| **Tổng** | **[Tổng Domain TC]** | **[Tổng BVA TC]** | **[Tổng TC]** | **0** | **0** |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC_ID](../test-cases/[module_slug]/[TC_ID].md) | [Feature - nhóm kiểm thử] | [Tên người test] | Not Run | None | [Điền actual result / ghi chú sau khi chạy] |

## Defect Log

Sau khi chạy test, cập nhật các test case `Fail` vào bảng dưới đây hoặc map sang bug report riêng.

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [BUG-ID] | [TC ID] | [Tóm tắt lỗi] | [High/Medium/Low] | Open | [Actual result / evidence] |
```

Mọi dòng execution mới sinh phải để `Tester = [Tên người test]`, `Result = Not Run`, `Related Bug = None`, và note dạng placeholder. Không điền tên tester thật hoặc kết quả thật khi chưa chạy.

### Bước 7: Ghi file summary

Sau khi sinh testcase và test run, tạo hoặc cập nhật file summary tại:

```text
tests/test-summary/[fr]-[module_slug]-decision-table-summary.md
```

Ví dụ:

```text
tests/test-summary/fr18-admin_order_management-decision-table-summary.md
```

Summary phải có các phần:

```markdown
# Decision Table Summary - [FR-XX] [Feature]

## Metadata

| Field | Value |
| :--- | :--- |
| Requirement ID | [FR-XX] |
| Module | [module_slug] |
| Technique | Decision Table + Pairwise reduction when needed |
| Generated test case folder | tests/test-cases/[module_slug]/ |
| Generated test run | tests/test-runs/[fr]-[module-kebab]-test-run.md |

## Sources Reviewed

| Source | Evidence / Note |
| :--- | :--- |
| [file/path] | [what was used] |

## Conditions and Actions

[condition table and action table]

## Full Decision Table

[full or normalized decision table]

## Reduction and Pairwise Rationale

- Mandatory rules kept: [list]
- Impossible/duplicate rules removed: [list + reason]
- Pairwise applied: [Yes/No]
- Reason: [why]

## Pairwise Coverage

| Pair | Covered By TC | Note |
| :--- | :--- | :--- |
| [C1=value + C2=value] | [TC_ID] | [note] |

## Generated Test Cases

| TC ID | Rule ID | Technique | File | Expected Status | Status / Related bugs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC_ID] | [Rxx] | [Decision Table/Pairwise] | [path] | [expected] | Not Run / None |

## Generated Test Run

| Artifact | Path |
| :--- | :--- |
| Test run template | tests/test-runs/[fr]-[module-kebab]-test-run.md |

## AI Steps Log

1. [Read source / extracted condition]
2. [Built decision table]
3. [Reduced rules / applied pairwise]
4. [Generated testcase files]
5. [Generated test-run template]
6. [Verified generated artifacts]

## Assumptions / Open Questions

- [Assumption or None]
```

`AI Steps Log` là bắt buộc. Ghi đủ các bước agent đã thực hiện, nhưng không đưa chain-of-thought nội bộ; chỉ ghi nhật ký thao tác, quyết định, giả định, và artifact đã tạo.

## Kiểm tra sau khi sinh

Trước khi trả lời người dùng:

1. Đọc lại các file testcase vừa tạo và file summary.
2. Kiểm tra mỗi testcase có đủ các heading trong template.
3. Kiểm tra `Requirement ID`, `TC_ID`, đường dẫn file, module slug, và trạng thái mặc định.
4. Kiểm tra test run có đủ dòng cho mọi testcase, các dòng đều `Not Run / None`, và tester còn là `[Tên người test]`.
5. Kiểm tra summary có `AI Steps Log`, rationale rút gọn, danh sách testcase, và đường dẫn test run.
6. Chạy validator hoặc lệnh kiểm tra Markdown có sẵn nếu repo cung cấp; nếu không có, nói rõ đã kiểm tra bằng đọc lại file.

## Cách trả lời sau khi hoàn thành

Trả lời ngắn gọn bằng tiếng Việt, nêu:

1. Skill/Feature đã xử lý.
2. Số lượng testcase đã tạo.
3. Đường dẫn thư mục testcase.
4. Đường dẫn test run.
5. Đường dẫn summary.
6. Bất kỳ giả định hoặc việc chưa thể xác minh.
