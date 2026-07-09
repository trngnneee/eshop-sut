# TC-MOBILE-CART-DT-013: Chặn cập nhật hồ sơ khi họ tên bị trống hoặc chỉ chứa khoảng trắng
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
User Profile / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và đang mở tab Hồ sơ cá nhân (Profile Screen) trên mobile.
## Test data
| Full Name input | "   " (Chỉ chứa khoảng trắng) |
| Phone | "912345678" |
| Address | "123 Lê Lợi, Q.1, TP. HCM" |
## Test steps
1. Tại ô nhập Họ Tên, xóa hết ký tự cũ và nhập 3 khoảng trắng.
2. Nhấn nút "Cập nhật".
3. Quan sát thông báo của ứng dụng.
## Expected result
- Ứng dụng di động hiển thị Alert cảnh báo lỗi dữ liệu (ví dụ: "Họ tên không được để trống").
- Yêu cầu cập nhật hồ sơ bị chặn và không gửi API request hoặc API backend trả về lỗi HTTP 400.
- Hồ sơ người dùng trong cơ sở dữ liệu giữ nguyên họ tên cũ.
## Status / Related bugs
Pass / None
