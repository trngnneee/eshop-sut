I use AI tools for the following tasks:

API đang xử lý: FR-09 `POST /api/apply-coupon` - áp dụng mã giảm giá, tính `discount_amount` và `final_amount`.
Khởi tạo log: 2026-08-23 01:03:00 +07

### Stage 1 — Domain Partition — apply-coupon

- **AI tool**: GPT-5 Codex
- **Date and time**: 2026-08-23 01:03:00 +07
- **Your prompt**:

  Hãy tạo test case cho Stage 1 — Domain Partitions với API được chọn là FR-09 `POST /api/apply-coupon`. Dựa trên `api_specification.md`: endpoint nhận Body JSON gồm `code`, `total_amount`, `user_id`; mô tả là tính toán tổng tiền sau khi giảm và trả JSON chứa `discount_amount` và `final_amount`. Duyệt từng tham số body và header liên quan một cách có hệ thống: valid điển hình, valid biên, invalid định dạng, invalid biên, thiếu field bắt buộc, field thừa/không mong đợi, sai kiểu dữ liệu, rỗng/null/whitespace. Không trộn logic bảo mật vào Stage 1. Trả về JSON array theo `references/test_case_schema.md`, mọi object có `category="DomainPartition"`, endpoint `POST /api/apply-coupon`, related_requirement `FR-09`.

- **The AI output**:

  Đã sinh 17 test case:
  - DP-01: Áp dụng mã coupon hợp lệ với tổng tiền đủ điều kiện
  - DP-02: Code hợp lệ có chữ thường cần được xử lý nhất quán
  - DP-03: Code không tồn tại trong hệ thống
  - DP-04: Thiếu field code trong body
  - DP-05: Code là chuỗi rỗng
  - DP-06: Code chỉ chứa khoảng trắng
  - DP-07: Code sai kiểu dữ liệu là number
  - DP-08: total_amount bằng 0
  - DP-09: total_amount là số âm
  - DP-10: total_amount là số dương rất nhỏ
  - DP-11: total_amount sai kiểu dữ liệu là string
  - DP-12: Thiếu field total_amount trong body
  - DP-13: user_id không tồn tại
  - DP-14: user_id sai kiểu dữ liệu là string
  - DP-15: Thiếu field user_id trong body
  - DP-16: Body có field thừa discount_amount do client gửi lên
  - DP-17: Content-Type không phải application/json

  Chi tiết đầy đủ tại `01_domain_partitions.json`.

### Stage 2 — State Transition — apply-coupon

- **AI tool**: GPT-5 Codex
- **Date and time**: 2026-08-23 01:07:00 +07
- **Your prompt**:

  Hãy tạo test case cho Stage 2 — State Transitions với API được chọn là FR-09 `POST /api/apply-coupon`. Dựa trên `api_specification.md`: endpoint nhận Body JSON gồm `code`, `total_amount`, `user_id`, dùng để tính `discount_amount` và `final_amount`; spec quản lý coupon có các field liên quan state ẩn như `min_order_amount`, `expired_at`, `max_uses_per_user`, và có thao tác xóa coupon `DELETE /api/admin/coupons/:id`. Vì FR-09 không có state machine chính thức như order, hãy xác định state ẩn của coupon/user/order amount: coupon active, expired, deleted; order amount below/at/above minimum; user chưa dùng, đã dùng hết quota; user khác còn quota. Sinh test case JSON theo `references/test_case_schema.md`, `category="StateTransition"`, có đủ `from_state`, `to_state`, `action`, `expected_allowed`, bao gồm cả chuyển trạng thái hợp lệ và không hợp lệ. Không trộn logic security vào Stage 2.

- **The AI output**:

  Đã sinh 8 test case:
  - ST-01: Coupon còn hiệu lực chuyển từ chưa áp dụng sang đã áp dụng
  - ST-02: Coupon hết hạn không được chuyển sang trạng thái đã áp dụng
  - ST-03: Coupon đã bị xóa không được áp dụng
  - ST-04: Đơn hàng chưa đạt min_order_amount không được áp dụng coupon
  - ST-05: Đơn hàng vừa đạt min_order_amount được áp dụng coupon
  - ST-06: User đã dùng hết max_uses_per_user không được áp dụng lại coupon
  - ST-07: User khác vẫn được áp dụng coupon khi quota của chính họ còn
  - ST-08: Coupon vừa hết hạn sau một lần áp dụng thành công không được áp dụng tiếp

  Chi tiết đầy đủ tại `02_state_transitions.json`.

