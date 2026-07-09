# TC-LOGIN-004: Kiểm thử tiêu chuẩn giao diện (UI) trang Đăng nhập

## Requirement ID
FR-21, FR-22

## Module / Test type / Technique
Login / UI / GUI Testing

## Preconditions
- Người dùng truy cập trang Đăng nhập (`http://localhost:5173/login`).

## Test data
Không yêu cầu dữ liệu nhập cụ thể.

## Test steps
1. Truy cập vào trang Đăng nhập của EShop.
2. Quan sát tiêu đề trang (Title).
3. Quan sát nhãn (Label) của trường nhập Email.
4. Nhập thử mật khẩu vào trường Mật khẩu và kiểm tra hiển thị.
5. Quan sát nhãn của nút Submit đăng nhập.
6. Kiểm tra sự xuất hiện của ký hiệu bắt buộc `*` bên cạnh các nhãn.

## Expected result
- Tiêu đề trang phải hiển thị đúng là **"Đăng Nhập"** (để phân biệt với trang Đăng ký).
- Nhãn của ô nhập email phải là **"Email"** hoặc **"Địa chỉ Email"** (thay vì hiển thị "Username").
- Trường nhập mật khẩu phải có thuộc tính `type="password"` để **ẩn mật khẩu** dưới dạng dấu chấm/sao khi nhập (không hiển thị rõ).
- Nút gửi form đăng nhập phải sử dụng tiếng Việt nhất quán là **"Đăng nhập"** (thay vì tiếng Anh "Sign In") theo FR-21.
- Có ký hiệu `*` bên cạnh các nhãn trường bắt buộc (Email, Mật khẩu) theo FR-22.

## Status / Related bugs
Fail / #34, #35, #36, #37, #38, #45, #46
