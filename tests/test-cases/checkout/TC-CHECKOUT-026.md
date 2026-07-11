# TC-CHECKOUT-026: Sửa tổng tiền trên UI không làm đơn hàng lưu sai giá trị

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có sản phẩm; `cartTotal` đã biết

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal (thực tế) | 300.000 ₫ |
| Giá trị cố sửa trên UI | 1 ₫ |

## Test steps
1. Đăng nhập; thêm sản phẩm vào giỏ; ghi nhận `cartTotal`.
2. Mở trang Thanh toán.
3. Nếu trường tổng tiền cho phép sửa, đổi giá trị sang `1` rồi xác nhận thanh toán.
4. Tra cứu `total_amount` của đơn hàng vừa tạo.

## Expected result
- Đơn hàng lưu `total_amount` = `cartTotal` thực tế, **không** bằng giá trị đã sửa trên UI.
- Hoặc hệ thống không cho phép sửa tổng tiền (đúng đặc tả FR-08).

## Sub-domains covered
SD-T04 (tổng UI bị sửa nhưng backend phải dùng tổng thực)

## Type
Invalid

## Status / Related bugs
Not Run / None
