# FR20-E-TC01: Mobile hiển thị empty state khi tìm kiếm không có kết quả

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Backend API đang chạy.
- Không có sản phẩm nào có tên chứa `ZZZ_NOT_FOUND_2026`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products?search=ZZZ_NOT_FOUND_2026 |
| Search keyword | ZZZ_NOT_FOUND_2026 |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Nhập `ZZZ_NOT_FOUND_2026` vào ô tìm kiếm.
3. Bấm nút `Tìm`.
4. Quan sát vùng danh sách sau khi request hoàn tất.

## Expected result
- Danh sách sản phẩm rỗng.
- Mobile app hiển thị thông báo empty state phù hợp, ví dụ `Không tìm thấy sản phẩm phù hợp`.
- Không hiển thị count sai như đang có sản phẩm.

## Status / Related bugs
Passed / None
