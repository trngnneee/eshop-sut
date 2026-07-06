# FR04-A-TC02: Cập nhật địa chỉ giao hàng hợp lệ

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
| shipping_address | 123 Nguyen Hue, Quan 1, TP.HCM |

## Test steps
1. Mở trang Hồ sơ.
2. Nhập địa chỉ giao hàng mặc định hợp lệ.
3. Bấm nút Cập nhật.
4. Tải lại hồ sơ người dùng.

## Expected result
- Hệ thống cập nhật hồ sơ thành công.
- Địa chỉ giao hàng mặc định mới được lưu cho người dùng hiện tại.

## Status / Related bugs
Passed / None
