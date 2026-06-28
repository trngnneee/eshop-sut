# FR20-X-TC02: Mobile hiển thị an toàn từ khóa có HTML event handler

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning / Security

## Preconditions
- Backend API đang chạy.
- Mobile app đang ở màn hình `Danh sách sản phẩm`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products?search=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E |
| Search keyword | <img src=x onerror=alert(1)> |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Nhập `<img src=x onerror=alert(1)>` vào ô tìm kiếm.
3. Bấm nút `Tìm`.
4. Quan sát nhãn kết quả tìm kiếm và vùng danh sách.

## Expected result
- Payload được hiển thị như text hoặc được xử lý an toàn.
- Không có HTML/event handler nào được thực thi.
- Mobile app không crash và không hiển thị lỗi backend thô.

## Status / Related bugs
Passed / None
