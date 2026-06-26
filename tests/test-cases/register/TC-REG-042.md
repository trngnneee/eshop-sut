# TC-REG-042: Đăng ký tài khoản từ giao diện Frontend Web với mật khẩu mạnh chứa ký tự đặc biệt thực tế

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / UI Testing / Scenario

## Preconditions
- Người dùng truy cập trang Đăng ký từ giao diện Frontend Web.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **Họ Tên** | "Tester Web" |
| **Email** | "tester_web@eshop.com" |
| **Mật khẩu** | "Secure123!" |

## Test steps
1. Nhập các giá trị dữ liệu kiểm thử vào form đăng ký ở Frontend Web.
2. Nhấp nút "Đăng Ký".

## Expected result
- Hệ thống cho phép đăng ký thành công và chuyển người dùng về trang Đăng nhập.
- Giao diện có trường "Xác nhận mật khẩu" để khớp với mật khẩu.

## Status / Related bugs
Fail / [BUG-REG-016](../../bug-reports/BUG-REG-016.md)
