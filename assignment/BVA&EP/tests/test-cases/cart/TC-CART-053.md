# TC-CART-053: Nhấn nút Xóa liên tục nhiều lần

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Robustness

## Preconditions
- Giỏ hàng đang có sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập `/cart`.
2. Nhấp đúp chuột thật nhanh (double click) hoặc click liên tục nhiều lần vào nút Xóa của một sản phẩm.

## Expected result
- Hệ thống chỉ ghi nhận 1 yêu cầu xóa duy nhất và hiển thị 1 dialog.
- Không xóa nhầm sản phẩm khác và giao diện không bị treo/crash.

## Status / Related bugs
Fail / BUG-FR07-B-10
