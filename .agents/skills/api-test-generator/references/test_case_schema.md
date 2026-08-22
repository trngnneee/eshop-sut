# Test Case Schema — dùng chung cho cả 4 stage

Mỗi test case sinh ra ở Stage 1–4 là **1 object JSON** theo schema dưới đây. 4 file `01_domain_partitions.json`, `02_state_transitions.json`, `03_security.json`, `04_schema_validation.json` mỗi file là **1 mảng JSON** các object này.

## Field bắt buộc (mọi category)

| Field | Kiểu | Mô tả |
|---|---|---|
| `temp_id` | string | ID tạm trong stage, vd `"DP-01"`, `"ST-01"`, `"SEC-01"`, `"SV-01"`. Sẽ được `consolidate.py` đánh lại thành ID cuối cùng. |
| `category` | string | Một trong: `"DomainPartition"`, `"StateTransition"`, `"Security"`, `"SchemaValidation"`. |
| `endpoint` | string | Vd `"POST /api/auth/login"`. |
| `related_requirement` | string | FR-xx và/hoặc SEC-xx liên quan, vd `"FR-02"` hoặc `"FR-10, SEC-03"`. |
| `title` | string | Mô tả ngắn gọn 1 dòng, đủ hiểu không cần đọc thêm. |
| `preconditions` | string | Điều kiện tiên quyết trước khi chạy (vd "đã có tài khoản user thường đã login"). |
| `request` | object | `{ "method": "...", "path": "...", "headers": {...}, "params": {...}, "body": {...} }`. Field nào không dùng thì bỏ qua, không cần null. |
| `expected_status` | number/string | HTTP status code kỳ vọng, hoặc mô tả nếu không phải HTTP thuần (hiếm). |
| `expected_result` | string | Mô tả kỳ vọng đầy đủ hơn `expected_status` — hành vi, nội dung response, side-effect. |
| `priority` | string | `"High"`, `"Medium"`, hoặc `"Low"`. |
| `notes` | string | Ghi chú thêm — payload cụ thể, giá trị biên, giới hạn của cách test (vd "chỉ test được gián tiếp qua API"). Có thể để rỗng `""`. |

## Field riêng theo category

### DomainPartition
- `parameter` (string): tên tham số đang test.
- `partition_type` (string): 1 trong `"valid-typical"`, `"valid-boundary"`, `"invalid-format"`, `"invalid-boundary"`, `"missing-required"`, `"unexpected-extra"`, `"wrong-type"`, `"empty-null-whitespace"`.

### StateTransition
- `from_state` (string)
- `to_state` (string) — trạng thái đích **được yêu cầu** trong request, không nhất thiết là kết quả thực tế.
- `action` (string) — hành động/API call gây chuyển trạng thái.
- `expected_allowed` (boolean) — true nếu cạnh này hợp lệ theo state machine.

### Security
- `sec_id` (string) — một hoặc nhiều trong `SEC-01`…`SEC-07`, hoặc `"OWASP-Other"`.
- `attack_vector` (string) — vd `"SQL Injection"`, `"Broken Auth"`, `"Role Escalation"`, `"IDOR"`, `"Mass Assignment"`, `"XSS"`, `"OTP Brute Force"`.

### SchemaValidation
- `schema_ref` (string) — phần trong spec đang đối chiếu, vd `"Product object schema"`, `"Error response schema"`.
- `fields_checked` (array of string) — danh sách field được kiểm tra kiểu/format/bắt buộc.

## Ví dụ 1 object hoàn chỉnh (Security)

```json
{
  "temp_id": "SEC-03",
  "category": "Security",
  "endpoint": "DELETE /api/admin/products/{id}",
  "related_requirement": "FR-15, SEC-03",
  "title": "User thường dùng token hợp lệ gọi thẳng API xoá sản phẩm (admin only)",
  "preconditions": "Đã có tài khoản role=user đăng nhập thành công, có JWT hợp lệ; đã có sản phẩm id=123 tồn tại",
  "request": {
    "method": "DELETE",
    "path": "/api/admin/products/123",
    "headers": { "Authorization": "Bearer {user_token}", "X-Student-Id": "{StudentID}" }
  },
  "expected_status": 403,
  "expected_result": "API từ chối, sản phẩm id=123 vẫn còn tồn tại (không bị xoá)",
  "priority": "High",
  "sec_id": "SEC-03",
  "attack_vector": "Role Escalation",
  "notes": "Bug nếu API chỉ check có token mà không check role trong token"
}
```

## Output cuối cùng: `test_cases_master.csv`

`consolidate.py` sẽ dịch toàn bộ field trên (kể cả field riêng theo category) thành các cột CSV phẳng, cột nào không áp dụng để trống. Cột `id` cuối cùng theo format:

```
TC-<API-SLUG>-<CAT>-<NNN>
```

Với `CAT` = `DP` (DomainPartition), `ST` (StateTransition), `SEC` (Security), `SV` (SchemaValidation). Vd: `TC-LOGIN-SEC-003`.