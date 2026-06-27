# TC-CART-086: Gửi GET /api/cart với token sai định dạng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Không đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Authorization | `'Bearer invalid-token-format'` |

## Test steps
1. Gửi request GET tới /api/cart.
2. Đính kèm Header Authorization chứa token sai định dạng (ví dụ: 'Bearer abcxyz' hoặc không có tiền tố Bearer).
3. Xác minh server trả về 401 Unauthorized.


## Expected result
- Trả 401, không crash server

## Status / Related bugs
Not Run / None
