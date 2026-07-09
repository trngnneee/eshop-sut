---
name: state-transition-testing-skill
description: Hỗ trợ tự động và bán tự động thực hiện thiết kế kịch bản State Transition Testing cho các tính năng có tính chất máy trạng thái (state machine) trong hệ thống EShop.
---

# State Transition Testing Skill (state-transition-testing-skill)

Kỹ năng này được thiết kế để dẫn dắt AI Agent thực hiện phân tích kiểm thử trạng thái, thiết kế test case, hỗ trợ chạy test và lập báo cáo lỗi cho các tính năng của EShop chứa các trạng thái và điều kiện chuyển trang/chuyển trạng thái phức tạp (ví dụ: FR10 - Order State Machine, FR02 - Account Lockout).

---

## 1. MỤC TIÊU & PHẠM VI ÁP DỤNG

* **Mục tiêu**: Xây dựng quy trình chuẩn thiết kế kiểm thử chuyển trạng thái (State Transition Testing) từ việc trích xuất Spec, mô hình hóa trạng thái bằng bảng chuyển trạng thái (State Transition Table) và sơ đồ Mermaid, phủ các kịch bản chuyển đổi hợp lệ và không hợp lệ, đến việc sinh test case dạng file Markdown độc lập và báo cáo bug.
* **Môi trường chạy**: Thực hiện trực tiếp trong thư mục `state-transtition-test/` của dự án.

---

## 2. ĐIỀU KIỆN KÍCH HOẠT (TRIGGER CONDITIONS)

Skill này được kích hoạt khi:
* Người dùng yêu cầu thực hiện "State Transition Testing" hoặc kiểm thử chuyển trạng thái cho một tính năng.
* Người dùng nhắc đến việc thiết kế test case cho các chức năng có tính chất vòng đời sản phẩm, tài khoản, đơn hàng (ví dụ: FR10 Order, FR02 Lockout).

---

## 3. QUY TRÌNH THỰC HIỆN TỪNG BƯỚC (STEP-BY-STEP WORKFLOW)

Agent phải tuân thủ các bước sau:

### Bước 1: Đọc đặc tả & Đề xuất Feature áp dụng
* Đọc tài liệu đặc tả `Requirements.pdf` hoặc các file tài liệu nghiệp vụ có sẵn trong dự án.
* Phân tích các tính năng có thể áp dụng State Transition Testing (các thực thể có thuộc tính trạng thái và sự kiện làm thay đổi trạng thái).
* Đề xuất danh sách feature phù hợp cho người dùng review và confirm.

### Bước 2: Thiết kế Testcase Design Analysis & Coverage Criteria
Sau khi người dùng chọn feature, Agent tạo tài liệu phân tích thiết kế kịch bản test. Tài liệu phải bao gồm đầy đủ các mức độ bao phủ (Coverage Criteria):
* **Các trạng thái (States)**: Xác định rõ tất cả các trạng thái có thể của thực thể (ví dụ: Pending, Paid, Shipped, Delivered, Cancelled).
* **Các sự kiện kích hoạt (Events/Inputs)**: Xác định các tác nhân hoặc API request làm thay đổi trạng thái (ví dụ: Pay, Ship, Deliver, Cancel).
* **Các điều kiện/Ràng buộc (Guards/Constraints)**: Các luật nghiệp vụ đi kèm (ví dụ: chỉ có thể hủy khi chưa thanh toán).
* **Sơ đồ chuyển trạng thái (State Transition Diagram)**: Vẽ bằng Mermaid diagram.
* **Bảng chuyển trạng thái (State Transition Table)**: Liệt kê các bộ `(Trạng thái hiện tại, Sự kiện, Trạng thái tiếp theo, Hành động/Kết quả)`.
* **Phân tích các tiêu chí bao phủ (Coverage Design)**:
  * **State Coverage**: Đảm bảo tất cả các trạng thái trong hệ thống được viếng thăm ít nhất một lần.
  * **Transition Coverage (0-switch)**: Đảm bảo tất cả các chuyển đổi hợp lệ được thực thi ít nhất một lần.
  * **n-Switch Coverage (đặc biệt là 1-switch)**: Kiểm thử các chuỗi chuyển đổi liên tiếp (Ví dụ: 1-switch: Trạng thái A -> Trạng thái B -> Trạng thái C).
  * **End-to-End Test (E2E Paths)**: Thiết kế các kịch bản kiểm thử đi từ trạng thái bắt đầu (Initial State) xuyên suốt qua các trạng thái trung gian đến trạng thái kết thúc (Final State).
  * **Final State Test**: Kiểm chứng tính đóng của trạng thái kết thúc (sau khi đơn hàng ở trạng thái hủy/hoàn thành hoặc tài khoản bị khóa, các sự kiện trái phép khác không thể làm thay đổi trạng thái nữa).
