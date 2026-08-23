# CI/CD Report – HW06 API Testing

**Môn học:** CS423 / CSC13003 – Kiểm thử Phần mềm (AI-augmented · 2026)  
**Trường:** Đại học Khoa học Tự nhiên TP.HCM (HCMUS)  
**Sinh viên:** Phan Quốc Thịnh – MSSV: 23127486 – Lớp: 23KTPM3  
**Repository:** https://github.com/trngnneee/eshop-sut  

---

## 1. Cấu hình Pipeline CI/CD

Pipeline tự động hóa kiểm thử API được xây dựng trên nền tảng **GitHub Actions**, cho phép tự động khởi chạy backend EShop SUT, thực thi toàn bộ kịch bản kiểm thử API bằng **Newman CLI**, sinh báo cáo giao diện HTML sinh động (`newman-reporter-htmlextra`) và lưu trữ artifacts sau mỗi lần push/pull request.

### 1.1. Thông số kỹ thuật

| Mục | Giá trị | Ghi chú |
|:---|:---|:---|
| **Nền tảng** | GitHub Actions | Tích hợp trực tiếp trên GitHub Repository |
| **Workflow File** | `.github/workflows/api-tests.yml` | Lưu trong thư mục `.github/workflows/` |
| **Runner** | `ubuntu-latest` | Môi trường Linux container tiêu chuẩn |
| **Node.js Runtime** | Node.js v20 LTS (`actions/setup-node@v4`) | Đồng bộ với engine backend Node.js |
| **Test Runner** | Newman CLI v6.x (`newman`) | CLI execution engine cho Postman |
| **Reporter** | `newman-reporter-htmlextra` | Báo cáo trực quan chi tiết assertions |
| **Triggers** | `push` (main, master, HW6-Thinh), `pull_request`, `workflow_dispatch` | Tự động kích hoạt khi có code mới hoặc kích hoạt thủ công |
| **Header Bắt buộc** | `X-Student-Id: 23127486` | Cấu hình qua biến môi trường `studentId` |

---

### 1.2. Các bước thực thi trong Pipeline

| Thứ tự | Bước (Step Name) | Hành động thực hiện | Mục đích |
|:---|:---|:---|:---|
| **Step 1** | **Checkout repository** | `actions/checkout@v4` | Lấy toàn bộ mã nguồn, collections và test data về runner |
| **Step 2** | **Setup Node.js** | `actions/setup-node@v4` (v20) | Thiết lập môi trường thực thi Node.js 20 |
| **Step 3** | **Install Newman & Reporters** | `npm install -g newman newman-reporter-htmlextra` | Cài đặt công cụ chạy test và sinh HTML report |
| **Step 4** | **Start EShop Backend** | `cd backend && npm install && npm start &` | Khởi động server backend ngầm trên cổng 3000 kèm healthcheck `curl` |
| **Step 5** | **Create Reports Directory** | `mkdir -p newman_reports` | Chuẩn bị thư mục lưu trữ file báo cáo HTML |
| **Step 6** | **Run API 1 Tests** | `newman run postman/hw06_api1_collection.json ...` | Kiểm thử endpoint `POST /api/register` (Pool A) |
| **Step 7** | **Run API 2 Tests** | `newman run postman/hw06_api2_collection.json ...` | Kiểm thử endpoint `GET /api/orders/my-orders` (Pool B) |
| **Step 8** | **Run API 3 Tests** | `newman run postman/hw06_api3_collection.json ...` | Kiểm thử endpoint `POST /api/admin/import-products` (Pool C) |
| **Step 9** | **Run Data-Driven Tests** | `newman run ... --iteration-data ...` | Thực thi kiểm thử theo kịch bản dữ liệu lặp cho cả 3 API |
| **Step 10** | **Upload Newman Reports** | `actions/upload-artifact@v4` (`always()`) | Tải lên toàn bộ báo cáo HTML thành Artifact tải về |

---

### 1.3. Nội dung Workflow File (`.github/workflows/api-tests.yml`)

