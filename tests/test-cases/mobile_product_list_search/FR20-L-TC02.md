# FR20-L-TC02: Mobile card sản phẩm hiển thị đủ ảnh, tên và giá

## Requirement ID
FR-20

## Module / Test type / Technique
Mobile Product List & Search / Functional / Equivalence Partitioning

## Preconditions
- Backend API đang chạy.
- Danh sách sản phẩm đã tải thành công trên mobile.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Platform | Mobile React Native / Expo |
| Sample product | {"name": "iPhone 15 Pro Max", "price": 30000000, "imageUrl": "https://placehold.co/300x300/png?text=iPhone+15"} |

## Test steps
1. Mở app mobile ở màn hình `Danh sách sản phẩm`.
2. Tìm card của sản phẩm `iPhone 15 Pro Max`.
3. Kiểm tra các thành phần hiển thị trên card.

## Expected result
- Card hiển thị ảnh sản phẩm.
- Card hiển thị tên sản phẩm.
- Giá hiển thị với ký hiệu `₫` và định dạng phân cách hàng nghìn.
- Card có thao tác `Xem chi tiết` và `Thêm vào giỏ`.

## Status / Related bugs
Passed / None
