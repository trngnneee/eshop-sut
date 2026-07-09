# TC-LOGIN-011: Kiểm tra thời hạn hết hạn của JWT Token (Session Expiration)

## Requirement ID
SEC-02

## Module / Test type / Technique
Login / Session / Security Testing

## Preconditions
- Đăng nhập thành công và có token JWT.

## Test data
- Token nhận được sau đăng nhập.

## Test steps
1. Phân tích nội dung token JWT (decode token) để kiểm tra trường `exp` (expiration time).
2. Kiểm tra xem token có hết hạn sau một khoảng thời gian không hoạt động hoặc thời gian quy định hay không.

## Expected result
- Token JWT phải được thiết lập thời gian hết hạn (trường `exp`) hợp lý để bảo vệ phiên làm việc của người dùng khỏi bị lạm dụng nếu rò rỉ.

## Status / Related bugs
Fail / #43
