# 00 — BUILD SPEC (Bản thi công tổng)

> **Đây là file đầu tiên phải đọc.** Mọi agent/người thực thi bắt đầu từ đây.
> Bài tập: **HW05 – Performance Testing** · SUT: **EShop** · MSSV: **23127207** · Branch: **`HW5`**

---

## 0. Đọc theo đúng thứ tự này

| Thứ tự | File | Vì sao phải đọc trước |
| :---: | :--- | :--- |
| 1 | `00_BUILD_SPEC.md` (file này) | Cây artifact, thứ tự thi công, quy ước tên, traceability |
| 2 | `00_GROUP_SCOPE.md` | **Ranh giới scope.** Đọc sai file này là hỏng cả bài |
| 3 | `01_ENVIRONMENT_SETUP.md` | Dựng JMeter + backend |
| 4 | `02_DATA_SPEC.md` | Seed data + CSV |
| 5 | `03_TEST_DESIGN.md` | Workflow + tham số tải |
| 6 | `04_JMX_BUILD_SPEC.md` | Cấu trúc `.jmx` |
| 7 | `05_EXECUTION_RUNBOOK.md` | Chạy + thu bằng chứng |
| 8 | `06_ANALYSIS_SPEC.md` | Phân tích `.jtl` |
| 9 | `07`–`12` | Nội dung báo cáo |

---

## 1. Cảnh báo trước khi gõ dòng lệnh đầu tiên

### 1.1 CẤM BỊA SỐ LIỆU

Đề bài mục 11 (Anti-AI-Cheat) nói rõ TA sẽ **verify** raw `.jtl`, video, hardware report. Vì vậy:

- **Mọi con số hiệu năng** (p95, throughput, error%, RAM, RPS) chỉ được điền **sau khi chạy thật**.
- Khi viết template báo cáo, chỗ cần số thật phải để nguyên placeholder dạng:
  ```
  <<FILL: p95 của label "02_BrowseProducts" — lấy từ results/load/summary.json>>
  ```
- **Không** được suy đoán, không được lấy "số ví dụ điển hình", không được copy số từ tài liệu khác.
- Nếu một run thất bại → ghi nhận thất bại đó vào `04_execution-report.md`, **không** thay bằng số của run khác.

### 1.2 CẤM LỆCH SCOPE

Xem `00_GROUP_SCOPE.md`. Workflow của MSSV 23127207 là **Browse-to-buy** gồm **đúng 5 request**. Các endpoint sau **thuộc thành viên khác** và không được xuất hiện trong bất kỳ `.jmx` nào:

`GET /api/products?search=` · `GET /api/categories` · `POST /api/apply-coupon` · `GET /api/orders/my-orders` · `POST /api/register` · `POST /api/forgot-password` · mọi `/api/admin/*`

### 1.3 CẤM "SỬA CHO ĐẸP"

SUT được thiết kế có lỗi cố ý. Khi test lộ ra lỗi (`SQLITE_BUSY`, `price` kiểu string, memory leak, lockout sai spec) → **ghi nhận thành finding và bug report**, tuyệt đối không sửa `backend/` để số liệu đẹp hơn.

---

## 2. Cây thư mục đích

