# [BUG-GUI-02] Web Registration Form Validation Regex & Styling Mismatch

**Platform:** Web Frontend  
**Screen/Route:** /register  
**Related Requirement:** FR-01 (Account Registration)  
**Severity:** High | **Priority:** High  
**Status:** PENDING_EXTERNAL_ACTION  

## Description & Steps to Reproduce
1. Truy cập http://localhost:5173/register
2. Nhập Họ Tên, Email '23127207_gui_01@hcmus.edu.vn'
3. Nhập mật khẩu hợp lệ chứa ký tự đặc biệt 'Password123!' theo đúng gợi ý bên dưới form.
4. Bấm nút 'Đăng Ký'.

## Expected Result
Form chấp nhận mật khẩu hợp lệ 'Password123!', tiến hành gọi API đăng ký tài khoản thành công.

## Actual Result
Form báo lỗi 'Mật khẩu quá yếu!' do regex frontend (flawedStrongPasswordRegex) bắt buộc chứa dấu khoảng trắng (\s) thay vì ký tự đặc biệt. Đồng thời trường email có type='text' và nút Đăng Ký có màu đỏ bg-red-500 bất đồng nhất.

## Evidence Screenshot
![Screenshot](../../evidence/web-register/BUG-GUI-02_web-register.png)
