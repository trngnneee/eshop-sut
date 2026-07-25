# UI Inventory — Màn hình Giỏ hàng (Cart)

- **Route:** `/cart` — **FR-07** (Giỏ hàng)
- **Files đã đọc:** `frontend-web/src/pages/Cart.jsx`, `frontend-web/src/context/CartContext.jsx`, `frontend-web/src/App.jsx` (route :57)
- Header/footer dùng chung: xem `_shared-layout.md`.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Heading (h2) (điều kiện: giỏ trống) | "Giỏ hàng của bạn đang trống" | Giữa trang | Empty state — FR-24 (có, dạng text) | Cart.jsx:20-23 |
| 2 | Link (điều kiện: giỏ trống) | "Tiếp tục mua sắm" | Dưới heading empty | Về trang chủ `/` — FR-23 | Cart.jsx:24 |
| 3 | Heading (h2) | "Giỏ Hàng" | Đầu card | Tiêu đề màn hình — IA-01 | Cart.jsx:31 |
| 4 | Table header | "Sản phẩm / Giá / Số lượng / Thành tiền / Thao tác" | Đầu bảng | Cấu trúc bảng giỏ hàng — IA-01 | Cart.jsx:32-40 |
| 5 | Table cell (mỗi item) | tên sản phẩm | Cột 1 | Hiển thị `item.name` | Cart.jsx:45 |
| 6 | Table cell (mỗi item) | "{price} ₫" | Cột 2 | Đơn giá (`toLocaleString`) | Cart.jsx:46 |
| 7 | Table cell (mỗi item) | số lượng (text tĩnh) | Cột 3 | Hiển thị `item.quantity` — **không có control tăng/giảm hay sửa số lượng trong giỏ** — FR-07/FR-22 | Cart.jsx:47 |
| 8 | Table cell (mỗi item) | "{price × quantity} ₫" | Cột 4 | Thành tiền — nếu quantity là NaN (từ ProductDetail) sẽ hiện "NaN ₫" | Cart.jsx:48 |
| 9 | Button (mỗi item) | "Xóa" (link đỏ) | Cột 5 | Xoá item khỏi giỏ — **không có confirmation dialog** trước hành động destructive — FR-24 (confirmation before destructive actions) | Cart.jsx:50-55 |
| 10 | Text | "Tổng tạm tính: {cartTotal} ₫" (đỏ, đậm) | Dưới bảng, trái | Tổng tiền giỏ — FR-07 | Cart.jsx:62-64 |
| 11 | Link | "← Mua tiếp" | Dưới bảng, phải | Về trang chủ — FR-23 (back/continue links) | Cart.jsx:66-68 |
| 12 | Button | "Tiến hành thanh toán" (nền xanh lá) | Dưới bảng, phải | Đến `/checkout`; nếu **chưa đăng nhập** → `alert("Bạn cần đăng nhập để thanh toán!")` + redirect `/login` — FR-24 (dùng alert native) | Cart.jsx:11-18, 69-74 |
| 13 | Native dialog (điều kiện: chưa login) | `alert("Bạn cần đăng nhập để thanh toán!")` | Popup trình duyệt | Chặn checkout khi chưa đăng nhập | Cart.jsx:13 |

**Ghi chú hành vi (chỉ thấy khi chạy):**
- `addToCart` (CartContext.jsx:8-10) **không gộp item trùng**: thêm cùng 1 sản phẩm 2 lần → 2 dòng riêng biệt trong bảng thay vì 1 dòng quantity 2 — FR-07.
- Row dùng `key={index}` (:44) — xoá dòng giữa có thể gây render sai thứ tự (đáng test khi giỏ nhiều item).
- Giỏ hàng chỉ nằm trong React state → **refresh trang là mất toàn bộ giỏ** (xem `_shared-layout.md`).
- Sau khi redirect sang `/login` vì chưa đăng nhập, đăng nhập xong điều hướng về `/` chứ **không quay lại giỏ hàng** — FR-23.
