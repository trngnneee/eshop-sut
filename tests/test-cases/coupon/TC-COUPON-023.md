# TC-COUPON-023: Nhập mã giảm giá viết thường

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Equivalence Partitioning

## Preconditions
- Đơn hàng đạt giá trị tối thiểu (300,000 VND), mã SAVE10 hoạt động, người dùng đã đăng nhập.

## Test data
code: "save10", total_amount: 300000

## Test steps
1. Đăng nhập tài khoản người dùng và lấy JWT Token.
2. Gửi request POST đến endpoint `/api/apply-coupon` để áp dụng mã giảm giá viết thường `"save10"`:
   ```http
   POST /api/apply-coupon HTTP/1.1
   Host: localhost:3000
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "code": "save10",
     "total_amount": 300000,
     "user_id": 3
   }
   ```

## Expected result
- Hệ thống tự động chuyển thành chữ hoa "SAVE10" và áp dụng thành công. Trả về HTTP 200.

## Status / Related bugs
Fail / [BUG-COUPON-006](../../bug-reports/BUG-COUPON-006.md)
