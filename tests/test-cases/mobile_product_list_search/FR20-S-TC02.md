# FR20-S-TC02: Mobile tìm kiếm sản phẩm bằng từ khóa chữ thường

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Backend API đang chạy.
- Database có sản phẩm `Samsung Galaxy S24 Ultra`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products?search=samsung |
| Search keyword | samsung |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Nhập `samsung` vào ô tìm kiếm.
3. Bấm nút `Tìm`.
4. Quan sát danh sách kết quả.

## Expected result
- Hệ thống tìm kiếm theo tên sản phẩm không phụ thuộc chữ hoa/thường cho dữ liệu Latin thông dụng.
- Danh sách hiển thị `Samsung Galaxy S24 Ultra`.
- Không hiển thị sản phẩm không khớp từ khóa.

## Status / Related bugs
Passed / None
