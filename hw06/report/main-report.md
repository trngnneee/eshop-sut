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

Human review trong API-1 và API-2 đã được ghi trong audit theo các phê duyệt người dùng đã cung cấp. API-3 mới có agent pre-review; chữ ký người học vẫn phải được bổ sung độc lập.

## 3. Newman execution

| Run | Iterations | Requests | Assertions | Failed assertions | Ý nghĩa |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `00-off-suite` | 1 | 19 | 18 | 0 | smoke/oracle quan sát hành vi SUT |
| `00-canary-suite` | 1 | 19 | 19 | 1 | strict canary: TC-API-LOGIN-018 |
| `00-full-suite` | 1 | 19 | 26 | 8 | strict toàn bộ probe |
| `01-ddt-login` | 16 | 16 | 16 | 0 | 16 domain partitions |
| `02-ddt-checkout` | 18 | 18 | 18 | 0 | 18 partition rows |
| `03-ddt-order-status` | 25 | 25 | 25 | 7 | 25 matrix rows; failures là mismatch oracle/bug |

HTML/JSON evidence: [`newman/reports`](../newman/reports/). DDT runner tự chuẩn bị environment/auth/order trước khi chạy folder, tránh kết quả giả do 401 hoặc orderId rỗng.

## 4. Postman, CI và generator

Collection có collection-level pre-request, environment variables, dynamic disposable user, token chaining, response assertions, strict modes `off/canary/full`, data-driven folders và htmlextra/JSON export. Chi tiết ở [`postman-features.md`](../postman/postman-features.md). Workflow nằm ở [`.github/workflows/hw06-newman-api-test.yml`](../../.github/workflows/hw06-newman-api-test.yml). Pseudocode và generator tham chiếu ở [`test-generator/design.md`](../test-generator/design.md) và [`generator.py`](../test-generator/generator.py).

OpenAPI audit: file [`openapi/eshop.openapi.yaml`](../openapi/eshop.openapi.yaml) chỉ mô tả các endpoint được test; mọi expected result vẫn đối chiếu SUT defect catalog.

## 5. Defects và giới hạn bằng chứng

15 defect IDs trong defect catalog đã được lập trong [`bug-report.md`](bug-report.md), mỗi dòng có Found by Test Case, expected/actual và nguồn evidence. Newman hiện quan sát trực tiếp 8 assertion fail trong full suite và 7 mismatch của matrix DDT. GitHub Issues/screenshots chưa được tạo trong phiên này vì đó là tác động external cần tài khoản/quyền và đề bài yêu cầu ảnh do HUMAN chụp.

`ai-critique.md` là bản nháp dữ liệu 200–300 từ để người học viết lại bằng nhận xét của chính mình; `diagram.mmd` là bản mô tả kỹ thuật, không thay thế `diagram.png` tự vẽ.

## 6. Artifact index

- [README tự chấm và summary](../README.md)
- [AI audit log](ai-audit-report.md)
- [Bug report](bug-report.md)
- [CI/CD report](cicd-report.md)
- [Excel/CSV](../excel/)
- [Traceability](../../tests/test-summary/traceability-matrix.md)

### Human completion gates

1. Ký API-3 audit; 2. tạo/link GitHub issues và chụp từng issue; 3. chụp Postman Console/Newman/CI; 4. tự vẽ `diagram.png`; 5. viết lại critique và xuất ba PDF; 6. đặt repo public và đóng zip theo tên đề bài.