```
performance-testing/
├── README.md                             # self-assessment + test summary (đề mục 14)
├── 23127207_HW05_Report.md               # MAIN REPORT → export PDF
├── docs/                                 # 14 file spec (ĐÃ CÓ — bạn đang đọc)
│   ├── 00_BUILD_SPEC.md
│   ├── 00_GROUP_SCOPE.md
│   ├── 01_ENVIRONMENT_SETUP.md
│   ├── 02_DATA_SPEC.md
│   ├── 03_TEST_DESIGN.md
│   ├── 04_JMX_BUILD_SPEC.md
│   ├── 05_EXECUTION_RUNBOOK.md
│   ├── 06_ANALYSIS_SPEC.md
│   ├── 07_HUMAN_REVIEW_TEMPLATE.md
│   ├── 08_AI_ANALYSIS_PROMPTS.md
│   ├── 09_MISINTERPRETATION_HUNT_TEMPLATE.md
│   ├── 10_CPT_PROPOSAL.md
│   ├── 11_AGENT_SKILL_SPEC.md
│   └── 12_REPORT_OUTLINE.md
├── deliverables/                         # ← Codex TẠO MỚI, là bài nộp
│   ├── 01_test-design.md
│   ├── 02_ai-generation-log.md
│   ├── 03_human-review-fixes.md
│   ├── 04_execution-report.md
│   ├── 05_endurance-threshold.md
│   ├── 06_ai-analysis-critique.md
│   ├── 07_continuous-performance-testing.md
│   ├── AI_AUDIT_REPORT.md
│   ├── AI_CRITIQUE.md
│   └── git-commit-log.txt
├── test-plans/
│   ├── 23127207_Load_<YYYYMMDD>.jmx
│   ├── 23127207_Stress_<YYYYMMDD>.jmx
│   ├── 23127207_Spike_<YYYYMMDD>.jmx
│   └── 23127207_Endurance_<YYYYMMDD>.jmx
├── data/
│   └── khoa_users.csv
├── scripts/
│   ├── seed_perf_data.js
│   ├── reset_lockout.js
│   ├── monitor_backend.ps1
│   ├── run_scenario.ps1
│   └── analyze_jtl.py
├── k6/
│   └── 23127207_Load_<YYYYMMDD>.js       # bonus
├── results/
│   ├── load/      { *.jtl, html-report/, resource-load.csv,      summary.json, summary.md }
│   ├── stress/    { *.jtl, html-report/, resource-stress.csv,    summary.json, summary.md }
│   ├── spike/     { *.jtl, html-report/, resource-spike.csv,     summary.json, summary.md }
│   └── endurance/ { *.jtl, html-report/, resource-endurance.csv, summary.json, summary.md }
└── evidence/                             # ← NGƯỜI thả ảnh vào, Codex không tạo
    ├── hardware/   dxdiag-*.png, spec-table.md
    ├── load/       jmeter+taskmgr-*.png
    ├── stress/     jmeter+taskmgr-*.png, lockout-reset-*.png
    ├── spike/      jmeter+taskmgr-*.png
    ├── endurance/  jmeter+taskmgr-*.png
    └── issues/     github-issue-*.png
```

Ngoài `performance-testing/`, còn tạo:

```
.agents/skills/performance_testing/       # Agent Skill (đề mục 7, 10 điểm)
├── SKILL.md
├── scripts/{generate_jmx.py, analyze_jtl.py}
└── examples/browse_to_buy_config.json

.github/workflows/perf-regression.yml     # đề xuất cho Task 3 (KHÔNG bật mặc định)
.tools/jmeter/                            # binary JMeter — thêm vào .gitignore
```

---

## 3. Quy ước tên — bất di bất dịch

Đề bài mục 4 và mục 11: tên test plan phải khớp `{StudentID}_{ScenarioType}_{YYYYMMDD}`.

| Thành phần | Giá trị |
| :--- | :--- |
| `{StudentID}` | `23127207` — không thêm ký tự nào khác |
| `{ScenarioType}` | đúng một trong `Load`, `Stress`, `Spike`, `Endurance` (viết hoa chữ đầu) |
| `{YYYYMMDD}` | **ngày chạy test thật**, ví dụ `20260812` |

Áp dụng cho: `.jmx`, `.jtl`, thư mục HTML report, file k6.

```
23127207_Load_20260812.jmx
23127207_Load_20260812.jtl
23127207_Load_20260812/           (thư mục html-report)
```

> Nếu ngày chạy khác `20260812`, đổi **đồng loạt** ở mọi nơi, kể cả trong `README.md` và report.

---

## 4. Thứ tự thi công 8 bước + commit message

Đề bài mục 12 yêu cầu **một commit riêng cho mỗi bước**. Dùng chính xác các message dưới đây (tiếng Anh, conventional commits, khớp phong cách repo).

| # | Việc | Doc hướng dẫn | Commit message |
| :---: | :--- | :--- | :--- |
| 1 | Dựng môi trường, `.gitignore` cho `.tools/` | `01` | `chore(perf): setup jmeter/k6 toolchain and gitignore` |
| 2 | `seed_perf_data.js`, `reset_lockout.js`, `data/khoa_users.csv` | `02` | `feat(perf): add seed data script and CSV dataset for browse-to-buy` |
| 3 | `deliverables/01_test-design.md` + `02_ai-generation-log.md` | `03`, `08` | `docs(perf): add browse-to-buy test design and AI generation log` |
| 4 | `23127207_Load_*.jmx` | `04` | `feat(perf): add Load test plan (50 VU, aggregate report)` |
| 5 | `23127207_Stress_*.jmx` | `04` | `feat(perf): add Stress test plan (25-200 VU stepped, summary report)` |
| 6 | `23127207_Spike_*.jmx` + `Endurance` + k6 | `04` | `feat(perf): add Spike and Endurance test plans plus k6 variant` |
| 7 | Chạy 4 scenario, đổ `results/`, `03_human-review-fixes.md`, `04_execution-report.md`, `05_endurance-threshold.md` | `05`, `06`, `07` | `test(perf): execute all scenarios with raw jtl, html reports and resource logs` |
| 8 | `06_ai-analysis-critique.md` | `08`, `09` | `docs(perf): add AI analysis critique and misinterpretation hunt` |
| 9 | `07_continuous-performance-testing.md` + workflow mẫu | `10` | `docs(perf): add continuous performance testing proposal` |
| 10 | Agent Skill | `11` | `feat(skill): add performance_testing agent skill` |
| 11 | `README.md`, main report, AI audit, AI critique, git log | `12` | `docs(perf): add main report, README, AI audit report and critique` |

