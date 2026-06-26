# TC-REG-038: Đăng ký với Mật khẩu chứa lệnh SQL Injection

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Pwd SQLi" |
| **email** | "tester_pwd_sqli@domain.com" |
| **password** | "' OR '1'='1" |
| **confirm_password** | "' OR '1'='1" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Mật khẩu không hợp lệ và xử lý chuỗi an toàn.

## Status / Related bugs
Fail / [BUG-REG-014](../../bug-reports/BUG-REG-014.md)
