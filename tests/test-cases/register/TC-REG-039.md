# TC-REG-039: Đăng ký với Xác nhận mật khẩu chứa mã độc XSS

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Confirm XSS" |
| **email** | "tester_conf_xss@domain.com" |
| **password** | "Secure123!" |
| **confirm_password** | "<script>alert('XSS')</script>" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Mật khẩu không khớp và mã hóa chuỗi đầu vào.

## Status / Related bugs
Fail / [BUG-REG-005](../../bug-reports/BUG-REG-005.md)
