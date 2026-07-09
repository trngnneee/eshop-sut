# TC-CART-042: POST thêm sản phẩm trùng ID

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API + State Testing / API + State Testing

## Preconditions
- Người dùng có token JWT hợp lệ.
- Sản phẩm ID 1 đã tồn tại trong giỏ hàng với quantity = 2.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Authorization: Bearer <valid_token>` |
| Body | `{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": 3}` |

## Test steps
1. Gửi request `POST /api/cart` với ID sản phẩm trùng lặp (id: 1) và số lượng 3.

## Expected result
- API phản hồi thành công (HTTP 200 OK).
- Dữ liệu giỏ hàng của user trên server cập nhật cộng dồn số lượng thành 5, không tạo thêm item mới.

## Status / Related bugs
Pass / None
