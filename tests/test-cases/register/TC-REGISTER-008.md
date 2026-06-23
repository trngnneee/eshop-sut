# TC-REGISTER-008: Kiểm thử Email với độ dài biên tối thiểu (5 ký tự)

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaa |

## Test steps
1. Mở form FR-01.
2. Nhập Email có độ dài đúng 5 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Email.

## Status / Related bugs
Not Run / None
