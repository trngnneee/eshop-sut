# FR04-N-TC01: Kiểm thử Họ Tên để trống

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Họ Tên | [Để trống] |

## Test steps
1. Mở form FR-04.
2. Nhập các trường khác hợp lệ ngoại trừ Họ Tên để trống.
3. Bấm nút Submit.

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường Họ Tên.

## Status / Related bugs
Passed / None
