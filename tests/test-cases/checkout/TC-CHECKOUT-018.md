# TC-CHECKOUT-018: Backend từ chối total_amount = cartTotal + 1

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
total_amount (client) at cartTotal+ — value: cartTotal + 1

## Preconditions
- Người dùng đã đăng nhập; có JWT Token hợp lệ
- Giỏ hàng có sản phẩm; `cartTotal` đã biết (ví dụ 150.000 ₫)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal (thực tế) | 150.000 ₫ |
| total_amount (client gửi) | 150.001 ₫ (= cartTotal + 1) |

## Test steps
1. Đăng nhập, thêm sản phẩm vào giỏ; ghi nhận `cartTotal`.
2. Gửi yêu cầu checkout tới API kèm JWT, đặt `total_amount` = `cartTotal + 1`.
3. Tra cứu `total_amount` trong đơn hàng hoặc đọc phản hồi lỗi.

## Expected result
- Backend **không** chấp nhận `total_amount` = `cartTotal + 1` làm giá trị cuối cùng.
- Đơn hàng lưu `total_amount` = `cartTotal`, hoặc API trả về lỗi.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None
