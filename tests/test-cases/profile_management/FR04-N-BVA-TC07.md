# FR04-N-BVA-TC07: Kiểm thử Họ Tên với độ dài vượt quá tối đa (51 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Họ Tên | NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN |

## Test steps
1. Mở form FR-04.
2. Nhập Họ Tên có độ dài 51 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Họ Tên vượt quá giới hạn tối đa 50 ký tự.

## Status / Related bugs
Not Run / None
