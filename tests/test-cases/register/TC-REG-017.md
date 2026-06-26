# TC-REG-017: Đăng ký với Họ Tên không viết hoa chữ cái đầu hoặc viết hoa các chữ cái không đứng đầu

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "phan Quoc tHinh" |
| **email** | "tester_reg017@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống tự động chuẩn hóa thành chữ viết hoa đầu từ hoặc báo lỗi yêu cầu định dạng đúng.

## Status / Related bugs
Fail / [BUG-REG-006](../../bug-reports/BUG-REG-006.md)
