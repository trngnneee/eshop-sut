# 01 — Phân tích Yêu cầu HW06 (API Testing)

Tài liệu này bóc tách `Requirements/Requirements.pdf` và `Requirements/Rule.pdf` thành danh sách yêu cầu có mã, kèm **tiêu chí nghiệm thu** để đối chiếu khi nộp bài.

---

## A. Thông tin khung

| Mục | Giá trị |
| :--- | :--- |
| Mã bài | HW06-AI |
| Thời lượng | 10 giờ |
| Hình thức | **Cá nhân** |
| Nộp | Moodle (báo cáo) — hạn xem link nộp |
| AI Policy | **Mở** — bắt buộc có Declaration + AI Audit Report đính kèm |
| Bloom-AI | G9.2 (Apply), G9.3 (Analyse), G9.4 (Collaborate), G9.5 (Create) |
| Nộp trễ | **Không được phép** |
| Thiếu tài liệu bắt buộc | **0 điểm** |
| Sao chép (kể cả prompt) | **0 điểm cả hai bên** |
| Vấn đáp | 30% sinh viên ngẫu nhiên, 5–7 phút, tuần sau deadline |

> ⚠️ "Thiếu bất kỳ tài liệu bắt buộc nào ⇒ 0 điểm" là ràng buộc nghiêm trọng nhất. Checklist `04-deliverables-checklist.md` tồn tại để chống rủi ro này.

---

## B. Năm nguyên tắc chỉ đạo (mục 2 của đề)

| Mã | Nguyên tắc | Hệ quả cụ thể lên cách làm bài |
| :--- | :--- | :--- |
| **P-01** | **AI-First** | Phải **dẫn dắt AI qua từng bước của kỹ thuật kiểm thử** như đã học. Cấm 1 prompt tổng kiểu *"generate all the API test cases from the spec and run them"*. ⇒ Mỗi API cần **chuỗi ≥ 4 prompt tách bạch**: (1) phân tích tham số & miền dữ liệu, (2) sinh case domain partition, (3) sinh case state transition, (4) sinh case security, (5) sinh case schema validation. Chuỗi prompt này phải hiện diện trong AI Audit Report. |
| **P-02** | **Human review** | Nộp output thô của AI là **không chấp nhận được**. ⇒ Bắt buộc có bước Audit gán nhãn VALID/INVALID/INCOMPLETE + sửa lại. |
| **P-03** | **AI Audit Report** | Toàn bộ quá trình dùng AI phải được log đầy đủ. Khuyến khích xây Agent Skill tự động hoá việc này. Nếu **không** dùng AI thì vẫn phải khai báo rõ. |
| **P-04** | **Documentation** | Toàn bộ quá trình làm phải được ghi ở định dạng **text-based (Markdown)**. |
| **P-05** | **Quality over completion** | Chấm theo **số lượng + chất lượng** của: test case, AI audit, Postman collection + Newman report, bug report, thiết kế test-generator, và các link tham chiếu. |

---

## C. Yêu cầu bắt buộc theo từng API (mục 6 của đề)

Áp dụng **cho cả 3 API**, mỗi API là một pipeline 5 bước.

| Mã | Bước | Nội dung bắt buộc | Tiêu chí nghiệm thu |
| :--- | :--- | :--- | :--- |
| **R-01** | **Generate with AI** | Đưa API spec cho AI, dẫn dắt **từng bước**, sinh **≥ 35 test case / API**. Bắt buộc phủ 4 nhóm:<br>① **Domain partitions** trên **mọi** tham số (định dạng email, độ mạnh mật khẩu, price > 0, …)<br>② **State transitions** (FR-10: `pending → confirmed → shipping → delivered` + luật huỷ)<br>③ **Security** (SEC-01→SEC-07: SQL injection, IDOR, role escalation, …)<br>④ **Schema validation** (hình dạng response khớp **chính xác** spec) | Đếm được ≥ 35 case/API; mỗi case gắn nhãn thuộc nhóm nào; chuỗi prompt nhiều bước có trong AI Audit |
| **R-02** | **Audit (human review)** | Gán nhãn **VALID / INVALID / INCOMPLETE** cho **từng** case AI sinh, kèm **lý do**; sửa lại case sai/thiếu | Bảng audit đủ 3 cột (ID, nhãn, lý do) phủ 100% case AI sinh; case INVALID/INCOMPLETE có phiên bản đã sửa |
| **R-03** | **Extend** | Thêm **≥ 5 test case tự nghĩ** mà AI bỏ sót — **đặc biệt về security và state transition** — và **giải thích vì sao AI bỏ sót** (chất lượng prompt / giới hạn model / đặc thù API) | ≥ 5 case/API có cột "Vì sao AI bỏ sót" điền thật, không chung chung |
| **R-04** | **Execute** | Chạy bằng **Postman + Newman** (hoặc Karate/RestAssured). **Mọi request** phải mang header `X-Student-Id: 23127207` (ví dụ qua pre-request script). Xuất **Newman/HTML report** | File HTML report tồn tại; hostname trong report là `localhost`/`127.0.0.1`; có screenshot console chứng minh header |
| **R-05** | **Report bugs** | Báo cáo **mọi bug thật** tìm được (kể cả bug AI bỏ sót) ở **cả hai nơi**: báo cáo Markdown **và** trang **GitHub Issues**, **mỗi issue kèm screenshot** | Mỗi bug: 1 issue GitHub + 1 mục trong `bug-report.md` + screenshot + liên kết ngược "Found by Test Case: TC-xxx" |

