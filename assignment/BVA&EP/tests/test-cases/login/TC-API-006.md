# TC-API-006: API Đăng nhập thành công phản hồi cấu trúc JSON an sau (không chứa password)

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

## Test steps
1. Gửi POST request login đúng.
2. Kiểm tra payload JSON nhận được trong response body.

## Expected result
- Đăng nhập thành công (HTTP 200).
- Response JSON chứa token, thông tin cơ bản của user nhưng tuyệt đối không được chứa trường password/hash password của user.

## Status / Related bugs
Pass / None
