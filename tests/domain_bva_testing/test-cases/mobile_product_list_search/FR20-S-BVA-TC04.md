# FR20-S-BVA-TC04: Kiểm thử Search Keyword với độ dài danh nghĩa 20 ký tự

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
| Boundary type | Nominal |
| Search keyword length | 20 |
| Search keyword | iphone pro max query |
| Endpoint | GET /api/products?search=iphone%20pro%20max%20query |

## Test steps
1. Nhập từ khóa 20 ký tự `iphone pro max query` vào ô tìm kiếm.
2. Bấm nút `Tìm`.
3. Quan sát response và UI.

## Expected result
- Từ khóa 20 ký tự được xử lý an toàn.
- Mobile app hiển thị danh sách khớp hoặc empty state phù hợp.
- Không có lỗi encoding khoảng trắng trong URL query.

## Status / Related bugs
Passed / None
