# TC-ERR-001: Thông báo lỗi chung khi nhập Email không tồn tại

## Requirement ID
FR-22

## Module / Test type / Technique
Privacy / Security Testing

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | notfound@eshop.com |
| Mật khẩu | Password123! |

## Test steps
1. Nhập email không tồn tại.
2. Nhập mật khẩu bất kỳ.
3. Nhấp Đăng nhập.

## Expected result
- Thông báo lỗi chung: 'Invalid email or password'.
- Không tiết lộ email này chưa tồn tại trong hệ thống (tránh thu thập email).

## Status / Related bugs
Pass / None
