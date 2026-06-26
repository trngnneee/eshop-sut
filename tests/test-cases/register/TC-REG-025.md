# TC-REG-025: Đăng ký với Email chứa 2 dấu chấm liên tiếp ở domain-part

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Email Double Dot" |
| **email** | "user@domain..com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi định dạng Email không hợp lệ.

## Status / Related bugs
Fail / [BUG-REG-001](../../bug-reports/BUG-REG-001.md)
