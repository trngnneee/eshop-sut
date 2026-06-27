# TC-CART-049: Truy cập /cart với token hết hạn

## Requirement ID
FR-07, FR-23

## Module / Test type / Technique
Cart / API / Security / API / Security

## Preconditions
- Token JWT của người dùng đã hết hạn.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Header | `Authorization: Bearer <expired_token>` |

## Test steps
1. Cấu hình token JWT đã hết hạn ở client.
2. Truy cập trang `/cart` và thực hiện gửi request lấy thông tin giỏ hàng.

## Expected result
- API `GET /api/cart` trả về mã trạng thái HTTP 401 Unauthorized.
- Frontend xử lý logout sạch token cũ, không hiển thị dữ liệu giỏ hàng cũ và điều hướng về `/login`.

## Status / Related bugs
Not Run / None
