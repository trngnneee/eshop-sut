# TC-CART-070: POST /api/cart với extra fields như isAdmin, discount, totalPrice

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Người dùng đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Body | `{"productId": 1, "quantity": 1, "isAdmin": true, "discount": 90}` |

## Test steps
1. Đăng nhập tài khoản.
2. Gửi request POST tới /api/cart đính kèm các trường dữ liệu lạ như "isAdmin": true hoặc "discount": 90.
3. Kiểm tra xem hệ thống có lọc bỏ trường dư thừa này hay lưu vào gây lỗ hổng Mass Assignment.


## Expected result
- Server bỏ qua field lạ hoặc reject, không lưu field nguy hiểm

## Status / Related bugs
Fail / BUG-FR07-B-16
