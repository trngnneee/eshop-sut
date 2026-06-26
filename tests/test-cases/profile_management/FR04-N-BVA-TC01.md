# FR04-N-BVA-TC01: Kiểm thử Họ Tên với độ dài dưới tối thiểu (0 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Họ Tên | [Để trống] |

## Test steps
1. Mở form FR-04.
2. Nhập Họ Tên có độ dài 0 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Họ Tên tối thiểu là 1 ký tự.

## Status / Related bugs
Not Run / None
