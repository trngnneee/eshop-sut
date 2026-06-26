# TC-REG-008: Đăng ký tài khoản thất bại do mật khẩu thiếu chữ thường

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Pwd Lower" |
| **email** | "tester_reg008@eshop.com" |
| **password** | "SECURE123!" |
| **confirm_password** | "SECURE123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối đăng ký và trả về mã lỗi HTTP 400.
- Hiển thị thông báo lỗi: "Mật khẩu phải chứa ít nhất 1 chữ thường".

## Status / Related bugs
Fail / [BUG-REG-008](../../bug-reports/BUG-REG-008.md)
