I use AI tools for the following tasks:

API under test: FR-03 - POST /api/forgot-password (Forgot password - request OTP).
Initialized at: 2026-08-22 23:32:18 +07

### Stage 1 — Domain Partition — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: 2026-08-22 23:32:18 +07
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, đọc README.md và api_specification.md. Sinh domain partition test case cho tham số body `email` và header/body format liên quan: email hợp lệ đã đăng ký, email hợp lệ chưa đăng ký, email hoa/thường, email có whitespace đầu/cuối, thiếu email, email rỗng/null/whitespace, email sai format, sai kiểu dữ liệu, field thừa, và Content-Type không phải JSON. Trả về JSON array theo references/test_case_schema.md, category=DomainPartition.

- **The AI output**:

  Đã sinh 14 test case:
  - DP-01: Email đã đăng ký với định dạng hợp lệ nhận được OTP
  - DP-02: Email hợp lệ có chữ hoa/thường vẫn được nhận diện đúng user
  - DP-03: Email hợp lệ nhưng chưa đăng ký
  - DP-04: Thiếu field email trong body
  - DP-05: Email là chuỗi rỗng
  - DP-06: Email chỉ chứa khoảng trắng
  - DP-07: Email null
  - DP-08: Email sai định dạng thiếu domain
  - DP-09: Email sai định dạng không có ký tự @
  - DP-10: Email có khoảng trắng đầu/cuối
  - DP-11: Email có kiểu number
  - DP-12: Email có kiểu object
  - DP-13: Body có field thừa role
  - DP-14: Content-Type không phải JSON

  Chi tiết đầy đủ tại `01_domain_partitions.json`.

### Stage 2 — State Transition — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: 2026-08-22 23:33:36 +07
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, phân tích state ẩn của vòng đời OTP cho email: chưa có OTP, đã có OTP, yêu cầu OTP lại, email chưa đăng ký, OTP đã dùng sau reset, và trạng thái bị rate-limit khi yêu cầu quá nhiều lần. Sinh test case JSON theo references/test_case_schema.md, category=StateTransition, có from_state, to_state, action, expected_allowed. Chỉ tập trung vào transition do endpoint request OTP gây ra; nếu cần kiểm chứng OTP cũ/hết hạn thì ghi trong preconditions/notes rằng cần phối hợp với POST /api/reset-password.

- **The AI output**:

  Đã sinh 6 test case:
  - ST-01: Email đã đăng ký từ trạng thái chưa có OTP chuyển sang có OTP hợp lệ
  - ST-02: Yêu cầu OTP lần hai cho cùng email thay thế OTP cũ
  - ST-03: Email chưa đăng ký không được chuyển sang trạng thái có OTP
  - ST-04: Request OTP không được làm mất quyền đăng nhập hiện tại của user
  - ST-05: Request OTP sau khi đã reset thành công tạo một OTP mới độc lập
  - ST-06: Request OTP quá nhiều lần trong thời gian ngắn bị giới hạn

  Chi tiết đầy đủ tại `02_state_transitions.json`.

### Stage 3 — Security — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: 2026-08-22 23:34:25 +07
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, rà checklist SEC-01 đến SEC-07 trong references/security_requirements.md. Chọn các mục liên quan: SEC-07 cho entropy OTP, expiry/rate-limit và invalidation; SEC-05 cho SQL injection vào email; SEC-04 cho XSS/reflection qua email lỗi; SEC-02/SEC-03 để ghi rõ endpoint public và admin role không áp dụng trực tiếp; SEC-06 cho mass assignment field role/isAdmin bị bỏ qua; SEC-01 cho việc response không lộ password/hash. Bổ sung OWASP-Other cho user enumeration. Sinh JSON array theo references/test_case_schema.md, category=Security, có sec_id và attack_vector.

- **The AI output**:

  Đã sinh 11 test case:
  - SEC-01: OTP sinh ra phải có đúng 6 chữ số
  - SEC-02: Nhiều lần request OTP liên tiếp bị rate limit
  - SEC-03: SQL injection payload trong field email không gây bypass hoặc SQL error
  - SEC-04: SQL injection phá hoại trong field email không thực thi
  - SEC-05: Email chưa đăng ký không làm lộ trạng thái tồn tại tài khoản
  - SEC-06: XSS payload trong email không được phản chiếu như HTML thực thi
  - SEC-07: Endpoint forgot-password không yêu cầu JWT
  - SEC-08: Admin role check không áp dụng cho endpoint public forgot-password
  - SEC-09: Mass assignment field role trong body bị bỏ qua
  - SEC-10: Forgot-password response không được trả password hoặc password hash
  - SEC-11: OTP mới không được trùng OTP liền trước cho cùng email

  Chi tiết đầy đủ tại `03_security.json`.

### Stage 4 — Schema Validation — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: 2026-08-22 23:35:34 +07
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, đối chiếu response schema từ api_specification.md và README.md. Sinh schema validation test case cho response thành công 200 gồm message/resetToken, format resetToken là OTP 6 chữ số dạng string, không có field nhạy cảm/thừa, error response cho email sai format, thiếu email, email chưa đăng ký, và lỗi server không lộ chi tiết nội bộ. Trả về JSON array theo references/test_case_schema.md, category=SchemaValidation, có schema_ref và fields_checked.

- **The AI output**:

  Đã sinh 7 test case:
  - SV-01: Response thành công có đúng message và resetToken
  - SV-02: resetToken trong response thành công đúng format OTP 6 chữ số
  - SV-03: Response thành công không có field ngoài schema
  - SV-04: Response lỗi validation email sai format có cấu trúc lỗi chuẩn
  - SV-05: Response khi thiếu email có status và JSON error đúng
  - SV-06: Response email chưa đăng ký không lộ schema khác biệt quá mức
  - SV-07: Response lỗi server không lộ chi tiết nội bộ

  Chi tiết đầy đủ tại `04_schema_validation.json`.

---