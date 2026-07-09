# TC-CART-065: POST /api/cart với quantity rất lớn, ví dụ 999999999

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Người dùng đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| productId | `1` |
| quantity | `999999999` |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart với quantity = 999999999.
3. Kiểm tra xem hệ thống có báo lỗi vượt giới hạn tồn kho khả dụng hoặc tràn số lượng hay không.


## Expected result
- Server reject hoặc báo vượt giới hạn/tồn kho

## Status / Related bugs
Fail / BUG-FR07-B-15
