# TC-MOBILE-CART-BVA-015: Chặn cập nhật hồ sơ với Địa chỉ có độ dài 4 ký tự (Min-1)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen).
## Test data
| Full Name | Nguyễn Văn A |
| Phone | "912345678" |
| Address input | "HCM1" (4 ký tự) |
## Test steps
1. Nhập chuỗi "HCM1" vào ô Địa chỉ giao hàng.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo lỗi.
## Expected result
- Hệ thống hiển thị cảnh báo lỗi (ví dụ: "Địa chỉ giao hàng quá ngắn, yêu cầu tối thiểu 5 ký tự").
- Dữ liệu bị chặn lại và hồ sơ trong CSDL giữ nguyên giá trị cũ.
## Status / Related bugs
Pass / None
