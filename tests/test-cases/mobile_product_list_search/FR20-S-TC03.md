# FR20-S-TC03: Mobile tìm kiếm với từ khóa rỗng để quay về toàn bộ danh sách

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Backend API đang chạy.
- Mobile app đang hiển thị kết quả của một lần tìm kiếm trước đó.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products?search= |
| Search keyword |  |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Tìm kiếm với từ khóa `iPhone` để thu hẹp kết quả.
3. Xóa toàn bộ nội dung ô tìm kiếm.
4. Bấm nút `Tìm`.

## Expected result
- Mobile app gửi request với từ khóa rỗng hoặc gọi lại danh sách sản phẩm.
- Danh sách quay về hiển thị toàn bộ sản phẩm.
- Không còn nhãn kết quả tìm kiếm cho từ khóa cũ.

## Status / Related bugs
Passed / None
