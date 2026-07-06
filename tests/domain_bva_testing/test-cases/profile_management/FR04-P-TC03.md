# FR04-P-TC03: Cập nhật số điện thoại hợp lệ 11 chữ số bắt đầu bằng 0

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
| phone | 01234567890 |

## Test steps
1. Mở trang Hồ sơ.
2. Nhập số điện thoại `01234567890`.
3. Bấm nút Cập nhật.
4. Tải lại hồ sơ người dùng.

## Expected result
- Hệ thống chấp nhận số điện thoại.
- Số điện thoại được lưu đúng cho hồ sơ của người dùng hiện tại.

## Status / Related bugs
Failed / BUG-FR04-P-01 - Sai rule validate Số điện thoại
