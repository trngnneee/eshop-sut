# FR18-X-TC02: Hiển thị địa chỉ giao hàng chứa HTML event handler dưới dạng văn bản an toàn

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning / Security

## Preconditions
- Admin đã đăng nhập bằng JWT hợp lệ.
- Có đơn hàng với `shipping_address = <img src=x onerror=alert("xss")>34 Nguyen Hue`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Endpoint | GET /api/admin/orders |
| shipping_address | <img src=x onerror=alert("xss")>34 Nguyen Hue |

## Test steps
1. Tạo hoặc seed một đơn hàng có shipping_address chứa `<img src=x onerror=alert("xss")>34 Nguyen Hue`.
2. Mở tab Quản lý Đơn hàng trong Admin UI.
3. Quan sát ô Địa chỉ của đơn hàng và kiểm tra console/browser alert.

## Expected result
- Địa chỉ được hiển thị như text đã escape, không render thành thẻ ảnh.
- Browser không thực thi onerror handler, không bật alert và DOM không tạo node `<img>` từ shipping_address.

## Status / Related bugs
Failed / BUG-FR18-X-01 - Admin UI không hiển thị địa chỉ giao hàng
