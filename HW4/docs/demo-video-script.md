# Kịch bản quay Video Demo (Task 2 — bắt buộc ≥5 phút)

**Yêu cầu bắt buộc theo đề bài (mục 5, mục 11):**
- ≥5 phút, thuyết minh bằng **tiếng Việt**, bằng **giọng nói thật của bạn**.
- Demo **1 script automation chạy end-to-end**, bao gồm chạy trên nhiều browser + xem report HTML sinh ra.
- Thuật lại **ít nhất 1 lỗi cụ thể** đã sửa từ script do AI tạo ra.
- Phải chứng minh danh tính: **hiện mặt qua webcam** HOẶC **quay terminal chạy `whoami` và `hostname`**.
- Upload YouTube ở chế độ **Unlisted** (không public, không private).

**Tính năng đề xuất demo: FR-02 (Login & Lockout)** — vì đây là tính năng có review/fix chi tiết nhất
và dễ kể chuyện nhất (bug +2 thay vì +1, bug khóa 3 phút thay vì 30 giây).

## Checklist chuẩn bị trước khi quay

- [ ] Backend (`cd backend && npm start`), frontend-web (`cd frontend-web && npm run dev`) đang chạy.
- [ ] Terminal đã mở sẵn tại `HW4/`.
- [ ] Nếu quay bằng terminal thay vì webcam: chuẩn bị sẵn lệnh `whoami` và `hostname` để chạy đầu video.
- [ ] Mở sẵn file `tests/login.spec.ts` và `docs/ai-review-login.md` trong editor để chỉ vào lúc thuyết minh phần "lỗi đã sửa".
- [ ] Xóa/dọn report cũ nếu muốn quay lại report mới tinh: `rm -rf reports/login`.

## Kịch bản theo mốc thời gian (tổng ~6-7 phút)

**0:00–0:30 — Xác minh danh tính**
- Hiện mặt qua webcam giới thiệu ngắn: "Chào thầy/cô, em là [Họ tên], MSSV 23127207, đây là video demo HW04."
- Hoặc: mở terminal, gõ `whoami` rồi `hostname`, để rõ trên màn hình vài giây.

**0:30–1:30 — Giới thiệu tổng quan**
- Nói: đã chọn 3 tính năng FR-02/FR-07/FR-13, hôm nay demo FR-02 (Login & Lockout).
- Cho xem nhanh cấu trúc thư mục `HW4/tests/`, `HW4/test-data/` — nhấn mạnh data-driven (63 case,
  4 file JSON riêng biệt ngoài code).

**1:30–2:30 — Kể lỗi AI đã sửa (bắt buộc)**
- Mở `docs/ai-review-login.md`, đọc to mục 2 hoặc mục 3.2: ví dụ kể lại chuyện AI ban đầu dùng
  `getByLabel` nhưng SUT thiếu `htmlFor` nên phải đổi sang locator theo container text; HOẶC kể lỗi
  cô lập test ở Cart (page.goto() làm mất giỏ hàng React state) — chọn 1 câu chuyện, kể rõ:
  **AI làm gì sai → vì sao sai → mình sửa thế nào**.

**2:30–5:00 — Chạy automation thật, nhiều browser**
```bash
npm run test:login:chromium
npm run test:login:firefox
npm run test:login:webkit
```
- Vừa chạy vừa nói: "Đây là lệnh chạy trên Chromium... Firefox... WebKit", chỉ ra số case (63),
  số pass/fail hiện trên terminal.
- Có thể dùng `npm run test:matrix:login` để chạy gộp cả 3 browser + in bảng tổng kết.

**5:00–6:00 — Xem report HTML, chỉ ra "Run by"**
```bash
npx playwright show-report reports/login/chromium
```
- Chỉ vào tiêu đề/banner có chữ **"Run by: 23127207"** kèm timestamp.
- Click vào 1 test case FAIL (ví dụ TC-LOGIN-025), cho xem chi tiết assertion fail — giải thích
  đây là bug thật (BUG-FR02-A-02, khóa tài khoản 3 phút thay vì 30 giây theo spec).

**6:00–6:30 — Kết**
- Tóm tắt: 158 test case, 3 tính năng, 39 bug tìm được, đề cập file `README.md`/`docs/main-report.md`.
- Cảm ơn.

## Sau khi quay

1. Upload YouTube → chọn **Unlisted**.
2. Dán link vào:
   - `HW4/README.md` mục 1 (chỗ `[fill in the unlisted YouTube link...]`)
   - `HW4/docs/main-report.md` nếu cần
3. Xóa file `docs/demo-video-script.md` khỏi bản nộp cuối nếu muốn (không bắt buộc phải nộp kịch bản,
   chỉ là công cụ chuẩn bị).

## Video thứ 2 (mục 7 — Agent Skill, 10 điểm, khuyến khích)

Đề bài yêu cầu video **riêng** minh chứng đã dùng `.agents/skills/playwright-skill/playwright-skill.md`
end-to-end trên 1 tính năng hoàn chỉnh. Cách làm nhanh nhất: mở Claude Code (hoặc AI tool bạn dùng)
trong một phiên MỚI, gõ prompt kiểu:

> "Dùng skill `.agents/skills/playwright-skill/playwright-skill.md` để tự động hóa tính năng FR-13
> Dashboard của EShop theo đúng quy trình 7 bước trong skill."

rồi quay màn hình AI thực thi qua các bước (Analyze → Design → ... → Verify), có thuyết minh ngắn
gọn giải thích từng bước đang làm gì. Có thể gộp chung với video Task 2 (làm 1 video dài ~10 phút
với 2 phần rõ ràng) để tiết kiệm thời gian, miễn là cả 2 yêu cầu đều được thỏa mãn rõ ràng.
