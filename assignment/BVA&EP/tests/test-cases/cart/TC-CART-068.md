# TC-CART-068: POST /api/cart với body rỗng {}

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Người dùng đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Body | `{}` |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart với body trống trơn {}.
3. Xác minh phản hồi lỗi từ API.


## Expected result
- Server trả 400, không thêm item rỗng

## Status / Related bugs
Fail / BUG-FR07-B-15
