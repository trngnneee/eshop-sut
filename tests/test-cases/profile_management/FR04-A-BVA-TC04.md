# FR04-A-BVA-TC04: Kiểm thử Địa chỉ giao hàng mặc định với độ dài Nominal (130 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Địa chỉ giao hàng mặc định | AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA |

## Test steps
1. Mở form FR-04.
2. Nhập Địa chỉ giao hàng mặc định có độ dài 130 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Địa chỉ giao hàng mặc định.

## Status / Related bugs
Not Run / None
