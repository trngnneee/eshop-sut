# TC-CART-007: Đơn giá hiển thị đúng định dạng VND

## Requirement ID
FR-07, FR-21

## Module / Test type / Technique
Cart / Functional / Domain Testing

## Preconditions
- Người dùng đã đăng nhập vào hệ thống.
- Giỏ hàng có ít nhất 1 sản phẩm với giá trị số nguyên cụ thể.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Đơn giá sản phẩm | `100000` |

## Test steps
1. Truy cập trang `/cart`.
2. Quan sát giá trị hiển thị tại cột 'Đơn giá'.

## Expected result
- Đơn giá hiển thị đúng định dạng tiền tệ Việt Nam (VND).
- Đơn giá hiển thị là '100.000 ₫', có ký hiệu '₫' ở cuối và có dấu chấm phân tách hàng nghìn.

## Status / Related bugs
Not Run / None
