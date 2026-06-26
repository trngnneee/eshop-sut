# TC-REG-002: Đăng ký tài khoản thất bại do thiếu Họ Tên

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "" |
| **email** | "tester_reg002@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối đăng ký và trả về mã lỗi HTTP 400.
- Hiển thị thông báo lỗi: "Họ tên không được để trống".

## Status / Related bugs
Fail / [BUG-REG-002](../../bug-reports/BUG-REG-002.md)
