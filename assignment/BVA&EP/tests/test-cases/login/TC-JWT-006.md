# TC-JWT-006: Kiểm tra đăng nhập nhiều lần liên tiếp sinh ra các Token JWT khác nhau

## Requirement ID
FR-02

## Module / Test type / Technique
JWT / Functional Testing

## Preconditions
- Tài khoản hoạt động bình thường.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Thực hiện đăng nhập thành công lần 1, lưu token 1.
2. Thực hiện đăng nhập thành công lần 2 trên tab/thiết bị khác, lưu token 2.

## Expected result
- Token 1 và Token 2 khác nhau (do timestamp khác nhau).
- Cả hai token đều hoạt động song song hoặc token cũ bị thu hồi tùy chính sách hệ thống.

## Status / Related bugs
Pass / None
