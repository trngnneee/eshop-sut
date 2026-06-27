# TC-COUPON-022: Nhập mã giảm giá có dấu cách ở giữa chuỗi

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning

## Preconditions
- Đơn hàng đạt giá trị tối thiểu (300,000 VND), mã SAVE10 hoạt động, người dùng đã đăng nhập.

## Test data
code: "SAV E10", total_amount: 300000

## Test steps
1. Nhập mã "SAV E10" vào ô nhập mã.
2. Nhấn nút "Áp dụng".

## Expected result
- Hệ thống tự động trim/loại bỏ khoảng trắng ở giữa (hoặc từ chối), áp dụng mã thành công. Trả về HTTP 200.

## Status / Related bugs
Fail / [BUG-COUPON-004](../../bug-reports/BUG-COUPON-004.md)
