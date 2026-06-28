# TC-MOBILE-CART-BVA-013: Cập nhật hồ sơ thành công với Họ tên có độ dài 50 ký tự (Max)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Positive / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen).
## Test data
| Full Name input | "Nguyen Van A Nguyen Van A Nguyen Van A Nguyen Van A" (độ dài đúng 50 ký tự) |
| Phone | "912345678" |
| Address | 123 Lê Lợi, Q.1, TP. HCM |
## Test steps
1. Nhập chuỗi 50 ký tự trên vào ô Họ Tên.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo.
## Expected result
- Hệ thống hiển thị thông báo "Cập nhật thành công!".
- Họ tên mới được lưu thành công vào cơ sở dữ liệu.
## Status / Related bugs
Not Executed
