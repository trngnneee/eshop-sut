# 4. Tích hợp CI/CD

## 4.1 Thiết kế pipeline

- Trigger: `push`, `pull_request`, và `workflow_dispatch`
- Các bước chính:
  1. Checkout repository.
  2. Setup Node.js 20 với npm cache cho lockfile của backend và `API-testing`.
  3. Cài backend dependencies bằng `npm ci`.
  4. Cài API-testing dependencies bằng `npm ci`.
  5. Seed database của backend.
  6. Start backend server và chờ `GET /api/products` trả `200`.
  7. Chạy `npm run forgot`, `npm run apply`, và `npm run admin`.
  8. Upload ba Newman HTML reports và backend log làm artifacts.

Workflow chạy cả ba collection ngay cả khi một collection fail. Pipeline lưu exit code từng lần chạy, in summary, và chỉ fail job ở cuối nếu có bất kỳ Newman run nào fail. Cách này vừa nghiêm ngặt, vừa đảm bảo vẫn có report cho cả ba API.

## 4.2 Lần chạy all-passing

| Thuộc tính | Giá trị |
|---|---|
| Commit | Test CI Pass |
| Evidence | ![](../artifacts/CI-Pass.png) |
| Link | https://github.com/trngnneee/eshop-sut/actions/runs/32650890035 |

## 4.3 Lần chạy failing

| Thuộc tính | Giá trị |
|---|---|
| Commit | Test CI Fail |
| Evidence | ![](../artifacts/CI-Fail.png) |
| Link | https://github.com/trngnneee/eshop-sut/actions/runs/32649108372 |

> [!NOTE]
> Lần chạy thành công (all-passing) thực tế chỉ sử dụng bộ test suite rút gọn (smoke test) nhằm xác minh cấu hình CI/CD pipeline hoạt động chính xác. Khi thực thi đầy đủ cả 3 collection kiểm thử thực tế, kết quả sẽ thất bại (fail) do các lỗi nghiệp vụ và bảo mật hiện có trên backend (chi tiết tại Mục 2).
