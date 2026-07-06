# FR20-S-BVA-TC03: Kiểm thử Search Keyword với độ dài 2 ký tự

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
| Boundary type | Min+2 |
| Search keyword length | 2 |
| Search keyword | ip |
| Endpoint | GET /api/products?search=ip |

## Test steps
1. Nhập `ip` vào ô tìm kiếm.
2. Bấm nút `Tìm`.
3. Quan sát danh sách kết quả.

## Expected result
- Từ khóa 2 ký tự được chấp nhận.
- Danh sách chỉ hiển thị sản phẩm khớp từ khóa.
- Nhãn kết quả tìm kiếm hiển thị đúng từ khóa `ip`.

## Status / Related bugs
Passed / None
