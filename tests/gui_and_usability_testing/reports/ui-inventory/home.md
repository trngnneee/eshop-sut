# UI Inventory — Trang chủ / Danh sách sản phẩm + Tìm kiếm (Home)

- **Route:** `/` — **FR-05** (Danh sách + tìm kiếm sản phẩm)
- **Files đã đọc:** `frontend-web/src/pages/Home.jsx`, `frontend-web/src/context/CartContext.jsx`, `frontend-web/src/App.jsx` (route :51)
- **Runtime cross-check (backend đã chạy):**
  - `GET /api/products` → 5 sản phẩm seed (iPhone 15 Pro Max, Samsung S24 Ultra, MacBook Pro M3, AirPods Pro 2, Keychron Q1); ảnh từ `placehold.co` (external host).
  - `GET /api/products?search='` → backend trả **raw HTML** `<h1>Database Error</h1><p>SQLITE_ERROR...</p>` → Home render thẳng khối HTML này (dòng 69-73).
- Header/footer dùng chung: xem `_shared-layout.md`.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Heading (h1) | "Danh sách sản phẩm" | Đầu trang, bên trái | Tiêu đề màn hình — IA-01 | Home.jsx:44 |
| 2 | Form (search) | form tìm kiếm | Đầu trang, bên phải | Gửi query tìm kiếm — FR-05 | Home.jsx:45-59 |
| 3 | Input (type="text") | placeholder "Tìm kiếm..." | Trong form search | Nhập từ khoá; cho phép submit rỗng (không `required`) | Home.jsx:46-52 |
| 4 | Button (submit) | "Tìm" | Cạnh input search | Thực hiện tìm kiếm | Home.jsx:53-58 |
| 5 | Text (điều kiện: có từ khoá) | "Kết quả tìm kiếm cho: {search}" | Dưới thanh search | Echo từ khoá — render bằng **`dangerouslySetInnerHTML`** → từ khoá chứa HTML/`<script>` được chèn thẳng vào DOM — đối chiếu yêu cầu render an toàn (mục 1 README/FR-24) | Home.jsx:62-67 |
| 6 | HTML block (điều kiện: backend trả HTML lỗi) | khối đỏ chứa nguyên trang lỗi backend | Thay thế grid sản phẩm | Render **raw HTML lỗi từ backend** bằng `dangerouslySetInnerHTML` (xác nhận runtime với search `'`) — FR-24 (error feedback) | Home.jsx:19-21, 69-73 |
| 7 | Grid | grid sản phẩm responsive 1/2/3 cột (sm/md) | Thân trang | Danh sách card sản phẩm — IA-01 (responsive) | Home.jsx:75 |
| 8 | Image (mỗi card) | ảnh sản phẩm, **`alt=""`** | Đầu card | Ảnh từ `p.imageUrl` (host ngoài `placehold.co`) — **alt rỗng** — FR-21/FR-24 (image alt-text) | Home.jsx:81-85 |
| 9 | Heading (h2, mỗi card) | tên sản phẩm (class `truncate`) | Card | Tên sản phẩm, cắt bớt nếu dài — đáng test với tên rất dài | Home.jsx:86 |
| 10 | Text (mỗi card) | "{price} **VND**" (đỏ, đậm) | Card | Giá — dùng đơn vị "VND" trong khi các màn khác dùng "₫" — IA-01 (consistency) | Home.jsx:87-89 |
| 11 | Link (mỗi card) | "Xem chi tiết" | Cuối card, trái | Đến `/product/{id}` — FR-23 | Home.jsx:91-96 |
| 12 | Button (mỗi card) | "Thêm vào giỏ" | Cuối card, phải | Thêm 1 sản phẩm vào giỏ — **không có bất kỳ feedback nào** sau khi bấm (không toast, header cũng không có badge) — FR-24 (action feedback) | Home.jsx:98-103 |
| 13 | Text (điều kiện: có sản phẩm) | "Hiển thị {N} sản phẩm" | Cuối trang, căn giữa | Đếm kết quả — dùng thẻ **h1** cho dòng chú thích (sai cấp heading, trang có 2 h1) — IA-01 | Home.jsx:110-114 |

**Trạng thái render có điều kiện (không hiển thị mặc định):**
- **Loading:** không có indicator nào khi đang fetch (`fetchProducts` không set loading state) — FR-24 (loading indicators). — Home.jsx:13-30
- **Empty (0 kết quả):** không có thông báo "không tìm thấy"; grid trống + dòng đếm (#13) cũng ẩn vì `products.length > 0` — FR-24 (empty-state visuals). — Home.jsx:75-114
- **Lỗi network (backend chết):** nếu response không phải string HTML thì bị nuốt im lặng (không nhánh else ở :26-29) → trang trống không báo lỗi.
