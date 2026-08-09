# [BUG][FR-05 Product Search] API tìm kiếm sản phẩm nối chuỗi SQL trực tiếp

## Found by Test Case

TC-FR05-11

## Requirement liên quan

FR-05, SEC-04

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows
- **Browser**: Chromium, Firefox, WebKit
- **URL**: http://localhost:5173/
- **Build/Commit**: Latest

## Steps to reproduce

1. Mở trang chủ web.
2. Nhập payload SQL-like: `%' OR '1'='1`.
3. Gửi form tìm kiếm.
4. Quan sát response/danh sách sản phẩm trả về.

## Expected result

API xử lý keyword như dữ liệu đầu vào thông thường, không trả về toàn bộ sản phẩm ngoài phạm vi tìm kiếm.

## Actual result

Backend tạo query bằng template string trong `/api/products`, làm payload có thể thay đổi điều kiện `LIKE` và gây rủi ro trả dữ liệu ngoài phạm vi tìm kiếm.

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/60#issue-4753686069

