# API-1 — Test case do người học mở rộng cho `POST /api/login`

> Các case dưới đây được thiết kế sau khi audit output AI. Chúng tập trung vào đường quay lui của state machine, negative schema và quan hệ giữa JWT với endpoint được bảo vệ.

| TC ID | Nhóm nguyên nhân | Test case tự bổ sung | Preconditions / Test data | Expected result theo đặc tả | Bug nhắm tới | Vì sao AI bỏ sót |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-LOGIN-037 | Chất lượng prompt | Sai đúng 2 lần rồi đăng nhập đúng | User dùng-một-lần, attempts=0; gửi wrong password 2 lần rồi correct password | Hai lần sai đều `401`; lần đúng trả `200` vì chỉ khóa từ lần sai thứ 3 | D-LOGIN-01 | Prompt ban đầu mô tả ngưỡng khóa nhưng không yêu cầu đo bước nhảy của biến đếm qua một chuỗi hành động hoàn chỉnh. |
| TC-API-LOGIN-038 | Đặc thù API | Đo thời lượng khóa thực ở giây 35 | User dùng-một-lần vừa bị khóa; chờ 35 giây rồi login đúng | `200`, token hợp lệ, attempts và lock được reset | D-LOGIN-02 | Case phụ thuộc đồng hồ thật và thời gian chờ; mô hình thường tránh sinh test kéo dài hoặc không ổn định nếu prompt không yêu cầu rõ. |
| TC-API-LOGIN-039 | Giới hạn model | Negative schema toàn bộ field nhạy cảm | Login đúng bằng seed user | Cả root và `user` không có `password`, `reset_token`, `login_attempts`, `locked_until` | D-LOGIN-03 | AI thường kiểm tra field bắt buộc hiện diện (positive schema) nhưng không lập danh sách field bị cấm. |
| TC-API-LOGIN-040 | Đặc thù API | Giải mã JWT và kiểm tra hạn dùng | Login đúng; decode JWT payload | Có `iat` và `exp`; `0 < exp - iat <= 86400` giây | D-LOGIN-05 | API spec chỉ nói trả chuỗi JWT, không mô tả claim; cần mở token và áp nguyên tắc bảo mật ngoài response schema. |
| TC-API-LOGIN-041 | Giới hạn model | Hết khóa rồi sai một lần không bị khóa lại | User từng bị khóa; sau khi hết hạn gửi wrong password một lần, rồi correct password | Lần sai là `401` và chỉ tính attempts=1; lần đúng kế tiếp trả `200` | D-LOGIN-06 | Đây là residual-state bug trên đường quay lui; AI thường phủ đường tiến đến locked state nhưng không kiểm tra state tồn dư sau timeout. |
| TC-API-LOGIN-042 | Chất lượng prompt | Tự ký JWT bằng secret trong source | Ký payload `{"id":1,"role":"admin"}` bằng secret hard-code, gọi `GET /api/admin/orders` | Token giả phải bị `401/403`; không được truy cập dữ liệu admin | D-LOGIN-05 | Prompt generate chỉ cung cấp API spec; nếu không đọc source thì AI không biết secret được hard-code và có thể tái sử dụng. |

## Thống kê

- Số case mở rộng: **6**.
- Security: **4** case (`039–042`).
- State transition / temporal: **3** case (`037, 038, 041`; case 042 còn kiểm tra trạng thái authorization).
- Mỗi case có nguyên nhân bỏ sót cụ thể thuộc một trong ba nhóm đề bài yêu cầu.
