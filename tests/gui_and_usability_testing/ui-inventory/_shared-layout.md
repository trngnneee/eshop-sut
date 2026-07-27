# UI Inventory — Shared Layout (Header / Footer / Page shell)

- **Phạm vi:** các element xuất hiện trên **mọi** màn hình của frontend-web (khách hàng). Liệt kê 1 lần ở đây, các file inventory từng màn hình sẽ không lặp lại.
- **Files đã đọc:** `frontend-web/src/App.jsx`, `frontend-web/index.html`
- **Runtime cross-check:** đã chạy backend (`node server.js`, port 3000) để xác minh API; dev server frontend không cần chạy vì toàn bộ nhánh render đã đọc trực tiếp từ source.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Header bar | (nền xanh `bg-blue-600`) | Đầu mọi trang | Khung điều hướng chính — FR-23, IA-01 | App.jsx:20 |
| 2 | Link (logo) | "EShop" | Header trái | Về trang chủ `/` — FR-23 | App.jsx:21 |
| 3 | Link | "Giỏ hàng" | Header phải | Đến `/cart`. **Không có badge/counter số lượng item** — đối chiếu FR-23 (badge/counter) | App.jsx:23 |
| 4 | Link (điều kiện: đã đăng nhập) | "Chào, {user.name}" (chữ vàng) | Header phải | Đến `/profile`. Render tên user bằng `dangerouslySetInnerHTML` → tên chứa HTML sẽ được thực thi (đối chiếu yêu cầu render an toàn) | App.jsx:26-28 |
| 5 | Button (điều kiện: đã đăng nhập) | **"Thoát"** (nền đỏ) | Header phải | Đăng xuất. Spec (FR-23) yêu cầu nhãn đúng là **"Đăng xuất"** | App.jsx:29 |
| 6 | Link (điều kiện: chưa đăng nhập) | "Đăng nhập" | Header phải | Đến `/login` — FR-23 | App.jsx:33 |
| 7 | Link (điều kiện: chưa đăng nhập) | "Đăng ký" | Header phải | Đến `/register` — FR-23 | App.jsx:34 |
| 8 | Footer | "© 2026 EShop SUT. Dành cho mục đích kiểm thử." | Cuối mọi trang | Thông tin bản quyền — IA-01 | App.jsx:61-63 |
| 9 | Page title (browser tab) | **"frontend-web"** | Tab trình duyệt | Cố định cho mọi màn hình, không đổi theo trang — đối chiếu FR-21 (page-title correctness) | index.html:7 |
| 10 | Favicon | vite.svg (mặc định Vite) | Tab trình duyệt | Chưa thay bằng logo EShop — IA-01 | index.html:5 |

**Ghi chú runtime/điều hướng:**
- Không có route catch-all (`*`) trong `App.jsx:50-59` → URL không hợp lệ (vd `/abc`) render **trang trắng** bên trong layout, không có trang 404 — đối chiếu FR-23 (invalid-URL handling).
- Trạng thái đăng nhập lưu token trong `localStorage` (`AuthContext.jsx:9`); giỏ hàng chỉ lưu trong state (`CartContext.jsx:6`) → **refresh trang là mất giỏ hàng** (đáng chú ý khi test back/forward).
