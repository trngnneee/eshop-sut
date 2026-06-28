# TC-MOBILE-CART-BVA-018: Cập nhật hồ sơ thành công với Địa chỉ có độ dài 255 ký tự (Max)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Positive / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen).
## Test data
| Full Name | Nguyễn Văn A |
| Phone | "912345678" |
| Address input | Chuỗi ký tự có độ dài đúng 255 ký tự (ví dụ: "123 Lê Lợi..." lặp lại cho đủ 255 ký tự) |
## Test steps
1. Nhập chuỗi 255 ký tự trên vào ô Địa chỉ giao hàng.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo.
## Expected result
- Hệ thống hiển thị thông báo "Cập nhật thành công!".
- Địa chỉ giao hàng mới được cập nhật thành công vào cơ sở dữ liệu.
## Status / Related bugs
Not Executed
