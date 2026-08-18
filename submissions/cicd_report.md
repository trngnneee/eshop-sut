# Báo cáo CI/CD – HW06 API Testing

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3

---

## 1. Tổng quan Pipeline

| Mục | Chi tiết |
|:---|:---|
| **Nền tảng CI/CD** | GitHub Actions |
| **Công cụ kiểm thử** | Newman (Postman CLI) |
| **Repository** | *(link GitHub repo)* |
| **Workflow file** | `.github/workflows/api-test.yml` |

---

## 2. Cấu hình Pipeline

*(Mô tả cấu hình GitHub Actions workflow)*

```yaml
# .github/workflows/api-test.yml
# (Dán nội dung file workflow tại đây)
name: API Testing with Newman

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      # (cập nhật đầy đủ khi thực hiện)
```

---

## 3. Pipeline Run 1 – Tất cả test PASS

| Thông tin | Chi tiết |
|:---|:---|
| **Commit** | *(link commit)* |
| **Run ID** | *(link GitHub Actions run)* |
| **Kết quả** | ✅ Tất cả test PASS |
| **Thời gian chạy** | *(cập nhật)* |

*(Screenshot kết quả run 1 đính kèm tại đây)*

---

## 4. Pipeline Run 2 – Có test FAIL

| Thông tin | Chi tiết |
|:---|:---|
| **Commit** | *(link commit)* |
| **Run ID** | *(link GitHub Actions run)* |
| **Kết quả** | ❌ Có ít nhất 1 test FAIL |
| **Test case FAIL** | *(tên TC)* |
| **Lý do FAIL** | *(mô tả ngắn)* |

*(Screenshot kết quả run 2 đính kèm tại đây)*

---

## 5. Nhận xét về CI/CD

*(Mô tả ngắn về quá trình tích hợp CI/CD: gặp khó khăn gì, cách giải quyết, bài học rút ra)*
