# UI Inventory — Màn hình Quên mật khẩu (Forgot Password, 2 bước)

- **Route:** `/forgot-password` — **FR-03** (Quên mật khẩu 2 bước: nhập email lấy OTP → nhập OTP + mật khẩu mới)
- **Files đã đọc:** `frontend-web/src/pages/ForgotPassword.jsx`, `frontend-web/src/App.jsx` (route :54)
- **Runtime cross-check:** backend chạy thử OK (`POST /api/forgot-password`, `POST /api/reset-password`). Header/footer dùng chung: xem `_shared-layout.md`.

## Bước 1 — Nhập email (state `step === 1`)

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Heading (h2) | "Quên Mật Khẩu" | Đầu card, căn giữa | Tiêu đề màn hình (chung cho cả 2 bước) — IA-01 | ForgotPassword.jsx:44 |
| 2 | Form (bước 1) | form yêu cầu OTP | Card giữa trang | FR-22. **Không có step indicator** (1/2) cho luồng 2 bước — FR-22 (multi-step indicator) | ForgotPassword.jsx:46-62 |
| 3 | Label | "Nhập Email của bạn" | Trên field email | Nhãn field | ForgotPassword.jsx:49 |
| 4 | Input (**type="text"**, required) | Email | Field duy nhất bước 1 | `type="text"` thay vì `email` — FR-22 | ForgotPassword.jsx:50-56 |
| 5 | Button (submit) | "Lấy mã OTP" | Full-width, nền xanh | Gửi yêu cầu OTP → chuyển bước 2 | ForgotPassword.jsx:58-60 |
| 6 | Native dialog (điều kiện: lỗi) | `alert("Lỗi: ...")` | Popup trình duyệt | Báo lỗi bằng `alert()` thay vì UI trong trang — FR-24 (feedback nhất quán) | ForgotPassword.jsx:21 |

## Bước 2 — Nhập OTP + mật khẩu mới (state `step === 2`, render có điều kiện)

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 7 | Message box (xanh lá) | "Mã OTP của bạn là: {resetToken}" | Đầu form bước 2 | **Hiển thị thẳng mã OTP trên UI** (lấy từ response API) thay vì gửi email — đáng chú ý về bảo mật/spec FR-03 | ForgotPassword.jsx:17-18, 66-68 |
| 8 | Label | "Mã OTP (4 số)" | Trên field OTP | Nhãn field | ForgotPassword.jsx:70 |
| 9 | Input (type="text", required) | Mã OTP | Field 1 bước 2 | Nhập OTP — **không có `maxLength`/`pattern` 4 số** dù nhãn ghi "(4 số)" — FR-22 (format constraints) | ForgotPassword.jsx:71-77 |
| 10 | Label | "Mật khẩu mới" | Trên field mật khẩu | Nhãn field | ForgotPassword.jsx:80 |
| 11 | Input (type="password", required) | Mật khẩu mới | Field 2 bước 2 | Nhập mật khẩu mới (có che ký tự) | ForgotPassword.jsx:81-87 |
| 12 | Button (submit) | "Đặt lại mật khẩu" | Full-width, **nền xanh lá** | Gửi reset | ForgotPassword.jsx:91-93 |
| 13 | Button (type="button") | "← Quay lại" | Ngay dưới nút submit, full-width, **cùng màu xanh lá** (`bg-green-600`) | Quay về bước 1 — **nút phụ trùng màu/kích thước với nút hành động chính**, dễ bấm nhầm — IA-01 (visual hierarchy) | ForgotPassword.jsx:94-96 |
| 14 | Native dialog (điều kiện) | `alert('Mật khẩu quá yếu! ... KÝ TỰ ĐẶC BIỆT.')` | Popup trình duyệt | Validate mật khẩu mới bằng **regex lỗi giống Register** (yêu cầu whitespace, không nhận ký tự đặc biệt) — ForgotPassword.jsx:27 | ForgotPassword.jsx:27-31 |
| 15 | Native dialog (điều kiện) | `alert("Đổi mật khẩu thành công!")` | Popup trình duyệt | Feedback thành công → điều hướng `/login` | ForgotPassword.jsx:35-36 |
| 16 | Native dialog (điều kiện) | `alert("Mã OTP không đúng hoặc có lỗi xảy ra.")` | Popup trình duyệt | Feedback lỗi reset | ForgotPassword.jsx:38 |

**Ghi chú hành vi (chỉ thấy khi chạy):**
- Toàn bộ feedback của màn hình này dùng `alert()` native — khác hẳn pattern alert-box trong trang của Register/Login — IA-01/FR-24 (consistency).
- Quay lại bước 1 rồi lấy OTP lần nữa: message box bước 2 cập nhật OTP mới (state `message` ghi đè).
