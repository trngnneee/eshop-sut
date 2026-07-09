# Boundary Value Analysis Report: [FEATURE_ID] - [FEATURE_NAME]

## 1. Xác Định Các Biến Biên (Boundary Variables)
* [Liệt kê các tham số đầu vào có tính chất biên, ví dụ: `quantity` (giá trị số), `username` (độ dài chuỗi)]

## 2. Khoảng Giá Trị & Giới Hạn (Ranges / Limits)
* [Xác định khoảng giá trị hợp lệ cho từng biến biên, ví dụ: `quantity` có khoảng hợp lệ `[1, 100]`]

## 3. Bảng Phân Tích Giá Trị Biên (Boundary Value Table)

| Tham Số (Variable) | Biên Dưới (Min) | Ngay Dưới Biên Dưới (Min - 1) | Ngay Trên Biên Dưới (Min + 1) | Biên Trên (Max) | Ngay Dưới Biên Trên (Max - 1) | Ngay Trên Biên Trên (Max + 1) | Giá Trị Đặc Biệt (Null / Empty / Wrong Type) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [Ví dụ: quantity] | `1` | `0` | `2` | `100` | `99` | `101` | `null`, `""`, `"abc"` |

## 4. Danh Sách Test Cases BVA (BVA Test Case Table)

| Test Case ID | Type | Objective | Preconditions | Test Data | Steps | Expected Result | Actual Result | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-[ID]-BVA-001` | Edge | [Mục tiêu test giá trị biên] | [Tiền đề] | [Dữ liệu test] | [Các bước thực hiện] | [Kết quả mong đợi] | [Ghi nhận khi chạy thực tế] | Not Executed | |

## 5. Giải Thích Chi Tiết Lựa Chọn Giá Trị (Step-by-step Explanation)
* [Giải thích tại sao lựa chọn các điểm biên cụ thể này và kỳ vọng của hệ thống đối với từng điểm biên].

## 6. Các Trường Hợp Biên Bổ Sung (Additional Edge Cases)
* [Mô tả các case biên đặc thù không chỉ phụ thuộc vào một trường độc lập, ví dụ: tồn kho thực tế của sản phẩm nhỏ hơn số lượng Max cho phép mua trong giỏ].

## 7. Ý Kiến Đánh Giá & Ghi Chú (Review Notes)
* [Ghi chú của người thực hiện review về tính đầy đủ và chính xác của các giá trị biên].
