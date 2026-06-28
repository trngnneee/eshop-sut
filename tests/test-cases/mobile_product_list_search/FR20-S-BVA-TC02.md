# FR20-S-BVA-TC02: Kiểm thử Search Keyword với độ dài 1 ký tự

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
| Boundary type | Min+1 |
| Search keyword length | 1 |
| Search keyword | i |
| Endpoint | GET /api/products?search=i |

## Test steps
1. Nhập `i` vào ô tìm kiếm.
2. Bấm nút `Tìm`.
3. Quan sát danh sách kết quả.

## Expected result
- Từ khóa 1 ký tự được chấp nhận.
- Danh sách chỉ hiển thị sản phẩm có tên chứa ký tự `i` theo rule tìm kiếm.
- App không crash hoặc trả HTML lỗi.

## Status / Related bugs
Passed / None
