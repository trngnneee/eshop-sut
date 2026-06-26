Title: [BUG][Register] Cho phép đăng ký Họ Tên vượt quá độ dài tối đa (101 ký tự)

## Found by Test Case
TC-REG-019

## Requirement liên quan
FR-01: Account registration (Họ Tên tối đa 100 ký tự)

## Severity / Priority
Major / P1

## Environment
Backend Node.js API, SQLite Database

## Steps to reproduce
1. Gọi API POST đến `/api/register` với Họ Tên dài 101 ký tự:
   ```json
   {
     "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
     "email": "tester_reg019@eshop.com",
     "password": "Secure123!",
     "confirm_password": "Secure123!"
   }
   ```

## Expected result
- Hệ thống từ chối đăng ký, trả về HTTP 400 Bad Request.
- Hiển thị thông báo lỗi: "Họ Tên quá dài (tối đa 100 ký tự)".

## Actual result
- Hệ thống trả về HTTP 200 OK và đăng ký thành công.

## Evidence
![BUG-REG-013 Screenshot](../bugs-screenshots/BUG-REG-013.png)

---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: register`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`
