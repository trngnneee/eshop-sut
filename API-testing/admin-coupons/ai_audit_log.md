I use AI tools for the following tasks:

API: FR-17 - Admin coupon management (`POST /api/admin/coupons`, related `DELETE /api/admin/coupons/:id`)

### Stage 1 - Domain Partition - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:13:17 +07
- **Your prompt**:

  Với endpoint FR-17 `POST /api/admin/coupons`, dựa trên spec body gồm `code`, `type`, `discount_value`, `min_order_amount`, `expired_at`, `max_uses_per_user` và yêu cầu admin JWT. Sinh domain partition test case cho từng tham số: valid điển hình, valid boundary, invalid format, invalid boundary, thiếu field bắt buộc, field thừa, sai kiểu dữ liệu, rỗng/null/whitespace. Không trộn SQLi/XSS/JWT/role security vào stage này. Trả về JSON array theo `test_case_schema.md`, `category=DomainPartition`, ghi rõ request, expected status/result, priority, parameter và partition_type.

- **The AI output**:

  Đã sinh 15 test case:
  - DP-01: Tao coupon percent hop le voi day du field bat buoc
  - DP-02: Tao coupon fixed amount hop le
  - DP-03: Tao coupon percent voi discount_value bien nho nhat hop le la 1
  - DP-04: Tao coupon percent voi discount_value bien tren hop le la 100
  - DP-05: Thieu field code khi tao coupon
  - DP-06: Code rong hoac chi co khoang trang
  - DP-07: Code bi trung voi coupon da ton tai
  - DP-08: Type nam ngoai enum hop le
  - DP-09: discount_value bang 0 cho coupon percent
  - DP-10: discount_value lon hon 100 cho coupon percent
  - DP-11: discount_value sai kieu du lieu la chuoi
  - DP-12: min_order_amount am
  - DP-13: expired_at sai dinh dang ngay
  - DP-14: max_uses_per_user bang 0
  - DP-15: Body co field thua is_active khi tao coupon

  Chi tiet day du tai `01_domain_partitions.json`.

### Stage 2 - State Transition - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:14:03 +07
- **Your prompt**:

  Với FR-17 quản lý mã giảm giá, spec không có state machine order nhưng coupon có state nghiệp vụ ẩn: non-existent, active, duplicate-created, deleted, expired, unused/used-by-user/used-beyond-limit. Sinh state transition test case cho `POST /api/admin/coupons`, `DELETE /api/admin/coupons/:id` và chỉ dùng `POST /api/apply-coupon` khi cần quan sát trạng thái sử dụng coupon. Mỗi case phải có from_state, to_state, action, expected_allowed theo `test_case_schema.md`, `category=StateTransition`.

- **The AI output**:

  Đã sinh 8 test case:
  - ST-01: Tao coupon moi chuyen tu non-existent sang active
  - ST-02: Tao lai coupon da active bi tu choi duplicate
  - ST-03: Xoa coupon active chuyen sang deleted
  - ST-04: Xoa lai coupon da deleted bi tu choi
  - ST-05: Coupon active duoc ap dung va tang usage count cua user
  - ST-06: Dung qua max_uses_per_user bi tu choi
  - ST-07: Coupon expired khong duoc ap dung
  - ST-08: Coupon deleted khong duoc ap dung

  Chi tiet day du tai `02_state_transitions.json`.

### Stage 3 - Security - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:15:08 +07
- **Your prompt**:

  Với FR-17 admin coupon API (`POST /api/admin/coupons` và `DELETE /api/admin/coupons/:id`), rà checklist security SEC-01 đến SEC-07. Bắt buộc test SEC-02 vì admin API yêu cầu JWT hợp lệ và SEC-03 vì admin API phải kiểm role=admin chứ không chỉ kiểm có token. Thêm các case phù hợp: token thiếu/rỗng/sai định dạng/hết hạn, user thường gọi API admin, SQL injection vào `code`, XSS payload trong `code`, mass assignment field ngoài spec, IDOR/scope nếu hệ thống có tenant, và response không lộ field nhạy cảm. Với SEC không áp dụng trực tiếp, ghi rõ trong notes. Trả về JSON array theo `test_case_schema.md`, `category=Security`, có `sec_id` và `attack_vector`.

- **The AI output**:

  Đã sinh 11 test case:
  - SEC-01: Goi API tao coupon khong co Authorization header
  - SEC-02: Authorization header rong khi tao coupon
  - SEC-03: Token sai dinh dang khi tao coupon
  - SEC-04: Token het han khi tao coupon
  - SEC-05: User thuong dung JWT hop le goi API admin tao coupon
  - SEC-06: User thuong dung JWT hop le xoa coupon admin
  - SEC-07: SQL injection payload trong code coupon
  - SEC-08: XSS payload trong code coupon
  - SEC-09: Mass assignment field role va created_by trong body tao coupon
  - SEC-10: IDOR: Admin cua scope khac hoac token hop le khong so huu resource thu xoa coupon
  - SEC-11: Response tao coupon khong duoc lo thong tin nhay cam cua admin

  Chi tiet day du tai `03_security.json`.

### Stage 4 - Schema Validation - admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 02:15:58 +07
- **Your prompt**:

  Với FR-17 admin coupon API, sinh schema validation test case đối chiếu response với spec: response tạo coupon thành công có đủ field coupon suy ra từ body (`id`, `code`, `type`, `discount_value`, `min_order_amount`, `expired_at`, `max_uses_per_user`), đúng kiểu dữ liệu, không có field thừa/nhạy cảm; response lỗi validation/401/403/404 là JSON có message hoặc error.message và không trả HTML/stack trace. Bao gồm cả `DELETE /api/admin/coupons/:id` vì spec cùng mục 6.4. Trả về JSON array theo `test_case_schema.md`, `category=SchemaValidation`, có `schema_ref` và `fields_checked`.

- **The AI output**:

  Đã sinh 8 test case:
  - SV-01: Response tao coupon thanh cong co du field coupon bat buoc
  - SV-02: Kieu du lieu response coupon dung voi spec
  - SV-03: Response tao coupon khong chua field ngoai schema
  - SV-04: Validation error khi thieu code co cau truc loi on dinh
  - SV-05: Unauthorized error khi thieu token dung status va schema
  - SV-06: Forbidden error khi user thuong goi API admin dung status va schema
  - SV-07: Response xoa coupon thanh cong co schema toi thieu nhat quan
  - SV-08: Response xoa coupon khong ton tai tra 404 dung schema loi

  Chi tiet day du tai `04_schema_validation.json`.
