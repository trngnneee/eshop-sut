---
name: gui-checklist-testing
description: Thiết kế và thực thi GUI checklist (>40 item) theo interface aspect cho một web app, kèm gap analysis, test case, bug report và GitHub Issues. Dùng khi cần kiểm thử giao diện / GUI checklist / usability-adjacent testing trên một tập màn hình, hoặc khi làm bài tập dạng "GUI & Usability" (HW03) trên SUT EShop và các app tương tự.
---

# GUI Checklist Testing (requirements-based)

Skill này đóng gói quy trình 8 giai đoạn đã chạy thật trên EShop HW03 Task 1 (66 item · 57 Failed · 48 bug · issues #194–241). Mục tiêu: **checklist neo vào yêu cầu giao diện thành văn của SUT**, không phải danh sách heuristic chung chung, và mọi kết luận Pass/Fail đều do người thực thi trên app đang chạy.

Xem `examples/eshop-hw03-task1.md` để biết một lần chạy hoàn chỉnh trông như thế nào.

## Nguyên tắc bất biến (vi phạm là làm lại)

1. **Không bao giờ dùng một prompt "sinh cả checklist"**. Mỗi giai đoạn là một lần gọi AI riêng, ăn output của giai đoạn trước. Mỗi lần gọi = một dòng trong AI Audit Report.
2. **Sinh item theo TỪNG interface aspect**, mỗi aspect một prompt riêng (không gộp 4 aspect vào một lần).
3. **AI không được quyết Pass/Fail.** Cột "Actual result" phải là quan sát trực tiếp trên SUT đang chạy (giá trị thật: chuỗi thật, computed style thật, toạ độ thật), không phải suy luận từ code.
4. **Item bổ sung do người tìm ra phải kèm lý do AI bỏ sót**, chọn trong 3 nhóm: *chất lượng prompt đầu vào* / *giới hạn mô hình* / *đặc thù giao diện SUT*, và phải giải thích bằng bằng chứng cụ thể.
5. **Screenshot chỉ cho item Failed.** Item Passed cố ý không có ảnh, và ghi rõ `Screenshot: (không có — test Passed)` để người chấm không đọc là thiếu bằng chứng.
6. **Chốt bằng script kiểm tra**, không bằng niềm tin: `scripts/verify_deliverables.py` phải sạch trước khi commit.

Ba thứ **ngoài phạm vi** skill này vì là việc chung của cả bài (Task 1+2+3): git commit log dạng text file, main report hợp nhất + bản PDF, và `README.md` self-assessment. Đừng sinh chúng trong đây.

## Input cần hỏi người dùng trước khi bắt đầu

Nếu chưa có trong ngữ cảnh, hỏi gọn một lượt:

| Thông tin | Ví dụ (EShop HW03) |
|---|---|
| Repo SUT + cách chạy | `eshop-sut`, `./run_servers.sh`, web `:5173`, API `:3000` |
| Frontend trong scope | `frontend-web` (khách) |
| Danh sách màn hình | 8 màn theo một luồng end-to-end: Đăng ký → Đăng nhập → Quên MK → Trang chủ → Chi tiết SP → Giỏ → Thanh toán → Lịch sử ĐH |
| **Test basis** — mục yêu cầu giao diện trong tài liệu SUT | `README.md` mục 8: FR-21 chung / FR-22 form / FR-23 điều hướng / FR-24 feedback-state |
| Bộ interface aspect | IA-01 General UI · IA-02 Forms · IA-03 Navigation · IA-04 Feedback/state |
| Tài khoản test | `test@eshop.com / Test1234!`, `admin@eshop.com / Admin123!` |
| Thư mục output | `tests/gui_and_usability_testing/` |
| Repo nhận GitHub Issues | `trngnneee/eshop-sut` |
| Sinh viên + môi trường thực thi | tên, MSSV, browser/OS, ngày thực thi |

Chọn màn hình **theo một luồng liền mạch**, không chọn rời rạc — luồng mới cho phép test được các quy tắc xuyên màn (điều hướng, nhất quán ngôn ngữ/màu, trạng thái giỏ). Một màn hình đơn lẻ không đủ ra 40 item có nghĩa.

Nếu tài liệu SUT **không có** mục yêu cầu giao diện: dừng lại, nói rõ checklist sẽ chỉ dựa trên heuristic (yếu hơn hẳn về mặt truy vết), và hỏi người dùng có nguồn yêu cầu nào khác không.

## Layout output

```
<output-dir>/
  ui-inventory/<screen-slug>.md        # GĐ1 — 1 file/màn + _shared-layout.md cho header/footer
  checklist-draft/ia-0N-<name>.md      # GĐ2 — 1 file/aspect
  checklist-draft/gap-analysis.md      # GĐ3 — Phần A (AI chẩn đoán) + Phần B (người kết luận)
  checklist-final.md                   # GĐ4 — bảng hợp nhất + cột Kết quả/Ghi chú + dedup log
  test-cases/IA-0N/<ID>.md             # GĐ5 — 1 file/item, bung thành test case đầy đủ
  test-cases/screenshots/<ID>.png      # GĐ5 — CHỈ item Failed
  test-cases/test_case_summary.md       # GĐ5 — bảng tổng + index tới từng file
  bug-report.md                        # GĐ6 — bảng tổng bug + chi tiết
  issues/BUG-NN.md                     # GĐ6 — thân issue, dùng cho `gh issue create`
  issue-map.tsv                        # GĐ6 — BUG ↔ severity ↔ issue URL ↔ title
  report.md                            # GĐ7 — báo cáo Task, gồm mục AI Critique 200–300 từ
  ai_declaration/[AI-02] AI Audit Report.md
```

ID: `GUI-IA0N-NN` cho item AI sinh, `GUI-GAP-NN` cho item người tự thêm — **không đánh số GAP lẫn vào dãy IA**, để luôn truy vết được cái nào AI sinh cái nào người thêm.

## Quy trình 8 giai đoạn

Prompt đầy đủ (dán được ngay): `references/prompts.md`. Template file: `references/templates.md`.

**GĐ0 — Chuẩn bị** *(người, không AI)*. Chạy SUT local, xác nhận port; tạo label `bug`,`ui` + label severity trên GitHub; chốt scope màn hình; ghi ngày giờ bắt đầu.
→ commit: `Task1: setup SUT + scope`

**GĐ1 — UI Inventory** *(AI, lặp theo màn hình — Prompt #1)*. Đọc component tree từ source (page + sub-component + **mọi nhánh render có điều kiện**: loading/error/empty/disabled), xuất bảng có cột `Source file:line`. Bắt buộc cross-check trên app đang chạy để bắt phần chỉ xuất hiện lúc runtime (nội dung từ API, computed class, lỗi backend rò ra UI). Header/footer dùng chung tách ra `_shared-layout.md` để không lặp qua các màn.
→ commit: `Task1: UI inventory for N screens (source-code based)`

**GĐ2 — Sinh item theo từng aspect** *(AI, 4 lần riêng — Prompt #2a→#2d)*. Input mỗi lần: inventory (tất cả màn) + **nguyên văn** mục yêu cầu tương ứng. Yêu cầu ≥12 item/aspect, mỗi item phải trỏ tới element cụ thể trong inventory, cấm item kiểu "giao diện phải đẹp". Với aspect Form, nói thẳng với AI: **quy tắc nào của spec ngược convention thì không được "sửa" cho giống thói quen** (ví dụ spec đòi lỗi hiện *phía trên* nút submit) — đây là điểm AI hay tự ý normalise.
→ commit: `Task1: AI-generated checklist draft (IA-01..IA-04)`

**GĐ3 — Gap analysis** *(AI chẩn đoán + người quyết — Prompt #3)*. **Đây là phần được chấm nặng nhất.** AI chỉ được *chẩn đoán* 8 chiều (accessibility, dark mode, RTL, viewport cực đoan, network resilience, text-overflow/localization, print/export, browser-native quirks) là đã phủ / phủ một phần / thiếu hẳn — **cấm thêm dòng checklist mới**. Sau đó **người tự thử trên SUT** (DevTools: zoom 200%, 320px, throttle 3G, offline, tab-only, dán `<script>` vào ô tìm kiếm, F5 giữa luồng) rồi mới chốt item bổ sung ở Phần B kèm cột `Lý do AI bỏ sót` + `Giải thích chi tiết` có bằng chứng (file:line, kết quả grep, quan sát thật).

Chiều nào quyết định loại khỏi scope thì **ghi rõ lý do** (ví dụ: app không có class `dark:` nào → bỏ dark mode; app thuần tiếng Việt và spec không đòi → bỏ RTL) — loại có lý do khác hoàn toàn với bỏ sót.
→ commit: `Task1: gap analysis - items missed by AI`

**GĐ4 — Hợp nhất & dedup** *(AI + người duyệt — Prompt #4)*. Gộp near-duplicate (thường phát sinh vì sinh item theo aspect độc lập → cùng một quy tắc bị hai aspect phát biểu lại), đánh số lại trong từng aspect, giữ prefix `GUI-GAP`, **ghi dedup log ở cuối file** để truy vết item nào gộp từ đâu. Xác nhận tổng > 40.
→ commit: `Task1: consolidated + deduped checklist (>40 items)`

**GĐ5 — Thực thi** *(người 100%, AI chỉ được chuốt văn phong — Prompt #5)*. Với từng item: thao tác thật trên browser, so với Expected, đánh Passed/Failed, ghi giá trị quan sát được. Item Failed → screenshot đặt tên **trùng ID** (`GUI-IA02-04.png`). Bung mỗi item thành một file test case đầy đủ (Preconditions / Test data / Test steps / Expected / Status+bug / Actual result có người thực thi + ngày + môi trường + Observed). Prompt #5 chỉ để viết lại ghi chú thô cho gọn, và phải cấm AI bịa root cause / severity.
→ commit: `Task1: checklist execution results + failed-item screenshots`

**GĐ6 — Bug report + GitHub Issues** *(AI soạn format — Prompt #6)*. **Gộp item Failed theo nguyên nhân gốc**: nhiều item cùng một chỗ hỏng thì một bug (ví dụ 3 item cùng thiếu loading/error state → 1 issue). Mỗi bug một file `issues/BUG-NN.md` theo đúng khung Title/Description/Steps/Expected/Actual/Environment/Related checklist item/Requirement/Severity/Screenshot. Severity do **người** chốt, không lấy đề xuất AI.

Ảnh phải render được trên GitHub → upload lên host ảnh rồi nhúng URL:
```bash
export CLOUDINARY_URL="cloudinary://KEY:SECRET@CLOUD_NAME"
python3 scripts/upload_screenshots.py --base <output-dir> --dry-run   # xem trước
python3 scripts/upload_screenshots.py --base <output-dir>
```
Rồi đăng issue và ghi lại URL vào `issue-map.tsv`:
```bash
for f in <output-dir>/issues/BUG-*.md; do
  gh issue create --repo <owner/repo> --title "$(sed -n '2p' "$f")" \
    --body-file "$f" --label bug,ui
done
```
Sau khi có số issue: back-fill vào `bug-report.md`, `issue-map.tsv`, và mục `Status / Related bugs` của từng test case → truy vết hai chiều item ↔ bug ↔ issue.
→ commit: `Task1: bug logging - N issues filed`

**GĐ7 — AI Audit Report**. Một dòng cho **mỗi lần gọi AI** (GĐ1 mỗi màn một dòng, GĐ2 bốn dòng, GĐ3, GĐ4, GĐ5 nếu dùng, GĐ6 mỗi bug hoặc một dòng gộp có nêu số lượng), gồm: tool + version, ngày giờ, **prompt nguyên văn**, output, verdict (VALID/INVALID/INCOMPLETE), lý do có dẫn ISTQB/slide, và **người đã sửa gì**. Cột "người đã sửa gì" là chỗ chứng minh có human review — không được để trống.

**GĐ8 — AI Critique 200–300 từ** *(người tự viết)*. Không tổng kết chung chung kiểu "AI hữu ích nhưng cần kiểm tra". Cấu trúc đã hiệu quả: (a) AI mạnh ở đâu khi được đưa khung cụ thể; (b) **một chỗ nó hỏng và hỏng thế nào** — ví dụ tự đề xuất chiều accessibility rồi chỉ liệt kê focus ring + contrast, bỏ qua `<html lang>` và label association; (c) những điểm mù do **cách người chia bài toán** (chia theo màn hình tĩnh → không thấy lỗi cần kết hợp hai thao tác); (d) nguyên tắc rút ra. Đếm từ trước khi chốt.

## Cổng kiểm tra trước khi commit

```bash
python3 scripts/verify_deliverables.py --dir <output-dir>            # offline
python3 scripts/verify_deliverables.py --dir <output-dir> --gh <owner/repo>   # + kiểm issue có ảnh
```
Script kiểm: bảng markdown lệch số cột (lỗi này làm GitHub/pandoc **không nhận ra bảng** → cả checklist render thành text thô), tổng item > 40 và mọi item có status, screenshot ↔ item Failed là song ánh, item Passed không có ảnh, test case 1:1 với item, mọi item Failed đều được một bug phủ, mọi item `GUI-GAP` có lý do AI bỏ sót, AI Critique nằm trong 200–300 từ, và (với `--gh`) mọi issue tồn tại + có ảnh nhúng.

Chỉ commit khi script sạch. Nếu script báo lỗi mà bạn cho là chấp nhận được, ghi lý do vào `report.md` mục Hạn chế thay vì bỏ qua im lặng.

## Cạm bẫy đã gặp thật

- **AI tự "sửa" quy tắc ngược convention** của spec cho giống thói quen phổ biến → luôn nhắc thẳng trong prompt là phải test theo spec.
- **Chia prompt theo màn hình tĩnh** → mù toàn bộ loại lỗi cần kết hợp nhiều thao tác (giỏ mất khi F5, thêm 2 lần ra 2 dòng). Sau GĐ2 phải tự hỏi: *"cách chia này làm mất loại lỗi nào?"* rồi đi thăm đúng các đường nối đó.
- **AI nêu được tên phạm trù nhưng không rà hết phạm trù đó** — dừng ở ví dụ điển hình nhất. Với accessibility, tự grep thêm `htmlFor`, `aria-`, `alt=`, `lang=`.
- **Kết luận trên một engine duy nhất** dễ sai ở các item về pixel/breakpoint. Nếu bài có phần cross-browser, đối chiếu lại và ghi rõ item nào bị lật.
- **Đường dẫn trong prompt đã log phải khớp nơi file thật nằm.** Nếu giữa đường có đổi thư mục output, sửa lại prompt trong Audit Report hoặc ghi chú đã relocate — người chấm sẽ đối chiếu.
- **Ảnh host bên ngoài** có thể hỏng link sau này → vẫn giữ đủ file `.png` trong repo, và cache URL vào `scripts/cloudinary-url-map.json` để chạy lại idempotent.
