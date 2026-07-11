# TC-CHECKOUT-042: Backend từ chối total_amount = 2 × cartTotal

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
total_amount (client) at 2×cartTotal — value: gấp đôi tổng thực tế

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- cartTotal đã biết (ví dụ 150.000 ₫)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal | 150.000 ₫ |
| total_amount (client) | 300.000 ₫ (= 2 × cartTotal) |

## Test steps
1. Gửi checkout với `total_amount` = 2 × `cartTotal`.
2. Tra cứu tổng lưu trong đơn.

## Expected result
- Backend lưu `total_amount` = `cartTotal`, không chấp nhận gấp đôi từ client.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None
