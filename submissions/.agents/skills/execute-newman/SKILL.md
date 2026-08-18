---
name: execute-newman
description: >
  Hướng dẫn AI tạo Postman collection từ test cases và chạy Newman để sinh báo cáo
  thực thi. Skill cũng cập nhật MainReport.md và tạo khung bug_report.md sau khi chạy.
---

# Skill: execute-newman

## Mục tiêu

Thực thi các test cases đã được audit và extend bằng Postman + Newman:
1. Tạo/cập nhật Postman Collection JSON từ các TC trong Markdown
2. Sinh script Newman chạy collection với header bắt buộc `X-Student-Id`
3. Tạo Newman HTML report
4. Cập nhật kết quả vào `MainReport.md` và tạo khung `bug_report.md`

---

## Thông tin đầu vào

| Mục | Giá trị |
|:----|:--------|
| `API_NUMBER`    | 1, 2, hoặc 3 |
| `STUDENT_ID`    | MSSV của sinh viên (Mặc định: 23127486) |
| `BASE_URL`      | URL server (mặc định: `http://localhost:3000`) |
| `TC_FILE`       | `submissions/test_cases_apiN.md` |
| `COLLECTION_DIR`| thư mục lưu Postman collection (ví dụ: `postman/`) |
| `REPORT_FILE`   | `submissions/MainReport.md` |
| `BUG_FILE`      | `submissions/bug_report.md` |

---

## Các bước thực hiện

### Bước 1 — Kiểm tra môi trường

Kiểm tra các công cụ cần thiết:
```powershell
# Kiểm tra Node.js và Newman
node --version
newman --version

# Nếu chưa có Newman, cài đặt:
npm install -g newman newman-reporter-html
```

Kiểm tra server EShop đang chạy:
```powershell
# Thử kết nối đến base URL
Invoke-WebRequest -Uri "http://localhost:3000/api/products" -Method GET
```

### Bước 2 — Tạo Postman Collection JSON

Đọc `test_cases_apiN.md` và chuyển đổi các TC đã audit thành Postman Collection:

```json
{
  "info": {
    "name": "HW06 – API [N] – [Pool] – [Feature]",
    "_postman_id": "[uuid]",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    { "key": "baseUrl", "value": "http://localhost:3000" },
    { "key": "studentId", "value": "[STUDENT_ID]" },
    { "key": "token", "value": "" }
  ],
  "item": [
    {
      "name": "TC-[X]-DP-01 – [Mô tả]",
      "request": {
        "method": "[GET/POST/PUT/DELETE]",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "X-Student-Id", "value": "{{studentId}}" },
          { "key": "Authorization", "value": "Bearer {{token}}" }
        ],
        "body": { "mode": "raw", "raw": "{}" },
        "url": { "raw": "{{baseUrl}}/api/..." }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 200', function() { pm.response.to.have.status(200); })",
              "pm.test('Response has expected fields', function() { ... })"
            ]
          }
        }
      ]
    }
  ]
}
```

**Quy tắc tạo collection:**
- Mỗi TC = 1 request item trong collection
- Pre-request script toàn cục đặt header `X-Student-Id: {{studentId}}`
- Request đầu tiên là login → lưu token vào `pm.environment.set("token", ...)`
- Các request cần auth đều dùng `Authorization: Bearer {{token}}`
- Thêm test script cho mỗi TC dựa theo Expected Output trong markdown

**Lưu file collection:**
```
postman/hw06_api[N]_collection.json
postman/hw06_environment.json
```

### Bước 3 — Tạo script chạy Newman

Tạo file `run_newman_api[N].ps1` (hoặc `.sh` nếu Linux/Mac):

```powershell
# run_newman_api1.ps1
$STUDENT_ID = "23127486"
$BASE_URL = "http://localhost:3000"
$COLLECTION = "postman/hw06_api1_collection.json"
$ENV_FILE = "postman/hw06_environment.json"
$REPORT_DIR = "newman_reports"

New-Item -ItemType Directory -Force -Path $REPORT_DIR | Out-Null

newman run $COLLECTION `
  --environment $ENV_FILE `
  --env-var "studentId=$STUDENT_ID" `
  --env-var "baseUrl=$BASE_URL" `
  --reporters cli,html `
  --reporter-html-export "$REPORT_DIR/newman_api1_report.html" `
  --reporter-html-title "HW06 API1 – Phan Quoc Thinh – $STUDENT_ID"
```

