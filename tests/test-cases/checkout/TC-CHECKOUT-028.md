# TC-CHECKOUT-028: Không thể thanh toán lần hai khi giỏ đã trống sau đơn đầu

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Vừa hoàn tất một lần thanh toán thành công

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Lần thanh toán | Lần 2 (sau khi giỏ đã xóa) |

## Test steps
1. Đăng nhập; thêm sản phẩm và thanh toán thành công lần 1.
2. Xác nhận giỏ hàng trống.
3. Thử mở trang Thanh toán và xác nhận đơn lần 2 (không thêm sản phẩm mới).

## Expected result
- Hệ thống không cho tạo đơn hàng thứ hai khi giỏ trống.
- Không tạo đơn với tổng tiền = 0.

## Sub-domains covered
SD-O03 (chặn thanh toán lặp khi giỏ trống), SD-C01

## Type
Invalid

## Status / Related bugs
Not Run / None
