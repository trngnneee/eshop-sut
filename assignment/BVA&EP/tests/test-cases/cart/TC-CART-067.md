# TC-CART-067: POST /api/cart với quantity: null

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
| quantity | `null` |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart với quantity = null hoặc trống.
3. Xác minh phản hồi từ API backend.


## Expected result
- Server trả 400 Bad Request

## Status / Related bugs
Fail / BUG-FR07-B-15
