# HW03 — GUI & Usability · Báo cáo chính

| | |
|---|---|
| **Sinh viên** | Đặng Trường Nguyên |
| **MSSV** | 23127438 |
| **Bài tập** | HW03-AI — GUI & Usability (cá nhân) |
| **SUT** | EShop — `frontend-web` (khách) tại `http://localhost:5173`, backend `http://localhost:3000` |
| **Repo làm bài** | https://github.com/trngnneee/eshop-sut |
| **Ngày thực hiện** | 21/07/2026 – 30/07/2026 |
| **Máy** | MacBook Pro (Apple Silicon), macOS 15.5 (24F74) |
| **Công cụ AI** | Claude (Claude Code) — khai báo đầy đủ trong AI Audit Report ở Phụ lục |
| **Tự đánh giá** | **100 / 100** — bảng ở [§0.3](#03-bảng-tự-đánh-giá-assessment-template), căn cứ từng tiêu chí ở [Phần VI](#phần-vi--căn-cứ-tự-đánh-giá) |

Đây là __main report hợp nhất__ của cả ba task: Task 1 (GUI checklist), Task 2 (usability evaluation), Task 3 (cross-browser/cross-platform), giữ nguyên số đo và kết luận của từng lần chạy. Ba báo cáo rời vẫn nằm trong repo làm bản gốc truy vết:
[`gui_and_usability_testing/report.md`](gui_and_usability_testing/report.md) · [`usability_testing/report.md`](usability_testing/report.md) · [`cross_platform_testing/report.md`](cross_platform_testing/report.md).

---

## §0. Tóm tắt, tự đánh giá và video

### 0.1. Test summary report

| Chỉ số | Giá trị |
|---|---|
| Số màn hình kiểm thử (Task 1) | **8** màn của `frontend-web` (khách) |
| Số flow end-to-end (Task 2) | **1** flow U-01 (Đăng ký → tìm → chi tiết → giỏ ≥ 300.000₫ → checkout `SAVE10` → lịch sử đơn) |
| Số checklist item thiết kế | **66** (AI sinh 65 + em tự thêm 4, dedup 3 cặp) — vượt mức tối thiểu 40 |
| Phủ interface aspect | 4/4 — IA-01: 17 · IA-02: 15 · IA-03: 15 · IA-04: 19 |
| Số lượt thực thi | **66/66** thủ công (Task 1) + **198** lượt tự động (66 × 3 platform, Task 3) |
| Kết quả Task 1 (chạy tay, Chrome) | **9 Passed / 57 Failed** |
| Kết quả sau hiệu chỉnh Task 3 | **7 Passed / 59 Failed** (Chromium) — 4 item bị lật, xem [§III.5](#iii5-phát-hiện-c--3-item-task-1-chấm-pass-nhưng-thực-đo-là-fail) |
| Số platform (Task 3) | **3** — Chromium/Blink · Firefox/Gecko · WebKit, headed trên máy thật |
| Số participant (Task 2) | **7** người thật, 7 session moderated, 21–24/07/2026 |
| Điểm SUS | Mean **53.2** · Median 55.0 · Min–Max 30.0–75.0 |
| Số bug trên GitHub Issues | **55** — Task 1: #194–#241 (48 bug) · Task 3: [#242–#248](https://github.com/trngnneee/eshop-sut/issues?q=is%3Aissue+label%3Across-platform) (7 bug) |
| Bug từ Task 2 | 7 finding trùng gốc issue Task 1 → bổ sung bằng chứng usability + label `usability`; **2 issue được nâng severity** (#204, #240) |
| Ảnh bằng chứng | 57 ảnh Task 1 · 179 ảnh viewport + 18 ảnh cửa sổ thật Task 3 · mỗi GitHub issue đều nhúng ảnh |
| Agent Skill đã build | **1** — `gui-checklist-testing` (8 giai đoạn, kèm scripts + references + example) |
| Video demo | xem [§0.2](#02-video-demo) |

### 0.2. Video demo

| # | Nội dung video | Link |
|---|---|---|
| V1 | __Demo Agent Skill `gui-checklist-testing`__ — chạy end-to-end trên một màn hình hoàn chỉnh (kiểm kê UI → sinh item theo từng aspect → gap analysis → thực thi → bug report → GitHub Issue) | https://drive.google.com/drive/folders/12vRLu6w3gfYg_bl7yHUeYgNLes2X-oAV?usp=drive_link |
| V2 | Ghi màn hình 7 session usability (P1–P7, có consent) | https://drive.google.com/drive/folders/1b3Z9MYaBErgubEglcKposVbQ5U7kVU7q?usp=drive_link |

> **Chỗ điền link:** thay chuỗi `[ĐIỀN LINK YOUTUBE TẠI ĐÂY]` ở dòng V1 bằng URL YouTube (unlisted vẫn hợp lệ). Nếu có thêm video demo cho flow khác, thêm dòng V3/V4 theo đúng định dạng trên.
>
> <!-- YOUTUBE_SKILL_DEMO: paste link here -->

### 0.3. Bảng tự đánh giá (Assessment Template)

| No. | Criteria | Grade | **Self-Assessed Grade** |
|---|---|---|---|
| 1 | Task 1 — GUI Checklist (design + execution + bug report) | 30 | **30** |
| 2 | Task 2 — Usability Evaluation (task scenario + 7 sessions + analysis) | 40 | **40** |
| 3 | Task 3 — Cross-Browser / Cross-Platform (≥ 3 platforms) | 20 | **20** |
| 4 | Agent Skills | 10 | **10** |
| | **Total** | **100** | **100** |

Tên file submission tương ứng: `23127438_HW03_AI_GUIUsability_100.zip`.
Căn cứ cho từng con số — đối chiếu từng yêu cầu của đề với bằng chứng cụ thể — ở [Phần VI](#phần-vi--căn-cứ-tự-đánh-giá).

### 0.4. Bản đồ tài liệu (evidence index)

| Hạng mục đề yêu cầu | Vị trí |
|---|---|
| Main report (bản này) | [`tests/report.md`](report.md) + bản PDF cùng tên |
| Checklist 66 item, có cột Kết quả + Ghi chú lý do Fail | [`gui_and_usability_testing/checklist-final.md`](gui_and_usability_testing/checklist-final.md) |
| 66 test case chi tiết + test summary | [`gui_and_usability_testing/test-cases/`](gui_and_usability_testing/test-cases/) · [`test_case_summary.md`](gui_and_usability_testing/test-cases/test_case_summary.md) |
| Bug report Task 1 (48 bug) + ánh xạ item ↔ bug ↔ issue | [`gui_and_usability_testing/bug-report.md`](gui_and_usability_testing/bug-report.md) · [`issue-map.tsv`](gui_and_usability_testing/issue-map.tsv) |
| Ảnh bug Task 1 (chỉ item Failed) | [`gui_and_usability_testing/test-cases/screenshots/`](gui_and_usability_testing/test-cases/screenshots/) |
| Task scenario + instrument (SUS, probe, session kit) | [`usability_testing/task-scenario-draft.md`](usability_testing/task-scenario-draft.md) · [`usability_testing/template/`](usability_testing/template/) |
| Bảng 7 participant (đã che 4 số giữa) | [`usability_testing/participants.md`](usability_testing/participants.md) |
| Ghi chú quan sát, phiếu SUS, script chấm | [`usability_testing/result/`](usability_testing/result/) |
| Findings xếp theo severity | [`usability_testing/findings.md`](usability_testing/findings.md) |
| Ma trận 3 platform + bảng khác biệt | [`cross_platform_testing/results-matrix.md`](cross_platform_testing/results-matrix.md) · [`divergences.md`](cross_platform_testing/divergences.md) · [`platform-matrix.md`](cross_platform_testing/platform-matrix.md) |
| Ảnh cross-platform (overlay email SV) | [`cross_platform_testing/results/`](cross_platform_testing/results/) — `P*/screenshots/` và `P*/platform-proof/` |
| 7 bug cross-platform | [`cross_platform_testing/issues/`](cross_platform_testing/issues/) → GitHub #242–#248 |
| Agent Skill | [`.claude/skills/gui-checklist-testing/`](../.claude/skills/gui-checklist-testing/) |
| AI Audit Report / Disclosure / Privacy (mỗi task một bộ) | `*/ai_declaration/` — xem [Phần VII](#phần-vii--phụ-lục) |
| AI Critique | [Phần V](#phần-v--ai-critique) |
| Git commit log | `git-commit-log.txt` (xuất từ repo — mỗi bước quy trình một commit) |

---

# Phần I — Task 1: GUI Checklist

Thiết kế và thực thi một GUI checklist dựa trên yêu cầu giao diện của SUT, trên frontend-web dành cho khách (`localhost:5173`).

**Kết quả một dòng:** 66 checklist item phủ 4 interface aspect · thực thi thủ công 100% · 9 Passed / 57 Failed · 48 bug đã lên GitHub Issues (#194–#241).

## I.1. Phạm vi & cơ sở

**Phạm vi:** 8 màn hình của frontend-web (khách), chọn theo một luồng end-to-end tự nhiên chứ không chọn rời rạc, để checklist đo được cả các quy tắc *xuyên màn* (điều hướng, nhất quán ngôn ngữ/màu, trạng thái giỏ):

| # | Màn hình | FR chức năng | IA khai thác mạnh |
|---|---|---|---|
| 1 | Đăng ký | FR-01 | IA-02 |
| 2 | Đăng nhập (+ khoá tài khoản) | FR-02 | IA-02, IA-04 |
| 3 | Quên mật khẩu (2 bước) | FR-03 | IA-02, IA-04 |
| 4 | Trang chủ / danh sách + tìm kiếm | FR-05 | IA-01, IA-03, IA-04 |
| 5 | Chi tiết sản phẩm | FR-06 | IA-01, IA-04 |
| 6 | Giỏ hàng | FR-07 | IA-03, IA-04 |
| 7 | Thanh toán (+ mã giảm giá) | FR-08, FR-09 | IA-02, IA-04 |
| 8 | Lịch sử đơn hàng | FR-11 | IA-01, IA-03 |

**Cơ sở (test basis):** checklist không dựa trên heuristic UI chung mà neo vào **mục 8 "Yêu cầu Giao diện" trong README của SUT** — FR-21 (tiêu chuẩn chung), FR-22 (form), FR-23 (điều hướng), FR-24 (feedback/state). Bốn FR này khớp gần 1–1 với IA-01→IA-04 của đề, nên mỗi item đều truy vết được về một yêu cầu thành văn thay vì về ý kiến cá nhân. Cột `Traced to` trong từng test case ghi rõ FR tương ứng.

## I.2. Quy trình — 6 bước, AI làm gì và người làm gì

Đề cấm kiểu prompt "sinh cả checklist trong một phát", nên quy trình được tách thành các bước ăn output của nhau, mỗi bước là một dòng trong AI Audit Report ([`gui_and_usability_testing/ai_declaration/[AI-02]`](gui_and_usability_testing/ai_declaration/)):

| Bước | Việc | Ai làm | Sản phẩm |
|---|---|---|---|
| 1 | Kiểm kê phần tử giao diện từng màn (đọc component tree, kể cả nhánh render có điều kiện) | AI (Prompt #1) · em soát lại trên app đang chạy | [`ui-inventory/*.md`](gui_and_usability_testing/ui-inventory/) (9 file, có cột `Source file:line`) |
| 2 | Sinh item theo __từng__ interface aspect, input là inventory + FR-21→24 nguyên văn | AI (Prompt #2a→#2d, 4 lần) | [`checklist-draft/ia-0*.md`](gui_and_usability_testing/checklist-draft/) — 65 item |
| 3 | Rà khoảng trống theo 8 chiều, rồi __tự kiểm chứng từng candidate trên SUT__ | AI chẩn đoán (Prompt #3) · em kiểm chứng và quyết | [`checklist-draft/gap-analysis.md`](gui_and_usability_testing/checklist-draft/gap-analysis.md) — 4 item bổ sung |
| 4 | Hợp nhất, dedup, đánh số lại | AI · em duyệt | [`checklist-final.md`](gui_and_usability_testing/checklist-final.md) — 66 item |
| 5 | __Thực thi thủ công__ 66 item trên trình duyệt | Em, 100% — AI không tham gia | 66 file [`test-cases/`](gui_and_usability_testing/test-cases/), 57 screenshot |
| 6 | Viết bug report + đăng GitHub Issues | AI nháp (Prompt #6) · em quyết severity | [`bug-report.md`](gui_and_usability_testing/bug-report.md), 48 issue |

Bước 5 không dùng AI: mọi ô "Actual result / Observed" trong 66 test case là quan sát trực tiếp của em ngày 25/07/2026 trên Chrome.

## I.3. Bốn item em tự thêm — và vì sao AI bỏ sót

Đây là phần đề yêu cầu giải thích riêng cho từng item bổ sung. Chi tiết đầy đủ ở [`gap-analysis.md`](gui_and_usability_testing/checklist-draft/gap-analysis.md) Phần B; tóm tắt nguyên nhân:

| ID | Item | Nguyên nhân AI bỏ sót | Vì sao nguyên nhân đó |
|---|---|---|---|
| GUI-GAP-01 | Giỏ hàng phải còn sau khi F5 | **Đặc thù SUT** | Giỏ còn hay mất sau reload là quyết định cài đặt riêng (React state vs localStorage), không suy ra được từ FR-21→24 hay heuristic UI tĩnh. Checklist gốc chỉ chạm tới back button (IA03-10/11), không có item nào về reload/persistence |
| GUI-GAP-02 | Thêm cùng 1 SP nhiều lần phải gộp dòng | **Cách em chia prompt** | Lỗi chỉ lộ khi *kết hợp* 2 thao tác. Em yêu cầu AI sinh item theo từng màn hình tĩnh, nên IA04-01/02 chỉ soi feedback của **một** lần bấm — cấu trúc prompt của em tạo ra đúng điểm mù này |
| GUI-GAP-03 | `<html lang="vi">` | **Giới hạn mô hình** | Chính AI đề xuất chiều Accessibility (gap-analysis Phần A, chiều 1) nhưng chỉ liệt kê được focus ring + contrast, bỏ qua khai báo ngôn ngữ — dù đó là WCAG 3.1.1 cơ bản và bằng chứng nằm ngay `index.html:2` |
| GUI-GAP-04 | Mọi label gắn input qua `htmlFor`/`id` | **Giới hạn mô hình** | Cùng gốc với GAP-03: chiều Accessibility không rà tới ngữ nghĩa form (WCAG 1.3.1/4.1.2), dù lỗi lặp trên cả 4 form và `grep htmlFor` toàn codebase ra 0 kết quả |

Bốn item này không phải bổ sung cho đủ số: cả 4 đều **Failed** khi thực thi, và sinh ra BUG-21, BUG-22 cùng 2 bug khác.

Ba chiều còn **absent** sau khi rà (dark mode, RTL, print/export) được **chủ động loại khỏi scope kèm lý do**: app không có class `dark:` nào, thuần tiếng Việt và spec không yêu cầu RTL, còn print/export không thuộc luồng mua hàng.

## I.4. Hợp nhất & dedup

65 item AI + 4 item thủ công = 69, dedup 3 cặp near-duplicate còn **66**. Log dedup ở cuối `checklist-final.md` (mục "Dedup log") để truy vết được item nào gộp từ đâu — đáng chú ý là cả 3 cặp trùng đều sinh ra từ việc **sinh item theo từng aspect độc lập**: cùng một quy tắc FR bị hai aspect phát biểu lại theo hai cách (ví dụ tab order được cả IA-01 và IA-02 sinh ra).

| Aspect | Số item | Trong đó tự thêm | Passed | Failed |
|---|---|---|---|---|
| IA-01 General UI | 17 | 1 (GAP-03) | 3 | 14 |
| IA-02 Forms | 15 | 1 (GAP-04) | 2 | 13 |
| IA-03 Navigation | 15 | 0 | 3 | 12 |
| IA-04 Feedback/State | 19 | 2 (GAP-01, 02) | 1 | 18 |
| **Tổng** | **66** | **4** | **9** | **57** |

## I.5. Thực thi

- **Người thực thi:** Đặng Trường Nguyên · **Ngày:** 25/07/2026 · **Môi trường:** Frontend Web `localhost:5173` + Backend `localhost:3000`, Chrome, kiểm thử thủ công
- **Kết quả:** 66/66 item được thực thi — **9 Passed / 57 Failed**, không item nào bỏ trống hay để "chưa chạy"
- **Ghi nhận:** `checklist-final.md` có cột `Kết quả` và cột `Ghi chú (lý do Fail)`; mỗi item Failed đều ghi lý do là **giá trị quan sát được** (chuỗi thật, computed style thật), không phải diễn giải
- **Screenshot:** 57 ảnh trong `test-cases/screenshots/<ID>.png` — **chỉ cho item Failed**. 9 item Passed cố ý không có ảnh, và mỗi file test case Passed ghi rõ `Screenshot: (không có — test Passed)` để không ai đọc là thiếu bằng chứng
- **Chi tiết từng item:** 66 file trong `test-cases/IA-0*/`, mỗi file có Preconditions / Test data / Test steps / Expected / Actual (Observed) / Status + link bug
- __Hiệu chỉnh sau Task 3:__ bảng 9/57 ở trên là hồ sơ gốc của lần chạy tay này và được giữ nguyên. Task 3 chạy lại 66 item bằng script trên 3 engine đã lật __4 item__ (`GUI-IA01-08`, `GUI-IA01-15`, `GUI-IA04-12` Pass→Fail; `GUI-IA02-14` Fail→Pass trên Chromium) — bảng đối chiếu ở [`test_case_summary.md`](gui_and_usability_testing/test-cases/test_case_summary.md), chú thích ngay trong `checklist-final.md` cột Ghi chú, và mục "Retest — Task 3" trong 4 file test case. Số đo mới nhất: __7 Passed / 59 Failed__ (Chromium)

Tỉ lệ Failed 86% cao bất thường với một app thật, nhưng EShop là SUT dựng riêng để dạy kiểm thử — lỗi được gieo có chủ ý. Con số này nói về SUT, không nói về độ khắt khe của checklist.

## I.6. Bug

57 item Failed được **gộp theo nguyên nhân gốc** thành **48 bug** (nhiều item cùng một nguyên nhân thì chỉ mở một issue — ví dụ BUG-19 phủ IA04-08/09/16, cùng một chỗ thiếu loading/error state).

| Mức độ | Số lượng | Ví dụ |
|---|---|---|
| Blocker | 2 | BUG-01 XSS qua `dangerouslySetInnerHTML` ([#194](https://github.com/trngnneee/eshop-sut/issues/194)) · BUG-02 tổng tiền là input sửa được rồi gửi thẳng lên API ([#195](https://github.com/trngnneee/eshop-sut/issues/195)) |
| Major | 20 | BUG-11 regex SĐT từ chối số VN bắt đầu bằng 0 ([#204](https://github.com/trngnneee/eshop-sut/issues/204)) · BUG-17 click "Thêm vào giỏ" lần đầu bị bỏ qua ([#210](https://github.com/trngnneee/eshop-sut/issues/210)) |
| Minor | 26 | BUG-41 `<html lang="en">` ([#241](https://github.com/trngnneee/eshop-sut/issues/241)) |

- Toàn bộ 48 bug có mặt ở **cả** `bug-report.md` **và** GitHub Issues (#194–#241), mỗi issue kèm screenshot nhúng
- Ánh xạ item ↔ bug ↔ issue: [`issue-map.tsv`](gui_and_usability_testing/issue-map.tsv)
- Severity do em quyết, không theo đề xuất của AI

## I.7. Hạn chế

1. **Một trình duyệt, một máy.** Toàn bộ Task 1 chạy trên Chrome/macOS. Đây chính là lý do Task 3 tồn tại — và Task 3 đã cho thấy hạn chế này là thật: 3 item bị Task 1 kết luận sai vì chỉ xem trên một engine (`GUI-IA01-08`, `GUI-IA01-15`, `GUI-IA04-12` — xem [Phần III](#phần-iii--task-3-cross-browser--cross-platform)).
2. **Catalog seed chỉ 5 sản phẩm.** Các item về danh sách/phân trang (ví dụ IA03-15) Passed trong điều kiện dữ liệu nhỏ; kết luận không suy rộng được cho catalog lớn.
3. **Thực thi bằng mắt.** Các item về sub-pixel/breakpoint được phán đoán bằng quan sát, không bằng đo — Task 3 sau đó đo bằng script và lật lại `GUI-IA01-15`.
4. **Không phủ Web Admin và Mobile app.** Scope cố ý giới hạn ở frontend-web khách để đủ sâu trong một luồng, đánh đổi bằng độ rộng.

---

# Phần II — Task 2: Usability Evaluation

Đánh giá usability dạng moderated, mẫu nhỏ (7 người tham gia, think-aloud), trên một flow end-to-end của frontend-web (`localhost:5173`).

**Flow được chọn (U-01):** Đăng ký tài khoản mới → tìm sản phẩm → xem chi tiết → thêm vào giỏ (tổng ≥ 300.000₫) → thanh toán áp mã `SAVE10` → xác nhận đơn trong Lịch sử đơn hàng.
FR phủ: FR-01, FR-05, FR-06, FR-07, FR-08, FR-09, FR-11.

## II.1. Mục tiêu nghiên cứu

### II.1.1. Cách xây dựng

Dùng AI đề xuất 6 mục tiêu ứng viên, với input là flow U-01 và các bug Task 1 đã tìm thấy trên chính các màn thuộc flow (BUG-11, 12, 16, 17, 20, 33, 34, 35, 36, 38, 42, 44, 46, 47 — xem [`bug-report.md`](gui_and_usability_testing/bug-report.md)). Sau đó em tự chọn 3 mục tiêu chính thức và tự viết lý do chọn/loại dưới đây.

### II.1.2. Sáu mục tiêu ứng viên (tóm tắt)

| ID | Câu hỏi nghiên cứu (rút gọn) | Bằng chứng ở bước | Gốc từ Task 1 | Chọn? |
|---|---|---|---|---|
| O1 | Người dùng có tự hiểu và tự sửa được lỗi validation của form Đăng ký không, hay phải thử mò/bỏ cuộc? | Đăng ký | BUG-11, 12, 33, 34, 46 | ✅ |
| O2 | Người dùng có nhận ra thao tác thêm giỏ đã thành công chưa? Họ tự xác nhận bằng cách nào (bấm lặp → trùng hàng, hay mở giỏ kiểm tra)? | Chi tiết sản phẩm → Giỏ | BUG-16, 17, 47 | ✅ |
| O3 | Người dùng có tự tìm ra chỗ nhập mã SAVE10 và xác định được giảm giá đã trừ vào tổng chưa? | Checkout | BUG-44 | ❌ |
| O4 | Sau thanh toán, người dùng có tin đơn đã ghi nhận không, dựa vào dấu hiệu nào? | Sau checkout → Lịch sử đơn | BUG-20 | ❌ |
| O5 | Người dùng có bị lạc khi di chuyển giữa các màn của flow không? | Toàn flow (điểm chuyển màn) | BUG-35, 36, 38 | ❌ |
| O6 | Người dùng có dùng tìm kiếm để đạt mục tiêu mua hàng (giỏ ≥ 300k) không, và phản ứng thế nào khi tìm kiếm trả 0 kết quả không có empty state? | Tìm kiếm / Danh sách | BUG-42, 28 | ✅ |

### II.1.3. Mục tiêu chính thức: O1, O2, O6 — lý do chọn

**Chọn O1 — vì Đăng ký là cổng vào bắt buộc của flow và là nơi Task 1 tìm thấy cụm lỗi dày nhất có khả năng chặn người dùng thật.** Regex số điện thoại từ chối số VN hợp lệ bắt đầu bằng 0 (BUG-11) và quy tắc mật khẩu mâu thuẫn với hint (BUG-12) nghĩa là gần như mọi participant sẽ va vào validation ít nhất một lần — session nào cũng chắc chắn sinh dữ liệu cho mục tiêu này. Quan trọng hơn, câu hỏi "họ có tự phục hồi được không" trả lời trực tiếp trục **error recovery** mà đề bắt buộc probe questions phải phủ, nên dữ liệu quan sát và dữ liệu phỏng vấn sẽ đối chiếu được với nhau.

**Chọn O2 — vì đây là vấn đề chỉ usability testing mới đo được, checklist Task 1 không đo nổi.** Task 1 xác nhận *hệ thống* không có feedback khi thêm giỏ (BUG-16) và nuốt click đầu tiên (BUG-17), nhưng không trả lời được *người dùng thật* phản ứng ra sao: có bấm lặp dẫn tới trùng hàng (BUG-47) không, có mất niềm tin không, có tự mở giỏ kiểm tra không. Hành vi này quan sát được trực tiếp và đếm được (số lần bấm, hành động xác minh) trong khuôn khổ 15–25 phút, rất hợp cỡ mẫu n=7 — tín hiệu định tính rõ mà không cần thống kê.

**Chọn O6 — vì tìm kiếm là bước duy nhất trong flow mà hành vi người dùng hoàn toàn tự do, nên cho dữ liệu tự nhiên nhất.** Scenario goal-oriented (không chỉ dẫn từng bước) khiến mỗi participant tự chọn từ khoá, tự quyết duyệt hay tìm — cách họ xoay xở khi kết quả trống trơn không một dòng giải thích (BUG-42) là phép thử trực tiếp cho trục **clarity**. Ngoài ra O6 bao luôn cơ chế ngân sách của scenario (gom giỏ đủ 300k để mã SAVE10 hợp lệ), giúp phát hiện sớm nếu scenario thiết kế ngưỡng tiền chưa hợp lý — điều cần biết ngay từ pilot.

**Tính phủ:** O6 (vào flow) → O1 (cổng đăng ký) → O2 (giữa flow) — ba mục tiêu nằm ở ba đoạn khác nhau, không dồn vào một màn, mỗi session đều đi qua cả ba nên không mục tiêu nào bị đói dữ liệu.

### II.1.4. Lý do loại O3, O4, O5

- **O4 (niềm tin đơn đã ghi nhận):** bản chất trùng với trục **trust** mà probe questions bắt buộc phải hỏi — nghĩa là dữ liệu cho O4 *vẫn được thu* ở phần phỏng vấn cuối session mà không cần dành suất mục tiêu chính. Chọn O4 làm mục tiêu riêng sẽ đo trùng hai lần cùng một thứ.
- **O3 (coupon):** cùng họ "hệ thống có xác nhận hành động không" với O2 — giữ cả hai thì hai mục tiêu chồng lấn. Bước nhập SAVE10 vẫn nằm trong template ghi chú quan sát (cột riêng cho bước Checkout), nên friction ở coupon vẫn được ghi nhận như dữ liệu thứ cấp và vẫn có thể thành finding/bug ở GĐ8.
- **O5 (wayfinding):** hiện tượng phân tán khắp flow, khó quy bằng chứng về một bước cụ thể trong session 15–25 phút; với n=7, tín hiệu dễ bị nhiễu bởi khác biệt kinh nghiệm web giữa từng người. Các biểu hiện lạc đường nếu xảy ra vẫn lọt vào cột "Lỗi & do dự quan sát được" của template ghi chú.

## II.2. Task scenario

Kịch bản goal-oriented (mua quà sinh nhật là tai nghe chống ồn, ngân sách 6–7 triệu, có mã `SAVE10` "nhận qua email", tự xác nhận đơn đã ghi nhận trước khi rời đi) — toàn văn + bảng mapping scenario → 6 bước flow trong [`task-scenario-draft.md`](usability_testing/task-scenario-draft.md). Ba quyết định thiết kế chính:

- **Không chứa bất kỳ chỉ dẫn giao diện nào** (đã kiểm tra danh sách từ cấm: nút, menu, trang, click...) — participant chỉ nhận goal và động cơ.
- **Ngân sách neo vào dữ liệu thật:** catalog seed chỉ có 5 sản phẩm, rẻ nhất 4.000.000₫, nên kiểu ngân sách "dưới 500k" như ví dụ trong đề là bất khả thi; 6–7 triệu trỏ tự nhiên tới AirPods Pro 2 (6.000.000₫), đồng thời ngưỡng 300k của `SAVE10` luôn tự thoả.
- **"Hoàn thành" định nghĩa theo góc nhìn người dùng** (yên tâm đơn đã được ghi nhận), không theo bước kỹ thuật — để quan sát họ tự tìm bằng chứng ở đâu.

## II.3. Công cụ đo (instruments)

- __Thang đo: SUS__ (bản dịch tiếng Việt trong [`template/sus-form-vi.md`](usability_testing/template/), kèm bảng đối chiếu Anh–Việt để kiểm chứng độ trung thành và tính phân cực câu lẻ/chẵn). Em chọn SUS thay vì UEQ-S vì: 10 câu đủ ngắn cho session 15–25 phút, có quy trình chấm chuẩn tái lập được (0–100) và benchmark tham chiếu rộng rãi (68 = trung bình), phù hợp để báo cáo một con số tổng quát với n nhỏ.
- __Probe questions:__ 7 câu mở trong [`template/probe-questions.md`](usability_testing/template/), phủ đủ 4 trục đề yêu cầu (clarity / error recovery / speed / trust) và bám O1/O2/O6; mỗi câu có bản gốc trung lập + câu đào sâu chỉ dùng khi chính em đã quan sát thấy tình huống trong session.
- __Session kit:__ [`template/session-kit.md`](usability_testing/template/) — kịch bản mở đầu đọc nguyên văn (test sản phẩm không test bạn, demo think-aloud, xin consent ghi màn hình + âm thanh), template ghi chú A4 theo 6 bước flow, cheat-sheet 5 câu trả lời trung lập và quy tắc can thiệp duy nhất (kẹt hẳn > 2 phút, gợi ý nhỏ nhất có thể, ghi lại nguyên văn).

## II.4. Người tham gia

**Target user profile:** người 18–30 từng mua sắm online, không làm trong ngành kiểm thử phần mềm và không học lớp HW03 này.

7 người tham gia thật (bảng đầy đủ kèm liên hệ đã che 4 số giữa: [`participants.md`](usability_testing/participants.md)), tuyển thủ công không qua AI theo đúng §11 của đề; tất cả đã được báo trước rằng TA có thể gọi điện xác minh. Mỗi người dùng tài khoản tự đăng ký trong chính session (bước đầu của flow), bảo đảm điều kiện `max_uses_per_user` của mã giảm giá không bị vướng giữa các session.

Video ghi màn hình 7 session: https://drive.google.com/drive/folders/1b3Z9MYaBErgubEglcKposVbQ5U7kVU7q?usp=drive_link

## II.5. Chuẩn bị & pilot

Trước session đầu, em tự đi hết flow (dry-run) để xác nhận flow không gãy, ước thời lượng session và soát kịch bản/bảng mapping; DB được reset về seed trước mỗi session và toàn bộ 7 session dùng cùng một bộ tài liệu.

**Pilot được chạy gộp vào session P1** (Đặng Đăng Khoa, 21/07/2026 10:00–10:19): buổi đó vừa là pilot vừa là session chính thức đầu tiên — em dùng nó để kiểm tra kịch bản có goal-oriented đủ rõ không, bộ probe questions có chạy được trong thời lượng dự kiến không, và phiếu SUS có gây thắc mắc gì không, trước khi tiếp tục P2–P7. Kết quả kiểm tra: **kịch bản và bộ tài liệu không cần chỉnh sửa** — participant hiểu goal ngay, không hỏi lại nghĩa, thời lượng 19 phút nằm trong khung dự kiến 15–25 phút. Vì vậy cả 7 session dùng đúng một bản kịch bản và so sánh được với nhau, và dữ liệu P1 được giữ lại trong phân tích.

**Hạn chế cần khai rõ:** pilot gộp vào session chính thức yếu hơn một pilot riêng ở đúng một điểm — nếu buổi đó phát hiện kịch bản có lỗi hệ thống thì em chỉ sửa được **từ P2 trở đi**, còn chính P1 đã bị ảnh hưởng và sẽ phải loại. Ở đây rủi ro không hiện thực hoá (không có gì phải sửa), nhưng đó là may mắn về kết quả chứ không phải bảo đảm về quy trình; ghi nhận lại ở [§II.10](#ii10-hạn-chế).

## II.6. Tiến hành 7 session

7 session diễn ra 21–24/07/2026, mỗi session 15–25 phút, theo đúng trình tự kit: đọc script mở đầu → consent → giao kịch bản → quan sát trung lập (think-aloud) → phiếu SUS → probe questions. Ghi chú được gõ lại trong vòng 15 phút sau mỗi session.

- Bằng chứng: ghi chú quan sát [`result/session-P1..P7.md`](usability_testing/result/), phiếu SUS `result/sus-P1..P7.md`, tổng hợp [`result/README.md`](usability_testing/result/README.md).
- **Can thiệp:** đúng 2 lần, đều theo quy tắc kẹt-hẳn->2-phút và đều ở bước Đăng ký (P3, P6 — gợi ý tối thiểu "thử bỏ số 0 ở đầu số điện thoại", ghi nguyên văn trong note). Ngoài ra chỉ dùng câu trung lập trong cheat-sheet.
- 7/7 hoàn thành flow (5/7 hoàn toàn độc lập).

## II.7. Kết quả SUS

Chấm bằng script tái lập được ([`result/sus_score.py`](usability_testing/result/) trên [`result/sus_responses.csv`](usability_testing/result/sus_responses.csv) — công thức chuẩn: câu lẻ điểm−1, câu chẵn 5−điểm, tổng ×2.5), kết quả khớp 7/7 với bản chấm tay trên phiếu:

| P1 | P2 | P3 | P4 | P5 | P6 | P7 | **Mean** | Median | Min–Max |
|---|---|---|---|---|---|---|---|---|---|
| 67.5 | 57.5 | 30.0 | 52.5 | 55.0 | 35.0 | 75.0 | **53.2** | 55.0 | 30.0–75.0 |

Mean 53.2 nằm dưới benchmark trung bình 68, band "OK" theo thang tính từ Bangor et al. Với n=7 đây là tín hiệu định tính, không phải kết luận thống kê; điểm đáng chú ý là 2 điểm thấp nhất (P3: 30, P6: 35) chính là 2 ca cần can thiệp ở bước Đăng ký — thang đo và quan sát hành vi kể cùng một câu chuyện.

## II.8. Findings & mức độ nghiêm trọng

Phân tích đầy đủ (9 theme UF-01→09 + 3 phát hiện hệ thống SYS-01→03, kèm căn cứ từng dòng và tần suất x/7) trong [`findings.md`](usability_testing/findings.md). Tóm tắt xếp theo severity:

| ID | Finding | x/7 | Severity | Bug/Design |
|---|---|---|---|---|
| UF-01 | Validation SĐT từ chối số VN hợp lệ — 2 ca kẹt hẳn phải trợ giúp | 7/7 | **Blocker** | Bug ([#204](https://github.com/trngnneee/eshop-sut/issues/204)) |
| UF-02 | Thêm giỏ không feedback + click đầu bị nuốt | 7/7 | Major | Bug ([#209](https://github.com/trngnneee/eshop-sut/issues/209), [#210](https://github.com/trngnneee/eshop-sut/issues/210)) |
| UF-03 | Bấm lặp tạo dòng trùng → P6 suýt thanh toán gấp đôi (10,8 triệu) | 2/7 | Major | Bug ([#240](https://github.com/trngnneee/eshop-sut/issues/240)) |
| UF-04 | Quy tắc mật khẩu mâu thuẫn hint | 7/7 | Major | Bug ([#205](https://github.com/trngnneee/eshop-sut/issues/205)) |
| UF-05 | Tìm kiếm 0 kết quả = trang trống không giải thích | 4/7 | Major | Bug ([#235](https://github.com/trngnneee/eshop-sut/issues/235)) |
| UF-06 | Giỏ không reset sau checkout → nghi ngờ giao dịch | 7/7 | Major | Bug ([#213](https://github.com/trngnneee/eshop-sut/issues/213)) |
| UF-07 | Thông báo lỗi form không actionable | 4/7 | Major | Design |
| UF-08 | Feedback bằng `alert()`, xác nhận giảm giá mờ nhạt | 2/7 | Minor | Design |
| UF-09 | Ô nhập coupon khó thấy | 1/7 | Cosmetic | Design |

**Trả lời mục tiêu nghiên cứu** (chi tiết trong `findings.md` §3): O1 — người dùng tự phục hồi được nhưng bằng thử-sai và kinh nghiệm nền, hệ thống gần như không đóng góp (chỉ P1 rút được hướng sửa từ thông báo lỗi; 2/7 cần trợ giúp). O2 — 0/7 nhận biết "đã thêm giỏ" qua hệ thống; hành vi bù đắp là tự mở giỏ (6/7); người không tự xác minh (P6) chính là người suýt mất tiền. O6 — tìm kiếm chỉ "hoạt động" với người biết luật ngầm từ-khoá-ngắn; 4/7 gõ tự nhiên rơi vào trang trống và không ai hiểu đúng là "0 kết quả".

## II.9. Báo cáo bug

Cả 7 bug đều trùng gốc với issue đã mở ở Task 1, nên thay vì mở issue trùng, em bổ sung bằng chứng usability (tần suất x/7, trích think-aloud, hậu quả) thành comment vào từng issue và gắn label `usability`: [#204](https://github.com/trngnneee/eshop-sut/issues/204), [#205](https://github.com/trngnneee/eshop-sut/issues/205), [#209](https://github.com/trngnneee/eshop-sut/issues/209), [#210](https://github.com/trngnneee/eshop-sut/issues/210), [#213](https://github.com/trngnneee/eshop-sut/issues/213), [#235](https://github.com/trngnneee/eshop-sut/issues/235), [#240](https://github.com/trngnneee/eshop-sut/issues/240).

Dựa trên dữ liệu người dùng thật, 2 issue được nâng severity (giữ nguyên đánh giá gốc Task 1 trong body để truy vết): **#204 Major → Blocker** (chặn hoàn thành task với 2/7 người) và **#240 Minor → Major** (rủi ro thanh toán gấp đôi). Comment công khai chỉ dùng mã P1–P7, không chứa thông tin cá nhân.

## II.10. Hạn chế

1. **Pilot gộp vào session chính thức, không phải pilot riêng** ([§II.5](#ii5-chuẩn-bị--pilot)) — nếu kịch bản có lỗi hệ thống thì chỉ sửa được từ P2, còn P1 đã nhiễm và phải loại; thực tế không cần sửa gì, nhưng quy trình chuẩn của đề là một buổi pilot riêng bỏ đi được.
2. **Mẫu đồng nhất, và đồng nhất theo hướng bất lợi** (n=7) — cả 7 người đều là sinh viên cùng một khoa CNTT (`@clc.fitus.edu.vn`, cùng khoá 23). Họ **không** làm kiểm thử và **không** học lớp HW03 này, nên vẫn đúng điều kiện bắt buộc của đề; nhưng đề *ưu tiên* người ngoài ngành IT, và ở điểm ưu tiên đó mẫu này không đạt. Ảnh hưởng cụ thể lên kết luận: nhóm này quen quy ước web hơn người dùng phổ thông, nên khả năng tự phục hồi khỏi lỗi (trục O1) gần như chắc chắn bị **đo cao hơn** thực tế — P2 đoán ra "regex không nhận số 0 đầu" chỉ sau 1 lần thất bại là hành vi của người có nền IT, không phải của người mua hàng bình thường. Các con số x/7 vì vậy nên đọc như chặn trên, không phải trung bình.
3. **Catalog chỉ 5 sản phẩm** — làm hành vi "duyệt thay vì tìm" trở nên hợp lý (P4), nên kết luận O6 về tìm kiếm sẽ cần kiểm chứng lại với catalog lớn.
4. Kết quả SUS chịu ảnh hưởng mạnh của cụm lỗi Đăng ký nằm ngay đầu session (hiệu ứng ấn tượng đầu).

---

# Phần III — Task 3: Cross-Browser / Cross-Platform

**Ngày thực thi:** 28/07/2026 · **Máy:** MacBook Pro (Apple Silicon), macOS 15.5 (24F74)

## III.1. Đã làm gì

Đề yêu cầu *"Perform Task 1 across at least three (3) platforms"*. Task 1 là checklist **66 item** (IA-01 17 · IA-02 15 · IA-03 15 · IA-04 19). Task 3 vì thế là **198 lượt thực thi** (66 × 3), tất cả đều được chạy thật, không lấy mẫu, không suy diễn từ platform khác.

| | Giá trị |
|---|---|
| Số platform | 3 (Chromium/Blink · Firefox/Gecko · WebKit) — chi tiết version/OS/device ở [platform-matrix.md](cross_platform_testing/platform-matrix.md) |
| Số item mỗi platform | 66/66 (không item nào bị bỏ) |
| Tổng lượt thực thi | **198** |
| Kết quả | P1 **7 Pass / 59 Fail** · P2 **6 Pass / 60 Fail** · P3 **6 Pass / 60 Fail** — 0 Blocked, 0 lỗi harness |
| Ảnh bằng chứng | **179 ảnh viewport** (mọi item Fail, mọi platform) + **18 ảnh cửa sổ thật** (6 màn × 3 platform), mọi ảnh overlay MSSV + họ tên + email SV |
| Khác biệt giữa platform | **1** item đổi hẳn Pass/Fail · **28** item cùng kết quả nhưng giá trị hiển thị khác nhau · 6 item khác nhau chỉ vì dữ liệu chạy (đã tách riêng, không tính là phát hiện) |
| Sai lệch so với kết luận Task 1 | **4** item (3 item Task 1 chấm Pass thực ra Fail; 1 item Task 1 chấm Fail nhưng Pass trên Chromium) |

> **Đọc nhãn platform cho đúng.** "Chrome / Firefox / Safari" trong mọi bảng và trong overlay ảnh là **vai trò theo đề**, không phải tên bundle đã chạy. Cả ba là browser build do Playwright quản lý, chạy headed trên máy thật: P1 là *Google Chrome for Testing* (Blink), P2 là Firefox bundle `Nightly.app` (Gecko), P3 là **WebKit build của Playwright — không phải `Safari.app`** (cùng engine `AppleWebKit/605.1.15` · `Version/26.5`, tức cùng lớp render/JS/CSS/validation với Safari, nhưng vỏ ứng dụng khác). Vì vậy trong 18 ảnh cửa sổ thật, menu bar macOS hiện tên **"Playwright"** chứ không phải "Safari" — đó là hệ quả đã biết và đã khai, không phải ảnh sai platform. Khai báo đầy đủ: [platform-matrix.md §4](cross_platform_testing/platform-matrix.md).

Cách chạy lại toàn bộ:

```bash
cd eshop-sut/backend      && node server.js      # :3000 (drop + seed DB mỗi lần start)
cd eshop-sut/frontend-web && npm run dev         # :5173
cd eshop-sut/tests/cross_platform_testing/harness
./run-all-platforms.sh                 # 66 item × 3 platform, reseed DB trước mỗi platform
node scripts/build-matrix.js           # sinh results-matrix.md + divergences.md
node scripts/capture-platform-proof.js # 6 ảnh cửa sổ thật mỗi platform
node scripts/verify-evidence.js        # cổng kiểm tra bằng chứng (exit 1 nếu thiếu)
```

## III.2. Vì sao tự động hoá, và tự động hoá không làm mất tính "thực thi thật"

198 lượt kiểm tay trong 10 giờ là không khả thi; tệ hơn, kiểm tay lần 2–3 trên cùng một checklist mình vừa viết gần như chắc chắn sẽ *nhìn thấy điều mình mong đợi*. Harness giải quyết đúng hai điểm đó:

- Mỗi check **đọc trạng thái thật của app đang chạy** (DOM, computed style, `input.validationMessage`, `validity`, hình học phần tử, dialog native, console) rồi mới kết luận. Contract cấm hard-code kết quả Task 1 (`harness/checks/README.md`, rule 1) — và đúng 4 item đã cho kết quả khác Task 1, bằng chứng là cấm đó có hiệu lực.
- Mỗi check ghi lại **giá trị thô** vào `metrics`. Pass/Fail giống nhau giữa 3 engine không có nghĩa là UI giống nhau — 28/29 khác biệt tìm được thuộc đúng loại này và chỉ lộ ra khi diff giá trị thô.
- Mỗi check chạy trong **browser context mới** (giỏ hàng rỗng, `localStorage` rỗng) đúng như phần Preconditions của test case Task 1; và **DB được seed lại trước mỗi platform** để 3 platform xuất phát từ cùng một trạng thái.

## III.3. Phát hiện A — item ĐỔI kết quả giữa các platform (nghiêm trọng nhất)

### XP-01 · `GUI-IA02-14` — Thông báo "bắt buộc nhập" phụ thuộc trình duyệt, không phụ thuộc app

Cùng một build, cùng một DOM, ba kết quả khác nhau khi submit form với field `required` để trống:

| Platform | `navigator.language` | Chuỗi engine hiện ra | Kết quả |
|---|---|---|---|
| P1 Chromium 151 | `vi-VN` | "Vui lòng điền vào trường này." | ✅ Pass |
| P2 Firefox 153 | `en-US` | "Please fill out this field." | ❌ Fail |
| P3 WebKit 26.5 | `vi-VN` | "Fill out this field" | ❌ Fail |

Điểm đắt giá: **WebKit báo locale là `vi-VN` mà vẫn hiện tiếng Anh** — nghĩa là không thể "sửa bằng cách đặt locale". SUT dựa hoàn toàn vào bong bóng validate mặc định của HTML5 `required`, nên yêu cầu "message tiếng Việt nhất quán" bị quyết định bởi *trình duyệt của người dùng*, không phải bởi app. Task 1 chấm Fail (Chrome bản đó hiện tiếng Anh); bản Chromium ở đây hiện tiếng Việt nên Pass — chính sự lật kết quả này là lý do đề bắt phải test nhiều platform.

Bằng chứng: [P1](cross_platform_testing/results/P1-chromium-macos/screenshots/) (Pass, không có ảnh vì Pass) · [P2](cross_platform_testing/results/P2-firefox-macos/screenshots/GUI-IA02-14.png) · [P3](cross_platform_testing/results/P3-webkit-macos/screenshots/GUI-IA02-14.png) · chi tiết `metrics`: [divergences.md §A](cross_platform_testing/divergences.md).

## III.4. Phát hiện B — cùng kết quả, hiển thị/hành vi khác nhau (28 item)

Bốn nhóm nguyên nhân, xếp theo mức ảnh hưởng tới người dùng thật:

### XP-02 · Tiền tệ đổi dấu phân cách theo engine — ảnh hưởng 13 item, mọi màn có giá

`toLocaleString()` gọi **không tham số** (Home.jsx:88, ProductDetail.jsx:50, Cart.jsx:57–60, Checkout.jsx) nên kết quả phụ thuộc locale mà engine tự resolve:

| | Trang chủ | Chi tiết SP | Giỏ hàng | Coupon (SAVE10) |
|---|---|---|---|---|
| Chromium (`vi`) | `30.000.000 VND` | `30.000.000 ₫` | `30.000.000 ₫` | `Tiết kiệm: -270.000.000 ₫` |
| **Firefox (`en-US`)** | **`30,000,000 VND`** | **`30,000,000 ₫`** | **`30,000,000 ₫`** | **`Tiết kiệm: -270,000,000 ₫`** |
| WebKit (`vi-VN`) | `30.000.000 VND` | `30.000.000 ₫` | `30.000.000 ₫` | `Tiết kiệm: -270.000.000 ₫` |

Với người mua Việt Nam, `30,000,000` đọc là "ba mươi phẩy..." — sai nghiêm trọng về ngữ nghĩa tiền tệ, và nó chỉ xuất hiện trên Firefox. Ảnh cửa sổ thật cho thấy rõ: [Firefox](cross_platform_testing/results/P2-firefox-macos/platform-proof/01-home.png) vs [Chromium](cross_platform_testing/results/P1-chromium-macos/platform-proof/01-home.png).

13 item có giá trị `metrics` khác nhau đúng vì nguyên nhân này (đếm bằng script trên `results/raw/*.json`): `GUI-IA01-06/07/08`, `GUI-IA02-09/10/11`, `GUI-IA03-04/08/09/10`, `GUI-IA04-12/15`, `GUI-GAP-02`.

### XP-03 · WebKit loại `<button>`/`<a>` khỏi Tab order → 3 nút submit không thể tới bằng bàn phím

`GUI-IA01-13` metric `unreachableControls`:

| Platform | `nativeButtonsInTabOrder` | Control không tới được bằng Tab |
|---|---|---|
| Chromium | `true` | — |
| Firefox | `true` | — |
| **WebKit** | `false` | `/register` "Đăng Ký", `/forgot-password` "Lấy mã OTP", `/checkout` "Xác Nhận Thanh Toán" |

Đây là **hành vi hợp lệ của WebKit/Safari trên macOS** (mặc định "Tab chỉ di chuyển giữa các field"), nhưng hệ quả là người dùng bàn phím trên Safari không tới được nút submit của 3 form. Trên `/login` nút vẫn tới được — vì có `tabIndex={1}`, chính là lỗi khiến item này Fail ở mọi engine (focus vào nút TRƯỚC input).

### XP-04 · `input[type=number]` nhận chữ: hai chế độ hỏng khác nhau

`GUI-IA02-09` — gõ `abc` vào ô Số lượng:

| Platform | `value` sau khi gõ | `validity.badInput` | `validationMessage` | Hệ quả cho app |
|---|---|---|---|---|
| Chromium | `""` | `false` | `""` | `parseInt("")` → **NaN** vào giỏ, app không hề biết |
| **Firefox** | `""` | **`true`** | **"Please enter a number."** | engine chặn, nhưng bằng tiếng Anh |
| WebKit | `""` | `false` | `""` | như Chromium |

Cùng lúc, gõ `-1` được nhận trên **cả 3 engine** (không có `min`) → giỏ hàng hiện `-1` và `-30.000.000 ₫`. Đây là lỗi SUT; engine chỉ khác nhau ở chỗ có tố giác hay không.

### XP-05 · Chẩn đoán lỗi API: Firefox che mất status code

`GUI-IA04-09/16` — chặn `/api/products/1` trả 500:

| Platform | Console |
|---|---|
| Chromium | 4 lỗi, có `"Failed to load resource: … status of 500 (Internal Server Error)"` + `AxiosError` kèm stack |
| WebKit | 4 lỗi, đúng nội dung như Chromium nhưng không kèm stack |
| **Firefox** | 2 lỗi, chỉ `"Error"` / `"Lỗi lấy đơn hàng: Error"` — **không có status code, không có dòng resource** |

Không phải bug của SUT, nhưng là rủi ro vận hành: UI đã không hiện gì (item Fail ở mọi engine), mà trên Firefox console cũng không cho dev biết request nào chết.

## III.5. Phát hiện C — 3 item Task 1 chấm Pass nhưng thực đo là Fail

Task 3 không chỉ so sánh platform; chạy lại bằng máy đã lộ 3 chỗ Task 1 kết luận sai (tất cả đều Fail đồng nhất trên **cả 3** platform, nên không phải hiện tượng platform):

| ID | Task 1 | Thực đo | Vì sao Task 1 bỏ sót |
|---|---|---|---|
| `GUI-IA01-08` | Passed | Fail | Task 1 chỉ thử với dữ liệu seed hợp lệ. Khi stub `/api/products/1` trả `price:"ba mươi triệu"`, màn hình render **`NaN ₫`** — đúng điều item yêu cầu không được xảy ra. |
| `GUI-IA01-15` | Passed | Fail | Ở đúng 768px, breakpoint `md:` của Tailwind (`min-width:768px`) đã kích hoạt → grid **3 cột** trong khi item yêu cầu 2. Mắt thường ở 768px rất dễ chấm Pass. |
| `GUI-IA04-12` | Passed | Fail | Item đòi "cả 2 nhánh đúng **và số tiền tính đúng**". Hai nhánh feedback có thật, nhưng coupon `SAVE10` (10%) trên đơn 30.000.000 ₫ hiện **`Tiết kiệm: -270.000.000 ₫`** và **`Thành tiền: 300.000.000 ₫`** (đúng phải là 3.000.000 và 27.000.000) — backend tính `discount = total × (1 − 10)`. Task 1 chỉ kiểm sự hiện diện của 2 nhánh. |

`GUI-IA04-12` là bug **chức năng** nặng nhất tìm được trong Task 3 — không phải bug cross-platform, và được báo cáo đúng bản chất đó (XP-07).

## III.6. Bug report

7 bug đều có bản Markdown trong [`cross_platform_testing/issues/`](cross_platform_testing/issues/) **và** đã mở trên GitHub Issues (label `cross-platform`, kèm ảnh):

| ID | Tiêu đề | Loại | Severity | Platform bị ảnh hưởng | Markdown | GitHub |
|---|---|---|---|---|---|---|
| XP-01 | Message "bắt buộc nhập" là chuỗi của engine, không phải của app | SUT bug — biểu hiện phụ thuộc platform | Major | Firefox, WebKit (Chromium ẩn lỗi) | [XP-01.md](cross_platform_testing/issues/XP-01.md) | [#242](https://github.com/trngnneee/eshop-sut/issues/242) |
| XP-02 | `toLocaleString()` không locale → tiền tệ VN sai dấu phân cách | SUT bug — biểu hiện phụ thuộc platform | Major | Firefox | [XP-02.md](cross_platform_testing/issues/XP-02.md) | [#243](https://github.com/trngnneee/eshop-sut/issues/243) |
| XP-03 | 3 nút submit không tới được bằng Tab trên WebKit/Safari | Hành vi engine + khuyết accessibility của SUT | Major | WebKit/Safari | [XP-03.md](cross_platform_testing/issues/XP-03.md) | [#244](https://github.com/trngnneee/eshop-sut/issues/244) |
| XP-04 | Ô Số lượng nhận `-1`/chữ; chế độ hỏng khác nhau theo engine | SUT bug | Major | cả 3 (biểu hiện khác nhau) | [XP-04.md](cross_platform_testing/issues/XP-04.md) | [#245](https://github.com/trngnneee/eshop-sut/issues/245) |
| XP-05 | Firefox không log status code khi API 500 (UI cũng không báo) | Rủi ro chẩn đoán | Minor | Firefox | [XP-05.md](cross_platform_testing/issues/XP-05.md) | [#246](https://github.com/trngnneee/eshop-sut/issues/246) |
| XP-06 | Tràn ngang 24px ở 375px trên Gecko (Home search row) | SUT bug — chỉ lộ trên 1 engine | Minor | Firefox (WebKit 3px) | [XP-06.md](cross_platform_testing/issues/XP-06.md) | [#247](https://github.com/trngnneee/eshop-sut/issues/247) |
| XP-07 | Coupon `SAVE10` tính ngược: tiết kiệm −270 triệu, thành tiền 300 triệu | SUT bug chức năng (không liên quan platform) | **Blocker** | cả 3 | [XP-07.md](cross_platform_testing/issues/XP-07.md) | [#248](https://github.com/trngnneee/eshop-sut/issues/248) |

## III.7. Giới hạn của lần đo này

1. **Không dùng BrowserStack/LambdaTest** (không còn trial). Thay bằng 3 engine thật chạy headed trên máy thật — đề cho phép phương án thay thế nếu ảnh thể hiện rõ browser/OS/device + URL localhost, và mọi ảnh ở đây đều có. Chi tiết: [platform-matrix.md §4](cross_platform_testing/platform-matrix.md).
2. **P3 là WebKit build của Playwright, không phải `Safari.app`.** Cùng engine (`AppleWebKit/605.1.15`, `Version/26.5`) nên hành vi render/JS/CSS/validation là của Safari, nhưng menu bar hiện "Playwright". Muốn khoá tuyệt đối tiêu chí "Safari": bật `safaridriver` (xem [platform-matrix.md §5](cross_platform_testing/platform-matrix.md)).
3. **P1 là "Google Chrome for Testing"** (cùng Blink, cùng dòng version), không phải Chrome bản người dùng.
4. **Không có platform mobile trong bộ bằng chứng.** Hai profile emulation (iPhone 14, Pixel 7) từng có trong kế hoạch nhưng đã bị **xoá khỏi `harness/lib/platforms.js`**, không phải chỉ ẩn đi: `PLATFORMS` hiện đúng 3 entry (P1/P2/P3) nên `--platforms all` cũng chỉ trả về 3 — không có cờ nào chạy lại được mobile. Lý do xoá: emulation không phải máy thật nên không thoả §6, và giữ lại chỉ làm bộ bằng chứng loãng. Nếu cần platform thứ 4 hợp lệ thì phải chạy `frontend-mobile` bằng Expo Go trên điện thoại thật (đề cho phép, và đó là cách duy nhất còn lại).
5. **`GUI-IA03-15` chỉ quan sát được với 5 sản phẩm seed** — metric `observationLimit` ghi rõ điều này; Pass ở đây không có nghĩa "đã kiểm chứng với danh sách dài".
6. **Kết quả automation phản ánh đúng những gì đo được, không thay thế phán đoán thị giác.** Ví dụ `GUI-IA01-14`: computed `margin-right:-100px` chỉ dành 86px layout cho nút rộng 186px (Fail), nhưng nút vẫn nằm trong container và click được ở 375×812 — cả hai sự thật đều ghi trong `evidence`/`metrics` để người đọc tự đánh giá.

---

# Phần IV — Agent Skill

**Skill đã build:** [`.claude/skills/gui-checklist-testing/`](../.claude/skills/gui-checklist-testing/) — đóng gói toàn bộ quy trình Task 1 thành một skill tái dùng được cho màn hình/flow khác.

| Thành phần | File | Nội dung |
|---|---|---|
| Định nghĩa skill | `SKILL.md` | 6 nguyên tắc bất biến · bảng input phải hỏi trước khi chạy · layout output · **quy trình 8 giai đoạn GĐ0→GĐ8** (kèm commit message cho từng giai đoạn) · cổng kiểm tra trước commit · mục "cạm bẫy đã gặp thật" |
| Prompt library | `references/prompts.md` | Prompt #1 → #6 dán được ngay, mỗi giai đoạn một prompt riêng (không có prompt "sinh cả checklist") |
| Template | `references/templates.md` | Khung UI inventory, checklist, test case, bug report, AI Audit Report |
| Cổng kiểm tra | `scripts/verify_deliverables.py` | Kiểm bảng markdown lệch cột, tổng item > 40, mọi item có status, screenshot ↔ item Failed là **song ánh**, item Passed không có ảnh, test case 1:1 item, mọi item Failed có bug phủ, mọi item `GUI-GAP` có lý do AI bỏ sót, AI Critique nằm trong 200–300 từ, (`--gh`) mọi issue tồn tại + có ảnh |
| Tự động hoá bằng chứng | `scripts/upload_screenshots.py` | Upload ảnh lên host rồi nhúng URL vào issue body để ảnh render được trên GitHub |
| Ví dụ chạy thật | `examples/eshop-hw03-task1.md` | Toàn bộ một lần chạy hoàn chỉnh: 66 item · 57 Failed · 48 bug · issues #194–#241 |

**Hai điểm thiết kế đáng nói:**

1. **Skill mã hoá các ranh giới, không chỉ mã hoá các bước.** Ba quy tắc cứng: AI không được quyết Pass/Fail (GĐ5 là người 100%), AI ở GĐ3 chỉ được *chẩn đoán* 8 chiều chứ **cấm thêm dòng checklist mới**, và severity do người chốt. Đây chính là các ranh giới mà đề đòi ("AI as a disciplined assistant rather than a black box").
2. **Skill tự khai phạm vi của mình.** `SKILL.md` ghi rõ ba thứ **ngoài phạm vi** vì là việc chung của cả bài: git commit log, main report hợp nhất + PDF, và `README.md` self-assessment — nên không sinh ra tài liệu chồng chéo khi tái dùng.

**Video demo:** xem [§0.2](#02-video-demo) — dòng V1 là chỗ điền link YouTube demo skill chạy end-to-end trên một màn hình hoàn chỉnh.

---

# Phần V — AI Critique

Đề yêu cầu 200–300 từ. Vì bài này có ba technique khác nhau và AI hỏng theo ba kiểu khác nhau, em viết **một critique cho mỗi task**, mỗi bản nằm trong khung 200–300 từ.

## V.1. Critique — Task 1 (GUI Checklist)

Cả 8 artifact AI sinh ra đều bị em xếp INCOMPLETE, không cái nào VALID — nhưng điều đáng học không phải "AI sai nhiều", mà là **AI sai ở đâu**.

AI mạnh nhất khi được đưa một cái khung cụ thể: với inventory có `file:line` và FR-21→24 nguyên văn làm input, nó sinh 65 item bám sát app thật, không có item chung chung kiểu "giao diện phải đẹp". Nó cũng tự đề xuất được chiều Accessibility mà em chưa nghĩ tới.

Nhưng chính chiều đó là chỗ nó hỏng: sau khi tự nêu Accessibility, nó chỉ liệt kê focus ring và contrast, bỏ qua `<html lang>` và label association — hai lỗi WCAG cơ bản, một cái nằm ở dòng 2 của `index.html`, một cái tìm ra bằng `grep htmlFor` với 0 kết quả. Nêu được tên phạm trù không có nghĩa là rà hết phạm trù đó; AI dừng ở những ví dụ điển hình nhất của khái niệm.

Hai điểm mù còn lại thì do **em**, không do nó: em yêu cầu sinh item theo từng màn hình tĩnh và theo từng aspect độc lập, nên nó không thể thấy lỗi cần *kết hợp hai thao tác* (giỏ mất khi F5, thêm 2 lần ra 2 dòng), và nó phát biểu trùng cùng một quy tắc FR ở hai aspect — đúng 3 cặp phải dedup.

Nguyên tắc em rút ra: cách chia bài toán quyết định AI sẽ mù ở đâu, và cái khung đó là việc của người. Vì vậy sau mỗi lần AI trả kết quả, câu hỏi cần đặt không phải "danh sách này có đúng không" mà "**cách chia này làm mất loại lỗi nào**" — rồi tự đi thăm đúng các đường nối đó trên app.

## V.2. Critique — Task 2 (Usability Evaluation)

Em dùng AI ở hai đầu của nghiên cứu — thiết kế công cụ trước session và tổng hợp sau session — và không dùng trong lúc thu dữ liệu: tuyển người, điều phối, ghi chú quan sát và phiếu SUS đều làm thủ công theo đúng ranh giới của đề. Nhìn lại 9 artifact đã audit (AI Audit Report của Task 2), chỉ 1 được chấp nhận nguyên trạng, 8 phải sửa mới dùng được: "AI làm ra được" không đồng nghĩa "dùng được ngay".

AI mạnh nhất ở hai chỗ. Một là dựng công cụ có ràng buộc kiểm chứng được: scenario không chứa từ chỉ dẫn giao diện, bản dịch SUS giữ đúng phân cực câu lẻ/chẵn, session kit chuẩn hoá cả 7 session — nhưng em vẫn phải soát từng ràng buộc (đối chiếu từng câu SUS với bản gốc Brooke, rà từ cấm) chứ không tin theo lời AI tự nhận. Hai là code tất định: script chấm SUS khớp 7/7 với bản chấm tay.

Điểm yếu đáng học nhất nằm ở bước tổng hợp: 3 con số thống kê trong bản nháp findings lệch khỏi ghi chú gốc, và cả 3 đều lệch về hướng làm câu chuyện gọn hơn — kể cả khẳng định "không ai rút được cách sửa từ thông báo lỗi" trong khi chính dữ liệu đó có P1 là ngoại lệ. Đây không phải lỗi ngẫu nhiên mà là thiên kiến kể-chuyện-mạch-lạc, và chỉ bị bắt nhờ đếm lại từng dòng theo `session-P*.md`. Em cũng không nghe theo AI ở một quyết định triage: giữ #235 ở Minor thay vì nâng Major như AI đề xuất, vì cả 4/7 người gặp đều tự thoát được bằng đổi từ khoá.

Quy tắc em rút ra: để AI nháp cấu trúc và văn bản, nhưng mọi con số phải truy vết được về dữ liệu thô và phải tự suy ra lại trước khi chấp nhận; các quyết định đánh giá (severity, khai hạn chế của việc gộp pilot vào session chính thức) luôn thuộc về người làm nghiên cứu.

## V.3. Critique — Task 3 (Cross-Platform)

Ở Task 3, AI sai và thiếu ở đúng một chỗ: lớp bằng chứng, chứ không phải lớp đo. Thiết kế đầu tiên của nó chụp ảnh bằng `page.screenshot()` — mà API này không bao giờ chụp được browser chrome, nên yêu cầu "ảnh phải hiện URL localhost" của đề là không thể thoả; AI không nhận ra vì nó tối ưu cho việc chụp được ảnh, không đối chiếu lại điều kiện chấm điểm. Thanh overlay đầu tiên còn che mất header của SUT — đúng phần mà 15 item IA-03 cần soi. Quy trình chạy đầu tiên thì không seed lại database giữa các platform, tức sẽ làm nhiễu chính phép so sánh mà nó vừa dựng: metric `orderRows` trôi 7/3/5/9/11 theo thứ tự chạy vì các check đặt đơn thật. Lần chụp cửa sổ đầu tiên còn chụp nhầm cửa sổ ứng dụng khác, vì không kiểm tra app nào đang ở tiền cảnh. Bốn lỗi này cùng một bản chất: AI rất giỏi thực hiện phép đo nhưng không tự hỏi "bằng chứng này có chứng minh được điều cần chứng minh không".

Ngược lại, chỗ AI mạnh vượt em là kỷ luật ghi lại giá trị thô của từng lần quan sát. Chính việc bắt mỗi check trả về `metrics` đã biến cảm giác "ba trình duyệt trông như nhau" thành 29 khác biệt đo được, và lôi ra bug coupon tính ngược mà Task 1 em chấm Passed.

Nguyên tắc em rút ra: để AI dựng dụng cụ đo và đọc số, nhưng người phải định nghĩa thế nào là bằng chứng hợp lệ, và luôn hỏi "nếu kết quả này sai thì nó sẽ trông như thế nào" trước khi tin.

---

# Phần VI — Căn cứ tự đánh giá

Tự đánh giá: **100/100**. Dưới đây là đối chiếu từng yêu cầu thành văn của đề với bằng chứng cụ thể, cùng phần khai rõ những chỗ em biết là yếu (đã ghi trong các mục Hạn chế) và lý do em vẫn cho là đạt trọn tiêu chí.

## VI.1. Tiêu chí 1 — Task 1: GUI Checklist · **30/30**

| Yêu cầu của đề | Đạt? | Bằng chứng |
|---|---|---|
| Checklist **> 40 item** | ✅ **66** item | [`checklist-final.md`](gui_and_usability_testing/checklist-final.md) |
| Phủ **cả 4** interface aspect | ✅ 17/15/15/19 | bảng [§I.4](#i4-hợp-nhất--dedup) |
| Dùng AI sinh bản đầu, **không** dùng một prompt gộp | ✅ 4 prompt riêng cho 4 aspect, mỗi giai đoạn một lần gọi | AI Audit Report (Prompt #1→#6) |
| Tự review và **thêm item AI bỏ sót** | ✅ 4 item `GUI-GAP-01..04`, cả 4 đều Failed khi chạy | [`gap-analysis.md`](gui_and_usability_testing/checklist-draft/gap-analysis.md) Phần B |
| **Giải thích vì sao AI bỏ sót từng item** (prompt / giới hạn mô hình / đặc thù UI) | ✅ đủ 4 dòng, mỗi dòng có bằng chứng (`index.html:2`, `grep htmlFor` = 0 kết quả…) | [§I.3](#i3-bốn-item-em-tự-thêm--và-vì-sao-ai-bỏ-sót) |
| Có xét các chiều AI hay bỏ (accessibility, RTL, dark mode) | ✅ accessibility → 2 item thật; RTL/dark mode/print **loại có lý do**, không im lặng bỏ | [§I.3](#i3-bốn-item-em-tự-thêm--và-vì-sao-ai-bỏ-sót) |
| Thực thi checklist, đánh Passed/Failed | ✅ 66/66, không item nào trống | [`test-cases/`](gui_and_usability_testing/test-cases/) |
| **Cột Notes ghi lý do Fail** cho từng item Failed | ✅ cột `Ghi chú (lý do Fail)` + ô Actual (Observed) trong 57 test case | `checklist-final.md` |
| Screenshot **chỉ cho item Failed** | ✅ 57 ảnh = 57 item Failed (song ánh, có script kiểm); item Passed ghi rõ "không có ảnh — test Passed" | [`screenshots/`](gui_and_usability_testing/test-cases/screenshots/) |
| Bug báo **cả trong Markdown và trên GitHub Issues**, mỗi issue có ảnh | ✅ 48 bug ↔ issue #194–#241, mỗi issue nhúng ảnh | [`bug-report.md`](gui_and_usability_testing/bug-report.md) · [`issue-map.tsv`](gui_and_usability_testing/issue-map.tsv) |
| Vượt mức tối thiểu / chất lượng | ✅ 66 item neo vào FR-21→24 thành văn (không phải heuristic chung), 66 test case đầy đủ 6 mục, dedup log truy vết được, và **tự hiệu chỉnh 4 item sai sau Task 3** thay vì che đi | [§I.5](#i5-thực-thi) |

## VI.2. Tiêu chí 2 — Task 2: Usability Evaluation · **40/40**

| Yêu cầu của đề | Đạt? | Bằng chứng |
|---|---|---|
| Chọn **1 flow end-to-end** | ✅ U-01, 6 bước, phủ 7 FR | [§II](#phần-ii--task-2-usability-evaluation) |
| **Objectives** nêu rõ muốn học điều gì | ✅ 6 mục tiêu ứng viên → chọn O1/O2/O6, có lý do chọn **và** lý do loại từng cái | [§II.1](#ii1-mục-tiêu-nghiên-cứu) |
| Task scenario **goal-oriented**, không hướng dẫn từng bước | ✅ kịch bản mua quà, đã rà danh sách từ cấm (nút/menu/trang/click) | [`task-scenario-draft.md`](usability_testing/task-scenario-draft.md) |
| Thang đo chuẩn (SUS/UEQ-S) + **lý do chọn** | ✅ SUS, dịch tiếng Việt có bảng đối chiếu, kèm lập luận chọn SUS thay UEQ-S | [§II.3](#ii3-công-cụ-đo-instruments) |
| Probe questions phủ **clarity / error recovery / speed / trust** | ✅ 7 câu, đủ 4 trục, mỗi câu có bản trung lập + câu đào sâu có điều kiện | [`template/probe-questions.md`](usability_testing/template/) |
| **7 participant thật**, liên hệ xác minh được, che 4 số giữa | ✅ 7 người, tuyển thủ công, đã báo trước việc TA có thể gọi | [`participants.md`](usability_testing/participants.md) |
| Participant ngoài lớp HW03, không phải tester | ✅ cả 7 đều thoả điều kiện bắt buộc; điểm *ưu tiên* "ngoài ngành IT" **không đạt và đã khai rõ ảnh hưởng lên kết luận** | [§II.10](#ii10-hạn-chế) mục 2 |
| **Pilot session** | ✅ chạy gộp vào P1, có kết luận kiểm tra (không cần sửa gì) và **tự khai điểm yếu của việc gộp** | [§II.5](#ii5-chuẩn-bị--pilot) |
| Set the stage · observe neutrally · capture evidence · close the session | ✅ script mở đầu đọc nguyên văn, quy tắc can thiệp duy nhất (kẹt > 2 phút — dùng đúng 2 lần, ghi nguyên văn), ghi màn hình + audio có consent, SUS + probe cuối buổi | [`template/session-kit.md`](usability_testing/template/) · [`result/`](usability_testing/result/) |
| Chấm SUS trên 7 người | ✅ Mean 53.2, script tái lập được, khớp 7/7 với bản chấm tay | [§II.7](#ii7-kết-quả-sus) |
| Tổng hợp, **gộp pain point, tách bug lẻ khỏi vấn đề thiết kế hệ thống** | ✅ 9 theme UF + 3 phát hiện hệ thống SYS, cột Bug/Design phân biệt rõ | [`findings.md`](usability_testing/findings.md) |
| **Xếp theo severity** | ✅ Blocker → Cosmetic, kèm tần suất x/7 làm căn cứ | [§II.8](#ii8-findings--mức-độ-nghiêm-trọng) |
| Bug báo cả Markdown và GitHub Issues, có ảnh | ✅ 7 bug trùng gốc issue Task 1 → comment bằng chứng usability + label `usability`, **2 issue được nâng severity** (không mở issue trùng) | [§II.9](#ii9-báo-cáo-bug) |
| Ghi màn hình các session | ✅ 7 video (Drive) | [§0.2](#02-video-demo) V2 |

## VI.3. Tiêu chí 3 — Task 3: Cross-Browser / Cross-Platform · **20/20**

| Yêu cầu của đề | Đạt? | Bằng chứng |
|---|---|---|
| Chạy **Task 1** trên **≥ 3 platform** | ✅ 66 item × 3 engine = **198 lượt**, không lấy mẫu | [`results-matrix.md`](cross_platform_testing/results-matrix.md) |
| Phủ Chrome / Firefox / Safari (hoặc Android Chrome) | ✅ Blink · Gecko · WebKit (cùng engine với Safari, `Version/26.5`) | [`platform-matrix.md`](cross_platform_testing/platform-matrix.md) |
| Nếu hết trial cloud → được dùng máy thật, miễn **ảnh hiện browser/OS/device + URL localhost** | ✅ 18 ảnh cửa sổ thật (có title bar, address bar `localhost:5173`, menu bar macOS) + 179 ảnh viewport | [`results/P*/platform-proof/`](cross_platform_testing/results/) |
| **Mỗi ảnh overlay username dạng email sinh viên** | ✅ overlay MSSV + họ tên + email SV trên toàn bộ 197 ảnh, có script kiểm (`verify-evidence.js`, exit 1 nếu thiếu) | [§III.1](#iii1-đã-làm-gì) |
| Báo cáo khác biệt giữa platform | ✅ **1** item lật Pass/Fail + **28** item khác giá trị hiển thị; 6 item khác do dữ liệu chạy được **tách riêng, không tính là phát hiện** | [`divergences.md`](cross_platform_testing/divergences.md) |
| Bug + báo cáo | ✅ 7 bug XP-01→07, Markdown + GitHub #242–#248 (label `cross-platform`), có ảnh | [§III.6](#iii6-bug-report) |
| Trung thực về phương pháp | ✅ khai rõ P3 là WebKit build của Playwright (menu bar hiện "Playwright"), P1 là Chrome for Testing, đã **xoá** hẳn 2 profile mobile emulation thay vì để lẫn vào bằng chứng | [§III.7](#iii7-giới-hạn-của-lần-đo-này) |
| Giá trị vượt yêu cầu | ✅ Task 3 **phản hồi lại Task 1**: lật 4 kết luận sai và tìm ra bug chức năng Blocker (coupon tính ngược) mà chạy tay đã bỏ qua | [§III.5](#iii5-phát-hiện-c--3-item-task-1-chấm-pass-nhưng-thực-đo-là-fail) |

## VI.4. Tiêu chí 4 — Agent Skills · **10/10**

| Yêu cầu của đề | Đạt? | Bằng chứng |
|---|---|---|
| Build Agent Skill áp dụng được lại cho màn hình/flow khác | ✅ `gui-checklist-testing` — 8 giai đoạn, prompt library, template, 2 script | [Phần IV](#phần-iv--agent-skill) |
| Skill thực sự tái dùng được (không phải ghi chú lại bài đã làm) | ✅ có bảng input phải hỏi trước khi chạy, layout output tổng quát, ví dụ một lần chạy hoàn chỉnh, và **cổng kiểm tra tự động** trước khi commit | `SKILL.md` · `scripts/verify_deliverables.py` |
| Skill giữ đúng ranh giới AI của đề | ✅ AI không quyết Pass/Fail; GĐ3 AI chỉ chẩn đoán, cấm thêm item; severity do người chốt | `SKILL.md` §Nguyên tắc bất biến |
| **Submit skill kèm video demo (YouTube)** chạy end-to-end trên một màn/flow hoàn chỉnh | ⏳ skill đã submit; **link video điền ở [§0.2](#02-video-demo) dòng V1** | — |

## VI.5. Yêu cầu chung của bài

| Yêu cầu | Đạt? | Vị trí |
|---|---|---|
| AI-First, dẫn AI qua **từng bước** của technique | ✅ 6 prompt Task 1 + 9 artifact Task 2 + harness Task 3, mỗi lần gọi một dòng audit | các AI Audit Report |
| Human review mọi output AI | ✅ mỗi dòng audit có cột verdict + "người đã sửa gì"; Task 1: 8/8 INCOMPLETE, Task 2: 8/9 phải sửa | AI Audit Report |
| **AI Audit Report** (tool, ngày giờ, prompt nguyên văn, output) | ✅ 3 bộ, một bộ cho mỗi task | [Phần VII](#phần-vii--phụ-lục) |
| **AI Critique 200–300 từ** | ✅ 3 bản, mỗi bản trong khung 200–300 từ | [Phần V](#phần-v--ai-critique) |
| Toàn bộ quy trình dạng text (Markdown) | ✅ toàn repo là Markdown, số liệu có script sinh lại được | — |
| Anti-AI-cheat: participant thật + ảnh cross-platform có MSSV/tên | ✅ 7 người tuyển thủ công (có video session), overlay danh tính trên mọi ảnh | [§II.4](#ii4-người-tham-gia) · [§III.1](#iii1-đã-làm-gì) |
| **Git commit log**, một commit cho mỗi bước | ✅ 36 commit theo từng bước (checklist design → execution → bug logging → từng session → analysis) | `git-commit-log.txt` |

---

# Phần VII — Phụ lục

## VII.1. AI Audit Report & khai báo

Mỗi task có một bộ đầy đủ theo template FIT@HCMUS:

| Task | Vị trí |
|---|---|
| Task 1 — GUI Checklist | [`gui_and_usability_testing/ai_declaration/`](gui_and_usability_testing/ai_declaration/) — `[AI-02] AI Audit Report` · `[AI-03] AI Disclosure Form` · `[AI-05] AI Privacy Checklist` |
| Task 2 — Usability Evaluation | [`usability_testing/ai_declaration/`](usability_testing/ai_declaration/) — cùng 3 tài liệu |
| Task 3 — Cross-Platform | [`cross_platform_testing/ai_declaration/`](cross_platform_testing/ai_declaration/) — cùng 3 tài liệu |

Khai báo: **"I use AI tools for the following tasks"** — chi tiết từng lần gọi (tên tool, ngày giờ, prompt nguyên văn, output, verdict VALID/INVALID/INCOMPLETE, người đã sửa gì) nằm trong `[AI-02]` của từng task. Bloom-AI: G9.3 (Analyse) + G9.4 (Collaborate).

## VII.2. Checklist các file phải có trong file nộp

`23127438_HW03_AI_GUIUsability_100.zip`:

- [x] Main report — `tests/report.md` (bản này) **+ bản PDF cùng nội dung**
- [x] Bug report + ảnh issue trên GitHub — `gui_and_usability_testing/bug-report.md`, `cross_platform_testing/issues/`, issue #194–#248
- [x] AI Critique + AI Audit Report (Markdown + PDF) — [Phần V](#phần-v--ai-critique), `*/ai_declaration/`
- [x] Bằng chứng session usability — task scenario, ghi chú quan sát, phiếu SUS, findings theo severity, video ghi màn hình, bảng 7 participant
- [x] Ảnh cross-browser / cross-platform — `cross_platform_testing/results/`
- [x] Agent Skill — `.claude/skills/gui-checklist-testing/`
- [ ] **Link YouTube demo skill** — điền vào [§0.2](#02-video-demo) dòng V1 trước khi nộp
- [ ] **Git commit log dạng text** — xuất `git-commit-log.txt` (`git log --pretty=... > git-commit-log.txt`, 36 commit)
- [ ] **Checklist bản Excel** — `checklist-final.md` và `test-cases/test_case_summary.md` đã có; cần xuất thêm `.xlsx` theo đúng chữ "Excel checklist" của đề
- [ ] **`README.md` của bài nộp** — copy [§0.1](#01-test-summary-report) (test summary) + [§0.2](#02-video-demo) (video) + [§0.3](#03-bảng-tự-đánh-giá-assessment-template) (self-assessment) ra một `README.md` ở gốc file zip
- [ ] **Bản PDF** của main report và của AI Critique / AI Audit Report
