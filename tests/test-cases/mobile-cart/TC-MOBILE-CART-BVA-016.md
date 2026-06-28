# TC-MOBILE-CART-BVA-016: Cập nhật hồ sơ thành công với Địa chỉ có độ dài 5 ký tự (Min)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Positive / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen).
## Test data
| Full Name | Nguyễn Văn A |
| Phone | "912345678" |
| Address input | "Q1HCM" (5 ký tự) |
## Test steps
1. Nhập chuỗi "Q1HCM" vào ô Địa chỉ giao hàng.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo.
## Expected result
- Hệ thống hiển thị thông báo "Cập nhật thành công!".
- Địa chỉ mới được cập nhật thành công vào cơ sở dữ liệu.
## Status / Related bugs
Not Executed
