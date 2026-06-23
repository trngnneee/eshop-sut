# TC-REGISTER-003: Kiểm thử Họ Tên với độ dài biên tối thiểu (1 ký tự)

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Họ Tên | a |

## Test steps
1. Mở form FR-01.
2. Nhập Họ Tên có độ dài đúng 1 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên.

## Status / Related bugs
Not Run / None
