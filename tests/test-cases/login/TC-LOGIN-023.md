# TC-LOGIN-023: Kiểm tra giới hạn kích thước gói tin gửi lên API Đăng nhập (DoS Protection)
## Requirement ID
SEC-01
## Module / Test type / Technique
Login / Security & Reliability / Stress Testing (Body Size Limits)
## Preconditions
- Sử dụng công cụ gửi yêu cầu API (như Postman, curl, hoặc python script).
## Test data
- Gói tin JSON gửi lên API `/api/login` với trường mật khẩu chứa chuỗi ngẫu nhiên có kích thước `5MB`.
## Test steps
1. Tạo một HTTP POST request đến `/api/login`.
2. Truyền payload JSON chứa địa chỉ email và mật khẩu có kích thước cực lớn `5MB`.
3. Gửi yêu cầu và quan sát mã phản hồi HTTP trả về từ server Node.js.
## Expected result
- Server không bị cạn kiệt bộ nhớ hoặc bị crash (Denial of Service).
- Backend phải từ chối yêu cầu với lỗi kích thước dữ liệu quá giới hạn (ví dụ: HTTP 413 Payload Too Large) thông qua cơ chế giới hạn Body Parser.
## Status / Related bugs
Passed / None
