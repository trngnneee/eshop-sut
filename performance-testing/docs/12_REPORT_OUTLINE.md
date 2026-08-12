# 12 — REPORT OUTLINE (Tài liệu nộp cuối)

> Khung cho main report, README, AI Audit Report, AI Critique, git log, và checklist nộp bài.
> Đề §14 (Submission Regulations) + §15 (Assessment Template) + §9 + §10.
> ⚠️ Đề §17: **thiếu bất kỳ tài liệu bắt buộc nào ⇒ 0 điểm.**

---

## 1. `23127207_HW05_Report.md` — Báo cáo chính

Export sang PDF sau khi hoàn tất. Bố cục:

```markdown
# HW05 — Kiểm thử Hiệu năng hệ thống EShop
**Họ tên:** <<FILL>> · **MSSV:** 23127207 · **Workflow:** Browse-to-buy
**Ngày thực hiện:** <<FILL>> · **Công cụ:** Apache JMeter 5.6.3 (chính), k6 (bổ sung)

## 1. Tổng quan
### 1.1 Hệ thống được kiểm thử (SUT)
### 1.2 Phạm vi và phân chia trong nhóm
    → từ docs/00_GROUP_SCOPE.md §2, §3 (bảng phân công + ma trận endpoint)
### 1.3 Môi trường thực thi
    → bảng phần cứng từ evidence/hardware/spec-table.md

## 2. Task 1 — Thiết kế và thực thi có AI hỗ trợ
### 2.1 Quy trình dẫn dắt AI theo từng bước
    → tóm tắt deliverables/02_ai-generation-log.md, dẫn link tới bản đầy đủ
### 2.2 Thiết kế workflow và ánh xạ 3 nhóm endpoint
    → deliverables/01_test-design.md
### 2.3 Dữ liệu kiểm thử (data-driven)
    → docs/02_DATA_SPEC.md §3 + khai báo điều kiện dữ liệu (+500 sản phẩm)
### 2.4 Ba kịch bản và ba loại report view
    → bảng tham số + bảng listener
### 2.5 Rà soát và sửa lỗi của AI (human review)
    → deliverables/03_human-review-fixes.md
### 2.6 Kết quả thực thi
    → bảng tổng hợp 4 kịch bản + ảnh chụp listener + ảnh Task Manager
### 2.7 Thủ tục reset khóa tài khoản
    → docs/05_EXECUTION_RUNBOOK.md §4 + ảnh
### 2.8 Ngưỡng chịu tải của phần cứng (Endurance)
    → deliverables/05_endurance-threshold.md
### 2.9 Lỗi và vấn đề hiệu năng đã ghi nhận
    → bảng GitHub Issues + ảnh

## 3. Task 2 — Phân tích bằng AI và săn lỗi diễn giải
### 3.1 Output thô của AI
### 3.2 Các lỗi diễn giải và giá trị đúng từ raw .jtl
### 3.3 Phán quyết các đề xuất tối ưu (feasible / hallucinated)
### 3.4 Kết luận
    → toàn bộ từ deliverables/06_ai-analysis-critique.md

## 4. Task 3 — Đề xuất Continuous Performance Testing
    → deliverables/07_continuous-performance-testing.md (flow chart + trade-offs)

## 5. Agent Skill
    → mô tả .agents/skills/performance_testing/ + link video demo

## 6. Phê bình AI (AI Critique)
    → deliverables/AI_CRITIQUE.md, 200-300 từ

## 7. Giới hạn phương pháp và hướng cải thiện
    → docs/03_TEST_DESIGN.md §7

## 8. Kết luận

## Phụ lục A — AI Audit Report
## Phụ lục B — Git commit log
## Phụ lục C — Danh mục bằng chứng đính kèm
```

---

## 2. `performance-testing/README.md`

Đề §14 yêu cầu README chứa **bảng tự chấm** + **báo cáo tóm tắt** với 5 nội dung cụ thể.

