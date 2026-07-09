# TC-LOGIN-028: Kiểm tra đăng nhập với email viết hoa/thường xen kẽ để xác minh tính đồng nhất của email và cơ chế khóa

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Functional / Equivalence Partitioning

## Preconditions
- Đã đăng ký tài khoản `test_tc29@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống (đăng ký bằng chữ thường hoàn toàn).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email gốc | test_tc29@eshop.com |
| Email nhập liệu | TeSt_tC29@eShOp.CoM |
| Mật khẩu đúng | ValidPassword1! |
| Mật khẩu sai | WrongPass123! |

## Test steps
1. Gửi yêu cầu đăng nhập bằng email viết hoa/thường xen kẽ `TeSt_tC29@eShOp.CoM` và mật khẩu đúng `ValidPassword1!`. Xác minh đăng nhập thành công.
2. Thực hiện đăng xuất.
3. Gửi yêu cầu đăng nhập sai 3 lần liên tiếp bằng email viết hoa/thường xen kẽ `TeSt_tC29@eShOp.CoM` và mật khẩu sai `WrongPass123!`.
4. Xác minh xem tài khoản gốc `test_tc29@eshop.com` có bị khóa hay không (bằng cách thử đăng nhập bằng email thường `test_tc29@eshop.com` với mật khẩu đúng).

## Expected result
- Hệ thống phân biệt chữ hoa chữ thường đối với Email đăng nhập. Việc đăng nhập bằng email viết hoa/thường xen kẽ `TeSt_tC29@eShOp.CoM` và mật khẩu đúng sẽ bị từ chối đăng nhập với lỗi HTTP 401.
- Các lần đăng nhập sai bằng `TeSt_tC29@eShOp.CoM` không làm ảnh hưởng đến bộ đếm hoặc trạng thái khóa của tài khoản viết thường gốc `test_tc29@eshop.com`.

## Status / Related bugs
Pass / None
