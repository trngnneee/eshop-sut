# TC-REG-035: Đăng ký với Email chứa mã độc XSS

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Email XSS" |
| **email** | "<script>alert('XSS')</script>@domain.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Email không hợp lệ và mã hóa chuỗi đầu vào.

## Status / Related bugs
Fail / [BUG-REG-005](../../bug-reports/BUG-REG-005.md)
