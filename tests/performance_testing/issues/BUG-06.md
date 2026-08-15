---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][DB/Ops] database.js DROP + reseed toàn bộ DB mỗi lần khởi động server'
labels: ['type: bug', 'status: new', 'found-by: test-case', 'severity: major', 'ops']
assignees: ''
---

## Found by Test Case

Phát hiện khi thiết kế quy trình reset lockout giữa các run Stress/Spike (PERF-STRESS-01 / PERF-SPIKE-01) — lý do **không** dùng restart để reset.

## Requirement liên quan

Hạ tầng dữ liệu / môi trường kiểm thử (liên quan FR-02 reset, và tính bền vững dữ liệu chung)

## Severity / Priority

Major / P1

## Environment

- **OS**: macOS 15.5 (Darwin 24.5.0), Apple M4
- **Browser**: N/A — Node.js backend (`node server.js`)
- **URL**: N/A (khởi động tiến trình)
- **Build/Commit**: eshop-sut (HW05 SUT) · `backend/database.js` dòng 13–117

## Steps to reproduce

1. Đăng ký user pool + tạo vài order (chạy 1 kịch bản bất kỳ).
2. Restart backend: `node server.js`.
3. Kiểm tra: `sqlite3 backend/database.sqlite "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM orders;"` → dữ liệu về seed mặc định (mất pool + orders).

## Expected result

Khởi động server **không** được xóa dữ liệu hiện có; init/seed chỉ chạy khi DB trống hoặc qua lệnh seed riêng biệt.

## Actual result

- `database.js:15–20`: `DROP TABLE IF EXISTS ...` cho mọi bảng, sau đó `initDatabase()` được gọi vô điều kiện ở cuối file (dòng 117) mỗi lần `require('./database')`.
- Hệ quả: mỗi lần khởi động server xóa sạch + reseed toàn bộ DB → không thể restart để reset lockout mà không mất 60 user pool + toàn bộ orders; rất nguy hiểm nếu vô tình chạy ở môi trường có dữ liệu thật. Đây là lý do tôi reset lockout bằng SQL thay vì restart.

## Evidence

`evidence/lockout_probe.md` (mục "Cách C — restart: KHÔNG dùng"), `docs/results_summary.md`.
![BUG-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1786794402/eshop-hw05/perf-bugs/BUG-06.png)
