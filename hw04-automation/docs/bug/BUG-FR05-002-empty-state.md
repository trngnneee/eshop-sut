# [BUG][FR-05 Product Listing] Không hiển thị empty state khi tìm kiếm không có kết quả

## Found by Test Case

TC-FR05-06

## Requirement liên quan

FR-05

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: Chromium, Firefox, WebKit
- **URL**: http://localhost:5173/
- **Build/Commit**: Latest

## Steps to reproduce

1. Mở trang chủ web.
2. Nhập từ khóa không khớp sản phẩm nào, ví dụ `SanPhamKhongTonTaiFR05`.
3. Gửi form tìm kiếm.

## Expected result

Không có thẻ sản phẩm nào hiển thị và có thông báo empty state phù hợp, ví dụ `Không có sản phẩm phù hợp`.

## Actual result

Không tìm thấy thông báo empty state trên giao diện.

## Link Github Issue:
https://github.com/trngnneee/eshop-sut/issues/28#issue-4746603879
