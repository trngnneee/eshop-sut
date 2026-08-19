# AI Audit Report — HW06 API Testing

> **Declaration:** I use AI tools for the following tasks,
> phân tích đặc tả, thiết kế test case theo từng kỹ thuật, rà soát độ bao phủ, tạo skeleton automation và hỗ trợ tổng hợp báo cáo. Mọi output đều phải được người học kiểm tra trước khi nộp.

## Công cụ đã dùng

| Công cụ | Phiên bản / mô hình | Vai trò | Quy tắc human review |
| :--- | :--- | :--- | :--- |
| OpenAI Codex | GPT-5 Codex (API workspace agent) | Phân tích repo, sinh và triển khai artifact HW06 | Đối chiếu `README.md`, `api_specification.md`, mã nguồn SUT và ký xác nhận từng bảng audit |

## Quy ước ghi log

- Mỗi kỹ thuật được thực hiện như một bước riêng, không dùng một prompt tổng để sinh toàn bộ suite.
- Thời gian dùng múi giờ `Asia/Bangkok` (UTC+07:00).
- Phần **Output** là bản tóm tắt có truy vết đến file output đầy đủ; không thay thế artifact gốc.
- Nhãn audit chỉ là đề xuất của AI cho đến khi người học ký dòng `Reviewed by` trong file `02-audit.md` tương ứng.

## Nhật ký tương tác

<!-- Các entry được append ngay sau mỗi bước generate/audit. -->

### INT-000 — Khởi tạo yêu cầu và chia pipeline

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:34:00+07:00`
- **Prompt của người học:** `dựa trên docs/hw06 để thực hiện toàn bộ requirements để đmả bảo được 100% số điểm`
- **Output của AI:** Đọc toàn bộ bộ tài liệu `docs/hw06`, xác nhận branch `HW6-Khoa`, lập kế hoạch Phase 0→9 và nhận diện các checkpoint bắt buộc do HUMAN thực hiện. AI không tạo bằng chứng giả và không bỏ qua human review của R-02.

### API-1 / P1 — Phân tích input và state, chưa sinh test case

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:54:00+07:00`
- **Prompt:**

  > Đối chiếu `POST /api/login` trong API specification, FR-02, SEC-01/02/05 và mã nguồn SUT. Chưa sinh test case. Chỉ liệt kê toàn bộ input ở body/header, kiểu, tính bắt buộc, partition có ý nghĩa; sau đó mô hình hóa `login_attempts` và `locked_until`, bao gồm đường reset và hết hạn. Phân biệt rõ ràng ràng buộc nghiệp vụ với ràng buộc riêng của HW06.

- **Output:** Nhận diện `email`, `password`, `Content-Type`, `X-Student-Id` và field thừa; tạo bảy trạng thái/transition từ Active-0 → Active-1 → Active-2 → Locked-30s → Lock-expired, cùng hai đường reset. Output đầy đủ ở `api-01-login/01-ai-generated.md` mục P1.

### API-1 / P2 — Domain partition và boundary value

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:56:00+07:00`
- **Prompt:**

  > Chỉ dùng mô hình input của P1. Áp dụng Equivalence Partitioning và Boundary Value Analysis cho từng input của `POST /api/login`. Mỗi invalid partition là một case độc lập. Expected phải phát biểu theo đặc tả; nếu phải giả định, vẫn giữ nguyên giả định để bước Human Audit phát hiện. Định dạng: ID, nhóm, tiêu đề, precondition, test data, HTTP status và body mong đợi.

- **Output:** Sinh 16 case `TC-API-LOGIN-001..016`: valid credential, wrong credential, unknown email, missing/empty/null/wrong-type fields, malformed/whitespace email, body array, missing content type và field thừa. AI đã tạo ba giả định cần audit: login password phải mạnh, email được trim, thiếu content type luôn là `415`.

### API-1 / P3 — State-transition coverage

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:58:00+07:00`
- **Prompt:**

  > Chỉ sinh test state transition dựa trên state model P1 và FR-02. Phủ threshold 3 lần sai, BVA thời gian 29/31 giây, đăng nhập đúng reset chuỗi sai và lần sai đầu tiên sau reset. Không dùng seed user chung cho case khóa tài khoản; nêu rõ precondition dùng user dùng-một-lần.

- **Output:** Sinh 8 case `TC-API-LOGIN-017..024`, phủ lần sai 1/2/3, request trong lock, 29 s, 31 s, reset sau hai lần sai và một lần sai sau reset. Các expected giữ đúng “+1, khóa 30 s” của FR-02 nên dự kiến phát hiện D-LOGIN-01 và D-LOGIN-02.

### API-1 / P4 — Security coverage

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:00:00+07:00`
- **Prompt:**

  > Chỉ sinh security cases áp dụng được cho login từ SEC-01..SEC-07: SQL injection ở từng credential, XSS/non-reflection, sensitive-field leakage, body role injection, khả năng dùng JWT trên protected endpoint và account-state disclosure. Expected là hành vi an toàn; nếu output lỡ mô tả tấn công thành công, giữ nguyên để Human Audit gắn INVALID.

- **Output:** Sinh 8 case `TC-API-LOGIN-025..032`. Một output sai có chủ đích giữ nguyên lịch sử: case 025 ghi “SQLi bypass thành công”; audit phải sửa thành `401` vì query thực tế parameterized. Cases 028/029 nhắm trực tiếp D-LOGIN-03; case 032 nhắm D-LOGIN-07.

### API-1 / P5 — Schema validation

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:01:00+07:00`
- **Prompt:**

  > Chỉ sinh schema cases cho nhánh success và invalid credential của login. Kiểm tra required fields, JSON content type, kiểu dữ liệu và negative schema cho field nhạy cảm. Không tự bịa cấu trúc `user`; mọi điểm chưa được API spec định nghĩa phải được nêu để audit.

- **Output:** Sinh 4 case `TC-API-LOGIN-033..036`: minimal success schema, JSON content type, error schema và extra-field rule. AI đã diễn đạt quá mạnh ở 033/035/036 vì API spec không công bố exact `user`/error schema; bước audit hạ thành contract tối thiểu + negative sensitive fields.

### API-1 / Audit — Gắn nhãn và sửa output

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:01:04+07:00`
- **Prompt:**

  > Audit từng dòng trong 36 case vừa sinh bằng bốn oracle: FR-02/SEC, API spec, mã nguồn login và defect catalog. Với từng case gắn đúng một nhãn VALID/INVALID/INCOMPLETE, giải thích cụ thể, và viết bản sửa cho mọi INVALID/INCOMPLETE. Không đổi expected theo hành vi lỗi hiện tại. Chừa checkpoint để sinh viên tự review và ký.

- **Output:** Audit đủ `36/36`: `28 VALID`, `3 INVALID`, `5 INCOMPLETE`. Tám bản sửa cụ thể dành cho cases 007, 008, 009, 015, 025, 033, 035, 036. Toàn bộ bảng và worksheet ký xác nhận nằm ở `api-01-login/02-audit.md`.
