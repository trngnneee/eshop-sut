# TC-REG-014: Đăng ký với Họ Tên chứa mã độc XSS

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "<script>alert('XSS')</script>" |
| **email** | "tester_reg014@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Họ Tên không hợp lệ và mã hóa chuỗi không cho thực thi script.

## Status / Related bugs
Fail / [BUG-REG-005](../../bug-reports/BUG-REG-005.md)