```markdown
# HW05 — Performance Testing · EShop · MSSV 23127207

**Workflow:** Browse-to-buy — `login → GET /api/products → GET /api/products/{id} → POST /api/cart → POST /api/checkout`
**Repository:** https://github.com/trngnneee/eshop-sut  ·  **Branch:** `HW5`
**Video demo:** <<FILL: link YouTube unlisted>>
**Video demo Agent Skill:** <<FILL: link YouTube unlisted>>

---

## 1. Bảng tự đánh giá  (đề §15)

| No. | Tiêu chí | Điểm tối đa | Tự chấm | Căn cứ |
|:---:|:---|:---:|:---:|:---|
| 1 | Task 1 — Load testing | 20 | <<FILL>> | `test-plans/23127207_Load_*.jmx`, `results/load/` |
| 2 | Task 1 — Stress testing | 20 | <<FILL>> | `test-plans/23127207_Stress_*.jmx`, `results/stress/` |
| 3 | Task 1 — Spike testing | 20 | <<FILL>> | `test-plans/23127207_Spike_*.jmx`, `results/spike/` |
| 4 | Task 2 — AI analysis + misinterpretation hunt | 10 | <<FILL>> | `deliverables/06_ai-analysis-critique.md` |
| 5 | Task 3 — Continuous Performance Testing (G9.6) | 10 | <<FILL>> | `deliverables/07_continuous-performance-testing.md` |
| 6 | Agent Skills | 10 | <<FILL>> | `.agents/skills/performance_testing/` |
| | **Tổng** | **100** | **<<FILL>>** | |

## 2. Báo cáo tóm tắt kiểm thử

### 2.1 Các kịch bản đã chạy
| Kịch bản | VU đỉnh | Thời lượng | Samples | RPS | Err% | p95 `02_Browse` | Report view |
|:---|---:|---:|---:|---:|---:|---:|:---|
| Load | 50 | 5' | <<FILL>> | <<FILL>> | <<FILL>> | <<FILL>> | Aggregate Report |
| Stress | 200 | 8' | <<FILL>> | <<FILL>> | <<FILL>> | <<FILL>> | Summary Report |
| Spike | 310 | 6' | <<FILL>> | <<FILL>> | <<FILL>> | <<FILL>> | View Results Tree |
| Endurance | 30 | 12' | <<FILL>> | <<FILL>> | <<FILL>> | <<FILL>> | Aggregate Report |

### 2.2 Nhóm endpoint đã phủ
| Nhóm | Endpoint | Label |
|:---|:---|:---|
| Auth-heavy | `POST /api/login` | `01_Login` |
| Read-heavy | `GET /api/products` (toàn bộ catalog) | `02_BrowseProducts` |
| Read-heavy | `GET /api/products/{id}` | `03_ProductDetail` |
| Transactional | `POST /api/cart` | `04_AddToCart` |
| Transactional | `POST /api/checkout` | `05_Checkout` |

### 2.3 Ngưỡng chịu tải của phần cứng
- **Phần cứng:** <<FILL: hostname, CPU, RAM, OS>>
- **Max stable RPS:** <<FILL>> req/s ở <<FILL>> VU đồng thời (p95 ≤ <<FILL>> ms, lỗi ≤ <<FILL>> %)
- **Điểm gãy:** từ bậc <<FILL>> VU, p95 tăng từ <<FILL>> ms lên <<FILL>> ms (+<<FILL>> %)
- **Trần bộ nhớ:** <<FILL>> MB (PrivateMemorySize của tiến trình node)
- **Tốc độ rò rỉ bộ nhớ:** <<FILL>> MB/phút trong 12 phút chạy bền, không giảm sau khi tải kết thúc

### 2.4 Lỗi và vấn đề hiệu năng đã ghi nhận
| # | Issue | Loại | Mức độ | Link |
|:--:|:---|:---|:---|:---|
| 1 | FR-02: bộ đếm login sai tăng 2, khóa 180s thay vì 30s | Functional | Cao | <<FILL>> |
| 2 | FR-06: `GET /api/products/:id` trả 200 cho id không tồn tại | Functional | Trung bình | <<FILL>> |
| 3 | FR-06: `price` trả kiểu string khi id chẵn | Functional | Trung bình | <<FILL>> |
| 4 | Giỏ hàng in-memory rò rỉ bộ nhớ | Performance | Cao | <<FILL>> |
| 5 | <<FILL nếu có: SQLITE_BUSY ở tải cao>> | Performance | <<FILL>> | <<FILL>> |

**Tổng:** <<FILL>> lỗi chức năng, <<FILL>> vấn đề hiệu năng.

## 3. Cấu trúc thư mục
    → cây thư mục từ docs/00_BUILD_SPEC.md §2

## 4. Cách tái lập
    → chuỗi lệnh: setup → seed → run → analyze
```

---

## 3. `deliverables/AI_AUDIT_REPORT.md`

Đề §9 — **phụ lục bắt buộc**. Mỗi lượt tương tác ghi đủ **4 trường**.

