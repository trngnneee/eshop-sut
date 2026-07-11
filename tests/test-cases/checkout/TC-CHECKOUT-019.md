# TC-CHECKOUT-019: Chưa đăng nhập truy cập trực tiếp trang Thanh toán

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng chưa đăng nhập
- Giỏ hàng có thể có hoặc không có sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Trạng thái đăng nhập | Chưa đăng nhập |
| Điểm vào | URL trang Thanh toán trực tiếp |

## Test steps
1. Đảm bảo chưa đăng nhập.
2. Truy cập trực tiếp trang Thanh toán (không qua nút từ Giỏ hàng).
3. Thử xác nhận thanh toán nếu nút hiển thị.

## Expected result
- Hệ thống không cho người chưa đăng nhập hoàn tất thanh toán (FR-08).
- Yêu cầu đăng nhập hoặc chặn thao tác xác nhận đơn hàng.

## Sub-domains covered
SD-A01 (chưa đăng nhập — lối vào trực tiếp URL)

## Type
Invalid

## Status / Related bugs
Not Run / None
