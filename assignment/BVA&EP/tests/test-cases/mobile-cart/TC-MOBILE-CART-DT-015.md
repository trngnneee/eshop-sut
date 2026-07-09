# TC-MOBILE-CART-DT-015: Chặn cập nhật hồ sơ khi số điện thoại chứa chữ cái hoặc ký tự đặc biệt
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và đang mở tab Hồ sơ cá nhân (Profile Screen) trên mobile.
## Test data
| Full Name | "Nguyễn Văn A" |
| Phone input | "0912abc345" |
| Address | "123 Lê Lợi, Q.1, TP. HCM" |
## Test steps
1. Tại ô nhập Số điện thoại, nhập vào chuỗi "0912abc345" (chứa chữ cái).
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo của ứng dụng.
## Expected result
- Ứng dụng di động hiển thị Alert cảnh báo: "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số."
- Trình gửi yêu cầu bị chặn lại, không cho phép lưu thông tin lỗi vào cơ sở dữ liệu.
## Status / Related bugs
Fail / BUG-FR21-D-03
