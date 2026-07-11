# TC-CHECKOUT-017: Backend chấp nhận total_amount khớp cartTotal (on-point)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
total_amount (client) at on-point — value: cartTotal (khớp tổng thực tế)

## Preconditions
- Người dùng đã đăng nhập; có JWT Token hợp lệ
- Giỏ hàng có sản phẩm; `cartTotal` đã biết

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal (thực tế) | 150.000 ₫ (ví dụ) |
| total_amount (client gửi) | 150.000 ₫ (= cartTotal) |

## Test steps
1. Đăng nhập, thêm sản phẩm vào giỏ; ghi nhận `cartTotal`.
2. Gửi yêu cầu checkout tới API kèm JWT, đặt `total_amount` = `cartTotal`.
3. Tra cứu đơn hàng vừa tạo.

## Expected result
- Checkout thành công.
- `total_amount` lưu trong đơn hàng bằng `cartTotal` (backend xác nhận/khớp tổng thực tế).

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None
