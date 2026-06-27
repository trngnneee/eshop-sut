# FR18-A-TC02: Từ chối request không có token xem danh sách đơn hàng Admin

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning / Authorization

## Preconditions
- Hệ thống có ít nhất một đơn hàng.
- Không gửi header Authorization.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | anonymous |
| Endpoint | GET /api/admin/orders |
| Authorization | [Không gửi] |

## Test steps
1. Gửi request `GET /api/admin/orders` không kèm token.
2. Kiểm tra response và đảm bảo dữ liệu đơn hàng không bị trả về.

## Expected result
- Hệ thống trả về HTTP 401 hoặc lỗi xác thực phù hợp.
- Response không chứa danh sách đơn hàng.

## Status / Related bugs
Passed / None
