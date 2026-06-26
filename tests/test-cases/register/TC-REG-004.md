# TC-REG-004: Đăng ký tài khoản thất bại do Email đã tồn tại trong hệ thống

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Email "test@eshop.com" đã tồn tại trong hệ thống (Seeded data).

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Email Exist" |
| **email** | "test@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối đăng ký và trả về mã lỗi HTTP 400 hoặc 409.
- Hiển thị thông báo lỗi: "Email đã được sử dụng".

## Status / Related bugs
Fail / [BUG-REG-007](../../bug-reports/BUG-REG-007.md)
