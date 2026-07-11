# TC-CHECKOUT-002: Người dùng đã đăng nhập truy cập trang thanh toán thành công

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Tài khoản `test@eshop.com` / `Test1234!` tồn tại và đã đăng nhập
- Giỏ hàng có ít nhất 1 sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | Test1234! |
| Sản phẩm trong giỏ | ≥ 1 mục |

## Test steps
1. Đăng nhập bằng tài khoản `test@eshop.com`.
2. Thêm ít nhất 1 sản phẩm vào giỏ hàng.
3. Từ trang Giỏ hàng, tiến hành thanh toán.
4. Quan sát trang Thanh toán.

## Expected result
- Người dùng đã đăng nhập được phép tiến hành thanh toán (FR-08).
- Trang Thanh toán hiển thị với thông tin đơn hàng cần xác nhận.

## Sub-domains covered
SD-A02 (đã đăng nhập hợp lệ), SD-C02 (giỏ hàng có sản phẩm)

## Type
Valid

## Status / Related bugs
Not Run / None
