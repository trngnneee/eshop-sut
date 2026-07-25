# UI Inventory — Màn hình Lịch sử đơn hàng (trang Profile)

- **Route:** `/profile` — **FR-11** (Lịch sử đơn hàng). Trang này gồm 2 cột: **form Hồ sơ** (trái) và **Lịch sử đơn hàng** (phải) — kiểm kê cả hai vì cùng nằm trên 1 màn hình trong scope.
- **Files đã đọc:** `frontend-web/src/pages/Profile.jsx`, `frontend-web/src/context/AuthContext.jsx`, `frontend-web/src/App.jsx` (route :55)
- **Runtime cross-check:** backend có `GET /api/orders/my-orders`, `PUT /api/users/me`, `PUT /api/orders/:id/cancel`. Header/footer dùng chung: xem `_shared-layout.md`.

## Guard chung

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Text (điều kiện: chưa login) | "Vui lòng đăng nhập" | Giữa trang | Guard — chỉ hiện text, **không có link/redirect về trang đăng nhập** — FR-23 | Profile.jsx:109 |

## Cột trái — Hồ sơ của bạn

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 2 | Heading (h2) | "Hồ sơ của bạn" | Đầu card trái | Tiêu đề khu vực — IA-01 | Profile.jsx:114 |
| 3 | Label + Input (disabled) | "Email (Không đổi)" — nền xám | Field 1 | Email chỉ đọc — FR-22 (disabled state) | Profile.jsx:117-125 |
| 4 | Label + Input (text, required) | "Họ Tên" | Field 2 | Sửa họ tên | Profile.jsx:128-135 |
| 5 | Label + Input (text) | "Số điện thoại", placeholder "VD: 0912345678" | Field 3 | Sửa SĐT — **mâu thuẫn**: regex validate `/^[1-9][0-9]{8,9}$/` (:44) **từ chối số bắt đầu bằng 0** → chính số trong placeholder "0912345678" cũng không pass — FR-22 (format constraints: phone) | Profile.jsx:44, 138-145 |
| 6 | Label + Textarea | "Địa chỉ giao hàng", placeholder "Nhập địa chỉ của bạn" | Field 4 | Sửa địa chỉ — địa chỉ này được yêu cầu render an toàn khi hiển thị lại (mục 1 README) — cần test với `<script>` | Profile.jsx:148-156 |
| 7 | Button (submit) | "Cập nhật" | Cuối form, full-width xanh | Gửi cập nhật hồ sơ | Profile.jsx:158-163 |
| 8 | Native dialog (điều kiện) | `alert("Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số.")` | Popup trình duyệt | Validate SĐT bằng alert thay vì message trong form — FR-22 (message placement) | Profile.jsx:44-47 |
| 9 | Native dialog (điều kiện) | `alert("Cập nhật thành công!")` / `alert("Lỗi cập nhật")` | Popup trình duyệt | Feedback kết quả — FR-24 | Profile.jsx:61, 63 |

## Cột phải — Lịch sử đơn hàng (FR-11)

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 10 | Heading (h2) | "Lịch sử đơn hàng" | Đầu card phải | Tiêu đề khu vực — IA-01 | Profile.jsx:168 |
| 11 | Text (điều kiện: 0 đơn) | "Bạn chưa có đơn hàng nào." | Thay bảng | Empty state — FR-24 | Profile.jsx:169-170 |
| 12 | Table header | "Mã ĐH / Ngày đặt / Tổng tiền / Trạng thái / Thao tác" | Đầu bảng | Cấu trúc bảng đơn hàng — IA-01 | Profile.jsx:172-180 |
| 13 | Table cell (mỗi đơn) | "#{id}" (font-mono) | Cột 1 | Mã đơn hàng | Profile.jsx:185 |
| 14 | Table cell (mỗi đơn) | ngày đặt — `toLocaleDateString()` | Cột 2 | Ngày đặt — format phụ thuộc locale trình duyệt (không cố định dd/mm/yyyy) — FR-21 nếu spec quy định format | Profile.jsx:186-188 |
| 15 | Table cell (mỗi đơn) | "{total_amount} ₫" (đỏ, đậm) | Cột 3 | Tổng tiền (fallback 0 nếu null) | Profile.jsx:189-191 |
| 16 | Badge (mỗi đơn) | nhãn trạng thái VN: "Chờ xác nhận / Đã xác nhận / Đang giao / Đã giao / Đã hủy" — màu vàng/chàm/xanh dương/xanh lá/đỏ | Cột 4 | Trạng thái đơn — status lạ sẽ hiện fallback `status.toUpperCase()` (tiếng Anh) — IA-01 | Profile.jsx:83-107, 192-198 |
| 17 | Button (điều kiện: status ≠ delivered/canceled) | "Hủy đơn" (đỏ, nhỏ) | Cột 5 | Huỷ đơn — comment code (:200) xác nhận nút hiện **cả khi đơn "Đang giao"**; bấm là huỷ ngay, **không có confirmation dialog** trước hành động destructive — FR-24 | Profile.jsx:200-208 |
| 18 | Native dialog (điều kiện) | `alert("Hủy đơn thành công!")` / `alert("Lỗi: ...")` | Popup trình duyệt | Feedback huỷ đơn — FR-24 | Profile.jsx:76, 79 |

**Ghi chú hành vi (chỉ thấy khi chạy):**
- Fetch đơn hàng lỗi → chỉ `console.error` + set bảng rỗng (:26-29) → người dùng thấy "Bạn chưa có đơn hàng nào." **kể cả khi thực chất là lỗi API** — empty state và error state không phân biệt — FR-24.
- Không có loading indicator khi đang tải danh sách đơn — FR-24.
- Không có phân trang cho danh sách đơn dài — FR-23 (pagination nếu spec yêu cầu).
