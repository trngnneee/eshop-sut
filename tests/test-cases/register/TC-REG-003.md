# TC-REG-003: Đăng ký tài khoản thất bại do Email sai định dạng

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Email Format" |
| **email** | "invalid_email" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối đăng ký và trả về mã lỗi HTTP 400.
- Hiển thị thông báo lỗi: "Email không hợp lệ".

## Status / Related bugs
Fail / [BUG-REG-001](../../bug-reports/BUG-REG-001.md)
