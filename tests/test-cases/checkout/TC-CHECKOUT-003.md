# TC-CHECKOUT-003: Giao diện hiển thị đầy đủ danh sách sản phẩm đặt mua

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có ít nhất 1 sản phẩm với tên, số lượng và đơn giá đã biết

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | 1 sản phẩm, số lượng = 1 |

## Test steps
1. Đăng nhập và thêm 1 sản phẩm (số lượng = 1) vào giỏ hàng.
2. Ghi nhận tên, đơn giá và số lượng từ trang Giỏ hàng.
3. Mở trang Thanh toán.
4. Đối chiếu danh sách sản phẩm hiển thị với dữ liệu giỏ hàng.

## Expected result
- Giao diện hiển thị **đầy đủ danh sách sản phẩm đặt mua** (FR-08).
- Mỗi sản phẩm hiển thị đúng tên, số lượng và thành tiền tương ứng.

## Sub-domains covered
SD-P01 (danh sách sản phẩm đầy đủ), SD-C02 (giỏ hàng có sản phẩm)

## Type
Valid

## Status / Related bugs
Not Run / None
