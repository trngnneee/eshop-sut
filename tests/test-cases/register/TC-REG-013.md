# TC-REG-013: Đăng ký với Họ Tên chứa ký tự đặc biệt

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Nguyễn@Văn_A" |
| **email** | "tester_reg013@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi Họ Tên không hợp lệ.

## Status / Related bugs
Fail / [BUG-REG-010](../../bug-reports/BUG-REG-010.md)
