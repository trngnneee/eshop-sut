# Domain Testing Report: [FEATURE_ID] - [FEATURE_NAME]

## 1. Tổng Quan Tính Năng (Feature Overview)
* **Feature ID & Name:** [FEATURE_ID] - [FEATURE_NAME]
* **Mô tả kiểm thử miền:** Thực hiện phân tích các phân vùng tương đương cho các trường đầu vào của tính năng nhằm giảm số lượng test case cần chạy nhưng vẫn đảm bảo độ bao phủ các điều kiện hợp lệ và không hợp lệ.

## 2. Xác Định Miền Dữ Liệu (Domain Identification)

### Miền đầu vào (Input Domain)
* [Liệt kê các biến đầu vào, ví dụ: `quantity` (kiểu số), `coupon_code` (kiểu chuỗi)]

### Miền đầu ra (Output Domain)
* [Liệt kê các trạng thái đầu ra của hệ thống, ví dụ: Thêm thành công (Success), Báo lỗi số lượng (Error Quantity), Báo lỗi mã giảm giá (Error Coupon)]

## 3. Phân Vùng Tương Đương (Equivalence Partitioning)

### Phân vùng hợp lệ (Valid Classes)
* **VC-01:** [Ví dụ: `quantity` nằm trong khoảng [1, 100]]
* **VC-02:** [Ví dụ: `coupon_code` để trống hoặc chứa mã hợp lệ còn hạn]

### Phân vùng không hợp lệ (Invalid Classes)
* **IC-01:** [Ví dụ: `quantity` <= 0]
* **IC-02:** [Ví dụ: `quantity` > 100]
* **IC-03:** [Ví dụ: `quantity` không phải là số nguyên (ví dụ: chữ cái, số thập phân)]
* **IC-04:** [Ví dụ: `coupon_code` chứa mã không tồn tại hoặc hết hạn]

## 4. Bảng Mô Hình Miền (Domain Model Table)

| Tham Số Đầu Vào (Input Parameter) | Phân Vùng Hợp Lệ (Valid Partitions) | Phân Vùng Không Hợp Lệ (Invalid Partitions) | Trạng Thái Hệ Thống Tương Ứng (System States/Rules) |
| :--- | :--- | :--- | :--- |
| [Ví dụ: Quantity] | `1 <= Q <= 100` | `Q <= 0`; `Q > 100`; `Q là chữ/ký tự` | Áp dụng cho nút tăng giảm số lượng sản phẩm |

## 5. Chiến Lược Thiết Kế Test Case (Test Case Design Strategy)
* Áp dụng nguyên tắc **Single Fault Assumption** đối với các phân vùng không hợp lệ: Mỗi test case kiểm tra phân vùng không hợp lệ chỉ được chứa duy nhất một tham số không hợp lệ, các tham số còn lại phải ở phân vùng hợp lệ. Điều này tránh việc các lỗi che lấp lẫn nhau.
* Kết hợp các phân vùng hợp lệ để tạo ra các kịch bản kiểm thử luồng hoạt động bình thường (Happy Path).

## 6. Danh Sách Test Cases Domain Testing (Domain Test Case Table)

| Test Case ID | Type | Objective | Preconditions | Test Data | Steps | Expected Result | Actual Result | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-[ID]-DT-001` | Positive | [Mục tiêu test] | [Tiền đề] | [Dữ liệu test] | [Các bước thực hiện] | [Kết quả mong đợi] | [Ghi nhận khi chạy thực tế] | Not Executed | |

## 7. Giải Thích Từng Bước & Thực Thi (Step-by-step Explanation)
* [Phần này giải thích chi tiết tại sao các giá trị kiểm thử cụ thể trong bảng trên lại được lựa chọn để đại diện cho từng phân vùng].

## 8. Ý Kiến Đánh Giá & Ghi Chú (Review Notes)
* [Ghi chú của người thực hiện review về tính đầy đủ và chính xác của các phân vùng đã thiết kế].
