Title: [BUG][Profile] Thiếu validate kiểm tra định dạng chữ số trong trường Họ Tên (name)

## Found by Test Case
TC-PROFILE-005

## Requirement liên quan
FR-26: Quản lý hồ sơ cá nhân (kế thừa ràng buộc FR-01)

## Severity / Priority
Medium / P2

## Environment
Chrome, Windows, Backend Node.js API, SQLite Database

## Steps to reproduce
1. Đăng nhập tài khoản người dùng và lấy JWT Token.
2. Gửi request PUT đến endpoint `/api/users/me` với trường `name: "Nguyen Van A 123"`:
   ```http
   PUT /api/users/me HTTP/1.1
   Host: localhost:3000
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "name": "Nguyen Van A 123",
     "shipping_address": "Address Original",
     "phone": "0987654321"
   }
   ```
* **Lưu ý:** Khi thực hiện kiểm thử trên giao diện người dùng (UI), hệ thống luôn báo lỗi "Số điện thoại không hợp lệ" đối với mọi số điện thoại 10 chữ số hợp lệ, ngăn cản việc gửi form cập nhật.

## Expected result
Hệ thống Hệ thống từ chối cập nhật, trả về HTTP 400 Bad Request và báo lỗi Họ Tên không hợp lệ (không được chứa chữ số).

## Actual result
Hệ thống chấp nhận cập nhật, trả về HTTP 200 OK và lưu Họ Tên có số vào database.

## Evidence
![Ảnh lỗi API/Database](../bugs-screenshots/BUG-PROFILE-005.png)
![Ảnh lỗi giao diện (UI)](../bugs-screenshots/BUG-PROFILE-018,002,005,006,007,008,009.jpg)

---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: profile`, `severity: medium`, `priority: P2`, `status: new`, `found-by: test-case`
