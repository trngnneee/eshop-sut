# TC-CHECKOUT-024: Danh sách đặt mua hiển thị đủ 3 loại sản phẩm

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có 3 sản phẩm khác nhau

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số loại sản phẩm | 3 |

## Test steps
1. Đăng nhập; thêm 3 sản phẩm khác nhau vào giỏ.
2. Mở trang Thanh toán.
3. Đếm số dòng và đối chiếu tên từng sản phẩm.

## Expected result
- Danh sách hiển thị đủ **3 dòng** tương ứng 3 sản phẩm; không thiếu, không trùng lặp sai.

## Sub-domains covered
SD-C04 (giỏ có nhiều loại sản phẩm), SD-P01 (danh sách đầy đủ)

## Type
Valid

## Status / Related bugs
Not Run / None
