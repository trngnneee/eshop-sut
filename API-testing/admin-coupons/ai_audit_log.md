I use AI tools for the following tasks:

API: FR-17 - Admin coupon management (`POST /api/admin/coupons`, related `DELETE /api/admin/coupons/:id`)

### Stage 1 - Domain Partition - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:13:17 +07
- **Your prompt**:

  Với endpoint FR-17 `POST /api/admin/coupons`, dựa trên spec body gồm `code`, `type`, `discount_value`, `min_order_amount`, `expired_at`, `max_uses_per_user` và yêu cầu admin JWT. Sinh domain partition test case cho từng tham số: valid điển hình, valid boundary, invalid format, invalid boundary, thiếu field bắt buộc, field thừa, sai kiểu dữ liệu, rỗng/null/whitespace. Không trộn SQLi/XSS/JWT/role security vào stage này. Trả về JSON array theo `test_case_schema.md`, `category=DomainPartition`, ghi rõ request, expected status/result, priority, parameter và partition_type.

- **The AI output**:

  Đã sinh 15 test case:
  - DP-01: Tạo coupon percent hợp lệ với đầy đủ field bắt buộc
  - DP-02: Tạo coupon fixed amount hợp lệ
  - DP-03: Tạo coupon percent với discount_value biên nhỏ nhất hợp lệ là 1
  - DP-04: Tạo coupon percent với discount_value biên trên hợp lệ là 100
  - DP-05: Thiếu field code khi tạo coupon
  - DP-06: Code rỗng hoặc chỉ có khoảng trắng
  - DP-07: Code bị trùng với coupon đã tồn tại
  - DP-08: Type nằm ngoài enum hợp lệ
  - DP-09: discount_value bằng 0 cho coupon percent
  - DP-10: discount_value lớn hơn 100 cho coupon percent
  - DP-11: discount_value sai kiểu dữ liệu là chuỗi
  - DP-12: min_order_amount âm
  - DP-13: expired_at sai định dạng ngày
  - DP-14: max_uses_per_user bằng 0
  - DP-15: Body có field thừa is_active khi tạo coupon

  Chi tiết đầy đủ tại `01_domain_partitions.json`.

### Stage 2 - State Transition - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:14:03 +07
- **Your prompt**:

  Với FR-17 quản lý mã giảm giá, spec không có state machine order nhưng coupon có state nghiệp vụ ẩn: non-existent, active, duplicate-created, deleted, expired, unused/used-by-user/used-beyond-limit. Sinh state transition test case cho `POST /api/admin/coupons`, `DELETE /api/admin/coupons/:id` và chỉ dùng `POST /api/apply-coupon` khi cần quan sát trạng thái sử dụng coupon. Mỗi case phải có from_state, to_state, action, expected_allowed theo `test_case_schema.md`, `category=StateTransition`.

- **The AI output**:

  Đã sinh 8 test case:
  - ST-01: Tạo coupon mới chuyển từ non-existent sang active
  - ST-02: Tạo lại coupon đã active bị từ chối duplicate
  - ST-03: Xóa coupon active chuyển sang deleted
  - ST-04: Xóa lại coupon đã deleted bị từ chối
  - ST-05: Coupon active được áp dụng và tăng usage count của user
  - ST-06: Dùng quá max_uses_per_user bị từ chối
  - ST-07: Coupon expired không được áp dụng
  - ST-08: Coupon deleted không được áp dụng

  Chi tiết đầy đủ tại `02_state_transitions.json`.

### Stage 3 - Security - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:15:08 +07
- **Your prompt**:

  Với FR-17 admin coupon API (`POST /api/admin/coupons` và `DELETE /api/admin/coupons/:id`), rà checklist security SEC-01 đến SEC-07. Bắt buộc test SEC-02 vì admin API yêu cầu JWT hợp lệ và SEC-03 vì admin API phải kiểm role=admin chứ không chỉ kiểm có token. Thêm các case phù hợp: token thiếu/rỗng/sai định dạng/hết hạn, user thường gọi API admin, SQL injection vào `code`, XSS payload trong `code`, mass assignment field ngoài spec, IDOR/scope nếu hệ thống có tenant, và response không lộ field nhạy cảm. Với SEC không áp dụng trực tiếp, ghi rõ trong notes. Trả về JSON array theo `test_case_schema.md`, `category=Security`, có `sec_id` và `attack_vector`.

- **The AI output**:

  Đã sinh 11 test case:
  - SEC-01: Gọi API tạo coupon không có Authorization header
  - SEC-02: Authorization header rỗng khi tạo coupon
  - SEC-03: Token sai định dạng khi tạo coupon
  - SEC-04: Token hết hạn khi tạo coupon
  - SEC-05: User thường dùng JWT hợp lệ gọi API admin tạo coupon
  - SEC-06: User thường dùng JWT hợp lệ xóa coupon admin
  - SEC-07: SQL injection payload trong code coupon
  - SEC-08: XSS payload trong code coupon
  - SEC-09: Mass assignment field role và created_by trong body tạo coupon
  - SEC-10: IDOR: Admin của scope khác hoặc token hợp lệ không sở hữu resource thử xóa coupon
  - SEC-11: Response tạo coupon không được lộ thông tin nhạy cảm của admin

  Chi tiết đầy đủ tại `03_security.json`.

### Stage 4 - Schema Validation - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:15:58 +07
- **Your prompt**:

  Với FR-17 admin coupon API, sinh schema validation test case đối chiếu response với spec: response tạo coupon thành công có đủ field coupon suy ra từ body (`id`, `code`, `type`, `discount_value`, `min_order_amount`, `expired_at`, `max_uses_per_user`), đúng kiểu dữ liệu, không có field thừa/nhạy cảm; response lỗi validation/401/403/404 là JSON có message hoặc error.message và không trả HTML/stack trace. Bao gồm cả `DELETE /api/admin/coupons/:id` vì spec cùng mục 6.4. Trả về JSON array theo `test_case_schema.md`, `category=SchemaValidation`, có `schema_ref` và `fields_checked`.

- **The AI output**:

  Đã sinh 8 test case:
  - SV-01: Response tạo coupon thành công có đủ field coupon bắt buộc
  - SV-02: Kiểu dữ liệu response coupon đúng với spec
  - SV-03: Response tạo coupon không chứa field ngoài schema
  - SV-04: Validation error khi thiếu code có cấu trúc lỗi ổn định
  - SV-05: Unauthorized error khi thiếu token đúng status và schema
  - SV-06: Forbidden error khi user thường gọi API admin đúng status và schema
  - SV-07: Response xóa coupon thành công có schema tối thiểu nhất quán
  - SV-08: Response xóa coupon không tồn tại trả 404 đúng schema lỗi

  Chi tiết đầy đủ tại `04_schema_validation.json`.
