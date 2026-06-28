# FR20-S-TC04: Mobile xử lý từ khóa có ký tự đặc biệt không khớp sản phẩm

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Backend API đang chạy.
- Không có sản phẩm nào có tên chứa chuỗi `@@@###`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products?search=%40%40%40%23%23%23 |
| Search keyword | @@@### |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Nhập `@@@###` vào ô tìm kiếm.
3. Bấm nút `Tìm`.
4. Quan sát response và UI.

## Expected result
- Hệ thống xử lý từ khóa đặc biệt an toàn, không crash và không trả HTML lỗi.
- Danh sách không hiển thị sản phẩm không khớp.
- Mobile app hiển thị empty state phù hợp khi không có kết quả.

## Status / Related bugs
Passed / None
