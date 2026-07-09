# TC-DASHBOARD-DT-005: Chặn truy cập khi Admin token bị sửa đổi hoặc hết hạn
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Security / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công trước đó và đang ở giao diện Admin
## Test data
| Authorization Token | Giả mạo hoặc sửa đổi vài ký tự ở phần signature của JWT |
## Test steps
1. Mở DevTools của trình duyệt (F12).
2. Đi tới Application -> Local Storage.
3. Chỉnh sửa thủ công giá trị của 'adminToken'.
4. Làm mới trang (F5) hoặc thực hiện chuyển tab trên sidebar.
5. Quan sát phản hồi hệ thống.
## Expected result
- Hệ thống nhận diện token không hợp lệ.
- Tự động xóa token sai khỏi localStorage.
- Chuyển hướng người dùng về trang Đăng nhập.
## Status / Related bugs
Pass / None
