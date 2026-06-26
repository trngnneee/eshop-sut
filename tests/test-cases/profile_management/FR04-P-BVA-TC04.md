# FR04-P-BVA-TC04: Kiểm thử Số điện thoại với độ dài vượt quá tối đa (12 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số điện thoại | 012345678901 |

## Test steps
1. Mở form FR-04.
2. Nhập Số điện thoại có độ dài 12 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống từ chối số điện thoại vì phải bắt đầu bằng 0 và có 10-11 chữ số.

## Status / Related bugs
Not Run / None
