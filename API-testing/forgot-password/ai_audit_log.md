I use AI tools for the following tasks:

API under test: FR-03 - POST /api/forgot-password (Forgot password - request OTP).
Initialized at: Sat 08/22/2026 23:32:18.68 Asia/Saigon

### Stage 1 — Domain Partition — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: Sat 08/22/2026 23:32:18.68 Asia/Saigon
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, đọc README.md và api_specification.md. Sinh domain partition test case cho tham số body `email` và header/body format liên quan: email hợp lệ đã đăng ký, email hợp lệ chưa đăng ký, email hoa/thường, email có whitespace đầu/cuối, thiếu email, email rỗng/null/whitespace, email sai format, sai kiểu dữ liệu, field thừa, và Content-Type không phải JSON. Trả về JSON array theo references/test_case_schema.md, category=DomainPartition.

- **The AI output**:

  ```json
  [
    { "temp_id": "DP-01", "title": "Email đã đăng ký với định dạng hợp lệ nhận được OTP" },
    { "temp_id": "DP-02", "title": "Email hợp lệ có chữ hoa/thường vẫn được nhận diện đúng user" },
    { "temp_id": "DP-03", "title": "Email hợp lệ nhưng chưa đăng ký" },
    { "temp_id": "DP-04", "title": "Thiếu field email trong body" },
    { "temp_id": "DP-05", "title": "Email là chuỗi rỗng" },
    { "temp_id": "DP-06", "title": "Email chỉ chứa khoảng trắng" },
    { "temp_id": "DP-07", "title": "Email null" },
    { "temp_id": "DP-08", "title": "Email sai định dạng thiếu domain" },
    { "temp_id": "DP-09", "title": "Email sai định dạng không có ký tự @" },
    { "temp_id": "DP-10", "title": "Email có khoảng trắng đầu/cuối" },
    { "temp_id": "DP-11", "title": "Email có kiểu number" },
    { "temp_id": "DP-12", "title": "Email có kiểu object" },
    { "temp_id": "DP-13", "title": "Body có field thừa role" },
    { "temp_id": "DP-14", "title": "Content-Type không phải JSON" }
  ]
  ```

### Stage 4 — Schema Validation — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: Sat 08/22/2026 23:35:34.16 Asia/Saigon
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, đối chiếu response schema từ api_specification.md và README.md. Sinh schema validation test case cho response thành công 200 gồm message/resetToken, format resetToken là OTP 6 chữ số dạng string, không có field nhạy cảm/thừa, error response cho email sai format, thiếu email, email chưa đăng ký, và lỗi server không lộ chi tiết nội bộ. Trả về JSON array theo references/test_case_schema.md, category=SchemaValidation, có schema_ref và fields_checked.

- **The AI output**:

  ```json
  [
    { "temp_id": "SV-01", "title": "Response thành công có đúng message và resetToken" },
    { "temp_id": "SV-02", "title": "resetToken trong response thành công đúng format OTP 6 chữ số" },
    { "temp_id": "SV-03", "title": "Response thành công không có field ngoài schema" },
    { "temp_id": "SV-04", "title": "Response lỗi validation email sai format có cấu trúc lỗi chuẩn" },
    { "temp_id": "SV-05", "title": "Response khi thiếu email có status và JSON error đúng" },
    { "temp_id": "SV-06", "title": "Response email chưa đăng ký không lộ schema khác biệt quá mức" },
    { "temp_id": "SV-07", "title": "Response lỗi server không lộ chi tiết nội bộ" }
  ]
  ```

### Stage 3 — Security — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: Sat 08/22/2026 23:34:25.20 Asia/Saigon
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, rà checklist SEC-01 đến SEC-07 trong references/security_requirements.md. Chọn các mục liên quan: SEC-07 cho entropy OTP, expiry/rate-limit và invalidation; SEC-05 cho SQL injection vào email; SEC-04 cho XSS/reflection qua email lỗi; SEC-02/SEC-03 để ghi rõ endpoint public và admin role không áp dụng trực tiếp; SEC-06 cho mass assignment field role/isAdmin bị bỏ qua; SEC-01 cho việc response không lộ password/hash. Bổ sung OWASP-Other cho user enumeration. Sinh JSON array theo references/test_case_schema.md, category=Security, có sec_id và attack_vector.

- **The AI output**:

  ```json
  [
    { "temp_id": "SEC-01", "title": "OTP sinh ra phải có đúng 6 chữ số" },
    { "temp_id": "SEC-02", "title": "Nhiều lần request OTP liên tiếp bị rate limit" },
    { "temp_id": "SEC-03", "title": "SQL injection payload trong field email không gây bypass hoặc SQL error" },
    { "temp_id": "SEC-04", "title": "SQL injection phá hoại trong field email không thực thi" },
    { "temp_id": "SEC-05", "title": "Email chưa đăng ký không làm lộ trạng thái tồn tại tài khoản" },
    { "temp_id": "SEC-06", "title": "XSS payload trong email không được phản chiếu như HTML thực thi" },
    { "temp_id": "SEC-07", "title": "Endpoint forgot-password không yêu cầu JWT" },
    { "temp_id": "SEC-08", "title": "Admin role check không áp dụng cho endpoint public forgot-password" },
    { "temp_id": "SEC-09", "title": "Mass assignment field role trong body bị bỏ qua" },
    { "temp_id": "SEC-10", "title": "Forgot-password response không được trả password hoặc password hash" },
    { "temp_id": "SEC-11", "title": "OTP mới không được trùng OTP liền trước cho cùng email" }
  ]
  ```

### Stage 2 — State Transition — forgot-password

- **AI tool**: Codex GPT-5
- **Date and time**: Sat 08/22/2026 23:33:36.44 Asia/Saigon
- **Your prompt**:

  Với endpoint POST /api/forgot-password thuộc FR-03, phân tích state ẩn của vòng đời OTP cho email: chưa có OTP, đã có OTP, yêu cầu OTP lại, email chưa đăng ký, OTP đã dùng sau reset, và trạng thái bị rate-limit khi yêu cầu quá nhiều lần. Sinh test case JSON theo references/test_case_schema.md, category=StateTransition, có from_state, to_state, action, expected_allowed. Chỉ tập trung vào transition do endpoint request OTP gây ra; nếu cần kiểm chứng OTP cũ/hết hạn thì ghi trong preconditions/notes rằng cần phối hợp với POST /api/reset-password.

- **The AI output**:

  ```json
  [
    { "temp_id": "ST-01", "title": "Email đã đăng ký từ trạng thái chưa có OTP chuyển sang có OTP hợp lệ" },
    { "temp_id": "ST-02", "title": "Yêu cầu OTP lần hai cho cùng email thay thế OTP cũ" },
    { "temp_id": "ST-03", "title": "Email chưa đăng ký không được chuyển sang trạng thái có OTP" },
    { "temp_id": "ST-04", "title": "Request OTP không được làm mất quyền đăng nhập hiện tại của user" },
    { "temp_id": "ST-05", "title": "Request OTP sau khi đã reset thành công tạo một OTP mới độc lập" },
    { "temp_id": "ST-06", "title": "Request OTP quá nhiều lần trong thời gian ngắn bị giới hạn" }
  ]
  ```
