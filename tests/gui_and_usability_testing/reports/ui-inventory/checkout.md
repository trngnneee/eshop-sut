# UI Inventory — Màn hình Thanh toán + Mã giảm giá (Checkout)

- **Route:** `/checkout` — **FR-08** (Thanh toán), **FR-09** (Mã giảm giá)
- **Files đã đọc:** `frontend-web/src/pages/Checkout.jsx`, `frontend-web/src/context/CartContext.jsx`, `frontend-web/src/context/AuthContext.jsx`, `frontend-web/src/App.jsx` (route :58)
- **Runtime cross-check:** backend có endpoint `POST /api/apply-coupon`, `POST /api/checkout`, `POST /api/coupon-usage`. Header/footer dùng chung: xem `_shared-layout.md`.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Heading (h2) | "Xác Nhận Đơn Hàng" | Đầu card | Tiêu đề màn hình — IA-01 | Checkout.jsx:81 |
| 2 | Heading (h3) + list | "Sản phẩm:" + danh sách `<ul>` "{name} x {qty} — {tiền} ₫" | Trên cùng | Tóm tắt đơn hàng — FR-08 | Checkout.jsx:83-90 |
| 3 | Label | "Tổng tiền thanh toán (VND):" | Trên input tổng tiền | Nhãn field | Checkout.jsx:93 |
| 4 | Input (**type="number"**, editable) | tổng tiền (chữ đỏ đậm) | Giữa card | **Tổng tiền thanh toán là input CHO PHÉP NGƯỜI DÙNG SỬA TUỲ Ý** — khởi tạo từ `cartTotal`, giá trị sửa được gửi thẳng lên API checkout (:44-48) — điểm bất thường lớn nhất màn hình này (FR-08) | Checkout.jsx:15, 94-103 |
| 5 | Label | "Mã Giảm Giá" | Đầu khối coupon (nền xám) | Nhãn khu vực coupon — FR-09 | Checkout.jsx:108 |
| 6 | Input (type="text") | placeholder "Nhập mã giảm giá...", CSS `uppercase` | Khối coupon | Nhập mã — hiển thị chữ hoa bằng CSS, giá trị gửi đi được `.toUpperCase()` (:30) | Checkout.jsx:110-116 |
| 7 | Button | "Áp dụng" / "..." (khi đang gọi API) | Cạnh input coupon, nền cam | Áp mã — `disabled` khi đang áp hoặc input trống (có style `disabled:opacity-50`) — FR-24 | Checkout.jsx:117-123 |
| 8 | Text (điều kiện: coupon lỗi) | message lỗi đỏ từ API hoặc "Không thể áp dụng mã" | Dưới input coupon | Feedback coupon không hợp lệ — FR-09/FR-24 | Checkout.jsx:36, 125-127 |
| 9 | Text block (điều kiện: coupon OK) | "✅ {message}" + "Tiết kiệm: {discount} ₫" + "Thành tiền: {final} ₫" | Dưới input coupon, chữ xanh lá | Feedback coupon thành công — FR-09/FR-24 | Checkout.jsx:128-134 |
| 10 | Text | "Tổng thanh toán: {final hoặc editableTotal} ₫" (đậm, xl) | Trên nút xác nhận, căn phải | Số tiền cuối cùng — đổi theo coupon/input #4 | Checkout.jsx:137-141 |
| 11 | Button | "Xác Nhận Thanh Toán" / "Đang xử lý..." | Cuối card, full-width, xanh lá | Gửi đơn — `disabled` khi loading — FR-24 (loading state) | Checkout.jsx:143-149 |
| 12 | Native dialog (điều kiện: lỗi) | `alert("Lỗi khi thanh toán: ...")` | Popup trình duyệt | Feedback lỗi bằng alert native — FR-24 | Checkout.jsx:64 |
| 13 | Success state (điều kiện: đặt hàng OK) | h2 xanh "Thanh toán thành công!" + "Cảm ơn bạn đã mua sắm tại EShop." + button "Quay lại trang chủ" | Thay toàn bộ card | Màn hình cảm ơn — FR-24; nút quay về style như link | Checkout.jsx:69-77 |

**Ghi chú hành vi (chỉ thấy khi chạy):**
- Sửa input tổng tiền (#4) sẽ **reset kết quả coupon** (`setCouponResult(null)` :99) — nhưng người dùng có thể áp coupon trên tổng tiền đã tự sửa (coupon tính trên `editableTotal` :31).
- **Không có guard giỏ trống**: vào thẳng `/checkout` bằng URL khi giỏ rỗng vẫn render form với tổng 0 ₫ và cho phép "thanh toán" — FR-23/FR-08.
- **Không kiểm tra đăng nhập ở màn này** (chỉ Cart chặn): mở `/checkout` trực tiếp khi chưa login vẫn dùng được (token null → header Authorization bỏ trống :51).
- Sau thanh toán thành công, **giỏ hàng không được xoá** (`clearCart` được import :9 nhưng không hề gọi) — quay về trang chủ giỏ vẫn còn nguyên — FR-08/FR-24.
- Không có bước nhập/xác nhận **địa chỉ giao hàng** hay phương thức thanh toán trong flow này (địa chỉ chỉ có ở Profile) — đối chiếu FR-08 khi test.
