# FR20-X-TC01: Mobile hiển thị an toàn từ khóa dạng script tag

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
| Endpoint | GET /api/products?search=%3Cscript%3Ealert(1)%3C%2Fscript%3E |
| Search keyword | <script>alert(1)</script> |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Nhập `<script>alert(1)</script>` vào ô tìm kiếm.
3. Bấm nút `Tìm`.
4. Quan sát nhãn kết quả tìm kiếm và vùng danh sách.

## Expected result
- Từ khóa được hiển thị như text thuần trong React Native, không được render như HTML.
- Không có alert/script nào được thực thi.
- App không hiển thị HTML lỗi từ backend.

## Status / Related bugs
Passed / None
