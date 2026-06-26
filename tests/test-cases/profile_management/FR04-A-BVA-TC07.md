# FR04-A-BVA-TC07: Kiểm thử Địa chỉ giao hàng mặc định với độ dài vượt quá tối đa (256 ký tự)

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Địa chỉ giao hàng mặc định | AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA |

## Test steps
1. Mở form FR-04.
2. Nhập Địa chỉ giao hàng mặc định có độ dài 256 ký tự.
3. Bấm nút Submit.

## Expected result
- Hệ thống báo lỗi độ dài Địa chỉ giao hàng mặc định vượt quá giới hạn tối đa 255 ký tự.

## Status / Related bugs
Not Run / None