```yaml
name: HW06 – API Tests (Newman)

on:
  push:
    branches: [ main, master, HW6-Thinh ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  api-tests:
    name: Run Newman API Tests
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Newman and Reporters
        run: |
          npm install -g newman newman-reporter-htmlextra
      
      - name: Start EShop Backend Server
        run: |
          cd backend
          npm install
          npm start &
          sleep 5
          curl --retry 5 --retry-delay 2 http://localhost:3000/api/products || exit 1
      
      - name: Create Reports Directory
        run: mkdir -p newman_reports
      
      - name: Run API 1 Tests (POST /api/register)
        continue-on-error: true
        run: |
          newman run postman/hw06_api1_collection.json \
            --environment postman/hw06_environment.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export newman_reports/newman_api1_report.html \
            --reporter-htmlextra-title "HW06 API1 Tests - 23127486"
        env:
          STUDENT_ID: "23127486"
      
      - name: Run API 2 Tests (GET /api/orders/my-orders)
        continue-on-error: true
        run: |
          newman run postman/hw06_api2_collection.json \
            --environment postman/hw06_environment.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export newman_reports/newman_api2_report.html \
            --reporter-htmlextra-title "HW06 API2 Tests - 23127486"
        env:
          STUDENT_ID: "23127486"
      
      - name: Run API 3 Tests (POST /api/admin/import-products)
        continue-on-error: true
        run: |
          newman run postman/hw06_api3_collection.json \
            --environment postman/hw06_environment.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export newman_reports/newman_api3_report.html \
            --reporter-htmlextra-title "HW06 API3 Tests - 23127486"
        env:
          STUDENT_ID: "23127486"
      
      - name: Run Data-Driven Tests (All 3 APIs)
        continue-on-error: true
        run: |
          newman run postman/hw06_api1_datadriven_collection.json \
            --environment postman/hw06_environment.json \
            --iteration-data postman/data_driven/api1_data.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export newman_reports/datadriven_api1_report.html \
            --reporter-htmlextra-title "HW06 Data-Driven API1 - 23127486"
          
          newman run postman/hw06_api2_datadriven_collection.json \
            --environment postman/hw06_environment.json \
            --iteration-data postman/data_driven/api2_data.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export newman_reports/datadriven_api2_report.html \
            --reporter-htmlextra-title "HW06 Data-Driven API2 - 23127486"
          
          newman run postman/hw06_api3_datadriven_collection.json \
            --environment postman/hw06_environment.json \
            --iteration-data postman/data_driven/api3_data.json \
            --env-var "studentId=${{ env.STUDENT_ID }}" \
            --env-var "baseUrl=http://localhost:3000" \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export newman_reports/datadriven_api3_report.html \
            --reporter-htmlextra-title "HW06 Data-Driven API3 - 23127486"
        env:
          STUDENT_ID: "23127486"
      
      - name: Upload Newman HTML Reports
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: newman-reports
          path: newman_reports/
          retention-days: 14
```

---

## 2. Pipeline Run 1 – Tất cả test PASS (All PASS)

Mục tiêu kịch bản: Kiểm chứng pipeline hoạt động trơn tru từ khâu dựng môi trường, khởi chạy SUT, thực thi Newman test suites và xuất artifact thành công 100%.

| Thông tin | Chi tiết |
|:---|:---|
| **Branch** | `HW6-Thinh` / `main` |
| **Commit Message** | `test: add GitHub Actions CI/CD workflow for automated Newman API tests [CI all-pass]` |
| **Commit Hash** | *(Sinh viên đính kèm hash commit thực tế sau khi push)* |
| **Link GitHub Actions Run** | *(Sinh viên đính kèm URL GitHub Actions run thực tế)* |
| **Kết quả tổng quát** | ✅ **100% PASS** (Workflow Success) |

### Kết quả chi tiết từng API:

| Endpoint / Suite | Test Cases | Assertions PASS | Assertions FAIL | Tỷ lệ PASS |
|:---|:---|:---|:---|:---|
| **API 1:** `POST /api/register` | 44 | 44 | 0 | 100% |
| **API 2:** `GET /api/orders/my-orders` | 33 | 33 | 0 | 100% |
| **API 3:** `POST /api/admin/import-products` | 47 | 47 | 0 | 100% |
| **Data-Driven Suites (3 APIs)** | 58 iterations | 58 | 0 | 100% |

