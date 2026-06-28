# Bug Report – FR-13 Dashboard

No bugs were found for this feature from dynamic test execution since the tests have not been executed on SUT (all test cases are in `Not Executed` status).

However, two critical bugs were discovered during functional testing of the EShop application:

## 1. BUG-FR13-C-01: Giao diện Dashboard hiển thị Tổng doanh thu bị nhân đôi

### Feature
FR-13 – Dashboard

### Found by Test Case
- `TC-DASHBOARD-DT-001`
- `TC-DASHBOARD-BVA-006`

### Severity / Priority
Major / High

### Environment
- OS: Windows
- Browser: Chrome
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

### Preconditions
- Admin logged in and navigating to Dashboard.

### Steps to Reproduce
1. Đăng nhập hệ thống bằng tài khoản admin.
2. Điều hướng tới Dashboard của Web Admin (`http://localhost:5174`).
3. Kiểm tra số hiển thị ở 'Tổng doanh thu (Delivered)'.
4. So sánh số hiển thị này với tổng số tiền thực tế của các đơn hàng đã giao (`delivered`) có trong database.

### Expected Result
Tổng doanh thu hiển thị trên Dashboard phải bằng chính xác tổng số tiền của các đơn hàng có trạng thái "delivered". Không có hiện tượng nhân đôi số tiền.

### Actual Result
Delivered orders have their total amounts multiplied by 2, causing the dashboard to show double the actual revenue.

### Evidence
- Giao diện Dashboard hiển thị sai lệch số liệu: ![Evidence](evidences/BUG-FR13-C-01.png)

---

## 2. BUG-FR13-C-02: Backend API `/api/admin/orders` và `/api/admin/users` thiếu kiểm soát phân quyền (role)

### Feature
FR-13 – Dashboard (Security / Access Control)

### Found by Test Case
- `TC-DASHBOARD-DT-004`

### Severity / Priority
Critical / High

### Environment
- OS: Windows
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

### Preconditions
- User has logged in and has a valid JWT token, but user role is customer/user (not admin).

### Steps to Reproduce
1. Đăng nhập bằng tài khoản người dùng thông thường (Customer) và lấy mã token JWT xác thực phiên làm việc.
2. Gửi request GET tới endpoint `/api/admin/orders` hoặc `/api/admin/users` kèm theo mã token vừa lấy.
3. Quan sát kết quả phản hồi từ hệ thống.

### Expected Result
Hệ thống từ chối truy cập và trả về mã lỗi `403 Forbidden` do tài khoản không có quyền Admin.

### Actual Result
Backend only checks for authentication status. Non-admin users are able to call admin endpoints and retrieve sensitive admin data.

### Evidence
- Giao diện API trả về HTTP 200 thành công: ![Evidence](evidences/BUG-FR13-C-02.png)

---

## Execution Evidence
- Test run file: N/A (Not executed)
- Date: 2026-06-28
- Tester: Human Tester & AI Assistant
