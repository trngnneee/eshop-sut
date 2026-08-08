# TC-LOGIN-018: Chặn truyền thông tin đăng nhập nhạy cảm qua URL Query Parameters
## Requirement ID
FR-02, SEC-01
## Module / Test type / Technique
Login / Security / Equivalence Partitioning (Input Channel Testing)
## Preconditions
- Người dùng chưa đăng nhập.
## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| URL | `http://localhost:5173/login?email=test@eshop.com&password=Test1234!` |
## Test steps
1. Nhập trực tiếp đường dẫn chứa tham số nhạy cảm vào thanh địa chỉ của trình duyệt: `http://localhost:5173/login?email=test@eshop.com&password=Test1234!` và nhấn Enter.
2. Kiểm tra xem giao diện có tự động điền (autofill) hoặc tự động submit đăng nhập bằng các giá trị trên hay không.
3. Kiểm tra xem URL trên thanh địa chỉ có hiển thị rõ mật khẩu hay không.
## Expected result
- Giao diện không tự động trích xuất thông tin nhạy cảm từ URL để điền vào form hoặc tự động đăng nhập (tránh rò rỉ thông tin qua lịch sử trình duyệt hoặc log máy chủ web).
- Mật khẩu tuyệt đối không được xuất hiện trên URL dưới dạng rõ (Plaintext).
## Status / Related bugs
Passed / None
