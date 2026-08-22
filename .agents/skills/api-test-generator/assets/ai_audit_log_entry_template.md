# AI Audit Log Entry — Template

Copy đúng khối dưới đây cho **mỗi lượt tương tác AI** cần log, điền đủ 4 field bắt buộc theo mục 9 đề bài HW06 (`Name of the AI tool / Date and time / Your prompt / The AI output`). Không được bỏ trống field nào.

Có 2 loại entry dùng chung 1 template này:
- **Entry theo stage** (Stage 1 → 4 — Domain Partition / State Transition / Security / Schema Validation) → ghi vào `<api-slug>/ai_audit_log.md`.
- **Entry chung** cho các việc khác thuộc HW06 (viết/sửa report, AI Critique, bug report...) → ghi vào `API-testing/general_audit_log.md`, tiêu đề tự đặt mô tả đúng việc đã làm.

**Không tạo entry cho Stage 0 (setup) hay Stage 5 (consolidate)** — đó là thao tác kỹ thuật (tạo thư mục, chạy script), không phải 1 lượt tương tác AI, nên không thuộc phạm vi AI Audit Log.

```markdown
### Stage <N> — <Domain Partition | State Transition | Security | Schema Validation> — <api-slug>
(hoặc với entry chung, đổi tiêu đề thành mô tả việc đã làm, ví dụ
"### Viết main report — mục 6. Requirements" hoặc
"### Sửa lại đoạn AI Critique theo góp ý")

- **AI tool**: <tên + phiên bản model đang chạy skill này, vd "Claude Sonnet 5">
- **Date and time**: <YYYY-MM-DD HH:MM:SS TZ, lấy từ lệnh `date` thật, KHÔNG bịa>
- **Your prompt**:

  <chép nguyên văn, đầy đủ chỉ dẫn cụ thể đã dùng cho lượt tương tác này — cụ thể hoá
  theo đúng endpoint/tham số/SEC-id (nếu là entry theo stage) hoặc đúng nội dung report/
  phần đã yêu cầu (nếu là entry chung), đủ chi tiết để người khác đọc lại tái tạo được
  kết quả. KHÔNG chỉ ghi "xem SKILL.md Stage N" hay "người dùng nhờ viết report" — phải
  là prompt thật sự, ví dụ:
  "Với endpoint POST /api/auth/login, liệt kê domain partition test case cho 2 tham số
  email và password: valid điển hình, valid biên, invalid định dạng, invalid biên,
  thiếu field bắt buộc, field thừa, sai kiểu dữ liệu, rỗng/null/whitespace. Trả về JSON
  array theo schema test_case_schema.md, category=DomainPartition."
  hoặc (entry chung): "Viết giúp mục 6 (Requirements) của main report dựa trên
  test_cases_master.csv của API login, gồm mô tả pipeline generate/audit/extend/execute/
  bugs đã thực hiện.">

- **The AI output**:

  <TÓM TẮT, không dán full nội dung. Với entry theo stage: số lượng test case đã sinh +
  danh sách ngắn temp_id/title mỗi case 1 dòng + ghi chú "Chi tiết đầy đủ tại 0N_....json".
  Với entry chung: mô tả ngắn đã tạo/sửa gì, độ dài khoảng bao nhiêu, ví dụ "Đã viết mục
  6 Requirements của main report, ~450 từ, gồm mô tả 5 bước pipeline và bảng kết quả.">
```

## Ví dụ đã điền (Stage 3 — Security)

```markdown
### Stage 3 — Security — login

- **AI tool**: Claude Sonnet 5
- **Date and time**: 2026-08-22 17:05:12 +07
- **Your prompt**:

  Với endpoint POST /api/auth/login (FR-02), rà qua các SEC liên quan: SEC-02 (JWT bắt
  buộc — ở đây login không cần JWT nên bỏ qua), SEC-05 (SQL injection vào field email/
  username), SEC-07 (không áp dụng trực tiếp cho login, chỉ áp dụng cho reset password).
  Ngoài ra thêm test rate-limit/account-lockout theo FR-02 (không thuộc SEC-01..07 nhưng
  liên quan bảo mật). Sinh test case JSON theo schema test_case_schema.md,
  category=Security, field sec_id tương ứng.

- **The AI output**:

  Đã sinh 8 test case:
  - SEC-01: SQL injection payload trong field email khi login (SEC-05)
  - SEC-02: SQL injection payload trong field password khi login (SEC-05)
  - SEC-03: Login sai mật khẩu 5 lần liên tiếp → tài khoản bị khoá (FR-02 lockout)
  - SEC-04: Login khi tài khoản đang bị khoá, dù nhập đúng mật khẩu → vẫn từ chối
  - SEC-05: Login thành công không trả password/hash trong response
  - SEC-06: Header Authorization giả mạo gửi kèm request login (kỳ vọng bị bỏ qua, không ảnh hưởng)
  - SEC-07: Brute-force nhiều username khác nhau cùng 1 password phổ biến → có rate-limit
  - SEC-08: Login với email dạng NoSQL/SQL injection payload khác (`" OR "1"="1`)

  Chi tiết đầy đủ tại `03_security.json`.
```

## Ví dụ đã điền (Entry chung — sửa report)

```markdown
### Sửa lại đoạn AI Critique theo góp ý

- **AI tool**: Claude Sonnet 5
- **Date and time**: 2026-08-22 20:14:03 +07
- **Your prompt**:

  Đoạn AI Critique mình viết đang chung chung quá, sửa lại cho cụ thể hơn: nêu rõ ví dụ
  Stage 3 (Security) ban đầu AI generic bỏ sót case role-escalation SEC-03 vì spec không
  nói rõ field role nằm trong JWT payload, mình phải tự bổ sung.

- **The AI output**:

  Đã viết lại đoạn AI Critique (~260 từ), thay ví dụ chung chung bằng ví dụ cụ thể
  SEC-03/role escalation nêu ở prompt, giữ nguyên phần còn lại của đoạn.
```