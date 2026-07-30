# Template file output

Mọi bảng markdown: **số ô dòng separator phải bằng số cột header**. Lệch một ô là GitHub/pandoc không nhận ra bảng và render cả bảng thành text thô — `scripts/verify_deliverables.py` kiểm cái này.

---

## 1. `ui-inventory/<screen-slug>.md`

```markdown
# UI Inventory — Màn hình <<Tên>> (<<English name>>)

- **Route:** `/<<route>>` — **<<FR-0X>>** (<<mô tả chức năng>>)
- **Files đã đọc:** `<<path>>:...`, `<<path>>`
- **Runtime cross-check:** <<đã chạy app / không chạy được và vì sao>>. Header/footer dùng chung: xem `_shared-layout.md`.

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|
| 1 | Heading (h2) | **"<<label>>"** | <<vị trí>> | <<mục đích>> — <<FR/IA>> | `File.jsx:24` |
```

Bôi đậm ngay trong inventory những chỗ đã thấy đáng ngờ (nhãn sai, `type="text"` cho mật khẩu, `<a>` thay `<Link>`) — GĐ2 sẽ ăn thẳng vào đó.

---

## 2. `checklist-draft/ia-0N-<name>.md`

```markdown
# Checklist Draft — IA-0N: <<Aspect name>>

- **Input:** inventory <<N>> file trong `../ui-inventory/` + <<UI-REQ-N>> nguyên văn (`<<path>>:<<lines>>`)
- **<<UI-REQ-N>> gồm <<k>> quy tắc:** (1) ... (2) ... (3) ...

| ID | Screen(s) | Checklist Item | Expected Result | Traced to (<<UI-REQ-N>> / heuristic) |
|---|---|---|---|---|
| GUI-IA0N-01 | <<màn>> | <<phát biểu kiểm được, có dẫn element + file:line hiện trạng>> | <<kết quả mong đợi cụ thể>> | <<UI-REQ-N>> (<<quy tắc nào>>) |
```

Ghi hiện trạng vào trong item (`hiện là "Sign In" — Login.jsx:58`) để lúc thực thi không phải đi tìm lại.

---

## 3. `checklist-draft/gap-analysis.md`

```markdown
# Gap Analysis

- **Input:** <<N>> item từ 4 file checklist-draft (IA-01: .., IA-02: .., IA-03: .., IA-04: ..)
- **Phần A** = chẩn đoán của AI theo 8 chiều (output Prompt #3).
- **Phần B** = kết luận sau khi tự kiểm chứng trên SUT.

## Phần A — Chẩn đoán AI (8 chiều)

| # | Chiều | Trạng thái | Bằng chứng trong checklist | Candidate items (CHƯA kiểm chứng) |
|---|---|---|---|---|
| 1 | Accessibility | Partially | Chỉ có <<ID>>, <<ID>> | (a) ... (b) ... |

**Tóm tắt:** <<x>> chiều fully · <<y>> partially · <<z>> absent. <<Chiều absent nào chủ động loại khỏi scope và vì sao>>

## Phần B — Kết luận sau khi tự kiểm chứng

| ID mới | Item bổ sung | Đã tự kiểm chứng trên SUT? | Lý do AI bỏ sót | Giải thích chi tiết |
|---|---|---|---|---|
| GUI-GAP-01 | <<item + hiện trạng quan sát>> | Có | <<Chất lượng prompt đầu vào / Giới hạn mô hình AI / Đặc thù giao diện SUT>> — <<một câu tại sao>> | <<bằng chứng: file:line, kết quả grep, thao tác đã làm và thấy gì>> |
```

Cột `Lý do AI bỏ sót` phải chọn đúng một trong ba nhóm và **giải thích được**, không dán nhãn suông. Ví dụ hợp lệ:
- *Đặc thù SUT* — hành vi phụ thuộc quyết định cài đặt riêng (state in-memory vs localStorage), không suy ra được từ yêu cầu thành văn.
- *Chất lượng prompt* — người yêu cầu sinh item theo từng màn hình tĩnh nên AI không thể thấy lỗi cần kết hợp hai thao tác.
- *Giới hạn mô hình* — AI tự nêu chiều accessibility nhưng chỉ liệt kê focus ring + contrast, bỏ `<html lang>` dù bằng chứng nằm ở `index.html:2`.

---

## 4. `checklist-final.md`

```markdown
# <<SUT>> — GUI Checklist cuối

- **Input:** <<N>> item AI (IA-01: .., IA-02: .., IA-03: .., IA-04: ..) + <<k>> item bổ sung thủ công (GUI-GAP).
- **Dedup:** <<m>> cặp near-duplicate được gộp (log cuối file). Item GUI-GAP giữ nguyên mã để truy vết nguồn gốc AI vs thủ công.
- **Tổng: <<T>> item**

| ID | Interface Aspect | Screen(s) | Checklist Item | Expected Result | Kết quả | Ghi chú (lý do Fail) |
|---|---|---|---|---|---|---|
| GUI-IA01-01 | IA-01 General UI | <<màn>> | <<item>> | <<expected>> | ❌ Failed | <<giá trị quan sát được>> *(BUG-05)* |
| GUI-IA01-07 | IA-01 General UI | <<màn>> | <<item>> | <<expected>> | ✅ Passed | |

## Tổng kết

| Aspect | Số item | Trong đó Manually added | Passed | Failed |
|---|---|---|---|---|
| IA-01 | 16 + 1 (GAP-03) = 17 | 1 | 3 | 14 |
| **Tổng** | **<<T>>** | **<<k>>** | **<<p>>** | **<<f>>** |

## Dedup log

| Giữ | Gộp từ | Lý do |
|---|---|---|
| GUI-IA02-15 | GUI-IA01-13 | Cùng một quy tắc tab order, hai aspect phát biểu lại |
```

