# TC-CHECKOUT-SUP-004: API từ chối khi items client gửi khác giỏ thực tế

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Supplementary

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- Giỏ có sản phẩm A; biết `cartTotal` thực tế

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Giỏ thực tế | Sản phẩm A, qty = 1 |
| items (client gửi) | Sản phẩm B giá cao hơn, qty = 1 |
| total_amount | Khớp tổng items giả mạo |

## Test steps
1. Thêm sản phẩm A vào giỏ; ghi nhận `cartTotal`.
2. Gửi checkout với `items` chứa sản phẩm B (không có trong giỏ) và `total_amount` theo B.
3. Tra cứu đơn hàng.

## Expected result
- Backend tính từ giỏ/sản phẩm thực tế của user, không tin `items` client tùy ý.
- `total_amount` đơn hàng = `cartTotal` thực tế, không theo payload giả.

## Sub-domains covered
GAP-01 — items payload không khớp giỏ server

## Type
Invalid

## Status / Related bugs
Not Run / None
