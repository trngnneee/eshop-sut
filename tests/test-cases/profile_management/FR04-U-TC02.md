# FR04-U-TC02: Không cho phép cập nhật hồ sơ của user khác

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning / Authorization

## Preconditions
- Có hai user A và B trong hệ thống.
- User A đã đăng nhập bằng JWT hợp lệ.
- User B có hồ sơ khác với user A.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| endpoint | PUT /api/users/me |
| token_owner | User A |
| attempted_target_user_id | User B |
| body | {"id": "{user_b_id}", "name": "Hacked User B", "phone": "0123456789", "shipping_address": "Dia chi bi thay doi"} |

## Test steps
1. Gửi request cập nhật hồ sơ bằng JWT của User A.
2. Trong body cố tình gửi thêm `id` của User B.
3. Tải lại hồ sơ của User A và User B.

## Expected result
- Hệ thống chỉ cho phép User A cập nhật hồ sơ của chính mình hoặc từ chối request.
- Hồ sơ của User B không bị thay đổi.

## Status / Related bugs
Passed / None
