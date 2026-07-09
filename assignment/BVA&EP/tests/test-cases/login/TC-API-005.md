# TC-API-005: API Đăng nhập bỏ qua hoặc từ chối các trường thừa (Extra fields) trong request body

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Security Testing

## Preconditions
- Tài khoản hoạt động.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| email | test@eshop.com |
| password | ValidPassword1! |
| extra_field | attack_payload |
| role | admin |

## Test steps
1. Gửi POST request tới `/api/login` kèm thêm các trường không định nghĩa trong tài liệu API.

## Expected result
- API đăng nhập thành công bình thường.
- Bỏ qua hoàn toàn trường thừa và không cho phép thay đổi quyền hạn role của người dùng.

## Status / Related bugs
Pass / None
