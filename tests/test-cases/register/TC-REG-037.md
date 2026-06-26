# TC-REG-037: Đăng ký với Mật khẩu chứa mã độc XSS

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Pwd XSS" |
| **email** | "tester_pwd_xss@domain.com" |
| **password** | "<script>alert('XSS')</script>" |
| **confirm_password** | "<script>alert('XSS')</script>" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Mật khẩu không hợp lệ và mã hóa chuỗi đầu vào.

## Status / Related bugs
Fail / [BUG-REG-005](../../bug-reports/BUG-REG-005.md)
