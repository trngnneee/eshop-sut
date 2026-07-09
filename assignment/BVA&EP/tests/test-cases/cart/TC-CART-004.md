# TC-CART-004: Hiển thị breadcrumb trên trang giỏ hàng

## Requirement ID
FR-23

## Module / Test type / Technique
Cart / UI Requirement / UI Requirement

## Preconditions
- Người dùng đã đăng nhập vào hệ thống.
- Người dùng đang ở bất kỳ trang nào và chuyển hướng đến trang `/cart`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Quan sát phần đầu trang phía dưới thanh điều hướng.

## Expected result
- Có thanh breadcrumb hiển thị đường dẫn định vị dạng: 'Trang chủ > Giỏ hàng' hoặc tương đương.
- Các thành phần trong breadcrumb hoạt động chính xác (click vào 'Trang chủ' chuyển về trang chủ).

## Status / Related bugs
Fail / BUG-FR07-B-08
