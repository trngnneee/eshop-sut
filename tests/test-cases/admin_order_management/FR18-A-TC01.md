# FR18-A-TC01: Từ chối user thường xem danh sách đơn hàng Admin

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning / Authorization

## Preconditions
- User thường đã đăng nhập bằng JWT hợp lệ với `role = user`.
- Hệ thống có ít nhất một đơn hàng của user khác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Endpoint | GET /api/admin/orders |
| Token role | user |

## Test steps
1. Đăng nhập bằng tài khoản user thường.
2. Gửi request `GET /api/admin/orders` với token user thường.
3. Kiểm tra response và đảm bảo dữ liệu đơn hàng không bị trả về.

## Expected result
- Hệ thống trả về HTTP 403 hoặc lỗi quyền truy cập phù hợp.
- Response không chứa danh sách đơn hàng toàn hệ thống.

## Status / Related bugs
Failed / BUG-FR18-A-01 - API Admin không kiểm tra role admin
