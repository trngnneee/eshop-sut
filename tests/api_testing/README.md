# HW06 — API Testing on EShop · Bài nộp

**Họ và tên:** Đặng Trường Nguyên

**MSSV:** 23127438

**Lớp:** 23KTPM3

**Môn:** CS423 / CSC13003 — Software Testing (AI-augmented, 2026)

**SUT:** EShop backend (Node/Express + SQLite) · `http://localhost:3000`

**Scope:** 3 API — `GET /api/products/:id` (FR-05/06) · `PUT /api/orders/:id/cancel` (FR-10) · `POST` + `PUT /api/products` (FR-15)

**Public repo:** https://github.com/trngnneee/eshop-sut

**GitHub Issues (bug):** https://github.com/trngnneee/eshop-sut/issues (20 issue, #440–#459)
**Video demo (AI Skill):** https://drive.google.com/drive/folders/13lSkQF2vfeJV9PTGLdRy5Aptm-ZgceKb?usp=sharing

> Nguyên tắc xuyên suốt: **Expected lấy theo CONTRACT (FR/OpenAPI), không hạ xuống cho khớp SUT.** Test FAIL do SUT sai spec là **kết quả đúng** (lộ bug), không sửa expected để làm xanh.

---

## 1. Test Summary Report

| Chỉ số | Giá trị |
|--------|---------|
| Số API trong scope | **3** |
| Test case **AI sinh** (Bước 2) | 212 |
| Test case **tự thêm** (audit Bước 3 + extend Bước 4) | 8 (TC-P3-073 + 7 extend) |
| Test case **gộp/bỏ** (audit) | 1 (TC-P3-048 → gộp 057) |
| **Tổng test case hiệu lực** | **219** (API-1: 85 · API-2: 59 · API-3: 75) |
| Test case **đã execute** | 219 / 219 (probe cURL live + chạy Postman/Newman) |
| Test case **kỳ vọng PASS** (SUT đúng spec) | ≈ 145 |
| Test case **kỳ vọng FAIL = lộ bug** (VALID-but-FAIL) | ≈ 74 |
| **Số bug đã verify** | **20** |
| Cờ SEC-04 (stored/reflected XSS vector — kiểm chéo tầng UI) | 1 nhóm |
| Bug ngoài scope (nêu 1 dòng trong report) | 5 |

**Kết quả chạy thực tế:**

- **Postman Collection Runner** (full collection 238 request): **905 tests → 629 pass / 276 fail**.
- **Newman + htmlextra** (full collection): **893 assertions → 566 pass / 327 failed**.
- Các FAIL là **có chủ đích** — ánh xạ 1-1 tới 20 bug (xem `bug-reports/README.md`).

**Phân bổ bug theo severity:** Critical/P0 = 8 · Major/P1 = 7 · Minor/P2 = 5.

---

## 2. Cấu trúc bài nộp

```ini
tests/api_testing/
├─ README.md                      ← file này (self-assessment + test summary)
├─ openapi.yaml                   ← contract 3 API + x-sut-actual (bug) + x-test-*
├─ testcases/                     ← 219 test case (12 file markdown, 4 nhóm/API)
│  └─ 00-TestCases-Summary.md     ← bảng tổng
├─ postman/
│  ├─ EShop-HW06.postman_collection.json   ← collection chính (v2.1.0, 238 request)
│  ├─ EShop-CI-green / -onefail…json        ← 2 suite CI
│  ├─ EShop-Local.postman_environment.json
│  ├─ schemas/ (5 JSON Schema)  ·  data/ (3 CSV data-driven)
│  └─ POSTMAN-FEATURES.md         ← bảng “feature → ở đâu”
├─ newman/
│  ├─ report.html · report-dd1.html · report-dd2.html
│  └─ screenshots/                ← ảnh anti-cheat + Runner + CI (xem manifest)
├─ bug-reports/                   ← 20 bug theo template Issue + README (link Issue)
│  └─ screenshots/                ← ảnh 20 Issue trên GitHub (manifest)
├─ docs/
│  ├─ report.md                   ← MAIN REPORT
│  ├─ ai-critique.md              ← AI Critique
│  ├─ ci-cd-report.md             ← CI/CD + 2 run
│  ├─ ai-testcase-audit.md · extended-cases.md · openapi-audit.md
│  └─ api_specification.md
└─ ai_declaration/                ← [AI-02] Audit · [AI-03] Disclosure · [AI-05] Privacy

.agent/skills/api-fr-testing/     ← Agent Skill: AI test-generator
├─ SKILL.md · references/pseudocode.md · scripts/generator.py
└─ architecture.drawio · architecture.png   ← diagram (tự vẽ)

.github/workflows/api-tests.yml   ← CI/CD (Newman)
```

---

## 3. Bảng tự đánh giá (Assessment Template — đề §15)

| No. | Criteria | Grade | **Self-Assessed Grade** |
|-----|----------|-------|-------------------------|
| 1 | API 1 — full pipeline (generate + audit + extend + execute + bugs) | 30 | **30** |
| 2 | API 2 — full pipeline (same criteria) | 30 | **30** |
| 3 | API 3 — full pipeline (same criteria) | 30 | **30** |
| 4 | Agent Skills — AI-driven test generator | 10 | **10** |
| | **Total** | **100** | **100** |

---

## 4. Ràng buộc Anti-AI-Cheat (đề §11) — bằng chứng

| Yêu cầu | Bằng chứng |
|---------|-----------|
| Header `X-Student-Id: 23127438` do pre-request script chèn | `newman/screenshots/console-x-student-id.jpg` (Postman Console log `[HW06] X-Student-Id = 23127438 -> ...`) |
| Newman chạy trên `localhost`/`127.0.0.1` | `newman/screenshots/newman-terminal-localhost.jpg` |
| Diagram AI test-generator **tự vẽ** | `.agent/skills/api-fr-testing/architecture.drawio` + `.png` (thiết kế bởi SV) |

---

## 5. Liên kết nhanh

- **Main report:** [`docs/report.md`](docs/report.md)
- __AI Audit Report:__ [`ai_declaration/[AI-02] - FIT@HCMUS - AI Audit Report_En.md`](ai_declaration/)
- **AI Critique:** [`docs/ai-critique.md`](docs/ai-critique.md)
- __AI Disclosure:__ [`ai_declaration/[AI-03] …`](ai_declaration/)
- **CI/CD report:** [`docs/ci-cd-report.md`](docs/ci-cd-report.md) — run pass: `…/actions/runs/32619544526` · run fail: `…/actions/runs/32619881963`
- **Postman features:** [`postman/POSTMAN-FEATURES.md`](postman/POSTMAN-FEATURES.md)
- **Bug ↔ Issue:** [`bug-reports/README.md`](bug-reports/README.md)
- **Video demo AI Skill:** https://drive.google.com/drive/folders/13lSkQF2vfeJV9PTGLdRy5Aptm-ZgceKb?usp=sharing (xem [`demo-video/`](demo-video/))
