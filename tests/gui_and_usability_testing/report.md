# EShop — Báo cáo GUI Checklist (Task 1)

Thiết kế và thực thi một GUI checklist dựa trên yêu cầu giao diện của SUT, trên frontend-web dành cho khách (`localhost:5173`).

**Kết quả một dòng:** 66 checklist item phủ 4 interface aspect · thực thi thủ công 100% · 9 Passed / 57 Failed · 48 bug đã lên GitHub Issues (#194–#241).

---

## 1. Phạm vi & cơ sở

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

## 2. Quy trình — 6 bước, AI làm gì và người làm gì

Đề cấm kiểu prompt "sinh cả checklist trong một phát", nên quy trình được tách thành các bước ăn output của nhau, mỗi bước là một dòng trong AI Audit Report (`ai_declaration/[AI-02]`):

| Bước | Việc | Ai làm | Sản phẩm |
|---|---|---|---|
| 1 | Kiểm kê phần tử giao diện từng màn (đọc component tree, kể cả nhánh render có điều kiện) | AI (Prompt #1) · em soát lại trên app đang chạy | `ui-inventory/*.md` (9 file, có cột `Source file:line`) |
| 2 | Sinh item theo **từng** interface aspect, input là inventory + FR-21→24 nguyên văn | AI (Prompt #2a→#2d, 4 lần) | `checklist-draft/ia-0*.md` — 65 item |
| 3 | Rà khoảng trống theo 8 chiều, rồi **tự kiểm chứng từng candidate trên SUT** | AI chẩn đoán (Prompt #3) · em kiểm chứng và quyết | `checklist-draft/gap-analysis.md` — 4 item bổ sung |
| 4 | Hợp nhất, dedup, đánh số lại | AI · em duyệt | `checklist-final.md` — 66 item |
| 5 | **Thực thi thủ công** 66 item trên trình duyệt | Em, 100% — AI không tham gia | 66 file `test-cases/`, 57 screenshot |
| 6 | Viết bug report + đăng GitHub Issues | AI nháp (Prompt #6) · em quyết severity | `bug-report.md`, 48 issue |

Bước 5 không dùng AI: mọi ô "Actual result / Observed" trong 66 test case là quan sát trực tiếp của em ngày 25/07/2026 trên Chrome.

## 3. Bốn item em tự thêm — và vì sao AI bỏ sót

Đây là phần đề yêu cầu giải thích riêng cho từng item bổ sung. Chi tiết đầy đủ ở `checklist-draft/gap-analysis.md` Phần B; tóm tắt nguyên nhân:

| ID | Item | Nguyên nhân AI bỏ sót | Vì sao nguyên nhân đó |
|---|---|---|---|
| GUI-GAP-01 | Giỏ hàng phải còn sau khi F5 | **Đặc thù SUT** | Giỏ còn hay mất sau reload là quyết định cài đặt riêng (React state vs localStorage), không suy ra được từ FR-21→24 hay heuristic UI tĩnh. Checklist gốc chỉ chạm tới back button (IA03-10/11), không có item nào về reload/persistence |
| GUI-GAP-02 | Thêm cùng 1 SP nhiều lần phải gộp dòng | **Cách em chia prompt** | Lỗi chỉ lộ khi *kết hợp* 2 thao tác. Em yêu cầu AI sinh item theo từng màn hình tĩnh, nên IA04-01/02 chỉ soi feedback của **một** lần bấm — cấu trúc prompt của em tạo ra đúng điểm mù này |
| GUI-GAP-03 | `<html lang="vi">` | **Giới hạn mô hình** | Chính AI đề xuất chiều Accessibility (gap-analysis Phần A, chiều 1) nhưng chỉ liệt kê được focus ring + contrast, bỏ qua khai báo ngôn ngữ — dù đó là WCAG 3.1.1 cơ bản và bằng chứng nằm ngay `index.html:2` |
| GUI-GAP-04 | Mọi label gắn input qua `htmlFor`/`id` | **Giới hạn mô hình** | Cùng gốc với GAP-03: chiều Accessibility không rà tới ngữ nghĩa form (WCAG 1.3.1/4.1.2), dù lỗi lặp trên cả 4 form và `grep htmlFor` toàn codebase ra 0 kết quả |

Bốn item này không phải bổ sung cho đủ số: cả 4 đều **Failed** khi thực thi, và sinh ra BUG-21, BUG-22 cùng 2 bug khác.

Ba chiều còn **absent** sau khi rà (dark mode, RTL, print/export) được **chủ động loại khỏi scope kèm lý do**: app không có class `dark:` nào, thuần tiếng Việt và spec không yêu cầu RTL, còn print/export không thuộc luồng mua hàng.

## 4. Hợp nhất & dedup

65 item AI + 4 item thủ công = 69, dedup 3 cặp near-duplicate còn **66**. Log dedup ở cuối `checklist-final.md` (mục "Dedup log") để truy vết được item nào gộp từ đâu — đáng chú ý là cả 3 cặp trùng đều sinh ra từ việc **sinh item theo từng aspect độc lập**: cùng một quy tắc FR bị hai aspect phát biểu lại theo hai cách (ví dụ tab order được cả IA-01 và IA-02 sinh ra).

| Aspect | Số item | Trong đó tự thêm | Passed | Failed |
|---|---|---|---|---|
| IA-01 General UI | 17 | 1 (GAP-03) | 3 | 14 |
| IA-02 Forms | 15 | 1 (GAP-04) | 2 | 13 |
| IA-03 Navigation | 15 | 0 | 3 | 12 |
| IA-04 Feedback/State | 19 | 2 (GAP-01, 02) | 1 | 18 |
| **Tổng** | **66** | **4** | **9** | **57** |

## 5. Thực thi

- **Người thực thi:** Đặng Trường Nguyên · **Ngày:** 25/07/2026 · **Môi trường:** Frontend Web `localhost:5173` + Backend `localhost:3000`, Chrome, kiểm thử thủ công
- **Kết quả:** 66/66 item được thực thi — **9 Passed / 57 Failed**, không item nào bỏ trống hay để "chưa chạy"
- **Ghi nhận:** `checklist-final.md` có cột `Kết quả` và cột `Ghi chú (lý do Fail)`; mỗi item Failed đều ghi lý do là **giá trị quan sát được** (chuỗi thật, computed style thật), không phải diễn giải
- **Screenshot:** 57 ảnh trong `test-cases/screenshots/<ID>.png` — **chỉ cho item Failed**. 9 item Passed cố ý không có ảnh, và mỗi file test case Passed ghi rõ `Screenshot: (không có — test Passed)` để không ai đọc là thiếu bằng chứng
- **Chi tiết từng item:** 66 file trong `test-cases/IA-0*/`, mỗi file có Preconditions / Test data / Test steps / Expected / Actual (Observed) / Status + link bug
- **Hiệu chỉnh sau Task 3:** bảng 9/57 ở trên là hồ sơ gốc của lần chạy tay này và được giữ nguyên. Task 3 chạy lại 66 item bằng script trên 3 engine đã lật **4 item** (`GUI-IA01-08`, `GUI-IA01-15`, `GUI-IA04-12` Pass→Fail; `GUI-IA02-14` Fail→Pass trên Chromium) — bảng đối chiếu ở `test-cases/test_case_summary.md`, chú thích ngay trong `checklist-final.md` cột Ghi chú, và mục "Retest — Task 3" trong 4 file test case. Số đo mới nhất: 7 Passed / 59 Failed (Chromium)

Tỉ lệ Failed 86% cao bất thường với một app thật, nhưng EShop là SUT dựng riêng để dạy kiểm thử — lỗi được gieo có chủ ý. Con số này nói về SUT, không nói về độ khắt khe của checklist.

## 6. Bug

57 item Failed được **gộp theo nguyên nhân gốc** thành **48 bug** (nhiều item cùng một nguyên nhân thì chỉ mở một issue — ví dụ BUG-19 phủ IA04-08/09/16, cùng một chỗ thiếu loading/error state).

| Mức độ | Số lượng | Ví dụ |
|---|---|---|
| Blocker | 2 | BUG-01 XSS qua `dangerouslySetInnerHTML` (#194) · BUG-02 tổng tiền là input sửa được rồi gửi thẳng lên API (#195) |
| Major | 20 | BUG-11 regex SĐT từ chối số VN bắt đầu bằng 0 (#204) · BUG-17 click "Thêm vào giỏ" lần đầu bị bỏ qua (#210) |
| Minor | 26 | BUG-41 `<html lang="en">` (#241) |

- Toàn bộ 48 bug có mặt ở **cả** `bug-report.md` **và** GitHub Issues (#194–#241), mỗi issue kèm screenshot nhúng
- Ánh xạ item ↔ bug ↔ issue: `issue-map.tsv`
- Severity do em quyết, không theo đề xuất của AI

## 7. Hạn chế

1. __Một trình duyệt, một máy.__ Toàn bộ Task 1 chạy trên Chrome/macOS. Đây chính là lý do Task 3 tồn tại — và Task 3 đã cho thấy hạn chế này là thật: 3 item bị Task 1 kết luận sai vì chỉ xem trên một engine (`GUI-IA01-08`, `GUI-IA01-15`, `GUI-IA04-12` — xem `../cross_platform_testing/report.md`).
2. **Catalog seed chỉ 5 sản phẩm.** Các item về danh sách/phân trang (ví dụ IA03-15) Passed trong điều kiện dữ liệu nhỏ; kết luận không suy rộng được cho catalog lớn.
3. **Thực thi bằng mắt.** Các item về sub-pixel/breakpoint được phán đoán bằng quan sát, không bằng đo — Task 3 sau đó đo bằng script và lật lại `GUI-IA01-15`.
4. **Không phủ Web Admin và Mobile app.** Scope cố ý giới hạn ở frontend-web khách để đủ sâu trong một luồng, đánh đổi bằng độ rộng.

## 8. AI Critique (200–300 từ)

Cả 8 artifact AI sinh ra đều bị em xếp INCOMPLETE, không cái nào VALID — nhưng điều đáng học không phải "AI sai nhiều", mà là **AI sai ở đâu**.

AI mạnh nhất khi được đưa một cái khung cụ thể: với inventory có `file:line` và FR-21→24 nguyên văn làm input, nó sinh 65 item bám sát app thật, không có item chung chung kiểu "giao diện phải đẹp". Nó cũng tự đề xuất được chiều Accessibility mà em chưa nghĩ tới.

Nhưng chính chiều đó là chỗ nó hỏng: sau khi tự nêu Accessibility, nó chỉ liệt kê focus ring và contrast, bỏ qua `<html lang>` và label association — hai lỗi WCAG cơ bản, một cái nằm ở dòng 2 của `index.html`, một cái tìm ra bằng `grep htmlFor` với 0 kết quả. Nêu được tên phạm trù không có nghĩa là rà hết phạm trù đó; AI dừng ở những ví dụ điển hình nhất của khái niệm.

Hai điểm mù còn lại thì do **em**, không do nó: em yêu cầu sinh item theo từng màn hình tĩnh và theo từng aspect độc lập, nên nó không thể thấy lỗi cần *kết hợp hai thao tác* (giỏ mất khi F5, thêm 2 lần ra 2 dòng), và nó phát biểu trùng cùng một quy tắc FR ở hai aspect — đúng 3 cặp phải dedup.

Nguyên tắc em rút ra: cách chia bài toán quyết định AI sẽ mù ở đâu, và cái khung đó là việc của người. Vì vậy sau mỗi lần AI trả kết quả, câu hỏi cần đặt không phải "danh sách này có đúng không" mà "**cách chia này làm mất loại lỗi nào**" — rồi tự đi thăm đúng các đường nối đó trên app.
