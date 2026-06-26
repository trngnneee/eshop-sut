# FR04-A-TC01: Kiểm thử Địa chỉ giao hàng mặc định để trống

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đang ở form của FR-04

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Địa chỉ giao hàng mặc định | [Để trống] |

## Test steps
1. Mở form FR-04.
2. Nhập các trường khác hợp lệ ngoại trừ Địa chỉ giao hàng mặc định để trống.
3. Bấm nút Submit.

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường Địa chỉ giao hàng mặc định.

## Status / Related bugs
Failed / BUG-FR04-A-01 - Thiếu validate Địa chỉ giao hàng
