# TC-CART-069: POST /api/cart với malformed JSON

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Người dùng đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Body | `{"productId": 1, "quantity": ` (Malformed) |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart với dữ liệu JSON bị lỗi cú pháp (thiếu ngoặc nhọn, dấu phẩy dư,...).
3. Xác minh server trả về lỗi cú pháp 400 và không bị crash.


## Expected result
- Server trả 400, không crash

## Status / Related bugs
Not Run / None
