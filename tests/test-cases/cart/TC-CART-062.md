# TC-CART-062: POST /api/cart với price âm hoặc bằng 0

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Boundary / Negative / API Boundary / Negative

## Preconditions
- Token JWT hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Body 1 | `{"id": 202, "name": "Zero Price", "price": 0, "quantity": 1}` |
| Body 2 | `{"id": 203, "name": "Negative Price", "price": -50000, "quantity": 1}` |

## Test steps
1. Gửi request `POST /api/cart` với `price = 0`.
2. Gửi request `POST /api/cart` với `price = -50000`.

## Expected result
- API từ chối cả hai request và trả về lỗi HTTP 400 Bad Request.

## Status / Related bugs
Not Run / None
