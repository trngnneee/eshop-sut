# TC-CHECKOUT-009: Giao diện hiển thị đầy đủ khi giỏ có nhiều mục hoặc số lượng > 1

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có nhiều hơn 1 dòng sản phẩm, hoặc 1 sản phẩm với số lượng > 1

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Kịch bản A | 2 sản phẩm khác nhau, mỗi loại số lượng = 1 |
| Kịch bản B | 1 sản phẩm, số lượng = 3 |

## Test steps
1. Đăng nhập.
2. **Kịch bản A:** Thêm 2 sản phẩm khác nhau vào giỏ. Mở trang Thanh toán và đối chiếu danh sách với giỏ hàng.
3. **Kịch bản B:** Làm trống giỏ, thêm 1 sản phẩm với số lượng = 3. Mở trang Thanh toán và xác nhận số lượng và thành tiền từng dòng.

## Expected result
- Giao diện hiển thị **đầy đủ danh sách sản phẩm đặt mua** (FR-08).
- Mỗi dòng gồm tên, số lượng và thành tiền; không thiếu hoặc gộp sai sản phẩm.
- Tổng tiền bằng tổng thành tiền các dòng.

## Sub-domains covered
SD-C03 (giỏ nhiều mục / số lượng > 1), SD-P01 (danh sách sản phẩm đầy đủ)

## Type
Valid

## Status / Related bugs
Not Run / None
