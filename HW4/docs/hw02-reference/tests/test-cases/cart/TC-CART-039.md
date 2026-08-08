# TC-CART-039: GET cart với token hợp lệ

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Testing / API Testing

## Preconditions
- Người dùng có token JWT hợp lệ từ việc đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Authorization: Bearer <valid_token>` |

## Test steps
1. Gửi request `GET /api/cart` kèm theo Authorization header chứa token hợp lệ.

## Expected result
- API phản hồi với mã trạng thái HTTP 200 OK.
- Response body chứa thông tin chi tiết danh sách sản phẩm trong giỏ hàng của người dùng dưới dạng JSON.

## Status / Related bugs
Not Run / None
