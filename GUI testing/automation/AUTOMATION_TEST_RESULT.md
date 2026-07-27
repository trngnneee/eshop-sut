# Kết quả Automation Test — EShop Product List

## Thông tin lần chạy

| Thuộc tính | Giá trị |
|---|---|
| Ngày chạy | 2026-07-20 |
| Màn hình | Danh sách sản phẩm — `/` |
| Công cụ | Playwright Test 1.61.1 |
| Trình duyệt | Chromium — Chrome for Testing 149.0.7827.55 |
| Dữ liệu | Mock API `/api/products` bằng `page.route()` |
| Tổng số test | 20 |
| Pass | 13 |
| Fail | 7 |
| Thời gian | 21.5 giây |
| Pass rate | 65% |

## Các test thất bại

| ID | Kết quả thực tế | Kết quả mong đợi | Mức độ đề xuất |
|---|---|---|---|
| PLP-FUN-05 | Tìm từ khóa không tồn tại làm danh sách trống nhưng không có thông báo. | Hiển thị thông báo `Không tìm thấy sản phẩm`. | Medium |
| PLP-STA-01 | Trong lúc API chậm, vùng danh sách trống và không có loading indicator. | Hiển thị loading state có `role="status"`. | Medium |
| PLP-STA-02 | API trả mảng rỗng nhưng màn hình không có empty state. | Hiển thị thông báo `Chưa có sản phẩm`. | Medium |
| PLP-STA-03 | API trả HTTP 500 dạng JSON nhưng màn hình không hiển thị thông báo lỗi. | Hiển thị thông báo thân thiện có `role="alert"`. | High |
| PLP-VAL-02 | Payload `<img src=x onerror=alert(1)>` được render và thực thi; cờ XSS chuyển thành `true`. | Payload chỉ được hiển thị như text, không tạo HTML và không chạy JavaScript. | Critical |
| PLP-RES-02 | Tại viewport `768 × 1024`, grid hiển thị 3 cột. | Grid tablet hiển thị 2 cột và không tràn ngang. | Low |
| PLP-ACC-02 | Accessible name của input là `Tìm kiếm...`; test dừng trước kiểm tra alt. Mã nguồn hiện đặt `alt=""` cho ảnh sản phẩm. | Input có tên `Tìm kiếm sản phẩm`; ảnh có alt là tên sản phẩm. | Medium |

## Artifact

- Báo cáo HTML: [`playwright-report/index.html`](playwright-report/index.html)
- Screenshot, video và trace cho từng test Fail: thư mục [`test-results/`](test-results/)

Mỗi thư mục lỗi có `test-failed-1.png`, `video.webm`, `trace.zip` và `error-context.md`. Có thể mở trace bằng:

```powershell
npx playwright show-trace "test-results/<failure-folder>/trace.zip"
```

## Kết luận

Bộ test và cấu hình chạy ổn định: 13 kiểm tra đạt và 7 kiểm tra phát hiện sai khác đúng theo expected result của checklist. Lỗi ưu tiên xử lý trước là `PLP-VAL-02` vì payload HTML từ ô tìm kiếm đang được thực thi trên giao diện.
