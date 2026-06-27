# TC-CART-060: POST /api/cart thiếu trường id

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Negative / API Negative

## Preconditions
- Token JWT hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Body | `{"name": "No ID Product", "price": 100000, "quantity": 1}` |

## Test steps
1. Gửi request `POST /api/cart` kèm token hợp lệ nhưng body lược bỏ hoàn toàn thuộc tính `id`.

## Expected result
- API từ chối request và trả về mã lỗi HTTP 400 Bad Request.
- Không lưu dữ liệu thiếu trường vào giỏ hàng.

## Status / Related bugs
Not Run / None
