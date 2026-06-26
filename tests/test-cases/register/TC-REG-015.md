# TC-REG-015: Đăng ký với Họ Tên chứa lệnh SQL Injection

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "' OR 1=1 --" |
| **email** | "tester_reg015@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Họ Tên không hợp lệ và xử lý chuỗi an toàn.

## Status / Related bugs
Fail / [BUG-REG-014](../../bug-reports/BUG-REG-014.md)
