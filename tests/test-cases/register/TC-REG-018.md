# TC-REG-018: Đăng ký với Họ Tên có độ dài bằng 1 ký tự

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis (3-Point - Invalid)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "A" |
| **email** | "tester_reg018@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Họ Tên quá ngắn.

## Status / Related bugs
Fail / [BUG-REG-012](../../bug-reports/BUG-REG-012.md)
