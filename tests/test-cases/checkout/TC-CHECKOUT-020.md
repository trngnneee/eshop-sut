# TC-CHECKOUT-020: JWT Token hết hạn không được thanh toán

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng từng đăng nhập nhưng JWT Token đã hết hạn hoặc bị thu hồi
- Giỏ hàng có sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| JWT Token | Hết hạn hoặc không còn hợp lệ |

## Test steps
1. Đăng nhập, thêm sản phẩm vào giỏ.
2. Làm hết hạn hoặc xóa JWT Token (đăng xuất phía server / xóa token client).
3. Mở trang Thanh toán và thử xác nhận thanh toán.

## Expected result
- Hệ thống từ chối thanh toán vì người dùng không còn phiên đăng nhập hợp lệ.
- Không tạo đơn hàng mới.

## Sub-domains covered
SD-A03 (token hết hạn — phân vùng không hợp lệ, luồng UI)

## Type
Invalid

## Status / Related bugs
Not Run / None
