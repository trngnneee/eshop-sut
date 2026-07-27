# UI Inventory — Màn hình Đăng nhập (Login)

- **Route:** `/login` — **FR-02** (Đăng nhập, kèm khoá tài khoản sau 3 lần sai / 30 giây)
- **Files đã đọc:** `frontend-web/src/pages/Login.jsx`, `frontend-web/src/context/AuthContext.jsx`, `frontend-web/src/App.jsx` (route :52)
- **Runtime cross-check:** backend chạy thử OK. Header/footer dùng chung: xem `_shared-layout.md`.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Heading (h2) | **"Đăng Ký"** | Đầu card form, căn giữa | Tiêu đề màn hình — **sai nội dung**: đây là trang Đăng nhập nhưng heading ghi "Đăng Ký" — FR-21/IA-01 | Login.jsx:24 |
| 2 | Form | form đăng nhập | Card giữa trang | Gói 2 field + nút submit — FR-22 | Login.jsx:26 |
| 3 | Label | **"Username"** | Trên field 1 | Nhãn field — thực tế field này nhập **email** (state `email`, gửi lên `/api/login` dưới key `email`); nhãn tiếng Anh giữa UI tiếng Việt — IA-01 (consistency) | Login.jsx:28 |
| 4 | Input (type="text", required) | Email/Username | Field 1 | Nhập email đăng nhập | Login.jsx:29-35 |
| 5 | Label | "Mật khẩu" | Trên field 2 | Nhãn field | Login.jsx:38 |
| 6 | Input (**type="text"**, required) | Mật khẩu | Field 2 | Nhập mật khẩu — **không che ký tự** (`type="text"` thay vì `password`) — FR-22 (input masking) | Login.jsx:39-45 |
| 7 | Link (thẻ `<a href>`) | "Quên mật khẩu?" | Dưới field mật khẩu, căn phải | Đến `/forgot-password` — dùng `<a>` thay vì `<Link>` → **full page reload** thay vì SPA navigation — FR-23 | Login.jsx:49-51 |
| 8 | Button (submit) | **"Sign In"** | Full-width, nền xanh | Gửi form — nhãn tiếng Anh giữa UI tiếng Việt — IA-01; có **`tabIndex={1}`** → phá thứ tự tab tự nhiên của form (nút được focus TRƯỚC các input) — FR-22 (tab order) | Login.jsx:53-58 |
| 9 | Link | "Đăng ký ngay" | Dưới nút submit | Đến `/register` — FR-23 | Login.jsx:61-63 |
| 10 | Error box (điều kiện: có lỗi) | "Đăng nhập thất bại. Vui lòng kiểm tra lại." | **Phía dưới form** (dưới nút submit) | Lỗi đăng nhập — spec FR-22 yêu cầu lỗi hiện **phía trên** nút submit; message chung chung, **không phân biệt trường hợp tài khoản bị khoá** (3 lần sai/30s theo FR-02) | Login.jsx:17-19, 66 |

**Ghi chú hành vi (chỉ thấy khi chạy):**
- Đăng nhập thành công → điều hướng về `/`, không có thông báo chào mừng; header đổi sang "Chào, {name}" + nút "Thoát" (xem `_shared-layout.md`).
- Khi backend trả lỗi khoá tài khoản, UI vẫn chỉ hiện message chung ở dòng 18 — cần test tay để xác nhận (FR-02 + FR-24 lockout messaging).