```markdown
# AI Audit Report — HW05 Performance Testing
**MSSV:** 23127207 · **Ngày:** <<FILL>>

## Tuyên bố
> I use AI tools for the following tasks.

## Danh sách công cụ AI đã dùng
| Công cụ | Phiên bản/Model | Dùng cho | Số lượt |
|:---|:---|:---|---:|
| <<FILL>> | <<FILL>> | Thiết kế và sinh test plan | <<FILL>> |
| <<FILL>> | <<FILL>> | Phân tích log và đề xuất tối ưu | <<FILL>> |

## Nhật ký tương tác

### [#01] Phân tích endpoint và chốt workflow
- **Công cụ:** <<FILL>>
- **Thời gian:** <<FILL: YYYY-MM-DD HH:MM (+07)>>
- **Prompt:**
  ```
  <<nguyên văn>>
  ```
- **Output:**
  ```
  <<nguyên văn, KHÔNG rút gọn>>
  ```
- **Đánh giá và can thiệp của tôi:** <<FILL>>

### [#02] ...
   (lặp cho MỌI lượt tương tác)

## Thống kê
- Tổng số lượt: <<FILL>>
- Số lượt phải sửa output: <<FILL>>
- Tỉ lệ output dùng được ngay: <<FILL>> %
```

### 3.1 Ba lỗi khiến mất điểm phần này

| Lỗi | Vì sao mất điểm |
| :--- | :--- |
| Rút gọn output AI | Đề ghi rõ *"The AI output"*, tức là đầy đủ |
| Chỉ ghi những lượt thành công | Nhật ký toàn màu hồng là dấu hiệu viết lại từ trí nhớ |
| Ghi ngày giờ ước chừng | Timestamp phải khớp với thời điểm chạy test trong `04_execution-report.md` |

---

## 4. `deliverables/AI_CRITIQUE.md` — 200–300 từ

Đề §10 yêu cầu trả lời **ba câu hỏi**:

1. AI sai / thiên lệch / thiếu sót ở đâu?
2. Vì sao nó không tự phát hiện?
3. Nguyên tắc gì rút ra được về việc cộng tác với AI?

### 4.1 Ràng buộc

- **200–300 từ.** Đếm trước khi nộp:
  ```powershell
  $t = Get-Content "performance-testing\deliverables\AI_CRITIQUE.md" -Raw
  ($t -split '\s+' | Where-Object { $_ -ne '' }).Count
  ```
  Ngoài khoảng → sửa. Đây là ràng buộc **đếm được**, người chấm sẽ đếm.
- Viết dạng **một đoạn văn liền mạch**, không gạch đầu dòng (đề nói *"a paragraph"*).
- Dẫn **ví dụ cụ thể** từ bài của mình, không viết chung chung về AI.

### 4.2 Ba trụ nội dung nên có

| Trụ | Nguyên liệu từ bài |
| :--- | :--- |
| **Sai gì** | Chọn 1–2 ví dụ mạnh nhất: AI tin `README.md` về ngưỡng khóa tài khoản trong khi `server.js:54,57` nói khác; hoặc AI đề xuất "thêm index" cho một truy vấn không có mệnh đề `WHERE` |
| **Vì sao không tự phát hiện** | AI suy luận từ **mẫu phổ biến** thay vì kiểm chứng bằng dữ liệu/mã nguồn cụ thể; nó không chạy được truy vấn, không đọc được file `.jtl` gốc, không có vòng phản hồi từ hệ thống thật; và nó không biết ràng buộc tổ chức (phân chia scope trong nhóm) vì thứ đó không nằm trong code |
| **Nguyên tắc rút ra** | Nêu một quy tắc **cụ thể, kiểm chứng được**. Ví dụ: *"với mọi nhận định định lượng, yêu cầu AI chỉ rõ cột dữ liệu nguồn; nhận định nào không chỉ được nguồn thì tự tính lại"* — chứ không phải *"cần review kỹ hơn"* |

> Câu kết mạnh nhất cho bài này: AI hữu ích nhất khi được dùng để **sinh ra thứ có thể kiểm chứng được** (file `.jmx`, đoạn phân tích có dẫn số), và nguy hiểm nhất khi được dùng để **kết luận** — vì kết luận nghe hợp lý là thứ nó tạo ra giỏi nhất, kể cả khi sai.

---

## 5. `deliverables/git-commit-log.txt`

```powershell
$root = "C:\My Workspace\HCMUS\Test\Week 3\Hw2"
git -C $root log --oneline --decorate --graph --date=iso `
  --pretty=format:"%h %ad %s" -40 |
  Out-File -Encoding utf8 "$root\performance-testing\deliverables\git-commit-log.txt"
