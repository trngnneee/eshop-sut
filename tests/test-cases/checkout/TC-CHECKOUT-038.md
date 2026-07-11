# TC-CHECKOUT-038: Backend từ chối total_amount âm tại biên (-1)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
total_amount (client) at negative on-point — value: -1

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- Giỏ có sản phẩm; cartTotal > 0

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal | 200.000 ₫ |
| total_amount (client) | -1 |

## Test steps
1. Gửi checkout với `total_amount` = -1 khi giỏ có sản phẩm.
2. Tra cứu đơn hàng hoặc lỗi API.

## Expected result
- Backend không lưu `total_amount` = -1; tự tính đúng hoặc trả lỗi.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None
