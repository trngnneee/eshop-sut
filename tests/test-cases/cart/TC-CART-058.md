# TC-CART-058: Sản phẩm có tên tiếng Việt có dấu

## Requirement ID
FR-07, FR-21

## Module / Test type / Technique
Cart / Functional / Domain Testing

## Preconditions
- Hệ thống có sản phẩm tên 'Áo thun nam xuất khẩu có cổ'.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Thêm sản phẩm trên vào giỏ hàng.
2. Truy cập `/cart`.

## Expected result
- Tên sản phẩm tiếng Việt hiển thị chính xác hoàn toàn, không bị lỗi font hoặc vỡ ký tự Unicode.

## Status / Related bugs
Not Run / None
