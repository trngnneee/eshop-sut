# 04 — Checklist Bài nộp HW06

> ⚠️ Đề bài mục 17: **"Thiếu bất kỳ tài liệu bắt buộc nào ⇒ 0 điểm."** Đi hết checklist này trước khi nén file.

**Tên file nộp:** `23127207_HW06_AI_API_<SelfAssessedGrade>.zip`
*(SelfAssessedGrade là số 3 chữ số trong khoảng [000, 100] — ví dụ `23127207_HW06_AI_API_090.zip`)*

---

## 1. Nội dung bắt buộc trong file `.zip` (mục 14 của đề)

| ☐ | Hạng mục đề bài yêu cầu | File / đường dẫn trong bài nộp | Owner | Yêu cầu R |
| :-: | :--- | :--- | :-: | :--- |
| ☐ | Báo cáo chính (**Markdown + PDF**), gồm phần API testing và AI audit | `report/main-report.md` + `main-report.pdf` | 🤖 + 🧑(PDF) | R-01…R-05 |
| ☐ | Link repository GitHub **công khai** (collection, script, report) | Ghi trong `README.md` và `main-report.md` | 🧑 | — |
| ☐ | Postman collection (`.json`) | `postman/EShop-HW06-23127207.postman_collection.json` | 🤖 | R-04 |
| ☐ | Newman report (**HTML**) | `newman/reports/00-full-suite.html` (+ 3 report DDT) | 🤖 | R-04, R-15 |
| ☐ | **Danh sách tính năng Postman đã dùng** | `postman/postman-features.md` | 🤖 + 🧑 | R-06 |
| ☐ | CI/CD report ngắn: cấu hình pipeline + **2 lần chạy** (1 xanh, 1 đỏ) kèm **screenshot và link** | `report/cicd-report.md` + `evidence/screenshots/04-ci-pass.png`, `05-ci-fail.png` | 🤖 + 🧑 | R-07 |
| ☐ | Test case dạng **Excel** + test summary | `excel/test-cases.xlsx`, `excel/test-summary.xlsx` | 🤖 (+🧑 nếu phải chuyển từ CSV) | — |
| ☐ | **Sơ đồ** AI test-generator (PNG/Mermaid) + **pseudocode** (`.md` / `.py`) | `test-generator/diagram.png`, `design.md`, `generator.py` | 🧑 (sơ đồ) + 🤖 | R-08, R-09, **R-16** |
| ☐ | *(Tuỳ chọn)* API spec chuyển sang OpenAPI (`.yaml`/`.json`) — **nếu AI sinh thì phải audit** | `openapi/eshop.openapi.yaml` + phần audit trong `main-report.md` | 🤖 | — |
| ☐ | **Bug report** + screenshot các bug trên trang GitHub Issues | `report/bug-report.md` + `evidence/screenshots/bug-*.png` | 🤖 + 🧑 | R-05 |
| ☐ | **AI Critique** và **AI Audit Report** (Markdown + PDF) | `report/ai-critique.md`, `report/ai-audit-report.md` (+ 2 file PDF) | 🧑 (critique) + 🤖 (audit) | R-11, R-12 |
| ☐ | **Git commit log** (file text) | `report/git-commit-log.txt` | 🤖 | R-13 |
| ☐ | `README.md` chứa **bảng tự chấm** + **test summary** (số API; số test case sinh / thêm / chạy / pass / fail; số bug) | `README.md` | 🤖 | — |
| ☐ | Tài liệu hỗ trợ khác | `docs/hw06/*` (bộ 4 file phân tích này) | 🤖 | P-04 |

---

## 2. Ràng buộc chống gian lận — TA kiểm tra trực tiếp (mục 11)

| ☐ | Ràng buộc | Bằng chứng | Kiểm tra thế nào |
| :-: | :--- | :--- | :-: |
| ☐ | **R-14** — Header `X-Student-Id: 23127207` trên mọi request | `evidence/screenshots/01-x-student-id-console.png` | Screenshot **Postman Console** phải đọc được rõ chuỗi `23127207` |
| ☐ | **R-15** — Newman run output khớp deployment | `newman/reports/*.html`, `evidence/screenshots/02-newman-cli-run.png` | Trong report phải thấy host `localhost` hoặc `127.0.0.1` |
| ☐ | **R-16** — Sơ đồ test-generator **tự vẽ** | `test-generator/diagram.png` | Không được là ảnh do AI sinh; sinh viên phải giải thích được từng khối khi vấn đáp |

