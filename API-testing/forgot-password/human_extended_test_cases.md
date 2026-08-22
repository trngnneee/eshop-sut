# Human-Extended Test Cases - FR-03 Forgot Password

File này liệt kê các test case do người kiểm thử bổ sung sau khi audit bộ test do AI sinh. Các case này tập trung vào security và state transitions mà AI còn bỏ sót, đặc biệt là luồng nối giữa `POST /api/forgot-password` và `POST /api/reset-password`.

## Summary

- API chính: `POST /api/forgot-password`
- API liên quan để kiểm state: `POST /api/reset-password`
- Số test case bổ sung: 7
- Lý do bổ sung: bộ AI-generated ban đầu kiểm nhiều input của forgot-password, nhưng chưa kiểm đủ vòng đời reset token sau khi dùng, ràng buộc giữa token và email, concurrency, password policy, method confusion, và cache/security header.

## Test Cases

| ID | Type | Scenario | Preconditions | Request / Steps | Expected Result |
| --- | --- | --- | --- | --- | --- |
| HT-FORGOT-EXT-001 | Security, State Transition | Không cho dùng OTP của user A để reset mật khẩu user B | Tồn tại `test@eshop.com` và `admin@eshop.com`; gọi forgot-password cho `test@eshop.com` để lấy OTP A | `POST /api/reset-password` với `email=admin@eshop.com`, `resetToken=OTP_A`, `newPassword=NewAdmin123!` | API trả `400`; mật khẩu của `admin@eshop.com` không đổi; OTP A không được áp dụng cho email khác. |
| HT-FORGOT-EXT-002 | State Transition, SEC-07 | OTP đã dùng thành công không được dùng lại | Gọi forgot-password cho `test@eshop.com`, sau đó reset-password thành công bằng OTP A | Gọi lại `POST /api/reset-password` lần hai với cùng `email`, cùng `resetToken=OTP_A`, và mật khẩu mới khác | Lần gọi thứ hai trả `400`; mật khẩu không bị đổi lần nữa; token đã chuyển từ `active` sang `consumed/invalid`. |
| HT-FORGOT-EXT-003 | State Transition, SEC-07 | OTP cũ bị vô hiệu khi user yêu cầu OTP mới | Gọi forgot-password cho `test@eshop.com` lấy OTP A, sau đó gọi forgot-password lần nữa lấy OTP B | Thử reset-password bằng OTP A trước, sau đó thử bằng OTP B | OTP A trả `400`; OTP B mới là token hợp lệ duy nhất và có thể reset thành công. |
| HT-FORGOT-EXT-004 | Security | Reset password phải kiểm password policy cho `newPassword` | Có OTP hợp lệ cho `test@eshop.com` | `POST /api/reset-password` với `newPassword="123"` hoặc `"password"` | API trả `400`; không cập nhật mật khẩu yếu; response không lộ token hoặc password. |
| HT-FORGOT-EXT-005 | State Transition, Race Condition | Hai request reset-password song song với cùng OTP chỉ được một request thành công | Có OTP hợp lệ cho `test@eshop.com`; có thể gửi 2 request gần như đồng thời | Gửi 2 request `POST /api/reset-password` cùng `email`, cùng `resetToken`, nhưng `newPassword` khác nhau | Chỉ một request được `200`; request còn lại phải `400`; trạng thái token không được cho phép double-spend. |
| HT-FORGOT-EXT-006 | Security | Method confusion: GET không được tạo OTP | Tồn tại `test@eshop.com`; reset_token ban đầu rỗng hoặc đã ghi nhận trạng thái trước test | Gửi `GET /api/forgot-password?email=test@eshop.com` hoặc request không phải `POST` tương đương | API trả `404` hoặc `405`; không tạo/reset OTP; state của user không đổi. |
| HT-FORGOT-EXT-007 | Security, Schema | Response chứa `resetToken` không được cache bởi browser/proxy | Tồn tại `test@eshop.com`; gọi forgot-password thành công | Kiểm response headers của `POST /api/forgot-password` | Response nên có `Cache-Control: no-store` hoặc header tương đương; nếu thiếu, OTP có thể bị lưu ở cache/intermediary. |

## Why The AI Missed Them

| Added Test Case | Why AI Missed It |
| --- | --- |
| HT-FORGOT-EXT-001 | Prompt ban đầu tập trung vào endpoint được chọn là `POST /api/forgot-password`, nên AI ít mở rộng sang bước `POST /api/reset-password`. Vì vậy AI không kiểm ràng buộc quan trọng `resetToken` phải khớp đúng email sở hữu token. |
| HT-FORGOT-EXT-002 | AI có nhắc lifecycle OTP ở mức mô tả, nhưng chưa biến trạng thái `used/consumed token` thành test case thao tác cụ thể trên `POST /api/reset-password`. Đây là giới hạn thường gặp khi model suy luận state transition nhưng thiếu bước verify state sau action. |
| HT-FORGOT-EXT-003 | AI đã có ý tưởng "OTP mới thay thế OTP cũ", nhưng chưa tách thành flow execute đầy đủ: lấy OTP A, lấy OTP B, thử lại OTP A, rồi xác nhận OTP B còn hợp lệ. Thiếu sót đến từ prompt chưa yêu cầu test sequence nhiều bước. |
| HT-FORGOT-EXT-004 | Model tập trung vào field `email` của forgot-password và SEC-07 về OTP, nên bỏ qua field `newPassword` ở API reset-password. Đây là limitation do phạm vi endpoint quá hẹp so với user journey hoàn chỉnh. |
| HT-FORGOT-EXT-005 | Race condition/concurrency thường không xuất hiện nếu prompt chỉ yêu cầu test case API thông thường. AI có xu hướng sinh single-request tests, ít nghĩ tới hai request song song dùng cùng token. |
| HT-FORGOT-EXT-006 | AI tập trung vào domain partition của body JSON, chưa kiểm HTTP method confusion. Đây là thiếu sót do prompt chưa yêu cầu kiểm tra method-level behavior hoặc route hardening. |
| HT-FORGOT-EXT-007 | Model đã kiểm response body/schema nhưng chưa kiểm security headers. Với API trả OTP trực tiếp trong response demo, cache-control là một rủi ro bảo mật quan trọng nhưng dễ bị bỏ qua nếu prompt không nhắc đến transport/header security. |

## Notes For Execution

- Các case `HT-FORGOT-EXT-001` đến `HT-FORGOT-EXT-005` cần chạy theo sequence vì phụ thuộc OTP vừa được sinh ra.
- Nếu backend demo vẫn trả `resetToken` trực tiếp trong response, có thể dùng Postman variable để lưu token giữa các request.
- Nếu môi trường không hỗ trợ gửi song song cho `HT-FORGOT-EXT-005`, có thể ghi case này là manual/security review hoặc dùng script/Newman external runner để gửi concurrent requests.
