# FR04-N-BVA-TC06: Kiểm thử Họ Tên với độ dài biên tối đa (50 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Họ Tên | NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN |

## Test steps
1. Mở form FR-04.
2. Nhập Họ Tên có độ dài 50 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên.

## Status / Related bugs
Not Run / None
