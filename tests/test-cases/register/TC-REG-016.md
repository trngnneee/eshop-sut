# TC-REG-016: Đăng ký với Họ Tên chỉ chứa khoảng trắng

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "   " |
| **email** | "tester_reg016@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Họ Tên không được để trống.

## Status / Related bugs
Fail / [BUG-REG-011](../../bug-reports/BUG-REG-011.md)
