# TC-LOGIN-015: Kiểm tra định dạng Email không hợp lệ ở cấp độ Backend
## Requirement ID
FR-02, FR-22
## Module / Test type / Technique
Login / Security & Functional / Equivalence Partitioning (Invalid Input)
## Preconditions
- Người dùng bypass giao diện HTML5 của trình duyệt bằng cách gửi yêu cầu HTTP POST trực tiếp đến `/api/login`.
## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | invalidemailform |
| Password | Test1234! |
## Test steps
1. Gửi trực tiếp yêu cầu HTTP POST đến `/api/login` với dữ liệu email `invalidemailform` và mật khẩu `Test1234!`.
2. Quan sát mã phản hồi HTTP và thông báo lỗi trả về từ Backend.
## Expected result
- Backend phải kiểm tra định dạng email và từ chối xử lý với lỗi yêu cầu không hợp lệ (ví dụ: HTTP 400 Bad Request) thay vì trực tiếp thực hiện xác minh phản hồi của API.
## Status / Related bugs
Fail / None
