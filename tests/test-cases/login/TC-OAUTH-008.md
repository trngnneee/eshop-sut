# TC-OAUTH-008: Kiểm tra xử lý khi URL callback OAuth bị gọi lại nhiều lần (Replay Attack)

## Requirement ID
SEC-02

## Module / Test type / Technique
OAuth / Security Testing

## Preconditions
- Đăng nhập Google thành công, lấy URL callback chứa Authorization Code.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Callback URL | /api/auth/google/callback?code=already_used_code |

## Test steps
1. Gửi yêu cầu callback này lần thứ 2 liên tiếp.

## Expected result
- Backend từ chối yêu cầu (mã code đã được sử dụng 1 lần sẽ mất hiệu lực).
- Không tạo thêm session trùng lặp hoặc crash.

## Status / Related bugs
Not Run / None
