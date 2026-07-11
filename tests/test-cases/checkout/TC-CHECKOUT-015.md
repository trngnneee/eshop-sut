# TC-CHECKOUT-015: Backend từ chối total_amount = 0 khi giỏ có sản phẩm

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
total_amount (client) at min− — value: 0 khi cartTotal > 0

## Preconditions
- Người dùng đã đăng nhập; có JWT Token hợp lệ
- Giỏ hàng có sản phẩm với cartTotal > 0 (ví dụ 150.000 ₫)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| cartTotal (thực tế) | 150.000 ₫ |
| total_amount (client gửi) | 0 |

## Test steps
1. Đăng nhập, thêm sản phẩm vào giỏ; ghi nhận `cartTotal` > 0.
2. Gửi yêu cầu checkout tới API kèm JWT, đặt `total_amount` = 0.
3. Tra cứu đơn hàng (nếu tạo) hoặc đọc phản hồi lỗi.

## Expected result
- Backend **không** lưu `total_amount` = 0 khi tổng thực tế > 0.
- Backend tự tính lại tổng đúng bằng `cartTotal`, hoặc trả về lỗi từ chối giá trị không hợp lệ.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None
