# HW06 — API Testing · Bộ tài liệu & Kế hoạch thực thi

> **MSSV:** 23127207 · **Repo:** https://github.com/trngnneee/eshop-sut · **Branch làm bài:** `HW6-Khoa`
> **SUT:** EShop (Node.js + Express + SQLite) — `http://localhost:3000`
> **Nguồn yêu cầu:** `Requirements/Requirements.pdf` (đề HW06) + `Requirements/Rule.pdf` (quy ước quản lý test case trên GitHub)

---

## 1. Bộ tài liệu này gồm gì

| File | Nội dung | Dùng để làm gì |
| :--- | :--- | :--- |
| [`01-requirements-analysis.md`](01-requirements-analysis.md) | Bóc tách toàn bộ đề bài thành danh sách yêu cầu có mã (R-xx), tiêu chí nghiệm thu, rubric, ràng buộc chống gian lận AI | Bảng đối chiếu "đã làm đủ chưa" |
| [`02-sut-defect-catalog.md`](02-sut-defect-catalog.md) | Phân tích SUT: đặc tả (README.md) đối chiếu mã nguồn (`backend/server.js`), danh mục lỗi đã cài sẵn kèm số dòng | **Oracle** để audit test case do AI sinh + nguồn cho bug report |
| [`03-execution-plan.md`](03-execution-plan.md) | Kế hoạch thực thi chia phase/task cho Codex: input, output, Definition of Done, commit message từng bước | File Codex đọc để làm bài |
| [`04-deliverables-checklist.md`](04-deliverables-checklist.md) | Checklist nộp bài: cấu trúc file `.zip`, mapping deliverable ↔ mục đề bài, bảng tự chấm điểm | Kiểm tra trước khi nộp |

---

## 2. Bộ 3 API đã chọn (đã chốt)

| # | Pool | API | FR liên quan | Vì sao chọn |
| :-: | :--- | :--- | :--- | :--- |
| **API-1** | A — Authentication | `POST /api/login` | FR-02, SEC-01, SEC-02, SEC-05 | Có state machine khoá tài khoản; nhiều miền dữ liệu trên `email`/`password`; lộ mật khẩu plaintext trong response |
| **API-2** | B — Cart & Checkout | `POST /api/checkout` | FR-08, FR-10, SEC-02 | Là điểm **tạo đơn hàng** (`pending`) → cửa vào state machine FR-10; backend tin `total_amount` do client gửi |
| **API-3** | C — Web Admin | `PUT /api/admin/orders/:id/status` | FR-10, FR-12, FR-18, SEC-03 | Chuyển trạng thái đơn hàng → phủ trọn ma trận state transition 5×5; không kiểm tra `role=admin` → role escalation |

**Vì sao bộ 3 này hợp lý:** ba API nối thành **một luồng end-to-end** — `login` lấy token → `checkout` tạo đơn `pending` → `admin/orders/:id/status` chuyển trạng thái. Nhờ đó Postman có thể chain biến (`{{token}}`, `{{orderId}}`) một cách tự nhiên, và bộ test phủ đủ 4 nhóm bắt buộc của đề: **domain partitions**, **state transitions (FR-10)**, **security (SEC-01→SEC-07)**, **schema validation**.

---

## 3. Ranh giới AGENT vs HUMAN (bắt buộc đọc)

Đề bài có **mục 11 — Anti-AI-Cheat Constraints**. Ba thứ dưới đây TA sẽ kiểm tra trực tiếp và **không được để AI sinh ra**:

| Hạng mục | Ai làm | Ghi chú |
| :--- | :--- | :--- |
| Sơ đồ AI test-generator (`test-generator/diagram.png`) | **HUMAN** | Phải tự vẽ (draw.io / Excalidraw / vẽ tay chụp lại). Quyết định thiết kế là của sinh viên. Codex **không** được sinh sơ đồ. |
| Screenshot console chứng minh header `X-Student-Id: 23127207` | **HUMAN** | Chụp từ Postman Console sau khi chạy pre-request script |
| Screenshot GitHub Issues (mỗi bug 1 ảnh) | **HUMAN** | Chụp trang issue thật đã tạo |
| Screenshot 2 lần chạy CI/CD (1 xanh, 1 đỏ) | **HUMAN** | Chụp từ tab Actions của repo |
| AI Critique 200–300 từ | **HUMAN** | Là bài tự phản tỉnh; Codex chỉ được chuẩn bị **dữ liệu đầu vào** (bảng "AI sai ở đâu"), không viết hộ đoạn văn |
| Newman run output (hostname `localhost`/`127.0.0.1`) | AGENT chạy thật | Phải là output chạy thật, không được chế |
| Toàn bộ phần còn lại | **AGENT (Codex)** | Xem `03-execution-plan.md` |

---

## 4. Bốn quy tắc vàng khi Codex chạy plan

1. **Mỗi bước một commit.** Đề bài mục 12 yêu cầu commit riêng cho từng bước (generate / audit / extend / execute) của **từng** API. Commit message đã quy định sẵn trong `03-execution-plan.md`.
2. **Ghi AI Audit ngay tại chỗ.** Mỗi lần gọi AI để sinh test case phải append ngay 1 entry (tool, thời gian, prompt đầy đủ, output) vào `hw06/report/ai-audit-report.md`. Ghi bù sau sẽ thiếu và mất điểm mục 9.
3. **Không bịa bằng chứng.** Không tạo screenshot giả, không viết sẵn số liệu Newman chưa chạy, không tạo link CI chưa tồn tại. Chỗ nào cần người làm thì để placeholder `<!-- TODO(HUMAN): ... -->` và ghi vào checklist.
4. **Audit là bắt buộc, không phải hình thức.** Mọi test case AI sinh ra phải được đối chiếu với `02-sut-defect-catalog.md` và gán nhãn VALID / INVALID / INCOMPLETE kèm lý do. Đây là phần chiếm điểm cao nhất và cũng là phần AI hay làm ẩu nhất.