### Bước 4 — Chạy Newman và ghi nhận kết quả

Chạy script Newman. Ghi nhận từ output:
- Tổng số TC chạy
- Số TC PASS / FAIL
- Các TC FAIL và lý do

> Lưu ý: **Kết quả thực thi** (PASS/FAIL cụ thể từng TC) **cần được sinh viên chụp screenshot** để đính kèm vào report. AI ghi nhận số liệu thống kê nếu được cung cấp.

### Bước 5 — Phát hiện Bug candidates

Dựa trên các TC FAIL, phân tích:
- Có phải bug thực sự của hệ thống không?
- Hay là lỗi trong test case (expected output sai)?

---

## Cập nhật tài liệu (BẮT BUỘC)

### 1. Cập nhật `test_cases_apiN.md`

Điền cột **Kết quả** trong bảng Execute:
```markdown
## Kết quả thực thi (Execute)

| Nhãn | Số lượng | Tỷ lệ |
|:-----|:---------|:------|
| PASS | [X] | [X]% |
| FAIL | [X] | [X]% |
| **Tổng** | [X] | 100% |

Newman report: `newman_reports/newman_api[N]_report.html`
*(Screenshot Postman Console / Newman output đính kèm tại đây)*
```

### 2. Cập nhật `MainReport.md`

Trong section 2.4 / 3.4 / 4.4 (Bước 4: Thực thi):
```markdown
### X.4. Bước 4: Thực thi (Execute)

- **Công cụ:** Postman + Newman
- **Header bắt buộc:** `X-Student-Id: [STUDENT_ID]`
- **Collection:** `postman/hw06_api[N]_collection.json`
- **Kết quả:**

| Nhãn | Số lượng | Tỷ lệ |
|:-----|:---------|:------|
| PASS | [X] | [X]% |
| FAIL | [X] | [X]% |

> Newman report: `newman_reports/newman_api[N]_report.html`
> *(Screenshot console đính kèm)*
```

### 3. Cập nhật `bug_report.md`

Thêm hàng cho mỗi TC FAIL có khả năng là bug thực:
```markdown
| BUG-[X]-01 | [mô tả bug] | [endpoint] | [HTTP status thực tế vs expected] | [severity] | *(sinh viên tạo GitHub Issue và điền link)* |
```

> Lưu ý: **Link GitHub Issue** và **screenshot** phải do sinh viên tự tạo và đính kèm.

---

## Các tính năng Postman cần sử dụng (ghi vào report)

Agent nhắc sinh viên tận dụng và ghi lại vào `MainReport.md` mục 5:

| Tính năng | Cách dùng |
|:----------|:----------|
| Workspaces | Tạo workspace riêng cho HW06 |
| Collections | Tổ chức TC theo API |
| Variables | `baseUrl`, `token`, `studentId` |
| Environments | `HW06-Local` environment |
| Pre-request Scripts | Tự động đặt `X-Student-Id` header |
| Test Scripts | Assert status code, response fields |
| Collection Runner | Chạy toàn bộ collection |
| Data-driven runs | Nếu dùng CSV data file |

---

## Ràng buộc

- Header `X-Student-Id: [STUDENT_ID]` phải có trong MỌI request
- Không giả mạo kết quả Newman – phải chạy thực trên server EShop
- Screenshot phải thực sự từ Postman Console hoặc Newman terminal
- Bug report chỉ ghi bug thực sự – không ghi TC failures do lỗi test script

---

## Checklist hoàn thành

- [ ] `postman/hw06_api[N]_collection.json` đã được tạo
- [ ] `postman/hw06_environment.json` đã được tạo
- [ ] Script Newman (`run_newman_api[N].ps1`) đã được tạo
- [ ] `newman_reports/newman_api[N]_report.html` đã sinh ra sau khi chạy
- [ ] `test_cases_apiN.md` bảng Execute đã có số liệu PASS/FAIL
- [ ] `MainReport.md` section Execute đã cập nhật
- [ ] `bug_report.md` đã có hàng cho các TC FAIL nghi là bug
