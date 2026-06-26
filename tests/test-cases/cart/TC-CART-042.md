# TC-CART-042: POST thêm sản phẩm hợp lệ

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Testing / API Testing

## Preconditions
- Người dùng có token JWT hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Authorization: Bearer <valid_token>` |
| Body | `{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": 2}` |

## Test steps
1. Gửi request `POST /api/cart` kèm theo token hợp lệ và body JSON chứa các trường id, name, price, quantity hợp lệ.

## Expected result
- API trả về mã trạng thái HTTP 200 OK hoặc 201 Created.
- Response body xác nhận sản phẩm đã được thêm vào giỏ hàng thành công.
- Dữ liệu giỏ hàng của user trên server được cập nhật chính xác.

## Status / Related bugs
Not Run / None
