# FR04-N-TC02: Cập nhật họ tên hợp lệ

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập bằng JWT hợp lệ.
- Người dùng đang ở trang Hồ sơ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| name | Nguyen Van A |
| phone | 0123456789 |
| shipping_address | 123 Nguyen Hue, Quan 1, TP.HCM |

## Test steps
1. Mở trang Hồ sơ.
2. Nhập họ tên hợp lệ và giữ phone/address hợp lệ.
3. Bấm nút Cập nhật.
4. Tải lại hồ sơ người dùng.

## Expected result
- Hệ thống cập nhật hồ sơ thành công.
- Tên mới được hiển thị trong hồ sơ của chính người dùng.

## Status / Related bugs
Not Run / None
