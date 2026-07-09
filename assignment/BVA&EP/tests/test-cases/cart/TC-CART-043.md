# TC-CART-043: POST quantity = 0

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Negative Testing / API Negative + BVA

## Preconditions
- Người dùng có token JWT hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Authorization: Bearer <valid_token>` |
| Body | `{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": 0}` |

## Test steps
1. Gửi request `POST /api/cart` với trường quantity là 0.

## Expected result
- API từ chối request và trả về lỗi validation (ví dụ: HTTP 400 Bad Request).
- Giỏ hàng không bị thay đổi và không lưu quantity không hợp lệ.

## Status / Related bugs
Fail / BUG-FR07-B-02
