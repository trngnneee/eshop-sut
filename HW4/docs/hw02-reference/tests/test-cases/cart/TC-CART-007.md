# TC-CART-007: Thành tiền hiển thị đúng

## Requirement ID
FR-07, FR-21

## Module / Test type / Technique
Cart / Functional / Domain Testing

## Preconditions
- Người dùng đã đăng nhập vào hệ thống.
- Giỏ hàng có sản phẩm có đơn giá 100000 và số lượng là 2.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Đơn giá | `100000` |
| Số lượng | `2` |

## Test steps
1. Truy cập trang `/cart`.
2. Quan sát giá trị hiển thị tại cột 'Thành tiền' của sản phẩm đó.

## Expected result
- Thành tiền hiển thị chính xác theo công thức: Đơn giá x Số lượng = 100.000 x 2 = 200.000.
- Định dạng hiển thị là '200.000 ₫', có ký hiệu '₫' ở cuối.

## Status / Related bugs
Not Run / None
