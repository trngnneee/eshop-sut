# TC-CART-044: POST quantity âm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Negative Testing / API Negative + EP

## Preconditions
- Người dùng có token JWT hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Authorization: Bearer <valid_token>` |
| Body | `{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": -1}` |

## Test steps
1. Gửi request `POST /api/cart` với quantity là -1.

## Expected result
- API từ chối request, trả về mã lỗi HTTP 400 Bad Request.
- Số lượng sản phẩm trong giỏ hàng không bị thay đổi.

## Status / Related bugs
Not Run / None