Sau bước cuối:

```powershell
git -C "C:\My Workspace\HCMUS\Test\Week 3\Hw2" log --oneline --decorate --graph -30 |
  Out-File -Encoding utf8 "performance-testing\deliverables\git-commit-log.txt"
```

> Bảng có 11 dòng vì bước 4–6 tách theo từng test plan để commit log thể hiện rõ "mỗi scenario một commit" như đề yêu cầu.

---

## 5. Bảng nghiệm thu artifact

| Artifact | Doc mô tả | Tiêu chí nghiệm thu |
| :--- | :--- | :--- |
| `scripts/seed_perf_data.js` | `02` | Chạy xong: `SELECT COUNT(*) FROM users WHERE email LIKE 'khoa%'` = 400; `SELECT COUNT(*) FROM products` ≥ 505 |
| `data/khoa_users.csv` | `02` | 400 dòng + 1 header; mọi `product_id` tồn tại trong DB |
| `scripts/reset_lockout.js` | `02` | Chạy xong: `SELECT COUNT(*) FROM users WHERE locked_until IS NOT NULL` = 0 |
| 4 file `.jmx` | `04` | Mở GUI không element đỏ; chạy 1 thread × 1 loop → 5/5 sampler `200` |
| `scripts/monitor_backend.ps1` | `05` | Sinh CSV ≥ 2 cột số, số dòng ≈ thời lượng run ÷ 2s |
| `scripts/run_scenario.ps1` | `05` | Một lệnh cho ra đủ `.jtl` + `html-report/` + `resource-*.csv` |
| `scripts/analyze_jtl.py` | `06` | p95 tính ra **khớp** HTML dashboard JMeter (sai lệch ≤ 1ms do làm tròn) |
| `results/*/` | `05` | `.jtl` không rỗng, `html-report/index.html` mở được |
| Agent Skill | `11` | `SKILL.md` có frontmatter `name`/`description`; `generate_jmx.py` sinh được `.jmx` mở bằng JMeter |
| `README.md` | `12` | Có bảng self-assessment + đủ 5 mục test summary theo đề |

---

## 6. Traceability — đề bài → doc phụ trách

| Mục đề bài | Yêu cầu | Doc phụ trách | Deliverable |
| :--- | :--- | :--- | :--- |
| §5 Scope | 3 endpoint group, không trùng workflow trong nhóm | `00_GROUP_SCOPE`, `03` | `deliverables/01_test-design.md` |
| §6 Task 1 – Design with AI | Dẫn AI **từng bước**, không 1 prompt generic | `08` | `deliverables/02_ai-generation-log.md` |
| §6 Task 1 – Data-driven | CSV parameterize | `02`, `04` | `data/khoa_users.csv` |
| §6 Task 1 – 3 report views | 3 listener khác nhau | `03`, `04` | 3 file `.jmx` |
| §6 Task 1 – Naming | `{MSSV}_{Type}_{YYYYMMDD}` | `00` §3 | tên file |
| §6 Task 1 – Review & fix | AI sai gì + **vì sao** | `07` | `deliverables/03_human-review-fixes.md` |
| §6 Task 1 – Run with evidence | screenshot tool + resource + hardware, reset lockout | `05` | `deliverables/04_execution-report.md`, `evidence/` |
| §6 Task 1 – Endurance | soak 10–15 phút, số cụ thể | `03`, `05`, `06` | `deliverables/05_endurance-threshold.md` |
| §6 Task 1 – Demo video | ≥ 6 phút, tool + monitor cùng khung, tiếng Việt | `05` §7 | link YouTube trong `README.md` |
| §6 Task 1 – Report issues | GitHub Issues + ảnh | `05` §8 | `evidence/issues/` |
| §6 Task 2 – Analyse with AI | AI phân tích `.jtl` | `08` | `06_ai-analysis-critique.md` §1 |
| §6 Task 2 – Review & correct | trích **giá trị đúng từ raw `.jtl`** | `06`, `09` | `06_ai-analysis-critique.md` §2 |
| §6 Task 2 – Judge recommendations | feasible / hallucinated | `09` | `06_ai-analysis-critique.md` §3 |
| §6 Task 3 – CPT (G9.6) | flowchart + trade-offs | `10` | `deliverables/07_continuous-performance-testing.md` |
| §7 Agent Skill | skill tái dùng + video | `11` | `.agents/skills/performance_testing/` |
| §9 AI Audit Report | tool/date-time/prompt/output | `12` | `deliverables/AI_AUDIT_REPORT.md` |
| §10 AI Critique | 200–300 từ | `12` | `deliverables/AI_CRITIQUE.md` |
| §11 Anti-AI-Cheat | tên file, `.jtl` đầy đủ, video, hardware | `00` §1.1, `05` | toàn bộ |
| §12 Git commit log | commit riêng mỗi bước + file log | `00` §4 | `deliverables/git-commit-log.txt` |
| §14 Submission | danh mục file trong `.zip` | `12` §5 | checklist |
| §15 Assessment | bảng tự chấm | `12` §2 | `README.md` |

