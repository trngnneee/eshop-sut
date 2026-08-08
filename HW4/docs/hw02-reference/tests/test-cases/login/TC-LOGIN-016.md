# TC-LOGIN-016: Kiểm tra khả năng chống tấn công Cross-Site Scripting (XSS) trên form Đăng nhập
## Requirement ID
FR-02, SEC-04
## Module / Test type / Technique
Login / Security / Equivalence Partitioning (Malicious Input)
## Preconditions
- Người dùng đang ở trang đăng nhập.
## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | `<script>alert('XSS_Email')</script>` |
| Password | `<img src=x onerror=alert('XSS_Password')>` |
## Test steps
1. Nhập payload XSS `<script>alert('XSS_Email')</script>` vào trường Email.
2. Nhập payload XSS `<img src=x onerror=alert('XSS_Password')>` vào trường Mật khẩu.
3. Nhấp nút "Đăng nhập".
4. Quan sát xem trình duyệt có hiển thị hộp thoại alert hay thực thi mã script hay không.
## Expected result
- Hệ thống từ chối đăng nhập (hiển thị thông báo lỗi tài khoản/mật khẩu không chính xác hoặc lỗi định dạng email).
- Không có đoạn mã JavaScript nào được thực thi, không xuất hiện hộp thoại cảnh báo (alert) trên trình duyệt (dữ liệu đầu vào được React render an toàn dưới dạng chuỗi thuần túy).
## Status / Related bugs
Passed / None
