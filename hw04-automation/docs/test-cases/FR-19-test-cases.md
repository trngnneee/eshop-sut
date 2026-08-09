# Bộ Test Case FR-19 - Quản Lý Người Dùng Admin

Tính năng: FR-19 - Quản lý người dùng trong Web Admin  
Phạm vi: Admin UI tab "Người dùng", API `GET /api/admin/users`, API `DELETE /api/admin/users/:id`  
Nguồn đặc tả: `README.md` mục FR-19, `api_specification.md` mục 6.1, ràng buộc access control từ FR-12

## Tóm Tắt Yêu Cầu

- Admin xem danh sách tất cả người dùng.
- Danh sách user không được lộ mật khẩu.
- Admin có thể xóa người dùng.
- Admin không được xóa chính tài khoản đang đăng nhập.
- Admin API yêu cầu JWT hợp lệ và role admin.

## Bảng Test Case

| TC ID | Loại | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu kiểm thử | Kết quả mong đợi | Độ ưu tiên | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| TC-FR19-01 | Tích cực | Admin xem được bảng quản lý người dùng | Backend/admin frontend đang chạy; tài khoản admin seed tồn tại | 1. Đăng nhập admin<br>2. Mở tab Người dùng<br>3. Chờ API user hoàn tất | data/fr19.json: ui_admin_user_list | Heading quản lý người dùng hiển thị; bảng user có ít nhất 2 dòng seed | Cao | Chưa chạy |
| TC-FR19-02 | Tích cực | Bảng user hiển thị các cột quản lý chính | Admin đã đăng nhập và đang ở tab Người dùng | 1. Mở tab Người dùng<br>2. Đọc header bảng | data/fr19.json: ui_required_columns | Các cột ID, Email, Role, Số ĐT, Hành động hiển thị | Cao | Chưa chạy |
| TC-FR19-03 | Bảo mật | API list user không trả về password | Có token admin hợp lệ | 1. Gọi `GET /api/admin/users` bằng token admin<br>2. Kiểm tra JSON từng user | data/fr19.json: api_list_excludes_password | Status 200; mỗi object user không có field `password` | Nghiêm trọng | Chưa chạy |
| TC-FR19-04 | Tích cực | UI hiển thị user seed và role tương ứng | Admin đã đăng nhập | 1. Mở tab Người dùng<br>2. Tìm email seed admin và user thường<br>3. Kiểm tra role | data/fr19.json: ui_seed_users_visible | `admin@eshop.com` có role admin; `test@eshop.com` có role user | Cao | Chưa chạy |
| TC-FR19-05 | Tích cực | Admin xóa được user thường | Tạo user thường dùng cho xóa; admin đã đăng nhập | 1. Tạo user target<br>2. Gọi xóa qua UI/API admin<br>3. Kiểm tra response | data/fr19.json: delete_regular_user | Xóa thành công với status 200/message phù hợp | Cao | Chưa chạy |
| TC-FR19-06 | Tích cực | User đã xóa biến mất khỏi danh sách | User target đã được tạo và bị xóa bởi admin | 1. Refresh danh sách user<br>2. Tìm email user đã xóa | data/fr19.json: deleted_user_removed_from_list | Email user đã xóa không còn xuất hiện trong API/UI | Cao | Chưa chạy |
| TC-FR19-07 | Bảo mật | Admin không được tự xóa tài khoản đang đăng nhập | Admin đã đăng nhập; biết id của admin hiện tại | 1. Gọi `DELETE /api/admin/users/{adminId}` bằng token admin<br>2. Lấy lại danh sách user | data/fr19.json: self_delete_blocked | Request bị từ chối; admin hiện tại vẫn tồn tại trong danh sách | Nghiêm trọng | Chưa chạy |
| TC-FR19-08 | Tiêu cực | API list user từ chối request không token | Không gửi Authorization header | 1. Gọi `GET /api/admin/users` không token | data/fr19.json: api_without_token | API trả 401 Unauthorized và không trả danh sách user | Nghiêm trọng | Chưa chạy |
| TC-FR19-09 | Tiêu cực | API list user từ chối token không hợp lệ | Có token sai/không verify được | 1. Gọi `GET /api/admin/users` với token sai | data/fr19.json: api_invalid_token | API trả 403 Forbidden và không trả danh sách user | Nghiêm trọng | Chưa chạy |
| TC-FR19-10 | Bảo mật | User thường không được lấy danh sách user | Tạo/đăng nhập user role user | 1. Đăng nhập user thường<br>2. Gọi `GET /api/admin/users` bằng token user | data/fr19.json: api_non_admin_list_forbidden | API trả 403 Forbidden; không trả dữ liệu user | Nghiêm trọng | Chưa chạy |
| TC-FR19-11 | Bảo mật | User thường không được xóa user | Tạo user thường actor và target | 1. Đăng nhập actor role user<br>2. Gọi `DELETE /api/admin/users/{targetId}`<br>3. Kiểm tra target vẫn tồn tại | data/fr19.json: api_non_admin_delete_forbidden | API trả 403 Forbidden; target user không bị xóa | Nghiêm trọng | Chưa chạy |
| TC-FR19-12 | Tiêu cực | UI admin từ chối đăng nhập bằng user thường | Tài khoản `test@eshop.com` tồn tại với role user | 1. Mở admin app<br>2. Đăng nhập bằng user thường | data/fr19.json: ui_non_admin_login_rejected | UI báo không phải admin; không hiển thị dashboard/tab Người dùng | Cao | Chưa chạy |
| TC-FR19-13 | Biên | Xóa một user không ảnh hưởng user khác | Tạo 2 user mới: target xóa và protected | 1. Xóa target bằng admin<br>2. Refresh list user<br>3. Kiểm tra protected user | data/fr19.json: delete_one_user_preserves_others | Target mất khỏi danh sách; protected user vẫn tồn tại | Cao | Chưa chạy |
| TC-FR19-14 | Bảo mật | UI không hiển thị password | Admin đã đăng nhập và mở tab Người dùng | 1. Đọc header bảng user<br>2. Đọc nội dung bảng user | data/fr19.json: ui_no_password_visible | Không có cột Password/Mật khẩu; không hiển thị password seed | Nghiêm trọng | Chưa chạy |

