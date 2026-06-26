# TC-REG-007: Đăng ký tài khoản thất bại do mật khẩu thiếu chữ hoa

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Pwd Upper" |
| **email** | "tester_reg007@eshop.com" |
| **password** | "secure123!" |
| **confirm_password** | "secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống từ chối đăng ký và trả về mã lỗi HTTP 400.
- Hiển thị thông báo lỗi: "Mật khẩu phải chứa ít nhất 1 chữ hoa".

## Status / Related bugs
Fail / [BUG-REG-008](../../bug-reports/BUG-REG-008.md)