* Trình bày tài liệu này dưới định dạng Markdown để người dùng review và confirm.

### Bước 3: Phát sinh Test Case chi tiết
Sau khi người dùng confirm tài liệu phân tích ở Bước 2, Agent sinh các test case chi tiết:
* Mỗi test case được viết vào một file Markdown riêng biệt đặt trong thư mục `state-transtition-test/tests/test-cases/<FR-ID>/`.
* Định dạng tên file: `TC-<FEATURE_ID>-ST-<NUMBER>.md` (ví dụ: `TC-FR10-ST-001.md`).
* Mỗi test case phải bao gồm đầy đủ:
  - **Mã Test Case** & Tiêu đề
  - **Requirement ID**
  - **Mô tả mục tiêu kiểm thử** (Ví dụ: Kiểm thử chuyển trạng thái từ Pending sang Paid khi người dùng thanh toán thành công).
  - **Tiêu chí bao phủ tương ứng** (State / Transition / 1-switch / E2E / Final State).
  - **Trạng thái ban đầu (Preconditions)**
  - **Dữ liệu kiểm thử (Test Data)**
  - **Các bước thực hiện (Steps)**
  - **Kết quả mong đợi (Expected Result)** (phải ghi rõ trạng thái tiếp theo của thực thể trong DB hoặc UI).
  - **Trạng thái thực thi (Status)** (Mặc định: `Not Run`) & Bugs liên quan.

### Bước 4: Thực thi testcase & Tạo Bug Report
* Hướng dẫn người dùng chạy kiểm thử trên giao diện hoặc gọi API SUT.
* Nhận kết quả chạy test từ người dùng (Pass / Fail).
* Nếu có test case nào **Fail**, Agent tự động tạo 1 file Bug Report định dạng Markdown lưu vào thư mục `state-transtition-test/tests/bug/<FEATURE_ID>/` với tên file `BUG-<FEATURE_ID>-ST-<NUMBER>.md`.
* Mỗi file bug report phải có định dạng bảng chuẩn chứa: Bug ID, Tên lỗi, Found by Test Case, Các bước tái hiện, Kết quả mong đợi, Kết quả thực tế, và đề xuất sửa lỗi (suggested fix).

---

## 4. QUY TẮC ĐỊNH DẠNG DELIVERABLES

### 4.1. Template Test Case Markdown File
```markdown
# TC-<FEATURE_ID>-ST-<NUMBER>: <Tiêu đề test case ngắn gọn>

## Requirement ID
<FEATURE_ID> (Ví dụ: FR10)

## Module / Test Type / Technique
<Module> / Functional / State Transition Testing

## Target Coverage
- [ ] State Coverage
- [ ] Transition Coverage (0-switch)
- [ ] 1-switch Coverage
- [ ] End-to-End Path
- [ ] Final State Verification

## Source Design Rule
- Trạng thái bắt đầu: <State A>
- Sự kiện kích hoạt: <Event X>
- Trạng thái đích: <State B>

## Preconditions
- <Điều kiện tiên quyết, trạng thái hiện tại của thực thể trong hệ thống>

## Test Data
| Field / Resource | Value | Note |
| :--- | :--- | :--- |
| <Tên trường hoặc API body> | <Giá trị cụ thể> | <Giải thích> |

## Test Steps
1. <Bước 1>
2. <Bước 2>
3. <Bước 3>

## Expected Result
- <Kết quả mong đợi chi tiết và có thể kiểm chứng được trực quan hoặc qua database>

## Status / Related Bugs
- **Result**: Not Run
- **Related Bug**: None
```

### 4.2. Template Bug Report Markdown File
```markdown
# BUG-<FEATURE_ID>-ST-<NUMBER>: <Tiêu đề lỗi ngắn gọn>

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-<FEATURE_ID>-ST-<NUMBER>` |
| **Status** | **Open** |
| **Found by Test Case** | [TC-<FEATURE_ID>-ST-<NUMBER>](file:///absolute/path/to/test-case) |
| **Requirement Name** | <Tên chức năng / FR> |
| **Severity** | <Critical / Major / Medium / Minor / Cosmetic> |
| **Priority** | <High / Medium / Low> |
| **Preconditions** | <Trạng thái tiên quyết để tái hiện> |
| **Steps to reproduce** | 1. <Bước 1> <br> 2. <Bước 2> <br> 3. <Bước 3> |
| **Expected Result** | <Kết quả đúng theo đặc tả> |
| **Actual Result** | <Hành vi lỗi thực tế của hệ thống> |
| **Suggested Fix** | <Gợi ý sửa lỗi trong source code nếu xác định được> |
| **Date** | <YYYY-MM-DD> |
```
