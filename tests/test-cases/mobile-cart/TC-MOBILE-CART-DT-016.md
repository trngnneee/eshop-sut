# TC-MOBILE-CART-DT-016: Chặn cập nhật hồ sơ khi địa chỉ giao hàng bị trống hoặc chỉ khoảng trắng
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và đang mở tab Hồ sơ cá nhân (Profile Screen) trên mobile.
## Test data
| Full Name | "Nguyễn Văn A" |
| Phone | "912345678" |
| Address input | "    " (Chỉ chứa khoảng trắng) |
## Test steps
1. Tại ô nhập Địa chỉ giao hàng, xóa sạch và nhập vào các khoảng trắng.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo của ứng dụng.
## Expected result
- Ứng dụng di động hiển thị cảnh báo lỗi dữ liệu (ví dụ: "Địa chỉ giao hàng không được để trống").
- Yêu cầu cập nhật bị chặn lại ở frontend hoặc bị từ chối bởi API backend.
- Địa chỉ giao hàng của người dùng trong cơ sở dữ liệu không bị cập nhật thành rỗng.
## Status / Related bugs
Not Executed
