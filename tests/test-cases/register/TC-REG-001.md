# TC-REG-001: Đăng ký tài khoản thành công với thông tin hợp lệ

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning

## Preconditions
- Email đăng ký chưa từng tồn tại trên hệ thống.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Success" |
| **email** | "tester_success@eshop.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống thực hiện đăng ký thành công.
- Trả về mã HTTP 200 (hoặc 201).
- Trả về thông báo thành công: "User registered successfully".

## Status / Related bugs
Pass / None
