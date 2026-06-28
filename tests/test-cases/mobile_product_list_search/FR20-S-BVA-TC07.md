# FR20-S-BVA-TC07: Kiểm thử Search Keyword vượt biên tối đa 256 ký tự

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
| Boundary type | Max+1 |
| Search keyword length | 256 |
| Search keyword | [Chuỗi 256 ký tự chữ a] |
| Endpoint | GET /api/products?search=[256_a] |

## Test steps
1. Nhập chuỗi 256 ký tự chữ `a` vào ô tìm kiếm.
2. Bấm nút `Tìm`.
3. Quan sát validation, response và UI.

## Expected result
- Hệ thống từ chối từ khóa vượt giới hạn bằng validation hoặc xử lý request an toàn với lỗi phù hợp.
- Mobile app không treo UI, không crash và không hiển thị HTML lỗi thô.
- Không trả về danh sách sản phẩm sai phạm vi.

## Status / Related bugs
Passed / None
