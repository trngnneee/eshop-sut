# FR20-S-BVA-TC06: Kiểm thử Search Keyword tại biên tối đa 255 ký tự

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
| Boundary type | Max |
| Search keyword length | 255 |
| Search keyword | [Chuỗi 255 ký tự chữ a] |
| Endpoint | GET /api/products?search=[255_a] |

## Test steps
1. Nhập chuỗi 255 ký tự chữ `a` vào ô tìm kiếm.
2. Bấm nút `Tìm`.
3. Quan sát response và UI.

## Expected result
- Từ khóa 255 ký tự được chấp nhận theo giới hạn kiểm thử.
- Mobile app xử lý an toàn, không treo UI và không crash.
- Nếu không có sản phẩm khớp, app hiển thị empty state phù hợp.

## Status / Related bugs
Passed / None
