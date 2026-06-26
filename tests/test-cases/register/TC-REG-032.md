# TC-REG-032: Đăng ký với Email có độ dài phần domain-part bằng 1 ký tự

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis (3-Point - Invalid)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Email Domain Len 1" |
| **email** | "user@d.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi định dạng Email không hợp lệ.

## Status / Related bugs
Fail / [BUG-REG-001](../../bug-reports/BUG-REG-001.md)
