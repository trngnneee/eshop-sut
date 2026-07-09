# TC-DASHBOARD-DT-021: Kiểm tra dashboard không hiển thị raw error hoặc stack trace khi API lỗi
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / UI/UX / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API dashboard (ví dụ: API orders hoặc users) trả về lỗi (ví dụ: lỗi SQL, lỗi kết nối db) kèm theo thông báo lỗi kỹ thuật hoặc stack trace chi tiết.
## Test data
- API response chứa message kỹ thuật, SQL error, hoặc stack trace.
## Test steps
1. Thiết lập API trả về thông báo lỗi kỹ thuật chi tiết.
2. Đăng nhập admin và truy cập Dashboard.
3. Quan sát thông báo lỗi hiển thị trên giao diện người dùng.
## Expected result
- Giao diện người dùng chỉ hiển thị thông báo lỗi thân thiện (ví dụ: "Đã xảy ra lỗi, vui lòng thử lại sau").
- Tuyệt đối không hiển thị các thông tin nhạy cảm như SQL error, stack trace, đường dẫn thư mục nội bộ, hay chi tiết token để đảm bảo an ninh thông tin.
## Status / Related bugs
Pass / None
