---
name: use-case-testing-skill
description: Hỗ trợ tự động và bán tự động thực hiện thiết kế kịch bản Use Case Testing cho các luồng nghiệp vụ liên tương tác (user flows) trong hệ thống EShop.
---

# Use Case Testing Skill (use-case-testing-skill)

Kỹ năng này được thiết kế để dẫn dắt AI Agent thực hiện phân tích kiểm thử theo ca sử dụng, thiết kế test case, hỗ trợ chạy test và lập báo cáo lỗi cho các tính năng của EShop chứa luồng tương tác giữa Actor và hệ thống phức tạp (ví dụ: FR08 - Checkout, FR01 - Registration).

---

## 1. MỤC TIÊU & PHẠM VI ÁP DỤNG

* **Mục tiêu**: Xây dựng quy trình chuẩn thiết kế kiểm thử theo ca sử dụng (Use Case Testing) từ việc trích xuất Spec, mô tả Actor, Preconditions, Postconditions, Main Flow, Alternate Flows, Exception Flows, liệt kê các kịch bản sử dụng (Use Case Scenarios), đến sinh test case dạng file Markdown độc lập và báo cáo lỗi.
* **Môi trường chạy**: Thực hiện trực tiếp trong thư mục `use-case-tes/` của dự án (hoặc thư mục được cấu hình).

---

## 2. ĐIỀU KIỆN KÍCH HOẠT (TRIGGER CONDITIONS)

Skill này được kích hoạt khi:
* Người dùng yêu cầu thực hiện "Use Case Testing" hoặc kiểm thử theo ca sử dụng cho một tính năng.
* Người dùng nhắc đến việc thiết kế test case cho các chức năng có tính tương tác người dùng cao, quy trình đa bước (ví dụ: FR08 Checkout, FR01 Register).

---

## 3. QUY TRÌNH THỰC HIỆN TỪNG BƯỚC (STEP-BY-STEP WORKFLOW)

Agent phải tuân thủ các bước sau:

### Bước 1: Đọc đặc tả & Đề xuất Feature áp dụng
* Đọc tài liệu đặc tả `Requirements.pdf` hoặc các file tài liệu nghiệp vụ có sẵn trong dự án.
* Phân tích các tính năng có thể áp dụng Use Case Testing (các luồng tương tác có Actor rõ ràng, có luồng chính thành công và các nhánh rẽ/nhánh lỗi).
* Đề xuất danh sách feature phù hợp cho người dùng review và confirm.

### Bước 2: Thiết kế Testcase Design Analysis
Sau khi người dùng chọn feature, Agent tạo tài liệu phân tích thiết kế kịch bản test:
* **Mô tả Use Case**: Xác định rõ Actor (Người dùng, Hệ thống, Gateway...), Điều kiện tiền quyết (Preconditions), Điều kiện sau (Postconditions).
* **Luồng chính (Main Flow / Happy Path)**: Trình bày từng bước thực hiện thành công từ đầu đến cuối.
* **Các luồng rẽ nhánh (Alternate Flows)**: Các đường đi phụ dẫn đến kết quả thành công khác (ví dụ: áp mã giảm giá thành công, thay đổi địa chỉ giao hàng trước khi đặt).
* **Các luồng ngoại lệ (Exception Flows)**: Các trường hợp gặp lỗi hoặc gián đoạn dẫn đến thất bại (ví dụ: thanh toán thất bại, giỏ hàng trống, hết hàng).
* **Các kịch bản sử dụng (Use Case Scenarios)**: Liệt kê các tổ hợp đường đi qua các luồng trên (ví dụ: Scenario 1 = Main Flow; Scenario 2 = Main Flow + Alternate Flow 1; Scenario 3 = Main Flow + Exception Flow 1).
* Trình bày tài liệu này dưới định dạng Markdown để người dùng review và confirm.

### Bước 3: Phát sinh Test Case chi tiết
Sau khi người dùng confirm tài liệu phân tích ở Bước 2, Agent sinh các test case chi tiết:
* Mỗi test case được viết vào một file Markdown riêng biệt đặt trong thư mục `use-case-tes/tests/test-cases/<FR-ID>/`.
* Định dạng tên file: `TC-<FEATURE_ID>-UC-<NUMBER>.md` (ví dụ: `TC-FR08-UC-001.md`).
* Mỗi test case phải bao gồm đầy đủ:
  - **Mã Test Case** & Tiêu đề
  - **Requirement ID**
  - **Mô tả mục tiêu kiểm thử** (Ví dụ: Kiểm thử kịch bản Checkout thành công với thông tin mặc định).
  - **Use Case Scenario tương ứng**
  - **Trạng thái ban đầu (Preconditions)**
  - **Dữ liệu kiểm thử (Test Data)**
  - **Các bước thực hiện (Steps)**
  - **Kết quả mong đợi (Expected Result)** (phải chỉ rõ phản hồi của UI và trạng thái dữ liệu thay đổi trong DB).
  - **Trạng thái thực thi (Status)** (Mặc định: `Not Run`) & Bugs liên quan.

### Bước 4: Thực thi testcase & Tạo Bug Report
* Hướng dẫn người dùng chạy kiểm thử trên giao diện hoặc gọi API SUT.
* Nhận kết quả chạy test từ người dùng (Pass / Fail).
* Nếu có test case nào **Fail**, Agent tự động tạo 1 file Bug Report định dạng Markdown lưu vào thư mục `use-case-tes/tests/bug/<FEATURE_ID>/` với tên file `BUG-<FEATURE_ID>-UC-<NUMBER>.md`.
* Mỗi file bug report phải có định dạng bảng chuẩn chứa: Bug ID, Tên lỗi, Found by Test Case, Các bước tái hiện, Kết quả mong đợi, Kết quả thực tế, và đề xuất sửa lỗi (suggested fix).

---

## 4. QUY TẮC ĐỊNH DẠNG DELIVERABLES

### 4.1. Template Test Case Markdown File
```markdown
# TC-<FEATURE_ID>-UC-<NUMBER>: <Tiêu đề test case ngắn gọn>

## Requirement ID
<FEATURE_ID> (Ví dụ: FR08)

## Module / Test Type / Technique
<Module> / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: <Tên kịch bản ca sử dụng được bao phủ>

## Preconditions
- <Điều kiện tiên quyết để thực hiện test case>

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
# BUG-<FEATURE_ID>-UC-<NUMBER>: <Tiêu đề lỗi ngắn gọn>

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-<FEATURE_ID>-UC-<NUMBER>` |
| **Status** | **Open** |
| **Found by Test Case** | [TC-<FEATURE_ID>-UC-<NUMBER>](file:///absolute/path/to/test-case) |
| **Requirement Name** | <Tên chức năng / FR> |
| **Severity** | <Critical / Major / Medium / Minor / Cosmetic> |
| **Priority** | <High / Medium / Low> |
| **Preconditions** | <Trạng thái tiên quyết để tái hiện> |
| **Steps to reproduce** | 1. <Bước 1> <br> 2. <Bước 2> <br> 3. <Bước 3> |
| **Expected Result** | <Kết quả đúng theo đặc tả> |
| **Actual Result** | <Hành vi lỗi thực tế của hệ thống> |
| **Evidence** | <Đường dẫn ảnh screenshot lỗi nếu có, ví dụ: ![Evidence](evidences/BUG-ID.png)> |
| **Suggested Fix** | <Gợi ý sửa lỗi trong source code nếu xác định được> |
| **Date** | <YYYY-MM-DD> |
```
