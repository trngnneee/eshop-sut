# FR04-A-TC03: Từ chối địa chỉ chỉ gồm khoảng trắng

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập bằng JWT hợp lệ.
- Các trường name/phone hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| shipping_address |       |

## Test steps
1. Mở trang Hồ sơ.
2. Nhập địa chỉ chỉ gồm khoảng trắng.
3. Bấm nút Cập nhật.

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi address.
- Địa chỉ giao hàng cũ không bị thay đổi.

## Status / Related bugs
Failed / BUG-FR04-A-01 - Thiếu validate Địa chỉ giao hàng