### Yêu cầu kỹ thuật xuyên suốt toàn bộ test suite

| Mã | Yêu cầu | Tiêu chí nghiệm thu |
| :--- | :--- | :--- |
| **R-06** | **Khai thác càng nhiều tính năng Postman càng tốt** — ví dụ: workspaces, collections, variables, environments, data-driven runs (Collection Runner + data file), monitors, mock servers. **Phải liệt kê danh sách tính năng đã dùng trong báo cáo** | Có file `postman-features.md` liệt kê từng tính năng + nơi dùng + bằng chứng |
| **R-07** | **Tích hợp CI/CD** — đưa test case vào pipeline (ví dụ chạy Newman trong GitHub Actions), viết **CI/CD report ngắn** mô tả cấu hình pipeline và **2 lần chạy**, kèm **screenshot và link**. Cung cấp **2 commit mẫu**: một commit mà pipeline **pass toàn bộ**, một commit mà pipeline có **đúng 1 test case fail** | File workflow tồn tại; `cicd-report.md` có 2 commit SHA + 2 link Actions run + 2 screenshot |

---

## D. Agent Skill — mức Create G9.5 (mục 7 của đề)

| Mã | Yêu cầu | Ghi chú |
| :--- | :--- | :--- |
| **R-08** | Thiết kế **AI-driven API test generator** cho SUT: đầu vào là API specification → tự động sinh ra test case | Đây là hạng mục 10 điểm trong rubric |
| **R-09** | Cung cấp **sơ đồ tự vẽ** + **pseudocode** của thiết kế | ⚠️ *"Self-drawn"* = **sinh viên ra quyết định thiết kế**; dùng công cụ vẽ nào cũng được nhưng **bản thân sơ đồ không được do AI sinh ra**. → **Việc của HUMAN** |
| **R-10** | *(Khuyến khích)* Hiện thực hoá thành **reusable Agent Skill** + nộp **video demo (link YouTube)** cho thấy nó sinh test cho 1 API | Không bắt buộc nhưng là điểm cộng rõ rệt; repo đã có tiền lệ `.agents/skills/` từ HW trước |

---

## E. Phụ lục bắt buộc

| Mã | Yêu cầu | Chi tiết |
| :--- | :--- | :--- |
| **R-11** | **AI Audit Report** (mục 9) | Câu khai báo bắt buộc: *"I use AI tools for the following tasks,"* — và với **mỗi lần tương tác** phải ghi: ① tên công cụ AI ② ngày & giờ ③ prompt của bạn ④ output của AI.<br>(Nếu không dùng AI: *"I do not use any AI help in this exercise."*) |
| **R-12** | **AI Critique 200–300 từ** (mục 10) | Bắt buộc trả lời: AI **sai / thiên lệch / thiếu sót** ở chỗ nào? **Vì sao** nó không phát hiện được vấn đề đó? **Nguyên tắc** gì đã học được khi cộng tác với AI? → **HUMAN viết**, Codex chỉ chuẩn bị dữ liệu đầu vào |
| **R-13** | **Git commit log** (mục 12) | Tạo commit riêng cho **từng bước** của quy trình (generate, audit, extend, execute — cho **từng** API). Xuất log ra **file text** |

---

