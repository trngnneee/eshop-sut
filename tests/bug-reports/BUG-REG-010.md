Title: [BUG][Register] Cho phép đăng ký Họ Tên chứa ký tự đặc biệt

## Found by Test Case
TC-REG-013

## Requirement liên quan
FR-01: Account registration (Họ Tên hợp lệ, không chứa ký tự đặc biệt)

## Severity / Priority
Major / P1

## Environment
Backend Node.js API, SQLite Database

## Steps to reproduce
1. Gọi API POST đến `/api/register` với Họ Tên chứa ký tự đặc biệt (Ví dụ: `"name": "Nguyễn@Văn_A"`):
   ```json
   {
     "name": "Nguyễn@Văn_A",
     "email": "tester_reg013@eshop.com",
     "password": "Secure123!",
     "confirm_password": "Secure123!"
   }
   ```

## Expected result
- Hệ thống từ chối đăng ký, trả về HTTP 400 Bad Request.
- Hiển thị thông báo lỗi: "Họ Tên không hợp lệ".

## Actual result
- Hệ thống trả về HTTP 200 OK và đăng ký thành công cho tài khoản có tên chứa ký tự đặc biệt.

## Evidence
![BUG-REG-010 Screenshot](../bugs-screenshots/BUG-REG-010.png)

---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: register`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`
