# TC-REGISTER-002: Kiểm thử Họ Tên với độ dài dưới tối thiểu (0 ký tự)

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Họ Tên | [Để trống] |

## Test steps
1. Mở form FR-01.
2. Nhập Họ Tên có độ dài 0 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Họ Tên tối thiểu là 1 ký tự.

## Status / Related bugs
Not Run / None
