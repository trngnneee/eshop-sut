# Gap Analysis

- **Input:** 65 item từ 4 file checklist-draft (IA-01: 16, IA-02: 16, IA-03: 15, IA-04: 18)
- **Phần A** = chẩn đoán của AI theo 8 chiều (output Prompt #3).
- **Phần B** = kết luận sau khi tự kiểm chứng trên SUT

## Phần A — Chẩn đoán AI (8 chiều)

| # | Chiều | Trạng thái | Bằng chứng trong checklist | Candidate items (CHƯA kiểm chứng — cần tự verify trên app) |
|---|---|---|---|---|
| 1 | Accessibility (keyboard ngoài tab order, ARIA, contrast, focus state) | Partially | Chỉ có alt text (IA04-07), tab order (IA01-13, IA02-15) | (a) Focus ring nhìn thấy được khi Tab qua link/nút, kể cả trên nền header xanh. (b) Contrast chữ xám nhạt: hint mật khẩu text-gray-400 (Register.jsx:65), dòng đếm (Home.jsx:111), link vàng trên xanh (App.jsx:26) — đạt WCAG 4.5:1? |
| 2 | Dark mode / theme | Absent | Không có item; app không có class `dark:` nào | Bật prefers-color-scheme: dark — trang có còn đọc được không (form control/scrollbar/alert native đổi màu theo OS, nền trang vẫn trắng) |
| 3 | RTL | Absent | Không có item | Ép dir="rtl" qua DevTools. Lưu ý: app thuần tiếng Việt, spec không yêu cầu — có thể chủ động loại khỏi scope kèm lý do |
| 4 | Viewport cực đoan (320px, zoom 200%+) | Partially | Mobile 375px (IA01-14), breakpoint grid (IA01-15) — chưa có zoom 200% và 320px | (a) Zoom 200% form Đăng nhập/Thanh toán. (b) 320px: bảng Giỏ hàng (Cart.jsx:32) và Lịch sử ĐH (Profile.jsx:172) không có wrapper cuộn ngang — khả năng vỡ |
| 5 | Network resilience | Partially (khá tốt) | IA04-08 (slow 3G), IA04-09 (backend chết), IA04-15 (lỗi thân thiện), IA04-17 (lỗi vs empty) | (a) Offline rồi bấm "Xác Nhận Thanh Toán" — nút kẹt hay báo lỗi rõ. (b) Chặn placehold.co — card ảnh broken có fallback không |
| 6 | Text-overflow / localization | Partially | IA01-16 (truncate Home), IA01-07 (separator), IA01-08 (NaN) | (a) Tên SP dài trong bảng Giỏ hàng + danh sách Checkout (không có truncate). (b) Số lượng 9999 → cột Thành tiền tràn? |
| 7 | Print / export | Absent | Không có item | Ctrl+P trang Xác nhận đơn / Lịch sử ĐH — bảng có bị cắt cột, nền đậm tốn mực. Ưu tiên thấp — cân nhắc scope |
| 8 | Browser-native quirks (autofill, bfcache) | Partially | IA02-16 (tooltip required native), IA03-10/11 (back button) | (a) Autofill: Login password type="text" + label "Username" → trình duyệt có offer lưu/điền mật khẩu đúng không. (b) Giỏ trong memory → bfcache/refresh hiện state cũ hoặc mất giỏ |

**Tóm tắt:** 0 chiều fully · 5 chiều partially (1, 4, 5, 6, 8) · 3 chiều absent (2, 3, 7). Các chiều absent đều thuộc loại có thể chủ động loại khỏi scope kèm lý do.

## Phần B — Kết luận sau khi tự kiểm chứng

| ID mới | Item bổ sung | Đã tự kiểm chứng trên SUT? | Lý do AI bỏ sót | Giải thích chi tiết |
|---|---|---|---|---|
| GUI-GAP-01 | Giỏ hàng phải được giữ lại sau khi refresh (F5) trang. Hiện tại: thêm SP vào giỏ → F5 ở bất kỳ trang nào → giỏ trống hoàn toàn | Có | Đặc thù giao diện SUT — việc giỏ hàng mất hay còn sau F5 phụ thuộc quyết định cài đặt riêng của SUT (state in-memory hay localStorage), không suy ra được từ FR-21→24 hay heuristic UI tĩnh; checklist gốc chỉ chạm tới back button (IA03-10/11), không có item nào về reload/persistence | Giỏ hàng chỉ nằm trong React state (`useState([])` — CartContext.jsx:6), không persist vào localStorage/sessionStorage (trong khi token đăng nhập CÓ dùng localStorage — AuthContext.jsx:9). Đã verify: thêm SP → F5 → `/cart` hiện "Giỏ hàng của bạn đang trống" |
| GUI-GAP-02 | Thêm cùng 1 sản phẩm nhiều lần phải gộp thành 1 dòng với số lượng cộng dồn trong Giỏ hàng. Hiện tại: bấm "Thêm vào giỏ" 2 lần trên cùng card → bảng giỏ hiện 2 dòng riêng biệt, mỗi dòng SL 1 | Có | Đặc thù giao diện SUT — lỗi chỉ lộ ra khi KẾT HỢP 2 thao tác (thêm 2 lần cùng 1 SP); checklist AI sinh theo từng màn hình tĩnh (IA04-01/02 chỉ soi feedback của 1 lần bấm) nên không bắt được hành vi tích luỹ state giữa các lần thao tác | `addToCart` luôn append item mới vào mảng, không kiểm tra trùng `id` để merge quantity (CartContext.jsx:8-10). Đã verify: thêm cùng SP 2 lần từ Trang chủ → Giỏ hàng hiện 2 dòng trùng tên. Tổng tiền vẫn đúng nhưng bảng giỏ gây nhầm lẫn và không có cách chỉnh số lượng gộp |
| GUI-GAP-03 | Thẻ `<html>` phải khai báo đúng ngôn ngữ nội dung (`lang="vi"`). Hiện tại: `<html lang="en">` trong khi toàn bộ UI là tiếng Việt | Có | Giới hạn mô hình AI — chính chiều Accessibility do AI tự đề xuất (chiều 1, Phần A) chỉ liệt kê được focus ring và contrast, bỏ qua khai báo ngôn ngữ dù đây là check WCAG cơ bản (3.1.1 Language of Page) và bằng chứng nằm ngay dòng 2 của index.html | `index.html:2` khai báo `lang="en"` — screen reader sẽ đọc text tiếng Việt bằng bộ phát âm tiếng Anh, trình duyệt có thể đề nghị dịch trang/spellcheck sai ngôn ngữ. Đã verify bằng DevTools Elements |
| GUI-GAP-04 | Mọi `<label>` phải gắn với input tương ứng qua `htmlFor`/`id` — click vào nhãn thì focus nhảy vào ô nhập, screen reader đọc được tên field. Hiện tại: toàn bộ 4 form (Đăng nhập, Đăng ký, Quên MK, Hồ sơ) không có label nào gắn `htmlFor`, input không có `id` | Có | Giới hạn mô hình AI — cùng lý do GAP-03: chiều Accessibility trong Phần A chỉ nêu focus ring + contrast, không rà tới ngữ nghĩa form (label association — WCAG 1.3.1/4.1.2) dù lỗi lặp trên cả 4 form và phát hiện được thuần bằng đọc code | Grep `htmlFor` trên toàn codebase ra 0 kết quả (Login.jsx:28,38; Register.jsx:37,47,57; ForgotPassword.jsx:49,70,80; Profile.jsx:117,128,138,148). Đã verify: click vào chữ "Mật khẩu" → con trỏ không focus vào ô input. Screen reader sẽ đọc các ô này là "edit text" không tên |
