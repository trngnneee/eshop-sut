# FR20-X-TC03: Mobile chống SQL injection qua từ khóa tìm kiếm

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning / Security

## Preconditions
- Backend API đang chạy.
- Database có nhiều sản phẩm seed để phát hiện trường hợp query bị broaden.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products?search=%25'%20OR%20'1'%3D'1 |
| Search keyword | %' OR '1'='1 |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Nhập `%' OR '1'='1` vào ô tìm kiếm.
3. Bấm nút `Tìm`.
4. Đối chiếu danh sách trả về với kết quả tìm kiếm theo tên sản phẩm thực tế.

## Expected result
- Backend phải xử lý từ khóa bằng truy vấn parameterized hoặc escape an toàn.
- Payload không được làm query trả về toàn bộ sản phẩm ngoài tiêu chí tên sản phẩm.
- Mobile app không hiển thị dữ liệu sai phạm vi hoặc HTML lỗi.

## Status / Related bugs
Failed / BUG-FR20-X-01 - SQL injection qua từ khóa tìm kiếm trả về toàn bộ danh sách sản phẩm
