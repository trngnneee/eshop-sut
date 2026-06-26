# TC-REG-031: Đăng ký với Email có phần domain-part chứa chữ in hoa

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Email Upper Domain" |
| **email** | "user@DOMAIN.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống tự động chuyển thành chữ thường hoặc từ chối áp dụng và báo lỗi.

## Status / Related bugs
Fail / [BUG-REG-015](../../bug-reports/BUG-REG-015.md)
