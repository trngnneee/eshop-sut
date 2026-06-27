# TC-CART-053: Xóa sản phẩm ở giữa danh sách nhiều sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đăng nhập.
- Giỏ hàng hiện có 3 sản phẩm: A (dòng 1), B (dòng 2), C (dòng 3).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập `/cart`.
2. Nhấp nút 'Xóa' của Sản phẩm B ở giữa bảng.
3. Xác nhận xóa trên hộp thoại.

## Expected result
- Chỉ duy nhất Sản phẩm B bị xóa khỏi giỏ hàng.
- Sản phẩm A và C vẫn giữ nguyên vị trí, số lượng, đơn giá và không bị ảnh hưởng.

## Status / Related bugs
Not Run / None
