# Test Run - FR-09 Coupon Application

__Ngày thực hiện__: [29/06/2026]  
__Người thực hiện__: Đặng Trường Nguyên  
__Môi trường thử nghiệm__: [Local Web/API, backend http://localhost:3000, frontend-web http://localhost:5173]

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Percent Discount Calculation | 1 | 0 | 1 | 0 | 1 |
| Fixed Discount Calculation | 1 | 0 | 1 | 1 | 0 |
| Minimum Order Threshold | 3 | 0 | 3 | 1 | 2 |
| Coupon Code Validation | 2 | 0 | 2 | 2 | 0 |
| Expiry Validation | 1 | 0 | 1 | 1 | 0 |
| Authentication | 1 | 0 | 1 | 0 | 1 |
| Usage Limit | 1 | 0 | 1 | 1 | 0 |
| **Tổng** | **10** | **0** | **10** | **6** | **4** |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR09-P-TC01](../test-cases/coupon_application/FR09-P-TC01.md) | Coupon Application - Percent Discount Calculation | Đặng Trường Nguyên | Failed | BUG-FR09-P-01 - Công thức giảm giá percent tính sai `discount_amount` | Expected `discount_amount = 50000`, `final_amount = 450000`; actual HTTP 200 trả `discount_amount = -4500000`, `final_amount = 5000000`. |
| [FR09-F-TC01](../test-cases/coupon_application/FR09-F-TC01.md) | Coupon Application - Fixed Discount Calculation | Đặng Trường Nguyên | Passed | None | HTTP 200; `discount_amount = 50000`, `final_amount = 550000`. |
| [FR09-T-TC01](../test-cases/coupon_application/FR09-T-TC01.md) | Coupon Application - Minimum Order Threshold | Đặng Trường Nguyên | Failed | BUG-FR09-T-01 - Hệ thống từ chối đơn hàng bằng đúng ngưỡng tối thiểu | Expected accept because `total_amount = min_order_amount = 300000`; actual HTTP 400 báo chưa đủ giá trị tối thiểu. |
| [FR09-T-TC02](../test-cases/coupon_application/FR09-T-TC02.md) | Coupon Application - Minimum Order Threshold | Đặng Trường Nguyên | Passed | None | HTTP 400 đúng kỳ vọng khi `total_amount = 299999 < min_order_amount = 300000`. |
| [FR09-T-TC03](../test-cases/coupon_application/FR09-T-TC03.md) | Coupon Application - Minimum Order Threshold | Đặng Trường Nguyên | Failed | BUG-FR09-T-01 - Hệ thống từ chối đơn hàng bằng đúng ngưỡng tối thiểu | Expected accept because `total_amount = min_order_amount = 500000`; actual HTTP 400 báo chưa đủ giá trị tối thiểu. |
| [FR09-C-TC01](../test-cases/coupon_application/FR09-C-TC01.md) | Coupon Application - Coupon Code Validation | Đặng Trường Nguyên | Passed | None | HTTP 404; response báo mã giảm giá không tồn tại hoặc bị vô hiệu hóa. |
| [FR09-C-TC02](../test-cases/coupon_application/FR09-C-TC02.md) | Coupon Application - Coupon Code Validation | Đặng Trường Nguyên | Passed | None | HTTP 400; response báo vui lòng nhập mã giảm giá. |
| [FR09-E-TC01](../test-cases/coupon_application/FR09-E-TC01.md) | Coupon Application - Expiry Validation | Đặng Trường Nguyên | Passed | None | HTTP 400; response báo mã giảm giá đã hết hạn. |
| [FR09-A-TC01](../test-cases/coupon_application/FR09-A-TC01.md) | Coupon Application - Authentication | Đặng Trường Nguyên | Failed | BUG-FR09-A-01 - API áp dụng coupon không yêu cầu JWT hợp lệ | Expected HTTP 401/403; actual HTTP 200 và áp dụng coupon khi không có `Authorization` header. |
| [FR09-U-TC01](../test-cases/coupon_application/FR09-U-TC01.md) | Coupon Application - Usage Limit | Đặng Trường Nguyên | Passed | None | HTTP 400; response báo user đã đạt giới hạn sử dụng coupon. |

## Defect Log

Sau khi chạy test, cập nhật các test case `Fail` vào bảng dưới đây hoặc map sang bug report riêng.

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR09-P-01 | FR09-P-TC01 | Công thức giảm giá percent tính sai, tạo `discount_amount` âm và `final_amount` lớn hơn tổng ban đầu. | High | Open | Actual: HTTP 200, `discount_amount = -4500000`, `final_amount = 5000000` khi áp dụng `SAVE10` cho đơn `500000`. |
| BUG-FR09-T-01 | FR09-T-TC01, FR09-T-TC03 | Hệ thống từ chối đơn hàng có tổng tiền bằng đúng `min_order_amount` dù FR-09 yêu cầu `>=`. | High | Open | Actual: HTTP 400 với thông báo chưa đủ giá trị tối thiểu khi `total_amount = min_order_amount`. |
| BUG-FR09-A-01 | FR09-A-TC01 | API `POST /api/apply-coupon` không yêu cầu JWT hợp lệ, cho phép anonymous áp dụng coupon. | High | Open | Actual: HTTP 200 và trả response thành công khi không gửi `Authorization` header. |
