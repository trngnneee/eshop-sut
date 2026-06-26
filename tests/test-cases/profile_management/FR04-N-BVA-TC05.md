# FR04-N-BVA-TC05: Kiểm thử Họ Tên với độ dài Max-1 (49 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Họ Tên | NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN |

## Test steps
1. Mở form FR-04.
2. Nhập Họ Tên có độ dài 49 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên.

## Status / Related bugs
Passed / None
