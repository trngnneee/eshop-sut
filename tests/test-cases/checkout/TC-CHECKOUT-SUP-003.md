# TC-CHECKOUT-SUP-003: Backend tự tính lại tổng tiền — không chấp nhận total_amount từ client

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Supplementary

## Preconditions
- Người dùng đã đăng nhập; có JWT Token hợp lệ
- Giỏ hàng có sản phẩm với tổng tiền thực tế lớn hơn giá trị giả mạo

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| total_amount (client gửi) | 1 (giá trị bị giả mạo, khác tổng thực tế) |
| Tổng thực tế (cartTotal) | Σ (đơn giá × số lượng) từ giỏ hàng |

## Test steps
1. Đăng nhập, thêm sản phẩm vào giỏ và ghi nhận `cartTotal`.
2. Gửi yêu cầu checkout tới API kèm JWT hợp lệ, trong body đặt `total_amount` = 1 (hoặc bất kỳ giá trị khác `cartTotal`).
3. Tra cứu đơn hàng vừa tạo (nếu API trả về thành công) hoặc đọc thông báo lỗi (nếu API từ chối).

## Expected result
- **Backend phải tự tính lại tổng tiền; không chấp nhận giá trị `total_amount` do client gửi lên** (FR-08).
- `total_amount` lưu trong đơn hàng phải bằng `cartTotal`, không bằng giá trị giả mạo.
- Hoặc API trả về lỗi khi `total_amount` client gửi không khớp tổng thực tế.

## Sub-domains covered
SD-T03 (total_amount client bị giả mạo — phân vùng không hợp lệ)

## Type
Invalid

## Status / Related bugs
Not Run / None
