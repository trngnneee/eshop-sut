# TC-CART-046: POST quantity thập phân

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
| Body | `{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": 1.5}` |

## Test steps
1. Gửi request `POST /api/cart` với quantity là 1.5.

## Expected result
- API từ chối request hoặc tự động ép kiểu thành số nguyên, hoặc trả về mã lỗi validation HTTP 400 Bad Request.

## Status / Related bugs
Not Run / None
