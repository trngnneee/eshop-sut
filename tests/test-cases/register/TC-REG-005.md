# TC-REG-005: Đăng ký tài khoản thất bại do mật khẩu ngắn hơn 8 ký tự

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis (3-Point - Invalid)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Pwd Length" |
| **email** | "tester_reg005@eshop.com" |
| **password** | "P@ss123" |
| **confirm_password** | "P@ss123" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối đăng ký và trả về mã lỗi HTTP 400.
- Hiển thị thông báo lỗi: "Mật khẩu phải từ 8 ký tự trở lên".

## Status / Related bugs
Fail / [BUG-REG-003](../../bug-reports/BUG-REG-003.md)
