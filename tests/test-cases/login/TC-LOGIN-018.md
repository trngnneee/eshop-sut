# TC-LOGIN-018: Kiểm tra ngắt kết nối mạng khi đang gửi yêu cầu Đăng nhập
## Requirement ID
FR-02, FR-24
## Module / Test type / Technique
Login / Reliability & Functional / State Transition (Exception Handling)
## Preconditions
- Người dùng đang ở trang đăng nhập của Frontend Web.
## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Password | Test1234! |
## Test steps
1. Nhập thông tin đăng nhập hợp lệ.
2. Nhấp nút "Đăng nhập".
3. Ngay lập tức ngắt kết nối mạng (Disconnect Internet / Simulation offline) khi yêu cầu HTTP đang được gửi đi và chưa nhận được phản hồi từ backend.
4. Quan sát phản hồi của giao diện người dùng (Frontend) sau khi timeout hoặc kết nối mạng bị đứt.
## Expected result
- Giao diện không bị crash hay đứng màn hình (frozen).
- Trạng thái loading kết thúc, nút "Đăng nhập" được khôi phục về trạng thái active (bỏ disabled).
- Hiển thị thông báo lỗi thân thiện với người dùng về sự cố kết nối mạng (ví dụ: "Không thể kết nối đến máy chủ. Vui lòng kiểm tra lại mạng.") thay vì in lỗi raw code/exception.
## Status / Related bugs
Failed / None