---

## 3. Danh sách việc chỉ HUMAN làm được

| ☐ | Việc | Task | Ghi chú |
| :-: | :--- | :--- | :--- |
| ☐ | Vẽ sơ đồ AI test-generator | T-8.1 | draw.io / Excalidraw / vẽ tay chụp lại — **quyết định thiết kế phải là của bạn** |
| ☐ | Viết AI Critique 200–300 từ | T-9.3 | Trả lời 3 câu: AI sai/thiên lệch/thiếu ở đâu · vì sao nó không bắt được · học được nguyên tắc gì. Codex đã chuẩn bị sẵn bảng dữ liệu đầu vào |
| ☐ | Duyệt 3 bảng audit và ký xác nhận | T-1.2, T-2.2, T-3.2 | R-02 quy trách nhiệm cho **người**, không cho AI |
| ☐ | Screenshot Postman Console (X-Student-Id) | T-5.3 | **Bắt buộc**, thiếu là vi phạm R-14 |
| ☐ | Screenshot Newman CLI | T-5.3 | |
| ☐ | Tạo Postman Workspace / Mock server / Monitor + screenshot | T-4.5 | Tăng điểm R-06 |
| ☐ | Screenshot 2 lần chạy CI (xanh / đỏ) trên tab Actions | T-6.2 | |
| ☐ | Screenshot từng GitHub Issue | T-7.3 | **Mỗi issue một ảnh** — đề bài ghi rõ |
| ☐ | Quay video demo Agent Skill → link YouTube | T-8.4 | Khuyến khích, điểm cộng cho R-10 |
| ☐ | Xuất PDF cho 3 báo cáo | T-9.8 | `main-report`, `ai-audit-report`, `ai-critique` |
| ☐ | Đặt repo ở chế độ **public** | T-9.8 | Đề bài yêu cầu "public GitHub repository link" |
| ☐ | Nén `.zip` đúng tên và nộp Moodle | T-9.8 | Nộp trễ **không được chấp nhận** |

---

## 4. Kiểm tra chất lượng trước khi nộp

| ☐ | Điểm kiểm tra | Cách kiểm |
| :-: | :--- | :--- |
| ☐ | Mỗi API có **≥ 35** test case do AI sinh | Đếm số dòng ở `api-0X-*/01-ai-generated.md` |
| ☐ | Mỗi API có **≥ 5** test case tự thêm, kèm lý do AI bỏ sót | `api-0X-*/03-extended.md` |
| ☐ | **100%** test case AI sinh đã được gán nhãn VALID/INVALID/INCOMPLETE + lý do | So số dòng `02-audit.md` với `01-ai-generated.md` |
| ☐ | Đủ 4 nhóm bao phủ ở **cả 3** API: domain partition · state transition · security · schema | Lọc cột "Nhóm" trong `test-cases.md` |
| ☐ | Chuỗi **≥ 5 prompt/API** có trong AI Audit Report (không phải 1 prompt tổng) | Đếm entry trong `ai-audit-report.md` — tối thiểu 15 entry cho phần generate |
| ☐ | Mỗi entry AI Audit đủ 4 thành phần: tên tool · ngày giờ · prompt · output | Rà từng entry |
| ☐ | AI Critique đúng **200–300 từ** | Đếm từ |
| ☐ | Mọi bug có **cả** mục trong `bug-report.md` **và** issue GitHub **và** screenshot | Đối chiếu 3 cột trong bảng ở §5 dưới |
| ☐ | Mọi bug ghi rõ `Found by Test Case: TC-…` | Nguyên tắc `Rule.pdf` §H.1 |
| ☐ | Mọi test case FAIL trong test run có `Related Bug` | `Rule.pdf` §H.6 |
| ☐ | Traceability matrix đã cập nhật phần HW06 | `tests/test-summary/traceability-matrix.md` |
| ☐ | Git log có **≥ 24 commit**, tách theo từng bước generate/audit/extend/execute của từng API | `git log --oneline HW6-Khoa \| wc -l` |
| ☐ | Không có file nào chứa placeholder `TODO(HUMAN)` còn sót | `grep -rn "TODO(HUMAN)" hw06/` |
| ☐ | Không có số liệu bịa: mọi con số Newman đều trích từ file `.json` thật | Đối chiếu `README.md` với `newman/reports/*.json` |

---

