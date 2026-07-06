# FR20-S-BVA-TC01: Kiểm thử Search Keyword tại biên rỗng 0 ký tự

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Boundary Value Analysis

## Preconditions
- Backend API đang chạy.
- Mobile app đang ở màn hình `Danh sách sản phẩm`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Boundary type | Min |
| Search keyword length | 0 |
| Search keyword |  |
| Endpoint | GET /api/products?search= |

## Test steps
1. Xóa toàn bộ nội dung ô tìm kiếm.
2. Bấm nút `Tìm`.
3. Quan sát danh sách sản phẩm sau khi request hoàn tất.

## Expected result
- Từ khóa rỗng được chấp nhận.
- Mobile app hiển thị toàn bộ danh sách sản phẩm.
- Không hiển thị lỗi validate cho ô tìm kiếm.

## Status / Related bugs
Passed / None
