# FR18-X-TC03: Hiển thị địa chỉ giao hàng hợp lệ bình thường

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập bằng JWT hợp lệ.
- Có đơn hàng với địa chỉ giao hàng văn bản bình thường.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| shipping_address | 12 Le Loi, Quan 1, TP.HCM |

## Test steps
1. Mở tab Quản lý Đơn hàng trong Admin UI.
2. Tìm đơn hàng có địa chỉ `12 Le Loi, Quan 1, TP.HCM`.

## Expected result
- Admin UI hiển thị đúng nguyên văn địa chỉ hợp lệ.
- Địa chỉ không bị mất ký tự hoặc render sai định dạng.

## Status / Related bugs
Failed / BUG-FR18-X-01 - Admin UI không hiển thị địa chỉ giao hàng
