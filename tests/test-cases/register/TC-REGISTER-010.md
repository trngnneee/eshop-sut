# TC-REGISTER-010: Kiểm thử Email với độ dài vượt quá tối đa (101 ký tự)

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |

## Test steps
1. Mở form FR-01.
2. Nhập Email có độ dài 101 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Email vượt quá giới hạn tối đa 100 ký tự.

## Status / Related bugs
Not Run / None
