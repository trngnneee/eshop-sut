# FR04-U-TC01: Từ chối cập nhật hồ sơ khi chưa đăng nhập

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning / Authorization

## Preconditions
- Client không có JWT hoặc JWT không hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| endpoint | PUT /api/users/me |
| Authorization | [Không gửi] |
| body | {"name": "Nguyen Van A", "phone": "0123456789", "shipping_address": "123 Nguyen Hue, Quan 1, TP.HCM"} |

## Test steps
1. Gửi request `PUT /api/users/me` không kèm header Authorization.
2. Quan sát status code và tải lại hồ sơ nếu có thể.

## Expected result
- Hệ thống từ chối request với lỗi xác thực phù hợp.
- Không có hồ sơ người dùng nào bị thay đổi.

## Status / Related bugs
Passed / None
