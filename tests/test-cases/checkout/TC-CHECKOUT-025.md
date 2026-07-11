# TC-CHECKOUT-025: Cùng sản phẩm thêm nhiều lần hiển thị một dòng với số lượng gộp

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Quy tắc FR-07: thêm cùng SP tăng số lượng, không tạo dòng mới

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | 1 loại |
| Lần thêm | 2 lần, mỗi lần số lượng = 1 |
| Số lượng gộp kỳ vọng | 2 |

## Test steps
1. Đăng nhập; thêm cùng một sản phẩm vào giỏ 2 lần (mỗi lần qty = 1).
2. Kiểm tra giỏ hàng chỉ có 1 dòng với số lượng = 2.
3. Mở trang Thanh toán và đối chiếu danh sách.

## Expected result
- Trang thanh toán hiển thị **1 dòng** cho sản phẩm đó với số lượng = 2.
- Thành tiền = đơn giá × 2.

## Sub-domains covered
SD-C05 (sản phẩm trùng gộp số lượng — kế thừa FR-07), SD-P01

## Type
Valid

## Status / Related bugs
Not Run / None
