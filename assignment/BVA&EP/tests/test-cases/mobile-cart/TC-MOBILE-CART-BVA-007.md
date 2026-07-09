# TC-MOBILE-CART-BVA-007: Chặn cập nhật hồ sơ với Số điện thoại có độ dài dưới biên (8 chữ số)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Boundary Value Analysis
## Preconditions
- Người dùng đã đăng nhập và đang ở màn hình Hồ sơ cá nhân (Profile Screen) trên mobile.
## Test data
| Full Name | Nguyễn Văn A |
| Phone input | "91234567" (8 chữ số) |
| Address | 123 Lê Lợi, Q.1, TP. HCM |
## Test steps
1. Nhập chuỗi số "91234567" vào ô nhập Số điện thoại.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo lỗi hiển thị.
## Expected result
- Ứng dụng di động hiển thị cảnh báo: "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số."
- Dữ liệu không được gửi lên API hoặc backend trả về mã lỗi validation.
- Số điện thoại trong CSDL giữ nguyên giá trị cũ.
## Status / Related bugs
Pass / None
