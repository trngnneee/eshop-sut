# TC-CHECKOUT-043: Backend xử lý total_amount dạng thập phân không khớp cartTotal

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
total_amount (client) at decimal — value: cartTotal + 0,5 (ví dụ 150.000,5)

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- cartTotal là số nguyên (ví dụ 150.000 ₫)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal | 150.000 |
| total_amount (client) | 150.000,5 |

## Test steps
1. Gửi checkout với `total_amount` = 150.000,5 khi `cartTotal` = 150.000.
2. Tra cứu tổng lưu trong đơn.

## Expected result
- Backend không chấp nhận giá trị thập phân lệch; lưu tổng nguyên đúng bằng `cartTotal` hoặc trả lỗi.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None
