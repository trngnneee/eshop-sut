# FR20-S-TC01: Mobile tìm kiếm sản phẩm theo từ khóa khớp một phần tên

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Backend API đang chạy.
- Database có sản phẩm `iPhone 15 Pro Max`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products?search=iPhone |
| Search keyword | iPhone |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Nhập `iPhone` vào ô `Tìm kiếm...`.
3. Bấm nút `Tìm`.
4. Quan sát danh sách kết quả.

## Expected result
- Mobile app gửi request tìm kiếm theo tên sản phẩm.
- Danh sách chỉ hiển thị các sản phẩm có tên chứa `iPhone`.
- Nhãn `Kết quả tìm kiếm cho: iPhone` hiển thị an toàn dưới dạng text.

## Status / Related bugs
Passed / None
