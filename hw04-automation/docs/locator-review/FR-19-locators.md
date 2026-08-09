# Locator Review - FR-19 Quản Lý Người Dùng Admin

Nguồn DOM đã đọc: `frontend-admin/src/App.jsx`.

## Page Object

File: `tests/pages/AdminUserManagementPage.js`

## Locator Inventory

| Element | Locator / Helper | Dùng bởi test case | Độ ổn định |
|---|---|---|---|
| Trang admin | `page.goto("/")` | TC-FR19-01, TC-FR19-12 | Ổn định theo cấu hình admin frontend |
| Heading login | `getByRole("heading", { level: 2, name: "Admin Login" })` | TC-FR19-01, TC-FR19-12 | Khá ổn; dựa vào role heading nhưng phụ thuộc text |
| Form login | `form` filtered by login heading | TC-FR19-01, TC-FR19-12 | Khá ổn trong DOM hiện tại |
| Email input | `loginForm.getByPlaceholder("Email")` | TC-FR19-01, TC-FR19-12 | Trung bình; phụ thuộc placeholder vì input chưa có label/test id |
| Password input | `loginForm.getByPlaceholder("Password")` | TC-FR19-01, TC-FR19-12 | Trung bình; phụ thuộc placeholder vì input chưa có label/test id |
| Nút Login | `loginForm.getByRole("button", { name: "Login" })` | TC-FR19-01, TC-FR19-12 | Khá ổn; button có accessible name |
| Shell admin | `getByRole("heading", { level: 1, name: "EShop Admin" })` | TC-FR19-01, TC-FR19-12 | Ổn định để xác nhận đã vào admin dashboard |
| Tab Người dùng | `page.locator("li").filter({ hasText: "Người dùng" }).first()` | TC-FR19-01..02, TC-FR19-04, TC-FR19-14 | Trung bình; nav item là `li` clickable, chưa phải button/link semantic |
| Tab Đăng xuất | `page.locator("li").filter({ hasText: "Đăng xuất" }).first()` | hỗ trợ cleanup nếu cần | Trung bình; phụ thuộc text và `li` clickable |
| Heading quản lý user | `getByRole("heading", { level: 2, name: "Quản lý Người dùng" })` | TC-FR19-01, TC-FR19-12 | Khá ổn; role tốt nhưng phụ thuộc copy |
| Bảng user | `page.locator("table").first()` sau khi mở tab Người dùng | TC-FR19-01..06, TC-FR19-13..14 | Trung bình; ổn khi tab User đang active, nhưng app chưa có `data-testid` |
| Header bảng | `usersTable.locator("thead th")`, `headerByName(name)` | TC-FR19-02, TC-FR19-14 | Khá ổn; dựa vào semantic table |
| Dòng user | `usersTable.locator("tbody tr")` | TC-FR19-01, TC-FR19-04..07, TC-FR19-11, TC-FR19-13 | Khá ổn; dựa vào semantic table |
| Dòng theo email | `rowByEmail(email)` | TC-FR19-04..07, TC-FR19-11, TC-FR19-13 | Khá ổn vì email là dữ liệu định danh duy nhất trong test |
| Checkbox dòng | `row.locator('td input[type="checkbox"]').first()` | hỗ trợ nếu cần mở rộng batch action | Trung bình; hiện chưa thuộc yêu cầu FR-19 core |
| Cell ID/Email/Role/Số ĐT/Hành động | `row.locator("td").nth(1..5)` | TC-FR19-02, TC-FR19-04, TC-FR19-14 | Trung bình; phụ thuộc thứ tự cột hiện tại |
| Nút Xóa theo dòng | `userActionCell(row).getByRole("button", { name: "Xóa" })` | TC-FR19-05..07, TC-FR19-11, TC-FR19-13 | Khá ổn; khoanh vùng trong action cell của đúng row |
| Chờ list users API | `waitForResponse(.../api/admin/users, GET)` | TC-FR19-01, hỗ trợ setup | Ổn định vì endpoint có trong API spec |

## Review Notes

- App admin hiện chưa có `data-testid`, nên page object ưu tiên role/semantic table trước, sau đó mới dùng text hoặc vị trí cell.
- Navigation sidebar dùng thẻ `li` có `onClick`, không phải `button` hoặc `a`, nên locator tab Người dùng chưa thật sự semantic. Nếu được sửa frontend, nên đổi thành button hoặc thêm `data-testid="admin-users-tab"`.
- Bảng user có HTML semantic `table`, `thead`, `tbody`, `tr`, `td`; đây là phần ổn nhất để kiểm tra danh sách, header, row theo email và các cell bắt buộc.
- Các cell dùng `nth(1..5)` vì cột đầu tiên là checkbox. Nếu thứ tự cột thay đổi, page object cần cập nhật. Nên thêm `data-testid="user-row-${id}"`, `data-testid="user-email"`, `data-testid="user-role"` và `data-testid="delete-user"` để selector bền hơn.
- Nút Xóa được scope trong row theo email để tránh bấm nhầm user khác, đặc biệt quan trọng cho các case xóa user và self-delete.