## 5. Bảng theo dõi bug (điền khi làm Phase 7)

| # | Bug ID | Tiêu đề | Test case phát hiện | ☐ `bug-report.md` | ☐ GitHub Issue # | ☐ Screenshot |
| :-: | :--- | :--- | :--- | :-: | :-: | :-: |
| 1 | D-LOGIN-01 | Bộ đếm đăng nhập sai tăng 2 đơn vị | `TC-API-LOGIN-013` | ☐ | ☐ #___ | ☐ |
| 2 | D-LOGIN-02 | Khoá 180 s thay vì 30 s | `TC-API-LOGIN-0__` | ☐ | ☐ #___ | ☐ |
| 3 | D-LOGIN-03 | Response trả mật khẩu plaintext | `TC-API-LOGIN-0__` | ☐ | ☐ #___ | ☐ |
| 4 | D-LOGIN-05 | JWT không hết hạn, secret hard-code | `TC-API-LOGIN-0__` | ☐ | ☐ #___ | ☐ |
| 5 | D-LOGIN-06 | Bộ đếm không reset sau khi hết khoá | `TC-API-LOGIN-0__` | ☐ | ☐ #___ | ☐ |
| 6 | D-CHK-01 | Tin `total_amount` từ client | `TC-API-CHECKOUT-0__` | ☐ | ☐ #___ | ☐ |
| 7 | D-CHK-02 | Chấp nhận `total_amount` âm / bằng 0 | `TC-API-CHECKOUT-0__` | ☐ | ☐ #___ | ☐ |
| 8 | D-CHK-03 | Không xoá giỏ sau checkout | `TC-API-CHECKOUT-0__` | ☐ | ☐ #___ | ☐ |
| 9 | D-CHK-04 | Checkout được với giỏ rỗng | `TC-API-CHECKOUT-0__` | ☐ | ☐ #___ | ☐ |
| 10 | D-CHK-07 | IDOR ở `GET /api/orders/:id` | `TC-API-CHECKOUT-0__` | ☐ | ☐ #___ | ☐ |
| 11 | D-ADM-01 | Role escalation ở API admin | `TC-API-ORDER-STATUS-0__` | ☐ | ☐ #___ | ☐ |
| 12 | D-ADM-02 | Cho phép `canceled → delivered` | `TC-API-ORDER-STATUS-0__` | ☐ | ☐ #___ | ☐ |
| 13 | D-ADM-03 | Admin không huỷ được đơn `shipping` | `TC-API-ORDER-STATUS-0__` | ☐ | ☐ #___ | ☐ |
| 14 | D-ADM-04 | Luôn trả 200 dù UPDATE lỗi | `TC-API-ORDER-STATUS-0__` | ☐ | ☐ #___ | ☐ |
| 15 | D-ADM-08 | User huỷ được đơn đang `shipping` | `TC-API-ORDER-STATUS-0__` | ☐ | ☐ #___ | ☐ |

---

## 6. Bảng tự chấm điểm (chép vào `hw06/README.md`)

| No. | Criteria | Grade | Self-Assessed Grade |
| :-: | :--- | :-: | :-: |
| 1 | API 1 — full pipeline (generate + audit + extend + execute + bugs) | 30 | ___ |
| 2 | API 2 — full pipeline (same criteria) | 30 | ___ |
| 3 | API 3 — full pipeline (same criteria) | 30 | ___ |
| 4 | Agent Skills (AI-driven test generator) | 10 | ___ |
| | **Total** | **100** | **___** |

**Gợi ý tự chấm:** làm đủ Phase 0–9 kèm toàn bộ bằng chứng HUMAN ⇒ khoảng **085–092**. Nếu bỏ video demo (T-8.4) và các tính năng Postman cloud (workspace/mock/monitor) ⇒ khoảng **075–082**.

---

## 7. Nhắc cuối

- Đề bài mục 13: **30% sinh viên** có thể bị gọi **vấn đáp 5–7 phút**. Phải tự giải thích được: vì sao chọn 3 API này · chuỗi prompt đã dùng · vì sao gán nhãn INVALID cho từng case cụ thể · từng khối trong sơ đồ test-generator · vì sao pipeline có 1 lần xanh 1 lần đỏ.
- Đề bài mục 17: **cấm sao chép giữa sinh viên, kể cả prompt** — chuỗi prompt trong AI Audit phải là của bạn, không lấy từ branch của bạn cùng nhóm.