### Stage 3 — Security — apply-coupon

- **AI tool**: GPT-5 Codex
- **Date and time**: 2026-08-23 01:09:00 +07
- **Your prompt**:

  Hãy tạo test case cho Stage 3 — Security với API được chọn là FR-09 `POST /api/apply-coupon`. Dựa trên `api_specification.md`: endpoint nhận Body JSON gồm `code`, `total_amount`, `user_id`, dùng để tính `discount_amount` và `final_amount`; spec không ghi rõ Authorization cho endpoint này, nhưng coupon có trạng thái/giới hạn theo user và có các field quản lý như `min_order_amount`, `expired_at`, `max_uses_per_user`. Rà checklist SEC-01 đến SEC-07 theo `references/security_requirements.md`: SEC-01 kiểm gián tiếp response không rò rỉ password/hash; SEC-02 kiểm broken auth/JWT và user_id mismatch vì endpoint tác động quota/giảm giá theo user; SEC-03 không áp dụng trực tiếp vì không phải admin API; SEC-04 kiểm XSS payload trong code nếu message echo ra UI; SEC-05 kiểm SQL injection vào code; SEC-06 không áp dụng trực tiếp vì không phải update profile nhưng cần xét mass assignment/parameter tampering tương đương; SEC-07 không áp dụng vì không liên quan OTP. Bổ sung OWASP-Other cho IDOR, parameter tampering, business logic abuse, rate limiting. Sinh JSON array theo `references/test_case_schema.md`, `category="Security"`, có `sec_id` và `attack_vector` rõ ràng cho từng case.

- **The AI output**:

  Đã sinh 10 test case:
  - SEC-01: SQL injection payload trong field code không được làm bypass coupon lookup
  - SEC-02: SQL injection destructive payload trong code không được gây lỗi DB hoặc thay đổi dữ liệu
  - SEC-03: Không cho client tự áp dụng coupon cho user_id khác khi không có JWT
  - SEC-04: Token hợp lệ của user này không được áp dụng coupon thay cho user khác
  - SEC-05: Client không được tự gửi discount_amount để tăng mức giảm
  - SEC-06: Client không được tự gửi final_amount để thao túng tổng tiền cuối
  - SEC-07: Không cho dùng total_amount giả lớn hơn giỏ hàng thật để đạt min_order_amount
  - SEC-08: Rate limit khi brute-force nhiều coupon code
  - SEC-09: Response apply-coupon không được rò rỉ password hoặc passwordHash của user
  - SEC-10: XSS payload trong code không được phản hồi như HTML thực thi được

  Chi tiết đầy đủ tại `03_security.json`.

### Stage 4 — Schema Validation — apply-coupon

- **AI tool**: GPT-5 Codex
- **Date and time**: 2026-08-23 01:11:00 +07
- **Your prompt**:

  Hãy tạo test case cho Stage 4 — Schema Validation với API được chọn là FR-09 `POST /api/apply-coupon`. Dựa trên `api_specification.md`: endpoint nhận Body JSON gồm `code`, `total_amount`, `user_id`; response thành công phải là JSON chứa `discount_amount` và `final_amount`. Đối chiếu hình dạng response với spec, không kiểm sâu business logic: response 2xx phải có đủ field bắt buộc, đúng kiểu dữ liệu number, không thiếu/không thừa field không được mô tả, giữ invariant `final_amount = total_amount - discount_amount`; response lỗi cho coupon không tồn tại, thiếu field bắt buộc, sai kiểu dữ liệu phải có JSON error schema ổn định và không trả stack trace/HTML/field success. Kiểm tra thêm response không lộ password/passwordHash/token nội bộ. Sinh JSON array theo `references/test_case_schema.md`, `category="SchemaValidation"`, có `schema_ref` và `fields_checked` rõ ràng.

- **The AI output**:

  Đã sinh 7 test case:
  - SV-01: Response thành công phải có đủ discount_amount và final_amount
  - SV-02: discount_amount và final_amount phải là number
  - SV-03: final_amount phải khớp công thức total_amount - discount_amount
  - SV-04: Response thành công không trả thừa object coupon hoặc user
  - SV-05: Coupon không tồn tại trả error schema, không trả success schema
  - SV-06: Thiếu field code trả lỗi validation có message rõ ràng
  - SV-07: Sai kiểu total_amount trả lỗi validation JSON ổn định

  Chi tiết đầy đủ tại `04_schema_validation.json`.
