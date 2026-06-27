# TC-CART-051: Confirm Dialog hiển thị đúng tên sản phẩm cần xóa

## Requirement ID
FR-07, FR-24

## Module / Test type / Technique
Cart / Functional / UI / Confirmation

## Preconditions
- Người dùng đăng nhập.
- Giỏ hàng có sản phẩm tên 'Sản phẩm A'.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập `/cart`.
2. Nhấp chọn nút 'Xóa' của 'Sản phẩm A'.

## Expected result
- Hộp thoại xác nhận hiển thị chứa nội dung ghi rõ tên sản phẩm cần xóa (ví dụ: 'Bạn có chắc chắn muốn xóa Sản phẩm A khỏi giỏ hàng?').

## Status / Related bugs
Not Run / None
