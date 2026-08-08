# TC-LOGIN-021: Kiểm tra tính tương thích với trình quản lý mật khẩu tự động điền (Autofill)
## Requirement ID
FR-22
## Module / Test type / Technique
Login / UI/UX / Boundary Value Analysis (Input Attributes)
## Preconditions
- Người dùng sử dụng trình duyệt hỗ trợ lưu mật khẩu (Chrome, Firefox, Safari) và đã lưu tài khoản e-shop.
## Test data
Thông tin tài khoản đã lưu trong trình duyệt.
## Test steps
1. Truy cập vào trang đăng nhập của Web và Admin.
2. Kiểm tra xem trình duyệt có hiển thị gợi ý tự động điền tài khoản/mật khẩu lên form hay không.
3. Nhấp đúp hoặc bấm vào gợi ý để thực hiện điền tự động.
4. Kiểm tra xem các trường `<input>` có đầy đủ thuộc tính định danh chuẩn (`name` và `autocomplete`) không.
## Expected result
- Trình quản lý mật khẩu nhận diện đúng biểu mẫu đăng nhập để hiển thị gợi ý tự động điền.
- Các trường nhập liệu có thuộc tính `name="email"` / `autocomplete="username"` và `name="password"` / `autocomplete="current-password"` để tương thích tối đa với các tiện ích mở rộng quản lý mật khẩu.
## Status / Related bugs
Failed / BUG-FR02-A-15
