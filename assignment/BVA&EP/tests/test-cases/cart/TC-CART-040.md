# TC-CART-040: GET cart không có token

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / API Negative Testing / API Negative Testing

## Preconditions
- Không truyền JWT token trong request.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Không có` |

## Test steps
1. Gửi request `GET /api/cart` không truyền header Authorization.

## Expected result
- API trả về mã lỗi xác thực (HTTP 401 Unauthorized).
- Không trả về bất kỳ dữ liệu giỏ hàng nào.

## Status / Related bugs
Pass / None
