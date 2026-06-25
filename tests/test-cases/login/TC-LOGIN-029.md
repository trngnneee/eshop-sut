# TC-LOGIN-029: Kiểm tra đăng nhập với email viết hoa/thường xen kẽ để xác minh tính đồng nhất của email và cơ chế khóa

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
- Email không phân biệt chữ hoa chữ thường. Việc đăng nhập bằng `TeSt_tC29@eShOp.CoM` và mật khẩu đúng phải thành công.
- 3 lần đăng nhập sai bằng `TeSt_tC29@eShOp.CoM` phải làm khóa tài khoản gốc `test_tc29@eshop.com`. Khi tài khoản đã bị khóa, việc đăng nhập lại bằng email viết thường `test_tc29@eshop.com` với mật khẩu đúng phải bị chặn với lỗi HTTP 403.

## Status / Related bugs
Failed / #48
