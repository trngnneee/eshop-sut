# TC-CHECKOUT-012: Thanh toán với số mục giỏ hàng tại biên min− (0 sản phẩm)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số mục trong giỏ hàng at min− — value: 0

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng trống (0 mục)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số mục trong giỏ | 0 |

## Test steps
1. Đăng nhập và đảm bảo giỏ hàng trống.
2. Thử tiến hành thanh toán.
3. Quan sát phản hồi hệ thống.

## Expected result
- Hệ thống không cho phép hoàn tất thanh toán khi số mục = 0.
- Không tạo đơn hàng mới.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None
