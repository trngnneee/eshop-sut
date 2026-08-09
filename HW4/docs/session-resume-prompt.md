# HW04 Resume Prompt

Dùng nguyên văn prompt bên dưới nếu phiên làm việc với Claude Code bị gián đoạn (mất tiến trình
nền / mất task tracking) và cần một phiên mới tiếp tục đúng chỗ đang dang dở.

---

đã

## PROMPT

Tiếp tục thực hiện HW04 (Automation Testing) cho repo EShop tại
`C:\My Workspace\HCMUS\Test\Week 3\Hw2`, branch `HW4-Khoa`, Student ID **23127207**.

**Bối cảnh đã xác lập (không cần phân tích lại):**

- 3 tính năng tự động hóa (kế thừa từ HW02, branch `HW2-Khoa`): **FR-02** Login & Lockout (Pool A),
  **FR-07** Shopping Cart (Pool B), **FR-13** Admin Dashboard (Pool C).
- Playwright + TypeScript, chạy 3 browser (chromium/firefox/webkit) qua
  `HW4/playwright.config.ts` (đọc env `FEATURE` + `BROWSER`, report ra
  `HW4/reports/<feature>/<browser>/`, tự chèn "Run by: 23127207" + timestamp qua
  `HW4/scripts/inject-student-id.js`).
- Kho test case nguồn (từ HW02) đã copy tham chiếu vào `HW4/docs/hw02-reference/` (test-case
  design `.md`, bug report `.md`, `issues_list.txt`).
- Plan chi tiết đầy đủ tại: `C:\Users\THIEN DUC\.claude\plans\d-a-theo-file-hw4-docs-2026-hw4-automati-distributed-hippo.md`

**Ràng buộc môi trường quan trọng — LUÔN làm bước này trước khi chạy test:**

1. Port 3000 trên máy này có thể bị 1 tiến trình khác (`ship-price`, không liên quan) chiếm dụng.
   Nếu vậy: khởi động backend bằng `PORT=3001 npm start` (trong `backend/`), và dùng
   `API_BASE_URL=http://localhost:3001` khi chạy Playwright test. Đây CHỈ là workaround cục bộ
   (không commit vào `server.js`/`config.js` — mặc định vẫn là port 3000 cho bài nộp thật).
2. Cả 3 service phải chạy song song trước khi test: `backend` (3000 hoặc 3001), `frontend-web`
   (5173), `frontend-admin` (5174). Lệnh khởi động: `npm start` (backend), `npm run dev`
   (frontend-web, frontend-admin).
3. `playwright.config.ts` đã set `locale: 'vi-VN'` — bắt buộc để `toLocaleString()` format tiền
   VND (dấu chấm ngăn cách hàng nghìn) khớp với assertion trong test.
4. **CartContext (frontend-web) chỉ lưu giỏ hàng trong React state (không localStorage, không
   sync backend)** — `page.goto()` sẽ remount toàn bộ SPA và XÓA SẠCH giỏ hàng. Mọi bước điều
   hướng giữa các action trong `cart.spec.ts` PHẢI dùng click link nội bộ
   (`gotoHome`/`gotoProductDetail`/`gotoCart` helpers đã có sẵn trong file), KHÔNG được gọi
   `page.goto()` lần thứ 2 trong cùng 1 test.

**Trạng thái tiến độ (theo TaskList — dùng TaskList để xem lại):**

- ✅ Phase 0 (scaffold) — xong, đã commit.
- ✅ Phase 1a (FR-02 Login, 63 case, 3 browser) — xong, đã commit
  (`feat(hw4): automate FR-02 Login & Lockout with 63 data-driven cases`). Kết quả: 46 passed /
  17 failed giống nhau trên cả 3 browser — 12 tái hiện bug cũ, 4 bug MỚI (1 High: lộ password
  plaintext trong response login). Docs: `HW4/docs/ai-review-login.md`,
  `HW4/docs/bug-report-login.md`.
- 🔄 Phase 1b (FR-07 Cart) — ĐANG LÀM, **CHƯA COMMIT**:
  - Đã viết xong: `HW4/tests/cart.spec.ts` (32 UI case + 5 edge case), `HW4/tests/cart-api.spec.ts`
    (26 API case) = 63 case, cùng `HW4/test-data/cart-{ui,api,edge}-cases.json`.
  - **cart.spec.ts đã được sửa quan trọng** (xem ràng buộc #4 ở trên) — giữ nguyên bản sửa này.
  - Chạy thử trên chromium 2 lần đều bị gián đoạn giữa chừng (session bị ngắt) — **cần chạy lại
    từ đầu trên cả 3 browser sau khi khởi động lại service**, review kết quả, viết
    `docs/ai-review-cart.md` + `docs/bug-report-cart.md` (theo mẫu 2 file tương ứng của FR-02),
    rồi mới commit.
- ⏳ Phase 1c (FR-13 Dashboard) — đã viết xong `HW4/tests/dashboard.spec.ts` +
  `HW4/tests/dashboard-api.spec.ts` + `HW4/test-data/dashboard-{data,api}-cases.json` (32 case)
  nhưng **CHƯA CHẠY LẦN NÀO**. Cần chạy `--list` kiểm tra trước, chạy thử 1 case, rồi full 3
  browser, viết review + bug report docs, commit.
- ⏳ Phase 2 (tổng hợp README, main report, AI Audit Report, AI Critique, commit_log.txt) — chưa
  làm.
- ⏳ Phase 3 (polish `.agents/skills/playwright-skill/`, chuẩn bị kịch bản video demo) — chưa làm.
- ⏳ Phase 4 (đóng gói zip nộp bài) — chưa làm.

**Việc cần làm tiếp theo ngay:**

1. Khởi động lại backend/frontend-web/frontend-admin (theo ràng buộc #1–#2).
2. Chạy `cart.spec.ts` + `cart-api.spec.ts` trên chromium trước (verify không còn lỗi do
   page.goto() làm mất cart state), sửa tiếp nếu còn sai, rồi chạy đủ 3 browser.
3. Viết `docs/ai-review-cart.md` + `docs/bug-report-cart.md`, gắn "Run by" vào 3 report, commit.
4. Làm tương tự cho Dashboard (Phase 1c).
5. Sang Phase 2–4.

**Lưu ý về GitHub Issues:** môi trường này KHÔNG có `gh` CLI cài sẵn và không có `GITHUB_TOKEN`.
Bug report Markdown vẫn phải viết đầy đủ (bắt buộc theo đề); phần filing lên GitHub Issues thực
sự cần student tự cung cấp token hoặc cài `gh` — đã ghi rõ trong `bug-report-login.md` mẫu.
