# TC-REGISTER-019: Kiểm thử Xác nhận mật khẩu với độ dài biên tối đa (50 ký tự)

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Xác nhận mật khẩu | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |

## Test steps
1. Mở form FR-01.
2. Nhập Xác nhận mật khẩu có độ dài đúng 50 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Xác nhận mật khẩu.

## Status / Related bugs
Not Run / None
