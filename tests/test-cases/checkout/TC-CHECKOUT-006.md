# TC-CHECKOUT-006: Thanh toán thành công với người dùng đã đăng nhập và giỏ hàng hợp lệ (on-point)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập (`test@eshop.com`)
- Giỏ hàng có ít nhất 1 sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | Test1234! |
| Sản phẩm | 1 sản phẩm bất kỳ, số lượng ≥ 1 |

## Test steps
1. Đăng nhập bằng `test@eshop.com` / `Test1234!`.
2. Thêm sản phẩm vào giỏ hàng.
3. Mở trang Thanh toán; xác nhận danh sách sản phẩm và tổng tiền.
4. Xác nhận thanh toán.

## Expected result
- Thanh toán hoàn tất thành công.
- Tổng tiền đơn hàng khớp tổng giỏ hàng tại thời điểm thanh toán.

## Sub-domains covered
SD-A02 (đã đăng nhập hợp lệ), SD-C02 (giỏ có sản phẩm), SD-T01 (tổng tiền tự động tính đúng)

## Type
Valid

## Status / Related bugs
Not Run / None
