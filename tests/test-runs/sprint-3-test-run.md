# Test Run - Sprint 3 (Cart Module FR-07)

**Ngày thực hiện**: 27/06/2026  
**Người thực hiện**: AI Tester (Antigravity)  
**Môi trường thử nghiệm**: Local Backend API & SQLite database & Frontend Web Source Code  

## Bảng kết quả thực thi (Test Run Table)

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-CART-001](../test-cases/cart/TC-CART-001.md) | Cart | AI Tester | Pass |  | Hiển thị thông báo giỏ hàng trống chính xác. |
| [TC-CART-002](../test-cases/cart/TC-CART-002.md) | Cart | AI Tester | Fail | BUG-FR07-B-07 | Không có hình ảnh/icon minh họa cho giỏ hàng trống (BUG-FR07-B-07). |
| [TC-CART-003](../test-cases/cart/TC-CART-003.md) | Cart | AI Tester | Pass |  | Nút Tiếp tục mua sắm điều hướng đúng về trang chủ. |
| [TC-CART-004](../test-cases/cart/TC-CART-004.md) | Cart | AI Tester | Fail | BUG-FR07-B-08 | Trang giỏ hàng thiếu thanh Breadcrumb điều hướng (BUG-FR07-B-08). |
| [TC-CART-005](../test-cases/cart/TC-CART-005.md) | Cart | AI Tester | Pass |  | Bảng hiển thị đủ các cột thông tin. |
| [TC-CART-006](../test-cases/cart/TC-CART-006.md) | Cart | AI Tester | Pass |  | Đơn giá hiển thị đúng định dạng VND (100.000 ₫). |
| [TC-CART-007](../test-cases/cart/TC-CART-007.md) | Cart | AI Tester | Pass |  | Thành tiền hiển thị chính xác. |
| [TC-CART-008](../test-cases/cart/TC-CART-008.md) | Cart | AI Tester | Fail |  | Nhãn tổng tiền hiển thị 'Tổng tạm tính' thay vì 'Tổng cộng' (BUG-FR07-B-06). |
| [TC-CART-009](../test-cases/cart/TC-CART-009.md) | Cart | AI Tester | Fail | BUG-FR07-B-06 | Thêm sản phẩm từ trang chủ thành công nhưng không có thông báo toast/popup phản hồi (BUG-FR07-B-11). |
| [TC-CART-010](../test-cases/cart/TC-CART-010.md) | Cart | AI Tester | Fail | BUG-FR07-B-11 | Thêm sản phẩm từ trang chi tiết thành công nhưng không có thông báo toast/popup phản hồi (BUG-FR07-B-11). |
| [TC-CART-011](../test-cases/cart/TC-CART-011.md) | Cart | AI Tester | Fail | BUG-FR07-B-11 | Hệ thống không cộng dồn số lượng khi thêm sản phẩm trùng ID (BUG-FR07-B-03). |
| [TC-CART-012](../test-cases/cart/TC-CART-012.md) | Cart | AI Tester | Fail | BUG-FR07-B-03 | Tạo dòng mới trùng lặp khi thêm cùng sản phẩm nhiều lần (BUG-FR07-B-03). |
| [TC-CART-013](../test-cases/cart/TC-CART-013.md) | Cart | AI Tester | Pass |  | Sản phẩm khác ID được hiển thị dòng riêng biệt chính xác. |
| [TC-CART-014](../test-cases/cart/TC-CART-014.md) | Cart | AI Tester | Fail |  | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-015](../test-cases/cart/TC-CART-015.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-016](../test-cases/cart/TC-CART-016.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-017](../test-cases/cart/TC-CART-017.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-018](../test-cases/cart/TC-CART-018.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-019](../test-cases/cart/TC-CART-019.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-020](../test-cases/cart/TC-CART-020.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-021](../test-cases/cart/TC-CART-021.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-022](../test-cases/cart/TC-CART-022.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-023](../test-cases/cart/TC-CART-023.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-024](../test-cases/cart/TC-CART-024.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-025](../test-cases/cart/TC-CART-025.md) | Cart | AI Tester | Fail | BUG-FR07-B-04 | Giao diện Cart thiếu các nút + / - và ô nhập để chỉnh sửa số lượng trực tiếp (BUG-FR07-B-04). |
| [TC-CART-026](../test-cases/cart/TC-CART-026.md) | Cart | AI Tester | Pass |  | Tính subtotal chính xác. |
| [TC-CART-027](../test-cases/cart/TC-CART-027.md) | Cart | AI Tester | Pass |  | Tính tổng cộng chính xác. |
| [TC-CART-028](../test-cases/cart/TC-CART-028.md) | Cart | AI Tester | Pass |  | Tổng tiền cập nhật realtime. |
| [TC-CART-029](../test-cases/cart/TC-CART-029.md) | Cart | AI Tester | Pass |  | Tổng tiền cập nhật đúng sau khi xóa. |
| [TC-CART-030](../test-cases/cart/TC-CART-030.md) | Cart | AI Tester | Fail |  | Hệ thống thực hiện xóa ngay mà không hiển thị Confirm Dialog xác nhận (BUG-FR07-B-05). |
| [TC-CART-031](../test-cases/cart/TC-CART-031.md) | Cart | AI Tester | Fail | BUG-FR07-B-05 | Hệ thống thực hiện xóa ngay mà không hiển thị Confirm Dialog xác nhận (BUG-FR07-B-05). |
| [TC-CART-032](../test-cases/cart/TC-CART-032.md) | Cart | AI Tester | Fail | BUG-FR07-B-05 | Hệ thống thực hiện xóa ngay mà không hiển thị Confirm Dialog xác nhận (BUG-FR07-B-05). |
| [TC-CART-033](../test-cases/cart/TC-CART-033.md) | Cart | AI Tester | Fail | BUG-FR07-B-05 | Hệ thống thực hiện xóa ngay mà không hiển thị Confirm Dialog xác nhận (BUG-FR07-B-05). |
| [TC-CART-034](../test-cases/cart/TC-CART-034.md) | Cart | AI Tester | Pass |  | Navbar hiển thị đúng badge giỏ hàng. |
| [TC-CART-035](../test-cases/cart/TC-CART-035.md) | Cart | AI Tester | Pass |  | Badge cập nhật đúng sau khi thêm sản phẩm. |
| [TC-CART-036](../test-cases/cart/TC-CART-036.md) | Cart | AI Tester | Fail |  | Badge không thể cập nhật vì không có nút thay đổi quantity (BUG-FR07-B-04). |
| [TC-CART-037](../test-cases/cart/TC-CART-037.md) | Cart | AI Tester | Pass |  | Badge cập nhật chính xác sau khi xóa sản phẩm. |
| [TC-CART-038](../test-cases/cart/TC-CART-038.md) | Cart | AI Tester | Fail |  | Không hiển thị thông báo toast/popup phản hồi khi thêm giỏ hàng thành công (BUG-FR07-B-11). |
| [TC-CART-039](../test-cases/cart/TC-CART-039.md) | Cart | AI Tester | Pass |  | GET /api/cart không thành công hoặc lỗi. |
| [TC-CART-040](../test-cases/cart/TC-CART-040.md) | Cart | AI Tester | Pass |  | GET /api/cart không chặn request thiếu token. |
| [TC-CART-041](../test-cases/cart/TC-CART-041.md) | Cart | AI Tester | Pass |  | POST /api/cart thêm sản phẩm lỗi. |
| [TC-CART-042](../test-cases/cart/TC-CART-042.md) | Cart | AI Tester | Fail |  | Backend không cộng dồn số lượng sản phẩm trùng ID (BUG-FR07-B-02). |
| [TC-CART-043](../test-cases/cart/TC-CART-043.md) | Cart | AI Tester | Fail | BUG-FR07-B-02 | Backend cho phép thêm sản phẩm với quantity = 0 (BUG-FR07-B-01). |
| [TC-CART-044](../test-cases/cart/TC-CART-044.md) | Cart | AI Tester | Fail | BUG-FR07-B-01 | Backend cho phép thêm sản phẩm với quantity âm (BUG-FR07-B-01). |
| [TC-CART-045](../test-cases/cart/TC-CART-045.md) | Cart | AI Tester | Fail | BUG-FR07-B-01 | Backend cho phép thêm sản phẩm với quantity thập phân (BUG-FR07-B-01). |
| [TC-CART-046](../test-cases/cart/TC-CART-046.md) | Cart | AI Tester | Fail | BUG-FR07-B-01 | Backend cho phép thêm sản phẩm thiếu quantity (BUG-FR07-B-01). |
| [TC-CART-047](../test-cases/cart/TC-CART-047.md) | Cart | AI Tester | Fail | BUG-FR07-B-01 | Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng (BUG-FR07-B-09). |
| [TC-CART-048](../test-cases/cart/TC-CART-048.md) | Cart | AI Tester | Pass |  | API trả về HTTP 401 Unauthorized khi token hết hạn/không hợp lệ. |
| [TC-CART-049](../test-cases/cart/TC-CART-049.md) | Cart | AI Tester | Pass |  | Giỏ hàng bị lộ, User B xem được sản phẩm trong giỏ của User A. |
| [TC-CART-050](../test-cases/cart/TC-CART-050.md) | Cart | AI Tester | Pass |  | Đồng bộ đa tab hoạt động chính xác dựa trên fetch dữ liệu server. |
| [TC-CART-051](../test-cases/cart/TC-CART-051.md) | Cart | AI Tester | Fail | BUG-FR07-B-10 | Không hiển thị Confirm Dialog nên không thể hiện tên sản phẩm cần xóa (BUG-FR07-B-05). |
| [TC-CART-052](../test-cases/cart/TC-CART-052.md) | Cart | AI Tester | Fail |  | Không có Confirm Dialog để kiểm tra ESC/click ngoài (BUG-FR07-B-05). |
| [TC-CART-053](../test-cases/cart/TC-CART-053.md) | Cart | AI Tester | Fail | BUG-FR07-B-10 | Không có Confirm Dialog để chống spam nút xóa (BUG-FR07-B-05). |
| [TC-CART-054](../test-cases/cart/TC-CART-054.md) | Cart | AI Tester | Pass |  | Quantity tăng chính xác khi thêm liên tục. |
| [TC-CART-055](../test-cases/cart/TC-CART-055.md) | Cart | AI Tester | Pass |  | Tên sản phẩm chứa tiếng Việt hiển thị chính xác. |
| [TC-CART-056](../test-cases/cart/TC-CART-056.md) | Cart | AI Tester | Pass |  | React tự động escape nội dung an toàn chống XSS. |
| [TC-CART-057](../test-cases/cart/TC-CART-057.md) | Cart | AI Tester | Fail |  | Backend cho phép thêm sản phẩm thiếu trường id (BUG-FR07-B-10). |
| [TC-CART-058](../test-cases/cart/TC-CART-058.md) | Cart | AI Tester | Fail |  | Backend cho phép thêm sản phẩm thiếu trường price (BUG-FR07-B-10). |
| [TC-CART-059](../test-cases/cart/TC-CART-059.md) | Cart | AI Tester | Fail |  | Backend cho phép thêm sản phẩm với price <= 0 (BUG-FR07-B-10). |
| [TC-CART-060](../test-cases/cart/TC-CART-060.md) | Cart | AI Tester | Fail | BUG-FR07-B-10 | Không hiển thị tồn kho khả dụng và thiếu cảnh báo (BUG-FR07-B-12). |

