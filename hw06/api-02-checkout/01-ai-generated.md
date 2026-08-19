# API-2 — AI-generated test cases for `POST /api/checkout`

> Output thô trước audit. Các expected chưa được chỉnh để khớp SUT; mọi sửa đổi được ghi ở `02-audit.md`.

## P1 — Phân tích tham số và trạng thái

| Tham số/trạng thái | Vị trí/điều kiện | Phân vùng nhận diện |
| :--- | :--- | :--- |
| `Authorization` | Header | thiếu, Bearer hợp lệ, token sai chữ ký, token hết hạn, token user khác |
| `total_amount` | JSON body | số dương, 0, âm, chuỗi, null, thiếu, số thực, rất lớn, khoa học |
| `shipping_address` | JSON body | hợp lệ, rỗng, thiếu, Unicode, XSS, SQLi, rất dài |
| Giỏ hàng | Server state | có item, rỗng, thuộc user khác, hậu điều kiện sau checkout |
| Đơn hàng | DB state | chưa có, pending sau checkout, truy vấn lại bằng orderId |

## P2–P5 — Danh sách test case AI sinh

| TC ID | Nhóm | Tiêu đề | Preconditions | Test data | Expected result theo output AI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-CHECKOUT-001 | Partition | Checkout với giỏ có sản phẩm và total hợp lệ | User có JWT; giỏ có một sản phẩm | `total_amount=200000; shipping_address='123 Le Loi'` | 200; orderId và tổng đơn bằng 200000 |
| TC-API-CHECKOUT-002 | Partition | Không có Authorization | Giỏ không quan trọng | `Không gửi Authorization` | 401; JSON error |
| TC-API-CHECKOUT-003 | Partition | Authorization không có Bearer | Không gửi request trước | `Authorization='abc'` | 403; token malformed |
| TC-API-CHECKOUT-004 | Partition | Token sai chữ ký | Có token giả | `Authorization='Bearer invalid.signature.token'` | 403 |
| TC-API-CHECKOUT-005 | Partition | total_amount bằng 0 | User có JWT; giỏ có sản phẩm | `total_amount=0; shipping_address='A'` | 400; tổng phải dương |
| TC-API-CHECKOUT-006 | Partition | total_amount âm | User có JWT; giỏ có sản phẩm | `total_amount=-500000; shipping_address='A'` | 400; tổng phải dương |
| TC-API-CHECKOUT-007 | Partition | total_amount là chuỗi số | User có JWT; giỏ có sản phẩm | `total_amount='200000'` | 400; sai kiểu dữ liệu |
| TC-API-CHECKOUT-008 | Partition | total_amount là null | User có JWT; giỏ có sản phẩm | `total_amount=null` | 400; thiếu giá trị |
| TC-API-CHECKOUT-009 | Partition | Thiếu shipping_address | User có JWT; giỏ có sản phẩm | `Chỉ gửi total_amount=200000` | 400; shipping_address bắt buộc |
| TC-API-CHECKOUT-010 | Partition | shipping_address rỗng | User có JWT; giỏ có sản phẩm | `shipping_address=''` | 400; địa chỉ không được rỗng |
| TC-API-CHECKOUT-011 | Partition | shipping_address rất dài | User có JWT; giỏ có sản phẩm | `Chuỗi 1001 ký tự` | 400; vượt giới hạn 1000 |
| TC-API-CHECKOUT-012 | Partition | Địa chỉ chứa XSS | User có JWT; giỏ có sản phẩm | `<img src=x onerror=alert(1)>` | 400 hoặc escape payload; không lưu raw |
| TC-API-CHECKOUT-013 | Partition | Địa chỉ chứa SQLi | User có JWT; giỏ có sản phẩm | `' OR 1=1 --` | 400; không lỗi SQL và không phản chiếu |
| TC-API-CHECKOUT-014 | Partition | Địa chỉ Unicode tiếng Việt | User có JWT; giỏ có sản phẩm | `12 Lê Lợi, Quận 1, TP.HCM` | 200; giữ nguyên Unicode |
| TC-API-CHECKOUT-015 | Partition | total_amount là số thực | User có JWT; giỏ có sản phẩm | `total_amount=200000.5` | 400; tiền phải là số nguyên |
| TC-API-CHECKOUT-016 | Partition | total_amount rất lớn | User có JWT; giỏ có sản phẩm | `total_amount=9000000000000000000` | 400; overflow |
| TC-API-CHECKOUT-017 | Partition | Body có field thừa | User có JWT; giỏ có sản phẩm | `extra role='admin' cùng body hợp lệ` | 200; bỏ qua field thừa |
| TC-API-CHECKOUT-018 | Partition | total_amount dùng ký hiệu khoa học | User có JWT; giỏ có sản phẩm | `total_amount=2e5` | 200; chấp nhận vì vẫn là number |
| TC-API-CHECKOUT-019 | State | Checkout tạo đơn pending | User có JWT; giỏ có sản phẩm | `Body hợp lệ; gọi POST /api/checkout` | 200; order mới có status=pending |
| TC-API-CHECKOUT-020 | State | Giỏ bị xóa sau checkout | User có JWT; giỏ có sản phẩm | `Checkout rồi GET /api/cart` | GET cart trả [] |
| TC-API-CHECKOUT-021 | State | Gửi lại cùng request checkout | User có JWT; giỏ có sản phẩm | `Gửi cùng body hai lần` | Request thứ hai trả order cũ, không tạo trùng |
| TC-API-CHECKOUT-022 | State | Checkout khi giỏ rỗng | User có JWT; không thêm sản phẩm | `Body total_amount=1` | 400; không tạo đơn |
| TC-API-CHECKOUT-023 | State | Chuỗi cart → checkout → my-orders | User có JWT | `POST cart rồi POST checkout rồi GET my-orders` | Order xuất hiện trong my-orders với pending |
| TC-API-CHECKOUT-024 | State | orderId được trả về | User có JWT; giỏ có sản phẩm | `Checkout thành công` | orderId là integer dương |
| TC-API-CHECKOUT-025 | State | user_id lấy từ token | User A có JWT; body cố gửi user_id của B | `user_id=999 trong body` | Đơn dùng user_id từ body |
| TC-API-CHECKOUT-026 | State | Checkout sau khi login lại | User đăng nhập; giỏ có sản phẩm | `Login → add cart → checkout` | 200; pending |
| TC-API-CHECKOUT-027 | Security | Không có token | Giỏ có thể có hoặc không | `POST checkout không Authorization` | 401 |
| TC-API-CHECKOUT-028 | Security | Token sai chữ ký | Có token giả | `Bearer token bị sửa payload` | 403 |
| TC-API-CHECKOUT-029 | Security | Token hết hạn | Có JWT exp trong quá khứ | `Bearer expired JWT` | 403 |
| TC-API-CHECKOUT-030 | Security | Token của user khác | User A có cart; User B có JWT | `B checkout với body cố trỏ tới cart/order của A` | Đơn của A được tạo |
| TC-API-CHECKOUT-031 | Security | Đọc order bằng GET /api/orders/:id không token | Có orderId của user khác | `GET /api/orders/{id} không Authorization` | 401/403 |
| TC-API-CHECKOUT-032 | Security | XSS không phản chiếu ở response | User có JWT; giỏ có sản phẩm | `shipping_address='<script>alert(1)</script>'` | Không phản chiếu raw payload |
| TC-API-CHECKOUT-033 | Schema | Schema response checkout thành công | User có JWT; giỏ có sản phẩm | `Body hợp lệ` | 200; object có message:string và orderId:string |
| TC-API-CHECKOUT-034 | Schema | Content-Type response | User có JWT; giỏ có sản phẩm | `Checkout hợp lệ` | application/json |
| TC-API-CHECKOUT-035 | Schema | orderId là số nguyên | User có JWT; giỏ có sản phẩm | `Checkout thành công` | orderId integer; không phải float/string/null |
| TC-API-CHECKOUT-036 | Schema | Không lộ field nhạy cảm | User có JWT; giỏ có sản phẩm | `Checkout thành công rồi đọc order` | Response chỉ có message/orderId; không password/token nội bộ |

## Thống kê output AI

| Nhóm | Số lượng |
| :--- | ---: |
| Domain partition / BVA | 18 |
| State transition / flow | 8 |
| Security | 6 |
| Schema validation | 4 |
| **Tổng** | **36** |
