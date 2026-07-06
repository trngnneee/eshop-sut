# FR04-P-TC05: Từ chối số điện thoại chứa ký tự không phải chữ số

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
| phone | 01234abcde |

## Test steps
1. Mở trang Hồ sơ.
2. Nhập số điện thoại `01234abcde`.
3. Bấm nút Cập nhật.

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi phone.
- Số điện thoại cũ trong hồ sơ không bị thay đổi.

## Status / Related bugs
Failed / BUG-FR04-P-01 - Sai rule validate Số điện thoại
