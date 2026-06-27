# TC-CART-083: Ảnh sản phẩm lỗi URL hoặc không tải được

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Có sản phẩm lỗi ảnh trong kho.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| imageUrl | `'http://invalid-url.com/non-existent.jpg'` |

## Test steps
1. Thêm sản phẩm có URL ảnh bị hỏng (lỗi 404 hoặc không hợp lệ) vào giỏ hàng.
2. Truy cập trang giỏ hàng và kiểm tra xem có ảnh fallback/mặc định thay thế được load để không làm vỡ layout bảng.


## Expected result
- Hiển thị ảnh mặc định, UI không vỡ

## Status / Related bugs
Not Run / None