## Checklist Bao Phủ

- [x] Có ít nhất 12 test case cho tính năng này
- [x] Có ít nhất một test case tích cực
- [x] Có ít nhất một test case tiêu cực
- [x] Có ít nhất một test case biên
- [x] Có test bảo mật cho admin-only access
- [x] Có test không lộ password
- [x] Có test chặn self-delete
- [x] Mỗi test case map tới dữ liệu trong `data/fr19.json`
- [x] Có file Markdown riêng cho từng test case từ `TC-FR19-01.md` đến `TC-FR19-14.md`

## File Riêng Từng Test Case

- `docs/test-cases/TC-FR19-01.md`
- `docs/test-cases/TC-FR19-02.md`
- `docs/test-cases/TC-FR19-03.md`
- `docs/test-cases/TC-FR19-04.md`
- `docs/test-cases/TC-FR19-05.md`
- `docs/test-cases/TC-FR19-06.md`
- `docs/test-cases/TC-FR19-07.md`
- `docs/test-cases/TC-FR19-08.md`
- `docs/test-cases/TC-FR19-09.md`
- `docs/test-cases/TC-FR19-10.md`
- `docs/test-cases/TC-FR19-11.md`
- `docs/test-cases/TC-FR19-12.md`
- `docs/test-cases/TC-FR19-13.md`
- `docs/test-cases/TC-FR19-14.md`

## Ghi Chú Review Theo Đặc Tả

- Expected result bám đặc tả FR-19: admin xem danh sách user, không lộ password, xóa user, và không được tự xóa chính mình.
- Các case phân quyền user thường đưa thêm ràng buộc FR-12 vì FR-19 nằm trong nhóm Web Admin.
- Các case `TC-FR19-07`, `TC-FR19-10`, `TC-FR19-11` có khả năng phát hiện bug do code hiện tại chưa kiểm tra role admin và chưa chặn self-delete.
