# [BUG][FR-05 Product Search] Từ khóa tìm kiếm bị render thành HTML trong kết quả tìm kiếm

## Found by Test Case

TC-FR05-09, TC-FR05-10, TC-FR05-15

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
2. Nhập payload HTML, ví dụ `<strong id="fr05-html-injection">Injected</strong>`.
3. Gửi form tìm kiếm.
4. Lặp lại với payload `<script>alert("xss-fr05")</script>` hoặc `<image src=1 href=1 onerror="javascript:alert(1)"></image>`.

## Expected result

Từ khóa tìm kiếm được escape và hiển thị như text thường; không có thẻ HTML/script/image nào được chèn vào DOM và không có JavaScript được thực thi.

## Actual result

DOM có phần tử được sinh từ input người dùng: `#fr05-html-injection`, `script`, hoặc `image`. Với payload image, phần summary chỉ còn `Kết quả tìm kiếm cho:` kèm một phần tử ảnh, cho thấy input đã bị render thành HTML.

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/53#issue-4748338316



