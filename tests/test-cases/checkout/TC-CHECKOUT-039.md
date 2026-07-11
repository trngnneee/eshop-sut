# TC-CHECKOUT-039: Backend từ chối total_amount = 1 khi cartTotal lớn

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
total_amount (client) at extreme low tamper — value: 1 khi cartTotal >> 1

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- Giỏ có sản phẩm với cartTotal ≥ 100.000 ₫

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal | 250.000 ₫ |
| total_amount (client) | 1 |

## Test steps
1. Thêm sản phẩm vào giỏ; ghi nhận `cartTotal` = 250.000 ₫.
2. Gửi checkout với `total_amount` = 1.
3. So sánh tổng lưu trong đơn với `cartTotal`.

## Expected result
- Đơn hàng lưu `total_amount` = 250.000 ₫, không phải 1.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None
