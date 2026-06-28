# FR20-L-TC01: Mobile hiển thị danh sách tất cả sản phẩm khi vào trang chủ

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Backend API đang chạy và mobile app kết nối được tới `API_URL`.
- Database có tối thiểu 5 sản phẩm seed.
- Người dùng mở app mobile ở màn hình Home.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Endpoint | GET /api/products |
| Search keyword |  |
| Expected seed products | ["iPhone 15 Pro Max", "Samsung Galaxy S24 Ultra", "MacBook Pro M3", "Tai nghe AirPods Pro 2", "Bàn phím cơ Keychron Q1"] |

## Test steps
1. Khởi chạy backend và frontend-mobile.
2. Mở app mobile và ở màn hình `Danh sách sản phẩm`.
3. Không nhập từ khóa tìm kiếm.
4. Quan sát danh sách sản phẩm sau khi trạng thái loading kết thúc.

## Expected result
- Mobile app gọi `GET /api/products` hoặc `GET /api/products?search=` thành công.
- Danh sách hiển thị tất cả sản phẩm seed.
- Màn hình không hiển thị lỗi HTML hoặc lỗi mạng.
- Dòng tổng kết hiển thị đúng số lượng sản phẩm đang được render.

## Status / Related bugs
Passed / None
