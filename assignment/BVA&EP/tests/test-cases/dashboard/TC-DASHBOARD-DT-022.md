# TC-DASHBOARD-DT-022: Kiểm tra các card dashboard điều hướng đúng sang trang quản lý tương ứng
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / UI/UX / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công.
- Giao diện Dashboard chứa các link hoặc card có thể click (ví dụ: Orders, Products, Users) để chuyển trang.
## Test data
- Đường dẫn điều hướng của các card/link.
## Test steps
1. Mở giao diện Dashboard.
2. Click vào card/link Orders. Quan sát và quay lại Dashboard.
3. Click vào card/link Products hoặc Users. Quan sát kết quả.
## Expected result
- Hệ thống điều hướng chính xác sang route quản lý tương ứng (ví dụ: sang danh sách đơn hàng, danh sách sản phẩm hoặc danh sách người dùng).
- Không xuất hiện lỗi 404.
- Không bị mất session đăng nhập của admin khi chuyển hướng.
## Status / Related bugs
Pass / None
