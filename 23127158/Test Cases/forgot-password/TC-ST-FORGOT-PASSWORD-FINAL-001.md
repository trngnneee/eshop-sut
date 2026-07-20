# TC-ST-FORGOT-PASSWORD-FINAL-001

## Test Case ID
TC-ST-FORGOT-PASSWORD-FINAL-001

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
Final State Test

## Covered State(s)
S3 (Đặt lại mật khẩu thành công)

## Covered Transition(s)
Không áp dụng (kiểm tra hành vi sau Final State, không phải chuyển đổi tiếp theo)

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng đã hoàn tất quy trình đặt lại mật khẩu và hệ thống đang ở trạng thái S3 (Đặt lại mật khẩu thành công).
- Mã OTP cũ đã được sử dụng để đặt lại mật khẩu.

## Test Data
| Parameter | Value |
| --- | --- |
| OTP cũ đã dùng | Mã OTP đã sử dụng ở bước trước |
| Mật khẩu cũ (trước khi reset) | Mật khẩu ban đầu của tài khoản |
| Mật khẩu mới (sau khi reset) | NewPass123! |

## Test Steps
1. Đảm bảo hệ thống đang ở trạng thái S3 sau khi đặt lại mật khẩu thành công cho `test@eshop.com`.
2. Thử gửi lại yêu cầu đặt lại mật khẩu với cùng mã OTP cũ đã dùng (hành động sau Final State).
3. Thử đăng nhập bằng **mật khẩu cũ** (trước khi reset).
4. Thử đăng nhập bằng **mật khẩu mới** `NewPass123!`.

## Expected Result
- Sau bước 2: Hệ thống từ chối yêu cầu. Mã OTP cũ đã hết hiệu lực sau khi sử dụng. Trạng thái S3 không thay đổi. (**Lưu ý:** Đặc tả không định nghĩa rõ nội dung phản hồi khi tái sử dụng OTP đã dùng — *"Đặc tả không định nghĩa quy tắc này."*)
- Sau bước 3: Đăng nhập **thất bại** — mật khẩu cũ không còn hợp lệ sau khi reset thành công.
- Sau bước 4: Đăng nhập **thành công** bằng mật khẩu mới `NewPass123!` — xác nhận mật khẩu mới đã được áp dụng vĩnh viễn.
- Trạng thái Final State S3 ổn định và không thể bị thay đổi bởi các hành động không hợp lệ sau đó.

## Final State
S3 (Đặt lại mật khẩu thành công)

## Risk Level
High

## Actual Result
Final State S3 ổn định: OTP cũ sau khi sử dụng không dùng lại được (trả 400). Mật khẩu cũ không đăng nhập được. Mật khẩu mới đăng nhập thành công. Tuy nhiên, trong quá trình test: OTP được sinh ra chỉ có **4 chữ số** (bug tại T2) nên Final State test không thể xác nhận đầy đủ theo đặc tả.

## Status
FAIL

## Bug Reference
BUG-FR03-001 — OTP sinh ra 4 chữ số thay vì 6 chữ số (nhưng Final State bản thân ổn định)
