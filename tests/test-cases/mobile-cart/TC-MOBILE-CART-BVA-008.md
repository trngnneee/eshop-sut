# TC-MOBILE-CART-BVA-008: Cập nhật hồ sơ thành công với Số điện thoại có độ dài ở biên cực tiểu (9 chữ số)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Positive / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen) trên mobile.
## Test data
| Full Name | Nguyễn Văn A |
| Phone input | "912345678" (9 chữ số) |
| Address | 123 Lê Lợi, Q.1, TP. HCM |
## Test steps
1. Nhập chuỗi số "912345678" vào ô nhập Số điện thoại.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo.
## Expected result
- Ứng dụng di động hiển thị thông báo "Cập nhật thành công!".
- Số điện thoại mới được cập nhật thành công vào cơ sở dữ liệu.
## Status / Related bugs
Not Executed
