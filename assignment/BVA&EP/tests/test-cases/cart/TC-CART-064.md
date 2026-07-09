# TC-CART-064: POST /api/cart với price rất lớn

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
| price | `999999999999999` |
| quantity | `1` |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart với price = 999999999999999 (hoặc giá trị cực đại của dữ liệu số).
3. Kiểm tra xem server có từ chối request hoặc xử lý giới hạn an toàn hay không.


## Expected result
- Server reject hoặc xử lý an toàn, không làm total lỗi

## Status / Related bugs
Fail / BUG-FR07-B-13
