# HW06 — AI-first API testing report

> Báo cáo kỹ thuật được dựng từ test table đã commit và Newman JSON. Các bằng chứng HUMAN-only (ảnh, chữ ký, issue GitHub, sơ đồ tự vẽ, bài critique) không được giả mạo.

## 1. Phạm vi và môi trường

SUT là EShop backend trong `backend/`, chạy Node.js/Express + SQLite. Bộ kiểm thử chọn ba luồng có rủi ro cao: đăng nhập, checkout và chuyển trạng thái order của admin. Newman chạy local với `http://127.0.0.1:3001` vì port 3000 đang được tiến trình khác sử dụng; workflow CI dùng `http://localhost:3000` theo đề bài.

Repository công khai: [https://github.com/trngnneee/eshop-sut](https://github.com/trngnneee/eshop-sut), branch `HW6-Khoa`.

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

19 defect IDs trong defect catalog đã được lập trong [`bug-report.md`](bug-report.md), mỗi dòng có Found by Test Case, expected/actual và nguồn evidence. Newman JSON ghi nhận 8 fail ở full probe cùng 23/17/7 fail ở ba DDT suite; request/test-script infrastructure đều không fail. Đã tạo đủ 19 GitHub Issues scrubbed (#413–#432) và lưu 19 ảnh trang issue tại `evidence/screenshots/github-issues/`. CI external đã chạy thật: mode `off` xanh ở commit `4bf4e5f8…`; mode `canary` đỏ ở commit `03f36993…` với đúng một failed assertion `TC-API-LOGIN-018`. SHA và Actions URL đầy đủ nằm trong [`cicd-report.md`](cicd-report.md).

[`ai-critique.md`](ai-critique.md) do người học tự viết (R-12). [`test-generator/diagram.png`](../test-generator/diagram.png) là HUMAN-only và đã được người học tự thiết kế bố cục, tự vẽ; `DRAWING-BRIEF.md` chỉ là checklist khối/quan hệ tối thiểu. Mermaid do AI sinh được cách ly tại `_reference/diagram-notes.mmd`, ghi rõ không phải sơ đồ nộp bài và không được export.

## 6. Tuân thủ `Rule.pdf` — quản lý test case trên GitHub

Ngoài `Requirements.pdf`, bài này áp dụng quy ước §H của `Rule.pdf`:

| Điều | Áp dụng trong bài |
| :--- | :--- |
| §H.1 liên kết hai chiều | Bug issue ghi `Found by Test Case`; [test run](../../tests/test-runs/hw06-api-test-run.md) ghi `Related Bug = #xx`; Pull Request tham chiếu `Related to` toàn bộ issue |
| §H.3 cấu trúc thư mục | `tests/test-cases/<module>/`, `tests/test-runs/`, `tests/test-summary/`, `.github/ISSUE_TEMPLATE/` |
| §H.4 mã test case | `TC-API-LOGIN-###`, `TC-API-CHECKOUT-###`, `TC-API-ORDER-STATUS-###` — tiền tố `API-` để không đụng `TC-LOGIN-001..013` của bài trước |
| §H.5 template | Mỗi file test case có Requirement · Technique · Preconditions · Data · Expected · Result · Related Bug |
| §H.6 test run | Bảng 128 dòng `Test Case ID / Module / Tester / Result / Related Bug / Note`, trạng thái Pass·Fail·Blocked·Not Run |
| §H.7 label | Issue gắn `type: bug`, `module: *`, `severity: *`, `priority: *`, `found-by: test-case` |
| §H.8 template bug | 19 issue theo cấu trúc Found by → Requirement → Severity → Environment → Steps → Expected → Actual → Evidence |
| §H.9 traceability | [`traceability-matrix.md`](../../tests/test-summary/traceability-matrix.md) §HW06 — 128 dòng `Requirement / Test Case / Result / Bug Issue / Status` |
| §H.10 automation | D-LOGIN-01 ghi rõ `Found by: GitHub Actions` + run URL + assertion — xem [`bug-report.md`](bug-report.md) |
| §H.11 điều kiện close | 19 issue giữ trạng thái Open vì SUT chưa được fix; chưa có retest pass nên chưa được close |

**Quy ước về số lượng file test case riêng lẻ.** Bảng test case đầy đủ (128 case) nằm ở `hw06/api-0X-*/test-cases.md` — dạng bảng để xuất Excel và đối chiếu nhanh. Trong `tests/test-cases/` chỉ sinh file `.md` riêng cho **các case đã FAIL (có bug truy vết được) cộng 5 case đại diện mỗi API**. Đây là quyết định có chủ đích để tránh nhân bản 128 file trùng nội dung với bảng gốc, đồng thời vẫn giữ đúng yêu cầu §H.2 rằng test case phát hiện bug phải tồn tại dưới dạng file có version history và review được qua Pull Request.

**Test case không thực thi tự động.** 4 case `Blocked` và 1 case `Not Run` không có assertion Newman; lý do ghi ở cột Note của test run (chờ lock thật 180 giây, không nhúng signing secret vào artifact công khai, SUT thiếu API quan sát hậu điều kiện). Các case này **không** được gán Pass/Fail suy diễn.

## 7. Artifact index

- [README tự chấm và summary](../README.md)
- [AI audit log](ai-audit-report.md)
- [Bug report](bug-report.md)
- [GitHub issue manifest](github-issues.json)
- [GitHub issue screenshot index](../evidence/screenshots/github-issues.md)
- [CI/CD report](cicd-report.md)
- [Excel/CSV](../excel/)
- [Traceability](../../tests/test-summary/traceability-matrix.md)
- [Test run theo §H.6](../../tests/test-runs/hw06-api-test-run.md)
- [Test case files](../../tests/test-cases/)

### Human completion gates

Đã hoàn tất: `diagram.png` tự vẽ · `ai-critique.md` tự viết · screenshot console (Bruno Timeline) và Newman CLI · hai screenshot CI · 19 issue link + 19 screenshot · repo public.

Còn lại: xuất ba PDF và đóng zip theo tên đề bài.
