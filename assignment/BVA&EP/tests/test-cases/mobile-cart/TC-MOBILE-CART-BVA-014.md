# TC-MOBILE-CART-BVA-014: Chặn cập nhật hồ sơ với Họ tên có độ dài 51 ký tự (Max+1)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen).
## Test data
| Full Name input | "Nguyen Van A Nguyen Van A Nguyen Van A Nguyen Van AB" (độ dài đúng 51 ký tự) |
| Phone | "912345678" |
| Address | 123 Lê Lợi, Q.1, TP. HCM |
## Test steps
1. Nhập chuỗi 51 ký tự trên vào ô Họ Tên.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo lỗi.
## Expected result
- Hệ thống hiển thị cảnh báo lỗi (ví dụ: "Họ tên không được vượt quá 50 ký tự").
- Dữ liệu bị chặn lại và hồ sơ trong CSDL giữ nguyên giá trị cũ.
## Status / Related bugs
Pass / None
