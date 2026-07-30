# [BUG-GUI-01] Web Login Page UI & Accessibility Defect Pack

**Platform:** Web Frontend  
**Screen/Route:** /login  
**Related Requirement:** FR-02 (Login & Account Lockout)  
**Severity:** High | **Priority:** High  
**Status:** PENDING_EXTERNAL_ACTION  

## Description & Steps to Reproduce
1. Mở trình duyệt truy cập http://localhost:5173/login
2. Quan sát tiêu đề trang H2, nhãn label của ô nhập email, và gõ mật khẩu vào ô Password.
3. Nhấn phím Tab để kiểm tra thứ tự di chuyển con trỏ focus.
4. Bấm vào link 'Quên mật khẩu?'.

## Expected Result
- Tiêu đề H2 ghi 'Đăng Nhập'
- Nhãn ghi 'Email', type='email'
- Ô mật khẩu type='password' (che ký tự)
- Link Quên mật khẩu dùng React Router Link không reload trang
- Nút có nhãn tiếng Việt 'Đăng nhập'

## Actual Result
- Tiêu đề H2 ghi 'Đăng Ký'
- Nhãn ghi 'Username', type='text'
- Ô mật khẩu type='text' (hiển thị rõ mật khẩu bằng văn bản trần)
- Link Quên mật khẩu dùng <a> làm reload toàn trang
- Nút có nhãn 'Sign In' và hardcoded tabIndex={1}

## Evidence Screenshot
![Screenshot](../../evidence/web-login/BUG-GUI-01_web-login.png)