---

## 5. `test-cases/IA-0N/<ID>.md`

```markdown
# <<ID>>: <<tiêu đề item>>

## Requirement ID
<<UI-REQ-N>> (<<quy tắc>>)

## Module / Test type / Technique
<<Aspect tiếng Việt>> / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | <<ID>> |
| Interface Aspect | <<...>> |
| Actor | <<Người dùng cuối (khách) / Admin>> |
| Goal | <<...>> |
| Screen(s) | <<...>> |
| Checklist item | <<phát biểu đầy đủ + hiện trạng file:line>> |
| Traced to | <<UI-REQ-N>> |

## Preconditions
- SUT đang chạy; frontend tại `<<URL>>`, backend tại `<<URL>>`.
- <<trạng thái đăng nhập / dữ liệu cần có>>

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | <<...>> |
| Interface | <<...>> |
| Endpoint / UI flow | <<routes>> |
| Input / Payload | <<...>> |
| Fixture | <<tài khoản/dữ liệu seed>> |

## Test steps
1. <<...>>
2. <<...>>
3. <<điều kiện fail rõ ràng>>

## Expected result
- <<...>>

## Status / Related bugs
<<Passed | Failed — BUG-NN (issue URL)>>

## Actual result
- Executed by: <<tên>>
- Execution date: <<YYYY-MM-DD>>
- Execution interface: <<browser/OS, kiểm thử thủ công>>
- Observed: <<giá trị quan sát THẬT — chuỗi, toạ độ, computed style>>
- Execution result: **<<Passed/Failed>>**
- Screenshot: ![<<ID>>](../screenshots/<<ID>>.png)      <!-- Passed: (không có — test Passed) -->
```

---

## 6. `test-cases/test_case_summary.md`

```markdown
# Test Cases — <<SUT>> GUI Checklist

Mỗi file = 1 checklist item từ `../checklist-final.md`, bung thành test case chi tiết.

## Kết quả thực thi
- **Người thực thi:** <<tên>> (kiểm thử thủ công trực tiếp trên trình duyệt)
- **Ngày thực thi:** <<YYYY-MM-DD>> · **Môi trường:** <<...>>
- **Screenshot mỗi test Failed:** `screenshots/<ID>.png`

| Aspect | Passed | Failed | Tổng |
|---|---|---|---|
| IA-01 | 3 | 14 | 17 |
| **Tổng** | **<<p>>** | **<<f>>** | **<<T>>** |

| # | Test Case | Aspect | Traced to | Screen(s) | Kết quả |
|---|---|---|---|---|---|
| 1 | [<<ID>>](IA-01/<<ID>>.md) | IA-01 | <<UI-REQ>> | <<màn>> | ❌ Failed |
```

---

## 7. `bug-report.md` + `issues/BUG-NN.md` + `issue-map.tsv`

`bug-report.md` mở đầu bằng bảng tổng, sắp theo severity giảm dần:

```markdown
# <<SUT>> — Bug Report

- Tổng hợp từ <<f>> checklist item **Failed** (<<T>> item, <<p>> Passed), gộp theo nguyên nhân gốc thành **<<B>> bug**.
- Screenshot tương ứng nằm trong `test-cases/screenshots/<checklist-id>.png`.

| Bug | Mức độ | Issue | Tiêu đề | Checklist liên quan |
|---|---|---|---|---|
| BUG-01 | Blocker | [194](https://github.com/<<owner/repo>>/issues/194) | <<title>> | GUI-IA04-13 |
```

`issues/BUG-NN.md` — đúng khung của Prompt #6, `## Title` ở dòng 1 nên tiêu đề nằm **dòng 2** (`sed -n '2p'` lấy được để `gh issue create --title`).

`issue-map.tsv` — tab-separated, 4 cột:

```
BUG	Severity	Issue_URL	Title
BUG-01	blocker	https://github.com/<<owner/repo>>/issues/194	[Blocker] <<title>>
```

Quy tắc gộp bug: một bug = **một nguyên nhân gốc**, kể cả khi nó làm fail nhiều item (ghi đủ ID vào `Related checklist item(s)`). Ngược lại, một item fail vì hai nguyên nhân độc lập thì tách hai bug.

---

## 8. Dòng AI Audit Report

| Cột | Nội dung |
|---|---|
| (1) Prompt + Tool | `__Tool:__ <<tool + version>>` · `__Artifact:__ GĐ<<n>> · <<tên bước>>` · `__Prompt (verbatim):__` <<nguyên văn, escape `\|` thành `&#124;`>> |
| (2) AI Output | Output là gì, ở file nào, số lượng bao nhiêu — nêu con số cụ thể |
| (3) Verdict | VALID / INVALID / INCOMPLETE |
| (4) Reasoning (ISTQB) | Dẫn khái niệm ISTQB cụ thể (test analysis / requirements-based design / defect management / experience-based techniques) và vì sao verdict đó |
| (5) Student Fix | Người đã kiểm chứng và sửa gì — **bắt buộc có nội dung thật** |
