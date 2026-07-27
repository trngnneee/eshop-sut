# UI Inventory — Màn hình Đăng ký (Register)

- **Route:** `/register` — **FR-01** (Đăng ký tài khoản)
- **Files đã đọc:** `frontend-web/src/pages/Register.jsx`, `frontend-web/src/App.jsx` (route :53), `frontend-web/src/config.js`
- **Runtime cross-check:** backend đã chạy thử để xác minh endpoint `POST /api/register` tồn tại. Element header/footer dùng chung: xem `_shared-layout.md`.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Heading (h2) | "Đăng Ký Tài Khoản" | Đầu card form, căn giữa | Tiêu đề màn hình — IA-01 | Register.jsx:33 |
| 2 | Alert box (điều kiện: có lỗi) | nền đỏ nhạt, chữ đỏ | **Phía trên form** (trên nút submit) | Hiển thị lỗi validate/API — FR-22 yêu cầu lỗi hiện phía trên nút submit | Register.jsx:34 |
| 3 | Form | form đăng ký | Card giữa trang | Gói 3 field + nút submit — FR-22 | Register.jsx:35 |
| 4 | Label | "Họ Tên" | Trên field 1 | Nhãn field. **Không có dấu `*` bắt buộc** dù input `required` — FR-22 (required-field indicator) | Register.jsx:37 |
| 5 | Input (text, required) | Họ Tên | Field 1 | Nhập họ tên | Register.jsx:38-44 |
| 6 | Label | "Email" | Trên field 2 | Nhãn field, không có dấu `*` | Register.jsx:47 |
| 7 | Input (**type="text"**, required) | Email | Field 2 | Nhập email — dùng `type="text"` thay vì `type="email"` → không có validate định dạng email phía client — FR-22 (input types) | Register.jsx:48-54 |
| 8 | Label | "Mật khẩu" | Trên field 3 | Nhãn field, không có dấu `*` | Register.jsx:57 |
| 9 | Input (type="password", required) | Mật khẩu | Field 3 | Nhập mật khẩu (có che ký tự) | Register.jsx:58-64 |
| 10 | Hint text | "Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt." | Dưới field mật khẩu | Mô tả quy tắc mật khẩu. **Mâu thuẫn với regex thực tế** (:16): regex yêu cầu **khoảng trắng** (`(?=.*\s)`) và chỉ cho phép `[A-Za-z\d\s]` — tức không nhận ký tự đặc biệt nào | Register.jsx:65-67 |
| 11 | Client validation | thông báo "Mật khẩu quá yếu! ... KÝ TỰ ĐẶC BIỆT." | Alert box #2 | Chặn submit khi mật khẩu không khớp regex lỗi nói trên — FR-22 (validation) | Register.jsx:16-21 |
| 12 | Button (submit) | "Đăng Ký" | Cuối form, full-width, **nền đỏ** (`bg-red-500`) | Gửi form. Màu đỏ khác nút submit xanh của Login/Forgot — IA-01 (color consistency; đỏ thường là màu destructive) | Register.jsx:71-76 |
| 13 | Link | "Đăng nhập" | Dưới nút submit | Đến `/login` cho người đã có tài khoản — FR-23 | Register.jsx:78-80 |
| 14 | Server error message | text từ `err.response.data.error` hoặc "Đăng ký thất bại." | Alert box #2 | Lỗi API (vd email trùng) — FR-24 | Register.jsx:27 |

**Ghi chú hành vi (chỉ thấy khi chạy):**
- Đăng ký **thành công** → điều hướng thẳng sang `/login`, **không có thông báo thành công** nào — đối chiếu FR-24 (action feedback).
- Không có field "Xác nhận mật khẩu" — đối chiếu FR-22 nếu spec yêu cầu confirmation-field matching.
