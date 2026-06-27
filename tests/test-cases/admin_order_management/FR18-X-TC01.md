# FR18-X-TC01: Hiển thị địa chỉ giao hàng chứa thẻ script dưới dạng văn bản an toàn

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning / Security

## Preconditions
- Admin đã đăng nhập bằng JWT hợp lệ.
- Có đơn hàng với `shipping_address = <script>alert("xss")</script>12 Le Loi`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Endpoint | GET /api/admin/orders |
| shipping_address | <script>alert("xss")</script>12 Le Loi |

## Test steps
1. Tạo hoặc seed một đơn hàng có shipping_address chứa `<script>alert("xss")</script>12 Le Loi`.
2. Mở tab Quản lý Đơn hàng trong Admin UI.
3. Quan sát ô Địa chỉ của đơn hàng và kiểm tra console/browser alert.

## Expected result
- Địa chỉ được hiển thị như text đã escape, ví dụ thấy nội dung `<script>alert("xss")</script>12 Le Loi` dưới dạng chữ.
- Browser không thực thi script, không bật alert và DOM không tạo node `<script>` từ shipping_address.

## Status / Related bugs
Failed / BUG-FR18-X-01 - Admin UI không hiển thị địa chỉ giao hàng
