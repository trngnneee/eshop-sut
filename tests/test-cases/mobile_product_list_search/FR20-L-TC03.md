# FR20-L-TC03: Mobile hiển thị trạng thái loading khi đang tải danh sách

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Có thể mô phỏng mạng chậm bằng throttling hoặc delay backend.
- Mobile app đang ở màn hình Home.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products |
| Network | Slow 3G / delayed response |

## Test steps
1. Bật chế độ mạng chậm hoặc thêm delay cho request `GET /api/products`.
2. Mở app mobile hoặc kéo reload luồng tải danh sách nếu có.
3. Quan sát màn hình trong lúc request chưa hoàn tất.

## Expected result
- Màn hình hiển thị thông báo `Đang tải...` trong lúc request đang pending.
- Sau khi request hoàn tất, loading biến mất và danh sách hoặc empty state được hiển thị phù hợp.

## Status / Related bugs
Passed / None