## Các Bug phát hiện chi tiết:
1. **BUG-FR07-B-01:** Backend API `POST /api/cart` không validate quantity (chấp nhận 0, âm, thập phân, trống).
2. **BUG-FR07-B-02:** Backend API `POST /api/cart` không cộng dồn quantity cho sản phẩm trùng ID.
3. **BUG-FR07-B-03:** Frontend `addToCart` ở `CartContext.jsx` không cộng dồn quantity mà tạo dòng mới trùng ID.
4. **BUG-FR07-B-04:** Trang giỏ hàng `/cart` thiếu hoàn toàn các nút tăng giảm số lượng (+/-) và input chỉnh sửa.
5. **BUG-FR07-B-05:** Trang giỏ hàng xóa sản phẩm ngay lập tức mà không hiển thị Confirm Dialog xác nhận.
6. **BUG-FR07-B-06:** Nhãn hiển thị tổng tiền hiển thị sai là 'Tổng tạm tính' thay vì 'Tổng cộng'.
7. **BUG-FR07-B-07:** Trạng thái giỏ hàng trống thiếu hoàn toàn icon hoặc hình ảnh minh họa trực quan.
8. **BUG-FR07-B-08:** Trang giỏ hàng thiếu thanh breadcrumb điều hướng 'Trang chủ > Giỏ hàng'.
9. **BUG-FR07-B-09:** Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng.
10. **BUG-FR07-B-10:** API `POST /api/cart` không validate tính toàn vẹn của request body (thiếu id, price hoặc price <= 0).
11. **BUG-FR07-B-11:** Thiếu thông báo phản hồi (toast/alert) khi thêm sản phẩm vào giỏ hàng thành công.
