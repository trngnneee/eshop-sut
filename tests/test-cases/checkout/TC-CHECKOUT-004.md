# TC-CHECKOUT-004: Tổng tiền thanh toán không cho phép người dùng chỉnh sửa trực tiếp

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có ít nhất 1 sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tổng tiền kỳ vọng | Tự động tính từ giỏ hàng |

## Test steps
1. Đăng nhập, thêm sản phẩm vào giỏ và mở trang Thanh toán.
2. Ghi nhận tổng tiền hiển thị.
3. Thử thay đổi tổng tiền thanh toán trên giao diện (nếu có trường nhập liệu).

## Expected result
- **Tổng tiền thanh toán được tính tự động từ giỏ hàng và không cho phép người dùng chỉnh sửa trực tiếp** (FR-08).
- Người dùng không thể thay đổi giá trị tổng tiền trên UI.

## Sub-domains covered
SD-T02 (tổng tiền không cho chỉnh sửa)

## Type
Valid

## Status / Related bugs
Not Run / None
