# HW06 — AI-first API testing report

> Báo cáo kỹ thuật được dựng từ test table đã commit và Newman JSON. Các bằng chứng HUMAN-only (ảnh, chữ ký, issue GitHub, sơ đồ tự vẽ, bài critique) không được giả mạo.

## 1. Phạm vi và môi trường

SUT là EShop backend trong `backend/`, chạy Node.js/Express + SQLite. Bộ kiểm thử chọn ba luồng có rủi ro cao: đăng nhập, checkout và chuyển trạng thái order của admin. Newman chạy local với `http://127.0.0.1:3001` vì port 3000 đang được tiến trình khác sử dụng; workflow CI dùng `http://localhost:3000` theo đề bài.

Header `X-Student-Id: 23127207` được chèn ở collection-level pre-request và được log ở console cho mọi request.

## 2. Pipeline sinh — audit — mở rộng

Mỗi API dùng chuỗi P1 phân tích input/state → P2 domain partition + BVA → P3 state transition → P4 security → P5 schema. Output thô nằm ở `01-ai-generated.md`; audit phân loại 100% case thành VALID/INVALID/INCOMPLETE trong `02-audit.md`; `03-extended.md` thêm 6 case ngoài phạm vi prompt; bảng chốt là `test-cases.md`.

| API | AI sinh | Audit | Human mở rộng | Bảng chốt | Audit thống kê |
| :--- | ---: | :--- | ---: | ---: | :--- |
| API-1 — `POST /api/login` | 36 | 100% gán nhãn | 6 | 42 | 28 VALID / 3 INVALID / 5 INCOMPLETE |
| API-2 — `POST /api/checkout` | 36 | 100% gán nhãn | 6 | 42 | 28 VALID / 3 INVALID / 5 INCOMPLETE |
| API-3 — `PUT /api/admin/orders/:id/status` | 38 | 100% gán nhãn | 6 | 44 | 28 VALID / 5 INVALID / 5 INCOMPLETE |

Human review trong API-1, API-2 và file audit API-3 hiện đều có metadata xác nhận; người nộp cần tự kiểm tra chữ ký API-3 trước khi nộp.

## 3. Newman execution

Báo cáo đối soát [`execution-coverage.md`](../newman/reports/execution-coverage.md) trích TC ID trực tiếp từ tên assertion trong mọi Newman JSON: **123/128 = 96.1%** case đã thực thi; 1 Manual và 4 Blocked đều có lý do trong bảng test case.

| Run | Iterations | Requests | Assertions | Failed assertions | Ý nghĩa |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `00-off-suite` | 1 | 19 | 18 | 0 | baseline CI xanh |
| `00-canary-suite` | 1 | 19 | 19 | 1 | strict canary: TC-API-LOGIN-018 |
| `00-full-suite` | 1 | 19 | 26 | 8 | strict toàn bộ probe chính |
| `01-ddt-login` | 39 | 89 | 39 | 23 | coverage DDT login |
| `02-ddt-checkout` | 41 | 178 | 41 | 17 | coverage DDT checkout |
| `03-ddt-order-status` | 43 | 127 | 43 | 7 | matrix + coverage DDT status |

HTML/JSON evidence: [`newman/reports`](../newman/reports/). DDT runner tự chuẩn bị environment/auth/order trước khi chạy folder, tránh kết quả giả do 401 hoặc orderId rỗng. Trước khi lưu/publish, sanitizer tự động chỉ redaction giá trị password/JWT; TC ID, assertion result, HTTP status và `run.stats` vẫn giữ nguyên để đối soát.

## 4. Postman, CI và generator

Collection có collection-level pre-request, environment variables, dynamic disposable user, token chaining, response assertions, strict modes `off/canary/full`, data-driven folders và htmlextra/JSON export. Chi tiết ở [`postman-features.md`](../postman/postman-features.md). Workflow nằm ở [`.github/workflows/hw06-newman-api-test.yml`](../../.github/workflows/hw06-newman-api-test.yml). Pseudocode và generator tham chiếu ở [`test-generator/design.md`](../test-generator/design.md) và [`generator.py`](../test-generator/generator.py).

OpenAPI audit: file [`openapi/eshop.openapi.yaml`](../openapi/eshop.openapi.yaml) chỉ mô tả các endpoint được test; mọi expected result vẫn đối chiếu SUT defect catalog.

## 5. Defects và giới hạn bằng chứng

15 defect IDs trong defect catalog đã được lập trong [`bug-report.md`](bug-report.md), mỗi dòng có Found by Test Case, expected/actual và nguồn evidence. Newman JSON ghi nhận 8 fail ở full probe cùng 23/17/7 fail ở ba DDT suite; request/test-script infrastructure đều không fail. Đã tạo đủ 15 GitHub Issues scrubbed (#413–#427) và lưu 15 ảnh trang issue tại `evidence/screenshots/github-issues/`; trạng thái CI external được ghi riêng trong `cicd-report.md`.

`ai-critique.md` là bản nháp dữ liệu 200–300 từ để người học viết lại bằng nhận xét của chính mình; `diagram.mmd` là bản mô tả kỹ thuật, không thay thế `diagram.png` tự vẽ.

## 6. Artifact index

- [README tự chấm và summary](../README.md)
- [AI audit log](ai-audit-report.md)
- [Bug report](bug-report.md)
- [GitHub issue manifest](github-issues.json)
- [GitHub issue screenshot index](../evidence/screenshots/github-issues.md)
- [CI/CD report](cicd-report.md)
- [Excel/CSV](../excel/)
- [Traceability](../../tests/test-summary/traceability-matrix.md)

### Human completion gates

1. Xác minh metadata/signature API-3; 2. kiểm tra 15 GitHub issue links + 15 screenshot local; 3. chụp Postman Console/Newman/CI; 4. tự vẽ `diagram.png`; 5. viết lại critique và xuất ba PDF; 6. đặt repo public và đóng zip theo tên đề bài.
