# FR04-R-TC01: Không cho phép user tự thay đổi role

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning / Security

## Preconditions
- User thường đã đăng nhập bằng JWT hợp lệ.
- User hiện tại có role = `user`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| endpoint | PUT /api/users/me |
| body | {"name": "Nguyen Van A", "phone": "0123456789", "shipping_address": "123 Nguyen Hue, Quan 1, TP.HCM", "role": "admin"} |

## Test steps
1. Gửi request `PUT /api/users/me` kèm JWT của user thường.
2. Trong body gửi thêm `role=admin` cùng các trường hồ sơ hợp lệ.
3. Tải lại thông tin user hiện tại.

## Expected result
- Hệ thống từ chối hoặc bỏ qua trường `role` từ client.
- Role của user vẫn là `user` và không bị nâng thành `admin`.

## Status / Related bugs
Not Run / None