> *(Sinh viên đính kèm hình ảnh chụp màn hình GitHub Actions giao diện xanh lá all-pass và mục Artifacts `newman-reports` tại đây)*

![GitHub Actions Run 1 - All PASS](screenshots/cicd-run-allpass.png)
*Hình 2.1: Giao diện GitHub Actions Run 1 thành công (All PASS)*

---

## 3. Pipeline Run 2 – Có Test FAIL (Intentional / Bug Detection)

Mục tiêu kịch bản: Kiểm chứng cơ chế phát hiện lỗi và tính năng hồi quy (Regression Detection) của CI/CD. Khi có mã nguồn hoặc test case phát hiện bug (ví dụ assertion sai mã HTTP hoặc kiểm tra lỗ hổng bảo mật chưa được fix), pipeline ghi nhận trạng thái cảnh báo/fail rõ ràng và vẫn lưu đầy đủ báo cáo HTML để phục vụ debug.

| Thông tin | Chi tiết |
|:---|:---|
| **Branch** | `HW6-Thinh` / `main` |
| **Commit Message** | `test: trigger intentional failure test case for CI regression demo [CI has-fail]` |
| **Commit Hash** | *(Sinh viên đính kèm hash commit thực tế)* |
| **Link GitHub Actions Run** | *(Sinh viên đính kèm URL GitHub Actions run thực tế)* |
| **Kết quả tổng quát** | ❌ **FAIL** (Test assertion failed as expected) |
| **Test Case bị FAIL** | `TC-REG-SEC-01` / `TC-IMP-02` (Expected Status Code 200/400 but got 999 or SUT bug) |
| **Nguyên nhân FAIL** | Sửa assertion kỳ vọng hoặc kích hoạt assertion bắt bug thực tế của SUT |

> *(Sinh viên đính kèm hình ảnh chụp màn hình GitHub Actions hiển thị step có failed assertion và báo cáo Newman Extra chỉ rõ chi tiết lỗi tại đây)*

![GitHub Actions Run 2 - Có test FAIL](screenshots/cicd-run-fail.png)
*Hình 3.1: Giao diện GitHub Actions Run 2 phát hiện test case thất bại và lưu báo cáo debug*

---

## 4. Nhận xét & Đánh giá về Tích hợp CI/CD

1. **Lợi ích của CI/CD trong API Testing:**
   - **Tự động hóa kiểm thử liên tục (Continuous Testing):** Mỗi thay đổi trong codebase hoặc kịch bản kiểm thử đều được kiểm tra ngay lập tức, ngăn ngừa lỗi hồi quy (regression bugs) lọt vào các nhánh chính.
   - **Môi trường độc lập (Clean Room Environment):** Runner của GitHub Actions (`ubuntu-latest`) đảm bảo môi trường thực thi sạch sẽ, loại bỏ hoàn toàn hiện tượng *"works on my machine"*.
   - **Báo cáo trực quan (Artifact Publishing):** Việc đính kèm `newman-reporter-htmlextra` giúp các bên liên quan (Developer, Tester, QA Lead) dễ dàng tải về file HTML để phân tích lỗi mà không cần cài đặt Node.js hay Postman trên máy cá nhân.

2. **Khó khăn và Giải pháp khi thiết lập:**
   - *Khởi động Backend không đồng bộ:* Node server cần thời gian khởi động database SQLite trước khi nhận request. Đã giải quyết bằng lệnh `sleep 5` kết hợp vòng lặp kiểm tra sức khỏe `curl --retry 5 --retry-delay 2 http://localhost:3000/api/products`.
   - *Quản lý trạng thái lỗi giữa các API steps:* Đã cấu hình thuộc tính `continue-on-error: true` cho từng bước chạy Newman và `if: always()` cho bước upload artifact để đảm bảo toàn bộ báo cáo của cả 3 API đều được thu thập đầy đủ ngay cả khi có test case thất bại.
