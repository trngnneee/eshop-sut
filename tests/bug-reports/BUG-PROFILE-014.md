Title: [BUG][Profile] Thiếu validate Số điện thoại chứa khoảng trắng

## Found by Test Case
TC-PROFILE-014

## Requirement liên quan
FR-26: Quản lý hồ sơ cá nhân

## Severity / Priority
Medium / P2

## Environment
Chrome, Windows, Backend Node.js API, SQLite Database

## Steps to reproduce
1. Đăng nhập tài khoản người dùng và lấy JWT Token.
2. Gửi request PUT đến endpoint `/api/users/me` với trường `phone: "0912 345 678"`:
   ```http
   PUT /api/users/me HTTP/1.1
   Host: localhost:3000
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "name": "Nguyen Van A",
     "shipping_address": "Address Original",
     "phone": "0912 345 678"
   }
   ```

## Expected result
Hệ thống Hệ thống từ chối cập nhật, trả về HTTP 400 Bad Request và báo lỗi Số điện thoại không được chứa khoảng trắng.

## Actual result
Hệ thống chấp nhận cập nhật, trả về HTTP 200 OK và lưu số điện thoại chứa khoảng trắng vào database.

## Evidence
![Ảnh lỗi API/Database](../bugs-screenshots/BUG-PROFILE-014.png)

---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: profile`, `severity: medium`, `priority: P2`, `status: new`, `found-by: test-case`
