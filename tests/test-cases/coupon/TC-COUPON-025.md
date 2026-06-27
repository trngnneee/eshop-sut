# TC-COUPON-025: Gọi API áp dụng mã giảm giá liên tục đồng thời (Race Condition)

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Concurrency Testing

## Preconditions
- Mã VIP100 hoạt động, max_uses_per_user = 1. Người dùng đã đăng nhập.

## Test data
code: "VIP100", total_amount: 350000, gửi 10 requests đồng thời

## Test steps
1. Đăng nhập tài khoản người dùng thông thường và lấy JWT Token.
2. Gửi đồng thời 10 request POST bất đồng bộ đến endpoint `/api/coupon-usage` với body JSON chứa ID của coupon giới hạn sử dụng 1 lần:
   ```http
   POST /api/coupon-usage HTTP/1.1
   Host: localhost:3000
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "coupon_id": 1
   }
   ```

## Expected result
- Chỉ có tối đa 1 request thành công và lưu vào CSDL, 9 requests còn lại bị từ chối. Trả về 1 HTTP 200 và 9 HTTP 400.

## Status / Related bugs
Fail / [BUG-COUPON-008](../../bug-reports/BUG-COUPON-008.md)
