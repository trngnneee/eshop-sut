# Domain Testing Report: FR-13 – Dashboard

## 1. Feature Specifications & Analysis
- **Feature ID:** FR-13
- **Feature Name:** Dashboard
- **Role/User:** Admin User
- **Description:** Dashboard displays system overview metrics (total orders, total revenue, users count, products count) and allows navigation to detailed admin pages.
- **Preconditions:**
  - Frontend-admin and Backend are running.
  - Admin account has been created.
  - Admin has logged in and has a valid JWT token.

## 2. Equivalence Partitions (Phân vùng tương đương)

### Input Partitions: Auth & Security
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-DASH-001 | Auth Token & Role | Valid | Token hợp lệ, `role = 'admin'` | Truy cập thành công Dashboard |
| IP-DASH-001 | Auth Token & Role | Invalid | Không có token | Từ chối truy cập (HTTP 401) |
| IP-DASH-002 | Auth Token & Role | Invalid | Token hết hạn / bị sửa đổi signature | Từ chối truy cập, redirect về login |
| IP-DASH-003 | Auth Token & Role | Invalid | Token hợp lệ, `role = 'customer'` | Từ chối truy cập (HTTP 403) |

### Input Partitions: API Response Data (`GET /api/admin/orders`)
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-DASH-002 | API Response | Valid | JSON Array hợp lệ chứa các order objects | Hiển thị chính xác số liệu |
| VP-DASH-003 | API Response | Valid | JSON Array rỗng `[]` (DB trống) | Hiển thị an toàn (0 đơn, 0 ₫) |
| IP-DASH-004 | API Response | Invalid | HTTP Status 500 / Server Error | Hiển thị lỗi thân thiện, fallback UI |
| IP-DASH-005 | API Response | Invalid | JSON Object hoặc chuỗi HTML (sai format) | Bắt exception an toàn, không crash |

### Input Partitions: Order Fields (`total_amount` & `status`)
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-DASH-004 | Order Status | Valid | `status = 'delivered'` | Cộng dồn `total_amount` vào doanh thu |
| VP-DASH-005 | Order Status | Valid | `status` thuộc {pending, confirmed, shipping, canceled} | Không cộng dồn vào doanh thu |
| IP-DASH-006 | Order Amount | Invalid | `total_amount < 0` (số âm) | Bỏ qua hoặc báo lỗi dữ liệu |
| IP-DASH-007 | Order Amount | Invalid | `total_amount` là `null`, `undefined` hoặc `NaN` | Bỏ qua, hiển thị mặc định 0 ₫, không crash |

---

## 3. Domain Test Cases List
All test cases are detailed in separate files in [tests/test-cases/dashboard/](file:///c:/My%20Workspace/HCMUS/Test%20Week%203/Hw2/tests/test-cases/dashboard/):

- [TC-DASHBOARD-DT-001: Hiển thị Dashboard thành công khi có đơn hàng mẫu hợp lệ](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-001.md)
- [TC-DASHBOARD-DT-002: Chặn truy cập Dashboard đối với người dùng chưa đăng nhập (Guest)](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-002.md)
- [TC-DASHBOARD-DT-003: Chặn truy cập Dashboard đối với tài khoản vai trò thường (Customer)](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-003.md)
- [TC-DASHBOARD-DT-004: Kiểm tra phân quyền API backend khi gọi GET /api/admin/orders bằng token Customer](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-004.md)
- [TC-DASHBOARD-DT-005: Chặn truy cập khi Admin token bị sửa đổi hoặc hết hạn](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-005.md)
- [TC-DASHBOARD-DT-006: Hiển thị Dashboard khi hệ thống chưa có đơn hàng nào (Database rỗng)](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-006.md)
- [TC-DASHBOARD-DT-007: Hiển thị Dashboard khi có đơn hàng nhưng không có đơn nào ở trạng thái 'delivered'](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-007.md)
- [TC-DASHBOARD-DT-008: Xử lý lỗi thân thiện khi API GET /api/admin/orders gặp sự cố lỗi Server (HTTP 500)](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-008.md)
- [TC-DASHBOARD-DT-009: Xử lý dữ liệu khi đơn hàng có total_amount mang số tiền âm](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-009.md)
- [TC-DASHBOARD-DT-010: Xử lý dữ liệu khi đơn hàng có total_amount là null, undefined hoặc NaN](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-010.md)
- [TC-DASHBOARD-DT-011: Xử lý dữ liệu khi API trả về sai định dạng JSON (Object thay vì Array)](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-011.md)
- [TC-DASHBOARD-DT-012: Kiểm tra tính Responsive của Dashboard trên các thiết bị Desktop/Tablet/Mobile](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-012.md)
- [TC-DASHBOARD-DT-013: Kiểm tra user customer không được gọi API /api/admin/users bằng token hợp lệ](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-013.md)
- [TC-DASHBOARD-DT-014: Kiểm tra user customer không được gọi API /api/admin/orders bằng token hợp lệ](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-014.md)
- [TC-DASHBOARD-DT-015: Kiểm tra token bị chỉnh sửa role từ customer thành admin không được truy cập dashboard API](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-015.md)
- [TC-DASHBOARD-DT-016: Kiểm tra dashboard xử lý khi API /api/admin/orders trả về mảng rỗng](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-016.md)
- [TC-DASHBOARD-DT-017: Kiểm tra dashboard xử lý khi API /api/admin/users trả về lỗi 500](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-017.md)
- [TC-DASHBOARD-DT-018: Kiểm tra dashboard khi chỉ có order trạng thái pending](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-018.md)
- [TC-DASHBOARD-DT-019: Kiểm tra dashboard khi chỉ có order trạng thái cancelled](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-019.md)
- [TC-DASHBOARD-DT-020: Kiểm tra dashboard khi order thiếu field total_amount](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-020.md)
- [TC-DASHBOARD-DT-021: Kiểm tra dashboard không hiển thị raw error hoặc stack trace khi API lỗi](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-021.md)
- [TC-DASHBOARD-DT-022: Kiểm tra các card dashboard điều hướng đúng sang trang quản lý tương ứng](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-022.md)
- [TC-DASHBOARD-DT-023: Kiểm tra doanh thu không bị nhân đôi sau khi fix BUG-FR13-C-01](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-023.md)
- [TC-DASHBOARD-DT-024: Kiểm tra backend admin APIs đã kiểm tra role sau khi fix BUG-FR13-C-02](../../tests/test-cases/dashboard/TC-DASHBOARD-DT-024.md)

