# TC-CHECKOUT-001: Người dùng chưa đăng nhập không được tiến hành thanh toán

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng **chưa** đăng nhập
- Giỏ hàng có ít nhất 1 sản phẩm (để có thể thử thao tác thanh toán)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Trạng thái đăng nhập | Chưa đăng nhập |
| Sản phẩm trong giỏ | ≥ 1 mục |

## Test steps
1. Không đăng nhập; thêm ít nhất một sản phẩm vào giỏ hàng.
2. Từ trang Giỏ hàng, bấm nút tiến hành thanh toán.
3. Quan sát phản hồi của hệ thống.

## Expected result
- Theo FR-08, chỉ người dùng **đã đăng nhập** mới tiến hành thanh toán được.
- Hệ thống không cho hoàn tất luồng thanh toán (ví dụ: yêu cầu đăng nhập trước hoặc chuyển đến trang Đăng nhập).
- Không tạo đơn hàng mới.

## Sub-domains covered
SD-A01 (chưa đăng nhập — phân vùng không hợp lệ)

## Type
Invalid

## Status / Related bugs
Not Run / None
