# TC-CART-061: POST /api/cart thiếu trường price

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Negative / API Negative

## Preconditions
- Token JWT hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Body | `{"id": 201, "name": "No Price Product", "quantity": 1}` |

## Test steps
1. Gửi request `POST /api/cart` kèm token hợp lệ nhưng body lược bỏ hoàn toàn thuộc tính `price`.

## Expected result
- API trả về lỗi HTTP 400 Bad Request, không cho phép lưu.

## Status / Related bugs
Not Run / None
