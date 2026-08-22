# AI Audit Log Entry — Template

Copy đúng khối dưới đây cho **mỗi stage** (Stage 1 → 5), điền đủ 4 field bắt buộc theo mục 9 đề bài HW06 (`Name of the AI tool / Date and time / Your prompt / The AI output`). Không được bỏ trống field nào; nếu 1 field thật sự không áp dụng (vd Stage 5 dùng script chứ không phải AI), ghi rõ lý do thay vì để trống hoặc bịa.

```markdown
### Stage <N> — <Domain Partition | State Transition | Security | Schema Validation | Consolidate> — <api-slug>

- **AI tool**: <tên + phiên bản model đang chạy skill này, vd "Claude Sonnet 5">
- **Date and time**: <YYYY-MM-DD HH:MM:SS TZ, lấy từ lệnh `date` thật, KHÔNG bịa>
- **Your prompt**:

  <chép nguyên văn, đầy đủ chỉ dẫn cụ thể đã dùng để sinh stage này — cụ thể hoá theo đúng
  endpoint/tham số/SEC-id đang xử lý, đủ chi tiết để người khác đọc lại tái tạo được kết quả.
  KHÔNG chỉ ghi "xem SKILL.md Stage N" — phải là prompt thật sự, ví dụ:
  "Với endpoint POST /api/auth/login, liệt kê domain partition test case cho 2 tham số
  email và password: valid điển hình, valid biên, invalid định dạng, invalid biên,
  thiếu field bắt buộc, field thừa, sai kiểu dữ liệu, rỗng/null/whitespace. Trả về JSON
  array theo schema test_case_schema.md, category=DomainPartition.">

- **The AI output**:

  ```json
  <dán nguyên khối JSON đã sinh ra ở stage này (nội dung của 0N_....json).
  Nếu quá dài (nhiều chục KB), có thể rút gọn thành danh sách temp_id + title,
  kèm ghi chú "full JSON tại 0N_....json trong cùng thư mục" — nhưng ưu tiên dán
  đầy đủ nếu không quá dài.>
  ```
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

  ```json
  [
    {
      "temp_id": "SEC-01",
      "category": "Security",
      "endpoint": "POST /api/auth/login",
      "related_requirement": "FR-02, SEC-05",
      "title": "SQL injection payload trong field email khi login",
      "preconditions": "Không có, gọi trực tiếp",
      "request": {
        "method": "POST",
        "path": "/api/auth/login",
        "body": { "email": "admin' OR '1'='1", "password": "anything" }
      },
      "expected_status": 401,
      "expected_result": "Đăng nhập thất bại, không bypass được auth, không lộ SQL error",
      "priority": "High",
      "sec_id": "SEC-05",
      "attack_vector": "SQL Injection",
      "notes": ""
    }
  ]
  ```
```