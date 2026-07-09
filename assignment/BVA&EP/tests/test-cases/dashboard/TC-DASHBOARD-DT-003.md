# TC-DASHBOARD-DT-003: Chặn truy cập Dashboard đối với tài khoản vai trò thường (Customer)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Security / Equivalence Partitioning
## Preconditions
- Tài khoản khách hàng thường tồn tại (test@eshop.com / Test1234!)
- Người dùng chưa đăng nhập admin
## Test data
| Account | test@eshop.com / Test1234! (role = customer) |
## Test steps
1. Truy cập trang đăng nhập Web Admin.
2. Nhập thông tin đăng nhập của tài khoản khách hàng thường.
3. Bấm nút đăng nhập.
## Expected result
- Đăng nhập thất bại.
- Hiển thị hộp thoại cảnh báo 'Bạn không phải là admin!'.
- Người dùng không thể truy cập vào trang Dashboard.
## Status / Related bugs
Pass / None
