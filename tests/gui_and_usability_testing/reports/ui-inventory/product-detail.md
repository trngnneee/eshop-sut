# UI Inventory — Màn hình Chi tiết sản phẩm (Product Detail)

- **Route:** `/product/:id` — **FR-06** (Chi tiết sản phẩm)
- **Files đã đọc:** `frontend-web/src/pages/ProductDetail.jsx`, `frontend-web/src/context/CartContext.jsx`, `frontend-web/src/App.jsx` (route :56)
- **Runtime cross-check (backend đã chạy):** `GET /api/products/999` (id không tồn tại) trả về `{}` → kích hoạt nhánh render #2 bên dưới. Header/footer dùng chung: xem `_shared-layout.md`.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Text (điều kiện: đang fetch) | "Đang tải..." | Toàn màn hình | Loading state — chỉ là plain text, không spinner/skeleton — FR-24 (loading indicators) | ProductDetail.jsx:34 |
| 2 | Text (điều kiện: id không tồn tại) | "Sản phẩm không tồn tại (Lỗi trắng trang do data rỗng)" | Toàn màn hình | Empty state khi API trả `{}` (xác nhận runtime) — FR-24 | ProductDetail.jsx:35-36 |
| 3 | Image | ảnh sản phẩm, `alt={product.name}` | Nửa trái (desktop) / trên (mobile) | Ảnh sản phẩm — có alt (khác Home) — IA-01 | ProductDetail.jsx:41-45 |
| 4 | Heading (h1) | tên sản phẩm | Nửa phải | Tiêu đề — IA-01 | ProductDetail.jsx:48 |
| 5 | Text | "{price} ₫" (đỏ, đậm, 2xl) | Dưới tên | Giá — comment trong code (:49) thừa nhận có thể hiện **NaN** nếu price sai định dạng từ backend — FR-21 | ProductDetail.jsx:50-52 |
| 6 | Text | mô tả sản phẩm | Dưới giá | `product.description` | ProductDetail.jsx:53 |
| 7 | Label | "Số lượng:" | Cạnh input số lượng | Nhãn field | ProductDetail.jsx:56 |
| 8 | Input (type="number") | số lượng, mặc định 1 | Cạnh label | Chọn số lượng — **không có `min`/`max`** → cho phép 0, số âm, để trống — FR-22 (format constraints: quantity) | ProductDetail.jsx:57-62 |
| 9 | Button | "Thêm vào giỏ hàng" / "Đã thêm" (2 giây) | Dưới cùng nửa phải, nền xanh lá | Thêm vào giỏ. **3 điểm đáng chú ý:** (a) lần bấm **đầu tiên không làm gì** — biến `clickCount` nuốt click đầu (:23-26); (b) class **`bug-mobile-hidden`** trên nút → khả năng bị ẩn trên viewport mobile; (c) feedback đổi nhãn thành "Đã thêm" trong 2s — FR-24 | ProductDetail.jsx:22-32, 65-70 |

**Ghi chú hành vi (chỉ thấy khi chạy):**
- Số lượng được parse bằng `parseInt(quantity)` (:28) — nhập trống/chữ → `NaN` vẫn được thêm vào giỏ, dẫn tới "Thành tiền" NaN bên màn Giỏ hàng.
- Fetch lỗi chỉ `console.error` (:19), người dùng kẹt ở "Đang tải..." vô hạn nếu backend chết — FR-24.
- Class `bug-mobile-hidden` được định nghĩa tại `frontend-web/src/index.css:10-14` (dưới comment "Custom CSS to simulate UI bugs"): trên viewport ≤ 640px áp `margin-right: -100px` → nút "Thêm vào giỏ hàng" bị lệch/tràn layout trên mobile — cần xác nhận bằng test tay ở viewport hẹp (FR-21 responsive).
