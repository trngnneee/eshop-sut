# FR04-P-TC01: Kiểm thử Số điện thoại để trống

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số điện thoại | [Để trống] |

## Test steps
1. Mở form FR-04.
2. Nhập các trường khác hợp lệ ngoại trừ Số điện thoại để trống.
3. Bấm nút Submit.

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường Số điện thoại.

## Status / Related bugs
Not Run / None
