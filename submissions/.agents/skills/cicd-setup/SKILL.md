---
name: cicd-setup
description: >
  Hướng dẫn AI thiết lập GitHub Actions CI/CD pipeline chạy Newman tự động
  cho HW6. Skill tạo workflow file, commit log sườn, và cập nhật cicd_report.md.
---

# Skill: cicd-setup

## Mục tiêu

Tích hợp API test vào CI/CD pipeline (GitHub Actions):
1. Tạo GitHub Actions workflow chạy Newman tự động
2. Tạo hai sample commits: một all-PASS, một có FAIL
3. Cập nhật `submissions/cicd_report.md` với mô tả pipeline

> Lưu ý: **Link runs thực tế**, **screenshots**, và **git commit log** phải do sinh viên
> tự thực hiện và đính kèm. AI chỉ tạo workflow file và cấu trúc tài liệu.

---

## Thông tin đầu vào

| Mục | Giá trị |
|:----|:--------|
| `STUDENT_ID`    | MSSV (ví dụ: 23127486) |
| `REPO_URL`      | GitHub repository URL |
| `BASE_URL`      | URL server trong CI (ví dụ: `http://localhost:3000`) |
| `CICD_FILE`     | `submissions/cicd_report.md` |

---

## Các bước thực hiện

### Bước 1 — Tạo GitHub Actions Workflow

Tạo file `.github/workflows/api-tests.yml`:

```yaml
name: HW06 – API Tests (Newman)

on:
  push:
    branches: [ main, master, HW6-Thinh ]
  pull_request:
    branches: [ main, master ]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Newman and HTML reporter
        run: npm install -g newman newman-reporter-html
      
      - name: Start EShop backend server
        run: |
          cd backend
          npm install
          npm start &
          sleep 10
          curl --retry 5 --retry-delay 3 http://localhost:3000/api/products
      
      - name: Run API 1 Tests
        run: |
          newman run postman/hw06_api1_collection.json \
            --environment postman/hw06_environment.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,html \
            --reporter-html-export newman_reports/newman_api1_report.html
        env:
          STUDENT_ID: "23127486"
      
      - name: Run API 2 Tests
        run: |
          newman run postman/hw06_api2_collection.json \
            --environment postman/hw06_environment.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,html \
            --reporter-html-export newman_reports/newman_api2_report.html
        env:
          STUDENT_ID: "23127486"
      
      - name: Run API 3 Tests
        run: |
          newman run postman/hw06_api3_collection.json \
            --environment postman/hw06_environment.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,html \
            --reporter-html-export newman_reports/newman_api3_report.html
        env:
          STUDENT_ID: "23127486"
      
      - name: Upload Newman Reports
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: newman-reports
          path: newman_reports/
```

**Lưu file:** `.github/workflows/api-tests.yml`

### Bước 2 — Tạo cấu trúc thư mục cần thiết

```powershell
New-Item -ItemType Directory -Force -Path "postman"
New-Item -ItemType Directory -Force -Path "newman_reports"
```

### Bước 3 — Hướng dẫn tạo 2 sample commits

> Lưu ý: Phần này hướng dẫn; sinh viên tự thực hiện và chụp screenshot.

**Commit 1 – All PASS:**
```bash
# Đảm bảo tất cả TC đều pass
git add postman/ .github/
git commit -m "test: add Postman collections for all 3 APIs [CI all-pass]"
git push
# → GitHub Actions chạy → tất cả pass → chụp screenshot
```

**Commit 2 – Có FAIL (intentional):**
```bash
# Tạm thời sửa một TC có expected wrong để trigger fail
# Ví dụ: đổi expected status code từ 200 thành 999
git add postman/
git commit -m "test: intentional fail test case for CI demo [CI has-fail]"
git push
# → GitHub Actions chạy → có 1 TC fail → chụp screenshot
# Sau đó revert lại
git revert HEAD
git push
```

---

## Cập nhật tài liệu (BẮT BUỘC)

### Cập nhật `cicd_report.md`

Agent cập nhật file với nội dung sườn đầy đủ:

```markdown
# CI/CD Report – HW06 API Testing

**Sinh viên:** [Họ tên] – [MSSV]  
**Repository:** [GitHub repo URL]

---

## 1. Cấu hình Pipeline

- **Nền tảng:** GitHub Actions
- **Trigger:** Push / Pull Request vào nhánh `main`
- **Runner:** `ubuntu-latest`
- **Node.js:** v20

**Workflow file:** `.github/workflows/api-tests.yml`

### Các bước trong pipeline:

| Bước | Mô tả |
|:-----|:------|
| Checkout | Clone repository |
| Setup Node.js | Cài Node.js v20 |
| Install Newman | `npm install -g newman newman-reporter-html` |
| Start Backend | Khởi động EShop server + health check |
| Run API 1 Tests | Newman chạy collection API 1 |
| Run API 2 Tests | Newman chạy collection API 2 |
| Run API 3 Tests | Newman chạy collection API 3 |
| Upload Reports | Lưu HTML reports làm artifacts |

---

## 2. Run 1 – All PASS

> Lưu ý: Sinh viên điền thông tin sau khi chạy thực tế.

- **Commit:** *(hash – sinh viên điền)*
- **Link GitHub Actions run:** *(sinh viên điền)*
- **Kết quả:**

| API | PASS | FAIL | Tổng |
|:----|:-----|:-----|:-----|
| API 1 | *(điền)* | 0 | *(điền)* |
| API 2 | *(điền)* | 0 | *(điền)* |
| API 3 | *(điền)* | 0 | *(điền)* |

*(Screenshot đính kèm tại đây)*

---

## 3. Run 2 – Có Test FAIL (Intentional)

> ⚠️ Sinh viên điền thông tin sau khi chạy thực tế.

- **Commit:** *(hash – sinh viên điền)*
- **Link GitHub Actions run:** *(sinh viên điền)*
- **TC bị fail:** *(tên TC – sinh viên điền)*
- **Lý do fail:** *(sinh viên giải thích)*

*(Screenshot đính kèm tại đây)*

---

## 4. Nhận xét

*(Sinh viên viết nhận xét về CI/CD pipeline: lợi ích, khó khăn gặp phải)*
```

### Cập nhật `MainReport.md`

Trong section **6. Tích hợp CI/CD**:
```markdown
## 6. Tích hợp CI/CD

- **Pipeline:** GitHub Actions (`.github/workflows/api-tests.yml`)
- **Trigger:** Push / Pull Request vào nhánh `main`
- **Run 1 (all PASS):** *(sinh viên điền link)*
- **Run 2 (có test FAIL):** *(sinh viên điền link)*

> Chi tiết xem file: `submissions/cicd_report.md`
```

---

## Ràng buộc

- Workflow file phải chứa `X-Student-Id` header (qua env var)
- Hai links GitHub Actions runs phải là thực tế, không giả mạo
- Screenshots phải chụp từ GitHub Actions interface thực
- Commit hash phải tương ứng với commits thực trong repo

---

## Checklist hoàn thành

- [ ] `.github/workflows/api-tests.yml` đã được tạo
- [ ] File workflow chứa đủ 3 bước chạy Newman cho 3 API
- [ ] `submissions/cicd_report.md` đã có cấu trúc sườn đầy đủ
- [ ] `submissions/MainReport.md` section CI/CD đã cập nhật
- [ ] Hướng dẫn tạo 2 commits đã được ghi rõ
- [ ] Các placeholder cho screenshots và links đã được đặt sẵn
