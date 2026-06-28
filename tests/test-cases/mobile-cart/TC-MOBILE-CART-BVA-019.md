# TC-MOBILE-CART-BVA-019: Chặn cập nhật hồ sơ với Địa chỉ có độ dài 256 ký tự (Max+1)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen).
## Test data
| Full Name | Nguyễn Văn A |
| Phone | "912345678" |
| Address input | Chuỗi ký tự có độ dài đúng 256 ký tự (ví dụ: "a" lặp lại 256 lần) |
## Test steps
1. Nhập chuỗi 256 ký tự trên vào ô Địa chỉ giao hàng.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo lỗi.
## Expected result
- Hệ thống hiển thị cảnh báo lỗi (ví dụ: "Địa chỉ giao hàng không được vượt quá 255 ký tự").
- Yêu cầu cập nhật bị chặn lại ở frontend hoặc bị backend từ chối, không cập nhật CSDL.
## Status / Related bugs
Not Executed