```

Kiểm tra: có **≥ 10 commit riêng biệt** theo bảng `00_BUILD_SPEC.md` §4, mỗi bước quy trình một commit. Một commit khổng lồ "add HW05" là mất điểm mục §12 của đề.

---

## 6. Checklist nộp bài — đối chiếu đề §14

Tên file zip: **`23127207_HW05_AI_Performance_<Grade>.zip`** (Grade là số 3 chữ số, ví dụ `090`).

| # | Yêu cầu của đề | File/thư mục | ✔ |
| :--: | :--- | :--- | :--: |
| 1 | Main report (Markdown + PDF), gồm báo cáo hiệu năng và phê bình AI | `23127207_HW05_Report.md` + `.pdf` | ☐ |
| 2 | Link GitHub repo công khai | trong `README.md` | ☐ |
| 3 | Ba test plan Load/Stress/Spike đúng quy ước tên | `test-plans/23127207_{Load,Stress,Spike}_*.jmx` | ☐ |
| 4 | Ba raw `.jtl` **đầy đủ** | `results/{load,stress,spike}/*.jtl` | ☐ |
| 5 | Ba thư mục HTML report | `results/{load,stress,spike}/html-report/` | ☐ |
| 6 | Ảnh resource monitor + hardware spec | `evidence/*/`, `evidence/hardware/` | ☐ |
| 7 | Link video demo YouTube unlisted | `README.md` | ☐ |
| 8 | AI Critique + AI Audit Report (Markdown + PDF) | `deliverables/AI_CRITIQUE.*`, `AI_AUDIT_REPORT.*` | ☐ |
| 9 | Git commit log (file text) | `deliverables/git-commit-log.txt` | ☐ |
| 10 | Bug report + ảnh GitHub Issues | `evidence/issues/` | ☐ |
| 11 | `README.md` có bảng tự chấm + tóm tắt kiểm thử | `performance-testing/README.md` | ☐ |
| 12 | Tài liệu hỗ trợ khác | `docs/`, `scripts/`, `.agents/skills/` | ☐ |

### 6.1 Bổ sung — không nằm trong danh mục bắt buộc nhưng nên có

| Hạng mục | Vì sao |
| :--- | :--- |
| `results/endurance/` | Đề §6 yêu cầu endurance test; tuy §14 chỉ liệt kê 3 `.jtl`, nộp thêm cái thứ tư là bằng chứng cho mục "ngưỡng chịu tải" |
| Agent Skill + video demo skill | Chiếm 10 điểm ở barem §15 nhưng §14 không liệt kê riêng — dễ quên |
| `k6/` + kết quả k6 | Phần bonus |
| `scripts/` | Chứng minh quy trình tái lập được |

### 6.2 Rà soát cuối trước khi nén

```powershell
$pt = "C:\My Workspace\HCMUS\Test\Week 3\Hw2\performance-testing"

# 1) Không còn placeholder nào sót lại
Select-String -Path "$pt\**\*.md" -Pattern "<<FILL" | Select-Object Path, LineNumber, Line

# 2) Không có endpoint ngoài scope trong test plan
Select-String -Path "$pt\test-plans\*.jmx" -Pattern "search=|apply-coupon|my-orders|/api/categories|/api/admin"

# 3) Tên file đúng quy ước
Get-ChildItem "$pt\test-plans\*.jmx" | Select-Object Name

# 4) File .jtl không rỗng
Get-ChildItem "$pt\results\*\*.jtl" | Select-Object Name, @{n='MB';e={[math]::Round($_.Length/1MB,2)}}

# 5) Đếm từ AI Critique
$t = Get-Content "$pt\deliverables\AI_CRITIQUE.md" -Raw
"AI_CRITIQUE word count: " + ($t -split '\s+' | Where-Object { $_ -ne '' }).Count

# 6) Số commit
git -C "C:\My Workspace\HCMUS\Test\Week 3\Hw2" log --oneline | Measure-Object -Line
```

| Kiểm tra | Kỳ vọng |
| :--- | :--- |
| 1 | **Không có kết quả** |
| 2 | **Không có kết quả** |
| 3 | Đúng 4 file, đúng định dạng `23127207_{Type}_{YYYYMMDD}.jmx` |
| 4 | Cả 4 file > 0 MB |
| 5 | Từ 200 đến 300 |
| 6 | ≥ 10 commit |

---

## 7. Checklist

- [ ] Main report đủ 8 phần + 3 phụ lục, export PDF
- [ ] `README.md` có bảng tự chấm và **đủ 5 nội dung** tóm tắt đề yêu cầu
- [ ] `AI_AUDIT_REPORT.md` ghi đủ 4 trường cho **mọi** lượt tương tác, output nguyên văn
- [ ] `AI_CRITIQUE.md` đếm được **200–300 từ**, một đoạn văn liền mạch
- [ ] `git-commit-log.txt` có ≥ 10 commit riêng biệt
- [ ] Checklist §6 tick đủ 12 mục
- [ ] Rà soát §6.2 pass cả 6 lệnh
- [ ] Tên zip đúng `23127207_HW05_AI_Performance_<Grade>.zip`
- [ ] Commit: `docs(perf): add main report, README, AI audit report and critique`
