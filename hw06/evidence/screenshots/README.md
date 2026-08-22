# Evidence screenshots

Thư mục này chỉ chứa bằng chứng chụp từ lần chạy thật. Không tạo ảnh mô phỏng hoặc ảnh do AI sinh.

## Đã có

| File | Nội dung | Chứng minh |
| :--- | :--- | :--- |
| `01-x-student-id-console.png` | Bruno — tab Timeline, request `GET http://localhost:3000/api/products` bung ra `HEADERS (1) — X-Student-Id: 23127207`, `200 OK` | R-14 |
| `02-newman-cli-run.png` | Newman CLI — `X-Student-Id: 23127207` trên mọi request, URL đã resolve `http://localhost:3000/...` | R-14, R-15 |
| `02b-newman-cli-summary.png` | Newman CLI — bảng tổng kết 19 requests / 18 assertions / 0 failed | R-15 |
| `04-ci-pass.png` | GitHub Actions run `#3` (SHA `4bf4e5f`) — Success | R-07 |
| `05-ci-fail.png` | GitHub Actions run `#4` (SHA `03f3699`) — Failure theo thiết kế | R-07 |
| `github-issues/bug-01..19-*.png` | 19 trang GitHub Issue công khai (#413–#432) | R-05 |

## Ghi chú về client

Collection và environment ở định dạng Postman và được thực thi bằng Newman ở local lẫn CI; mọi số liệu trong báo cáo lấy từ Newman. Ảnh `01-x-student-id-console.png` chụp bằng **Bruno** (API client tương thích collection Postman) ở tab Timeline — tương đương Postman Console. Không khai là ảnh Postman.

## Tuỳ chọn, chưa có

- `03-postman-workspace.png`, `03-postman-mock.png`, `03-postman-monitor.png` — tính năng Postman cloud, điểm cộng R-06.
