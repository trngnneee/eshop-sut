# TC-CHECKOUT-033: Tài khoản admin đã đăng nhập được thanh toán

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Tài khoản `admin@eshop.com` / `Admin123!` tồn tại
- Giỏ hàng có sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | admin@eshop.com |
| Mật khẩu | Admin123! |

## Test steps
1. Đăng nhập bằng tài khoản admin.
2. Thêm sản phẩm vào giỏ và tiến hành thanh toán.
3. Hoàn tất xác nhận đơn hàng.

## Expected result
- Admin (đã đăng nhập) được phép thanh toán như user thường.
- Thanh toán thành công; tổng tiền khớp giỏ hàng.

## Sub-domains covered
SD-A04 (đã đăng nhập — vai trò admin, phân vùng hợp lệ)

## Type
Valid

## Status / Related bugs
Not Run / None
