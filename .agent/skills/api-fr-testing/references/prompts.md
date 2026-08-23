# Parameterized prompt sequence (Phase 2)

Drive the AI **one technique per chat**, save each prompt + output as an AI-audit log. Replace
the `<...>` placeholders. The context block goes at the top of every session.

## Context block (paste first, every time)

```
Bối cảnh: t đang kiểm thử API cho <SUT name> (<stack>, chạy <base URL>).
Endpoint đang test: <METHOD PATH> — map FR-<xx> (<mô tả FR ngắn>).
Đây là source, m BÁM theo, ĐỪNG đoán hành vi:
- FR spec: <dán đoạn FR trong README>
- Route handler: <dán đoạn server code>
- DB schema bảng liên quan: <dán CREATE TABLE>
- Tài khoản/secret nếu có: <...>

Quy ước BẮT BUỘC:
- Expected LẤY THEO SPEC (FR). Code lệch spec = BUG → GIỮ expected theo spec, đừng sửa cho pass.
- Đừng bịa status code theo REST convention; suy từ code t đưa.
- Mọi request kèm header <X-Student-Id: ...> (nếu đề yêu cầu).
Output: 1 bảng Markdown đúng cột:
TC-ID | API | FR/SEC | Technique | Precondition | Method+URL | Headers | Body | Expected status | Expected body/schema | Priority
TC-ID đánh <PREFIX>-001, 002, ... Xác nhận đã đọc source rồi bắt đầu.
```

## Prompt 1 — Equivalence partitioning + boundary value

```
Kỹ thuật phân hoạch tương đương + phân tích giá trị biên. Với MỖI tham số (<liệt kê param:
path/query/body field>), tách 1 bảng partition (valid classes + mỗi invalid class 1 lớp),
rồi sinh test case + các giá trị biên (min-1/min/min+1/max-1/max/max+1).
Nhớ: input vi phạm ràng buộc FR → expected là mã lỗi theo spec, kể cả khi m đoán SUT trả khác.
Bảng <PREFIX>-###.
```

## Prompt 2 — State-transition (chỉ khi FR có state machine)

```
Endpoint này có state machine (FR-<xx>). Xuất bảng chuyển trạng thái đầy đủ: mỗi from-state ×
action → expected LẤY THEO SPEC. Trạng thái nào spec cấm chuyển mà code cho phép thì expected
vẫn là lỗi (đó là bug cần bắt — đừng để expected = hành vi SUT).
Với MỖI state ghi rõ chuỗi fixture để dựng state đó (vd checkout → admin set status ...).
Thêm: double-action liên tiếp (idempotency) + action ngay sau khi vào final state. Bảng <PREFIX>-###.
```

## Prompt 3 — Security (SEC-01..07)

```
Nhóm bảo mật, bám từng mã SEC, mỗi case có payload thật + assertion đo được:
- Auth (SEC-02): không token / header rỗng / "Bearer " trống / token rác / thiếu prefix / sai secret.
- Role (SEC-03): token role thấp gọi endpoint admin-only.
- Forge token: nếu secret lộ trong source → tự sign token nạn nhân/role admin → chứng minh escalation.
- Injection (SEC-05): nếu code nối chuỗi query → SQLi (' OR '1'='1, UNION SELECT ...); assert số record + không lộ HTML/stacktrace.
- XSS (SEC-04): payload <script>; assert có escape / content-type JSON.
- IDOR / mass-assignment: truy cập tài nguyên người khác; gửi field lạ (id/role/...) xem có bị nuốt.
Bảng <PREFIX>-###, cột FR/SEC điền mã.
```

## Prompt 4 — JSON-schema validation

```
Viết JSON Schema (draft-07, additionalProperties:false) cho từng response shape (success + error),
rồi sinh test dùng pm.response.to.have.jsonSchema(...). Chú ý kiểu field phải khớp DB schema
(vd cột INTEGER ⇒ number). Thêm: status code đúng, Content-Type, response time < 2000ms.
Ra schema trước rồi bảng <PREFIX>-###.
```

## Prompt 5 — Negative / contract

```
Chốt bằng negative/contract:
- Sai method (vd POST vào route chỉ nhận PUT; route không tồn tại).
- Content-Type text/plain, body malformed JSON, body rỗng, body là array.
- Thiếu header bắt buộc.
Với route lỗi: assert body vẫn là JSON {error} đúng contract (nếu SUT trả HTML ⇒ FAIL). Bảng <PREFIX>-###.
```

## After generating

- Save each chat as `docs/ai-logs/<API>-stepN-<technique>.md` (raw prompt + output) for the AI Audit Report.
- Go to Phase 3 (audit) — do NOT trust the output as-is.
