# TC-CART-054: Nhấn “Thêm vào giỏ hàng” liên tục nhiều lần rất nhanh

## Requirement ID
FR-07, FR-24

## Module / Test type / Technique
Cart / Functional / Robustness / Race Condition

## Preconditions
- Người dùng ở trang chủ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Nhấp liên tiếp 5 lần thật nhanh vào nút 'Thêm vào giỏ hàng' của sản phẩm A.
2. Truy cập `/cart` kiểm tra số lượng.

## Expected result
- Hệ thống xử lý bất đồng bộ chính xác, số lượng sản phẩm A được cộng dồn tăng đúng lên thêm 5 đơn vị.

## Status / Related bugs
Pass / None
