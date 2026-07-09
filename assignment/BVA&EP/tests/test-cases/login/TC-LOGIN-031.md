# TC-LOGIN-031: Đăng nhập thất bại khi để Email rỗng

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | [Để trống] |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Để trống trường Email.
2. Nhập mật khẩu đúng.
3. Nhấn nút 'Đăng nhập'.

## Expected result
- Hệ thống hiển thị thông báo lỗi bắt buộc nhập email (ví dụ: 'Email/Username is required').
- Ngăn chặn gửi yêu cầu API lên server.

## Status / Related bugs
Pass / None
