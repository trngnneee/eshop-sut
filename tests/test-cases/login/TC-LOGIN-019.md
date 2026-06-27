# TC-LOGIN-019: Kiểm tra chặn JWT Token giả mạo thuật toán ký (None Algorithm Bypass)
## Requirement ID
SEC-02, SEC-03
## Module / Test type / Technique
Login / Security / Equivalence Partitioning (Token Tampering)
## Preconditions
- Hệ thống đang hoạt động và người dùng thực hiện gửi yêu cầu có xác thực.
## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| JWT Token giả mạo | Phần header: `{"alg": "none", "typ": "JWT"}`<br>Phần payload: `{"id": 1, "role": "admin"}`<br>Chữ ký: (Bỏ trống) |
## Test steps
1. Tạo một JWT token giả mạo với thuật toán ký là `none` và payload tự nhận là quyền admin.
2. Gửi yêu cầu HTTP GET đến API cần xác thực `/api/users/me` hoặc API admin `/api/admin/users`, chèn token giả này vào header `Authorization: Bearer <token>`.
3. Quan sát phản hồi và mã trạng thái HTTP từ Backend.
## Expected result
- Backend phải từ chối yêu cầu và trả về lỗi xác thực (ví dụ: HTTP 403 Forbidden hoặc HTTP 401 Unauthorized).
- Tuyệt đối không được chấp nhận token sử dụng thuật toán `none` để truy cập tài nguyên.
## Status / Related bugs
Passed / None
