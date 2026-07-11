# TC-CHECKOUT-008: Không thể thanh toán khi giỏ hàng trống

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng **trống** (0 sản phẩm)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Trạng thái giỏ hàng | Trống |

## Test steps
1. Đăng nhập bằng `test@eshop.com` / `Test1234!`.
2. Đảm bảo giỏ hàng trống.
3. Thử tiến hành thanh toán (từ giỏ hàng hoặc trang thanh toán nếu truy cập được).
4. Quan sát phản hồi hệ thống.

## Expected result
- Hệ thống không cho phép hoàn tất thanh toán khi không có sản phẩm trong giỏ.
- Không tạo đơn hàng mới.

## Sub-domains covered
SD-C01 (giỏ hàng trống — phân vùng không hợp lệ)

## Type
Invalid

## Status / Related bugs
Not Run / None
