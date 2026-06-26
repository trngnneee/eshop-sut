# FR04-P-TC04: Từ chối số điện thoại không bắt đầu bằng 0

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập bằng JWT hợp lệ.
- Các trường name/address hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| phone | 9123456789 |

## Test steps
1. Mở trang Hồ sơ.
2. Nhập số điện thoại `9123456789`.
3. Bấm nút Cập nhật.

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi phone.
- Số điện thoại cũ trong hồ sơ không bị thay đổi.

## Status / Related bugs
Not Run / None
