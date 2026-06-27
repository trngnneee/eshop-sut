Title: [BUG][Coupon] Phân biệt chữ hoa/thường khi so khớp mã coupon

## Found by Test Case
TC-COUPON-023

## Requirement liên quan
FR-09: Discount coupons

## Severity / Priority
Minor / P3

## Environment
Chrome, Windows, Backend Node.js API, SQLite Database

## Steps to reproduce
1. Đăng nhập tài khoản người dùng và lấy JWT Token.
2. Gửi request POST đến endpoint `/api/apply-coupon` để áp dụng mã giảm giá viết thường `"save10"` dưới dạng API request sau:
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
Hệ thống Hệ thống tự động chuẩn hóa chữ hoa/chữ thường (ví dụ: chuyển "save10" thành chữ hoa "SAVE10") và áp dụng mã giảm giá thành công, trả về HTTP 200.

## Actual result
Hệ thống so khớp phân biệt chữ hoa/thường, từ chối áp dụng và trả về HTTP 404 với thông báo lỗi: "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa".

## Evidence
![BUG-COUPON-006 Screenshot](../bugs-screenshots/BUG-COUPON-006.png)

---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: coupon`, `severity: minor`, `priority: P3`, `status: new`, `found-by: test-case`
