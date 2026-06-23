# TC-REGISTER-007: Kiểm thử Email với độ dài dưới tối thiểu (4 ký tự)

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaa |

## Test steps
1. Mở form FR-01.
2. Nhập Email có độ dài 4 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Email tối thiểu là 5 ký tự.

## Status / Related bugs
Not Run / None
