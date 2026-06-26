# FR04-A-BVA-TC01: Kiểm thử Địa chỉ giao hàng mặc định với độ dài dưới tối thiểu (4 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Địa chỉ giao hàng mặc định | AAAA |

## Test steps
1. Mở form FR-04.
2. Nhập Địa chỉ giao hàng mặc định có độ dài 4 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Địa chỉ giao hàng mặc định tối thiểu là 5 ký tự.

## Status / Related bugs
Not Run / None
