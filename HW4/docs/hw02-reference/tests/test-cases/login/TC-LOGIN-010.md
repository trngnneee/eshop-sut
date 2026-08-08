# TC-LOGIN-010: Kiểm tra nút ẩn/hiện mật khẩu trên form Đăng nhập

## Requirement ID
FR-22

## Module / Test type / Technique
Login / UI/UX / Usability Testing

## Preconditions
- Người dùng ở trang Đăng nhập.

## Test data
- Nhập mật khẩu: `Test1234!`

## Test steps
1. Nhập mật khẩu vào trường Mật khẩu.
2. Kiểm tra xem mật khẩu ban đầu có được che đi hay không.
3. Nhấp vào nút/biểu tượng ẩn/hiện mật khẩu (Toggle Show/Hide) bên cạnh trường mật khẩu và kiểm tra hiển thị.

## Expected result
- Mật khẩu mặc định phải được che đi dưới dạng `type="password"`.
- Có nút Toggle bên cạnh để người dùng bấm hiển thị rõ mật khẩu và bấm lại để ẩn đi.

## Status / Related bugs
Failed / #12
