# FR04-P-BVA-TC02: Kiểm thử Số điện thoại với độ dài biên tối thiểu (10 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số điện thoại | 0123456789 |

## Test steps
1. Mở form FR-04.
2. Nhập Số điện thoại có độ dài 10 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống chấp nhận số điện thoại bắt đầu bằng 0 và có 10-11 chữ số.

## Status / Related bugs
Failed / BUG-FR04-P-01 - Sai rule validate Số điện thoại