## F. Ràng buộc chống gian lận AI (mục 11) — TA kiểm tra trực tiếp

| Mã | Ràng buộc | Bằng chứng phải nộp |
| :--- | :--- | :--- |
| **R-14** | Header `X-Student-Id: 23127207` | **Screenshot console** từ pre-request script |
| **R-15** | Newman run output | Hostname phải khớp deployment của bạn (`localhost` / `127.0.0.1` được chấp nhận) |
| **R-16** | Sơ đồ AI test-generator | **Tự vẽ** — do bạn thiết kế, không phải AI sinh trực tiếp |

---

## G. Rubric chấm điểm (mục 15)

| # | Tiêu chí | Điểm |
| :-: | :--- | :-: |
| 1 | API 1 — pipeline đầy đủ (generate + audit + extend + execute + bugs) | 30 |
| 2 | API 2 — pipeline đầy đủ (tiêu chí như trên) | 30 |
| 3 | API 3 — pipeline đầy đủ (tiêu chí như trên) | 30 |
| 4 | Agent Skills (AI-driven test generator) | 10 |
| | **Tổng** | **100** |

**Đọc ngược từ rubric:** 90/100 điểm nằm ở việc làm **đủ và sâu 5 bước cho từng API**. Vì vậy kế hoạch thực thi được tổ chức theo trục *"mỗi API là một phase độc lập, hoàn thành trọn vẹn 5 bước rồi mới sang API kế"* — thay vì làm ngang theo loại công việc. Cách này còn giúp commit log phản ánh đúng quy trình mà mục 12 yêu cầu.

---

## H. Quy ước từ `Rule.pdf` — Quản lý test case trên GitHub

Đây là quy ước của môn học, áp dụng cho toàn bộ artifact của bài này.

### H.1 Mô hình tư duy

```
Requirement → Test Case → Test Run → Bug Issue → Pull Request → Retest
```

- **Test case** là *tài sản kiểm thử* (thiết kế). **Bug** là *kết quả phát hiện* khi execute test case.
- **Nguyên tắc bắt buộc — liên kết hai chiều:**
  - Trong Bug Issue phải ghi **`Found by Test Case: TC-xxx`**
  - Trong file Test Run phải ghi **`Result = Fail, Related Bug = #xx`**
  - Trong Pull Request phải ghi **`Fixes #xx`** hoặc `Related to #xx`
  - → *"Không tạo bug chung chung. Bug phải truy ngược được test case nào đã phát hiện."*

### H.2 Mô hình quản lý được khuyến nghị

Lớp học dùng **Hybrid**: **test case = file Markdown trong repo**, **bug = GitHub Issue**. Test case dưới dạng file có version history, review được bằng Pull Request, dễ chấm điểm.

### H.3 Cấu trúc thư mục chuẩn

```
tests/
├── test-cases/<module>/TC-<MODULE>-<NUM>.md   # thiết kế test case chính thức
├── test-runs/<sprint>-test-run.md             # kết quả thực thi theo đợt
└── test-summary/traceability-matrix.md        # báo cáo tổng hợp + truy vết
.github/ISSUE_TEMPLATE/                        # mẫu Bug Report / Test Run
```

> **Quy tắc:** không sửa test case trực tiếp trên `main` — tạo branch + Pull Request để review.

### H.4 Quy ước mã test case

`TC-[MODULE]-[NUMBER]` — ví dụ `TC-LOGIN-001`, `TC-CHECKOUT-010`.
**Không dùng:** `test1`, `check-login`, `case-a`, `login-success-test-v2-final`. Mã ổn định giúp traceability không đứt khi đổi tiêu đề.

> **Áp dụng cho HW06:** branch `HW6-Khoa` đã tồn tại `TC-LOGIN-001..013` (test case **giao diện** của FR-02 từ bài trước). Để tránh đụng mã, HW06 dùng module có tiền tố `API-`:
> `TC-API-LOGIN-###`, `TC-API-CHECKOUT-###`, `TC-API-ORDER-STATUS-###`.

### H.5 Template file test case chuẩn

Mỗi test case phải đủ: **Requirement ID** (đo coverage) · **Module / Test type / Technique** · **Preconditions** (tránh lỗi do môi trường/test data) · **Test data** (rõ hợp lệ/không hợp lệ) · **Test steps** · **Expected result** (căn cứ xác định pass/fail) · **Status / Related bugs**.

