# TC-COUPON-028: Áp dụng mã sát hạn sử dụng nhưng thay đổi múi giờ client

## Requirement ID
FR-09: Discount coupons

## Module / Test type / Technique
Coupon / Functional / Timezone Security Testing

## Preconditions
- Mã EXPIRED đã hết hạn trên server nhưng múi giờ client bị chỉnh lùi lại để hiển thị chưa hết hạn.

## Test data
code: "EXPIRED", total_amount: 150000, múi giờ client bị thay đổi

## Test steps
1. Đăng nhập tài khoản người dùng và lấy JWT Token.
2. Thay đổi múi giờ/giờ hệ thống của thiết bị Client lùi lại so với Server (ví dụ lùi về năm 2019 để mã hết hạn từ 2020 trông như chưa hết hạn).
3. Gửi request POST đến endpoint `/api/apply-coupon` để áp dụng mã `EXPIRED`:
   ```http
   POST /api/apply-coupon HTTP/1.1
   Host: localhost:3000
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "code": "EXPIRED",
     "total_amount": 150000,
     "user_id": 3
   }
   ```

## Expected result
- Hệ thống chỉ sử dụng thời gian chuẩn UTC/GMT trên Server để kiểm tra hạn sử dụng, từ chối mã. Trả về HTTP 400.

## Status / Related bugs
Pass / None
