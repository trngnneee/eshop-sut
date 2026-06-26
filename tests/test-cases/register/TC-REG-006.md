# TC-REG-006: Đăng ký tài khoản thành công với mật khẩu dài đúng 8 ký tự

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis (3-Point - Valid)

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Pwd Length 8" |
| **email** | "tester_reg006@eshop.com" |
| **password** | "P@ss1234" |
| **confirm_password** | "P@ss1234" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống đăng ký thành công.
- Trả về mã HTTP 200 (hoặc 201).
- Trả về thông báo: "User registered successfully".

## Status / Related bugs
Pass / None
