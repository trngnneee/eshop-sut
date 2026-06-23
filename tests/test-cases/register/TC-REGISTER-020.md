# TC-REGISTER-020: Kiểm thử Xác nhận mật khẩu với độ dài vượt quá tối đa (51 ký tự)

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Xác nhận mật khẩu | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |

## Test steps
1. Mở form FR-01.
2. Nhập Xác nhận mật khẩu có độ dài 51 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Xác nhận mật khẩu vượt quá giới hạn tối đa 50 ký tự.

## Status / Related bugs
Not Run / None
