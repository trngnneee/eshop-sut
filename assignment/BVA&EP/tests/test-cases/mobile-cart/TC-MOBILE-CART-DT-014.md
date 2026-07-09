# TC-MOBILE-CART-DT-014: Chặn cập nhật hồ sơ khi số điện thoại bị trống
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và đang mở tab Hồ sơ cá nhân (Profile Screen) trên mobile.
## Test data
| Full Name | "Nguyễn Văn A" |
| Phone input | "" (Trống) |
| Address | "123 Lê Lợi, Q.1, TP. HCM" |
## Test steps
1. Tại ô nhập Số điện thoại, xóa toàn bộ ký tự.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo của ứng dụng.
## Expected result
- Ứng dụng di động hiển thị cảnh báo lỗi dữ liệu (ví dụ: "Số điện thoại không hợp lệ").
- Yêu cầu cập nhật bị chặn lại ở frontend hoặc bị từ chối bởi API backend.
- Số điện thoại người dùng trong cơ sở dữ liệu không bị thay đổi thành rỗng.
## Status / Related bugs
Pass / None
