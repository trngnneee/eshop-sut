# TC-CART-046: POST thiếu trường quantity

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Negative Testing / API Negative

## Preconditions
- Người dùng có token JWT hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Authorization: Bearer <valid_token>` |
| Body | `{"id": 1, "name": "Sản phẩm A", "price": 100000}` |

## Test steps
1. Gửi request `POST /api/cart` nhưng lược bỏ hoàn toàn trường quantity trong body.

## Expected result
- API trả về lỗi validation (HTTP 400 Bad Request) thông báo thiếu trường bắt buộc.
- Không thực hiện thêm sản phẩm lỗi vào giỏ hàng.

## Status / Related bugs
Not Run / None