---

## 7. Việc CON NGƯỜI phải tự làm — Codex không được tạo giả

| # | Việc | Vì sao máy không làm được |
| :---: | :--- | :--- |
| 1 | **Quay video YouTube unlisted ≥ 6 phút**, thuyết minh tiếng Việt, JMeter + Task Manager **cùng khung hình** | Đề mục 11 nói TA verify giọng nói và khung hình |
| 2 | **Screenshot Task Manager** trong lúc mỗi run đang chạy | Phải là ảnh chụp thật tại thời điểm chạy |
| 3 | **Screenshot `dxdiag`** — hostname phải khớp các HW trước | Đề mục 11 đối chiếu hostname |
| 4 | **Video demo Agent Skill** riêng (đề mục 7) | |
| 5 | **Tạo GitHub Issues** cho bug + chụp màn hình | Cần tài khoản GitHub của sinh viên |
| 6 | **Export PDF** từ Markdown | |
| 7 | **Đóng gói + nộp Moodle** `23127207_HW05_AI_Performance_<Grade>.zip` | |

Codex chỉ được **soạn sẵn nội dung** cho các việc này (kịch bản lời thoại video ở `05` §7, nội dung issue ở `05` §8), rồi để người thực hiện.

---

## 8. Rủi ro đã biết

| Rủi ro | Dấu hiệu | Cách xử lý |
| :--- | :--- | :--- |
| **Lệch scope nhóm** (rủi ro số 1) | `.jmx` có sampler `?search=` / `my-orders` / `apply-coupon` | Đọc lại `00_GROUP_SCOPE.md`; `.jmx` chỉ được có **đúng 5** sampler |
| **Lockout dây chuyền** ở Stress/Spike | Nhiều `403` với body "Tài khoản đã bị khóa" | 400 account cho 310 thread; nếu vẫn dính, nâng seed lên 600 (`02` §2) |
| **JMeter và SUT cùng máy** | CPU 100%, số đo nhiễu | Bắt buộc chạy **non-GUI**; **ghi rõ giới hạn phương pháp này trong report** — đây là điểm cộng khi phân tích, không phải điểm trừ |
| **`SQLITE_BUSY`** khi ≥ 200 thread checkout | HTTP 500, body chứa `SQLITE_BUSY` | Đây là **kết quả thật**, ghi thành finding + bug report. Không sửa backend |
| **Seed thêm 500 product** làm lệch so sánh với thành viên khác | | **Khai báo điều kiện dữ liệu** trong `01_test-design.md` và report |
| Cổng 3000 bận | `EADDRINUSE` | `01` §5 |

---

## 9. Định nghĩa "xong"

Bài chỉ được coi là xong khi **tất cả** đúng:

- [ ] 4 file `.jmx` đúng quy ước tên, mở được bằng JMeter GUI
- [ ] 4 thư mục `results/*` có `.jtl` **đầy đủ** (không phải bản tóm tắt) + `html-report/`
- [ ] 3 listener khác nhau trên bộ Load/Stress/Spike, không lặp loại
- [ ] `05_endurance-threshold.md` có **số thật**: max stable RPS, trần RAM, điểm gãy
- [ ] `06_ai-analysis-critique.md` có ≥ 3 misinterpretation, mỗi cái **trích giá trị đúng từ `.jtl`**
- [ ] `07_continuous-performance-testing.md` có flowchart + trade-offs
- [ ] Agent Skill chạy được
- [ ] `AI_CRITIQUE.md` đếm được 200–300 từ
- [ ] `git-commit-log.txt` có ≥ 10 commit riêng biệt theo bảng §4
- [ ] Không còn placeholder `<<FILL: ...>>` nào sót lại
- [ ] Checklist đề mục 14 ở `12_REPORT_OUTLINE.md` §5 tick đủ
