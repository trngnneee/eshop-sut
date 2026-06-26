Title: [BUG][Register] Cho phép đăng ký Họ Tên quá ngắn (1 ký tự)

## Found by Test Case
TC-REG-018

## Requirement liên quan
FR-01: Account registration (Họ Tên tối thiểu từ 2 ký tự trở lên)

## Severity / Priority
Major / P1

## Environment
Backend Node.js API, SQLite Database

## Steps to reproduce
1. Gọi API POST đến `/api/register` với Họ Tên dài 1 ký tự (Ví dụ: `"name": "A"`):
   ```json
   {
     "name": "A",
     "email": "tester_reg018@eshop.com",
     "password": "Secure123!",
     "confirm_password": "Secure123!"
   }
   ```

## Expected result
- Hệ thống từ chối đăng ký, trả về HTTP 400 Bad Request.
- Hiển thị thông báo lỗi: "Họ Tên quá ngắn".

## Actual result
- Hệ thống trả về HTTP 200 OK và đăng ký thành công.

## Evidence
![BUG-REG-012 Screenshot](../bugs-screenshots/BUG-REG-012.png)

---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: register`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`
