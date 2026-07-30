# Worked example — EShop HW03 Task 1

Lần chạy thật của quy trình này, dùng làm mốc so sánh khi áp lên màn hình/flow khác.
Artifact đầy đủ: `tests/gui_and_usability_testing/`.

## Cấu hình

| Mục | Giá trị |
|---|---|
| SUT | EShop (Node/Express/SQLite + React/Vite/Tailwind), `run_servers.sh` |
| Scope | `frontend-web` (khách) · 8 màn theo luồng: Đăng ký → Đăng nhập → Quên MK → Trang chủ → Chi tiết SP → Giỏ → Thanh toán → Lịch sử ĐH |
| Test basis | `README.md` mục 8 — FR-21 chung / FR-22 form / FR-23 điều hướng / FR-24 feedback-state |
| Tool AI | Claude Code (Claude Opus 4.8) |
| Môi trường thực thi | Chrome / macOS, thủ công, 25/07/2026 |
| Issues | `trngnneee/eshop-sut` #194–241 |

## Con số ra được

| Giai đoạn | Kết quả |
|---|---|
| GĐ1 UI Inventory | 9 file (8 màn + `_shared-layout`), ~116 dòng element, mọi dòng có `Source file:line` |
| GĐ2 Sinh theo aspect | 65 item — IA-01: 16 · IA-02: 16 · IA-03: 15 · IA-04: 18 |
| GĐ3 Gap analysis | 8 chiều: 0 fully · 5 partially · 3 absent (loại khỏi scope kèm lý do) → **4 item tự thêm** |
| GĐ4 Hợp nhất | 69 → **66 item** sau dedup 3 cặp |
| GĐ5 Thực thi | 66/66 chạy — **9 Passed / 57 Failed**, 57 screenshot |
| GĐ6 Bug | 57 item Failed → **48 bug** (gộp theo nguyên nhân gốc): 2 Blocker · 20 Major · 26 Minor |
| GĐ8 AI Critique | 295 từ |

Tỉ lệ Failed 86% là vì EShop là SUT dựng để dạy kiểm thử, lỗi được gieo có chủ ý — không suy ra được cho app thật.

## 4 item tự thêm và lý do AI bỏ sót

| ID | Item | Nguyên nhân |
|---|---|---|
| GUI-GAP-01 | Giỏ hàng phải còn sau F5 | **Đặc thù SUT** — persistence là quyết định cài đặt riêng (`CartContext.jsx:6` chỉ dùng `useState`, trong khi token *có* localStorage), không suy ra từ FR-21→24 |
| GUI-GAP-02 | Thêm cùng SP 2 lần phải gộp dòng | **Cách chia prompt** — sinh item theo màn hình tĩnh nên AI chỉ soi feedback của *một* lần bấm, không thấy state tích luỹ (`CartContext.jsx:8-10` append không merge) |
| GUI-GAP-03 | `<html lang="vi">` | **Giới hạn mô hình** — AI tự nêu chiều accessibility rồi chỉ liệt kê focus ring + contrast, bỏ WCAG 3.1.1 dù bằng chứng ở `index.html:2` |
| GUI-GAP-04 | Label gắn input qua `htmlFor`/`id` | **Giới hạn mô hình** — cùng gốc GAP-03; `grep htmlFor` toàn codebase ra 0 kết quả, lỗi lặp trên cả 4 form (WCAG 1.3.1/4.1.2) |

Cả 4 item đều Failed khi thực thi và sinh ra bug thật → không phải thêm cho đủ số.

## Bug đáng chú ý (kiểu lỗi nên chủ động đi tìm)

- **Blocker** — XSS: từ khoá tìm kiếm + tên user render bằng `dangerouslySetInnerHTML`; verify bằng `<img src=x onerror=window.__xss=1>` rồi đọc `window.__xss` trong Console.
- **Blocker** — tổng tiền thanh toán là `<input>` sửa được rồi gửi thẳng lên API.
- **Major** — spec đòi lỗi form hiện *phía trên* nút submit; app để *dưới* (đo được: `errY=517` vs `btnY=425`). Đây đúng là quy tắc AI hay tự ý normalise về convention phổ biến.
- **Major** — ô mật khẩu dùng `type="text"`; `tabindex=1` phá thứ tự Tab; regex SĐT từ chối số VN bắt đầu bằng `0`.

## Điều lần sau làm khác

1. **Sửa separator bảng ngay khi sinh** — `checklist-final.md` từng có header 7 cột / separator 6 cột, GitHub sẽ không render bảng. Giờ `verify_deliverables.py` bắt được, chạy nó trước mỗi commit.
2. **Commit tách theo từng GĐ** ngay lúc làm. Lần này GĐ2/GĐ3/GĐ4 bị gộp vào một commit → không chứng minh được "một commit mỗi bước".
3. **Giữ đường dẫn output cố định từ đầu.** Prompt đã log trong Audit Report ghi `reports/<MSSV>/...` nhưng file thật nằm ở `tests/gui_and_usability_testing/` → phải sửa lại log cho khớp.
4. **Đối chiếu chéo với cross-platform trước khi chốt.** 3 item bị Task 1 kết luận sai vì chỉ xem trên một engine (`GUI-IA01-08`, `GUI-IA01-15`, `GUI-IA04-12`).