> *"Test case tốt không chỉ có steps, mà phải có điều kiện, dữ liệu và expected result rõ ràng."*

### H.6 Test Run

Bảng ghi nhận: `Test Case ID | Module | Tester | Result | Related Bug | Note`.
Trạng thái: **Pass / Fail / Blocked / Not Run**.

> Khi `Result = Fail` hoặc `Blocked` ⇒ **bắt buộc** có Related Bug hoặc lý do rõ ràng.

### H.7 Hệ thống label GitHub

| Nhóm | Label |
| :--- | :--- |
| Type | `type: test-case`, `type: test-run`, `type: bug`, `type: task` |
| Module | `module: login`, `module: register`, `module: cart`, `module: checkout`, **`module: api`** |
| Technique | `technique: EP`, `technique: BVA`, `technique: decision-table`, **`technique: state-transition`** |
| Result/Status | `result: pass`, `result: fail`, `result: blocked`, `status: ready for retest` |
| Priority/Severity | `severity: critical`, `severity: major`, `priority: P0`, `priority: P1` |

### H.8 Template Bug Report

Bug là Issue riêng, **không** chỉ ghi comment trong file test case. Cấu trúc:
`Title: [BUG][Module] Tóm tắt` → `## Found by Test Case` → `## Requirement liên quan` → `## Severity / Priority` → `## Environment` → `## Steps to reproduce` → `## Expected result` → `## Actual result` → `## Evidence`.

> *"Nếu thiếu Expected/Actual/Evidence, developer rất khó sửa và tester khó retest."*

Repo đã có sẵn `.github/ISSUE_TEMPLATE/bug_report.md` theo mẫu này (⚠️ file hiện bị lặp nội dung 3 lần — xem task `T-0.3`).

### H.9 Traceability Matrix

Bảng `Requirement | Test Case | Result | Bug Issue | Status` — chứng minh 3 việc: **Coverage** (requirement nào đã test), **Defect traceability** (bug thuộc requirement nào), **Regression** (test case nào cần chạy lại).

### H.10 Kết hợp Automated Test + GitHub Actions

- Test report lưu dưới dạng **artifact** (`actions/upload-artifact`) và liên kết ngược về bug.
- Khi test tự động fail: kiểm tra log → xác định test case fail → **chỉ tạo Bug Issue nếu lỗi do hệ thống, không phải lỗi test script** → trong bug ghi `Found by: GitHub Actions + workflow run + test case/script`.
- Sau khi fix, workflow phải pass trước khi close bug.

> *"Automation không thay thế test case; automation là cách execute một phần test case nhanh và lặp lại."*

### H.11 Checkpoint bắt buộc trước khi close bug

① PR đã merge ② Tester retest pass ③ Comment kết quả retest ④ Không phát sinh regression nghiêm trọng.

---

## I. Rủi ro & điểm dễ mất điểm

| Rủi ro | Hệ quả | Cách phòng |
| :--- | :--- | :--- |
| Dùng 1 prompt tổng để sinh hết test case | Vi phạm P-01, mất điểm nặng cả 3 API | Chuỗi ≥ 4 prompt/API, log đủ trong AI Audit |
| Ghi AI Audit bù vào cuối buổi | Thiếu prompt/output/timestamp ⇒ vi phạm R-11 | Append entry **ngay sau mỗi lần gọi AI** |
| Audit gán nhãn qua loa ("VALID" hàng loạt) | Vi phạm P-02 + R-02, đây là phần chấm nặng | Đối chiếu từng case với `02-sut-defect-catalog.md` |
| Nhờ AI vẽ sơ đồ test-generator | Vi phạm R-16 — TA kiểm tra trực tiếp | Sinh viên tự vẽ, Codex không đụng vào |
| Pipeline CI luôn đỏ (vì test assert đúng spec mà SUT có bug) | Không có commit "all passing" theo R-07 | Tách 2 chế độ chạy — xem `03-execution-plan.md` Phase 6 |
| Gom hết công việc vào 1–2 commit | Vi phạm R-13 | Bảng commit message theo từng task trong plan |
| Quên header `X-Student-Id` ở một vài request | Vi phạm R-14 | Đặt pre-request script ở **cấp collection**, không đặt lẻ từng request |
| Chỉ báo bug trong Markdown, quên GitHub Issues (hoặc ngược lại) | Vi phạm R-05 | Checklist `04` bắt buộc tick cả 2 cột |
