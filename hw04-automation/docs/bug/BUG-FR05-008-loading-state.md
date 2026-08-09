# [BUG][FR-05 Product Listing] Không hiển thị trạng thái loading khi tải sản phẩm

## Found by Test Case

TC-FR05-14

## Requirement liên quan

FR-05

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows
- **Browser**: Chromium, Firefox, WebKit
- **URL**: http://localhost:5173/
- **Build/Commit**: Latest

## Steps to reproduce

1. Intercept request `GET /api/products` và delay response.
2. Mở trang chủ web.
3. Quan sát UI trong lúc response chưa hoàn tất.

## Expected result

Trang hiển thị loading indicator, ví dụ text `Đang tải`, trong lúc chờ dữ liệu sản phẩm.

## Actual result

Không tìm thấy loading indicator trong lúc request sản phẩm bị delay.

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/27#issue-4746377610

