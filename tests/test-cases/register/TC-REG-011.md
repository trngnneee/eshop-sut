# TC-REG-011: Đăng ký tài khoản thất bại do xác nhận mật khẩu không khớp

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Confirm Pwd" |
| **email** | "tester_reg011@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123#" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối đăng ký và trả về mã lỗi HTTP 400.
- Hiển thị thông báo lỗi: "Mật khẩu xác nhận không khớp".

## Status / Related bugs
Fail / [BUG-REG-009](../../bug-reports/BUG-REG-009.md)
