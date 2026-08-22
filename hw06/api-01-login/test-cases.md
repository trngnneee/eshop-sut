# API-1 — Danh sách test case chốt cho `POST /api/login`

> Nguồn chốt: 36 case AI sau audit + 6 case người học mở rộng. Expected result luôn theo đặc tả/oracle, không sửa để khớp hành vi lỗi của SUT.

| TC ID | Requirement | Nhóm | Kỹ thuật | Preconditions | Method + Endpoint / Test data | Expected result | Nguồn | Kỳ vọng chạy | Bug ID | Execution | Lý do |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-LOGIN-001 | FR-02 | Partition | EP | Seed user active | `POST /api/login`; credentials đúng | `200`; có `token:string` và `user:object` | AI | PASS | — | Automated | — |
| TC-API-LOGIN-002 | FR-02 | Partition | EP | Seed user attempts=0 | Sai password | `401`; lỗi chung, không token | AI | PASS | — | Automated | — |
| TC-API-LOGIN-003 | FR-02 | Partition | EP | Email không tồn tại | Email lạ + password bất kỳ | `401`; cùng lỗi như sai password | AI | PASS | — | Automated | — |
| TC-API-LOGIN-004 | FR-02 | Partition | EP | DB sạch | Thiếu `email` | Controlled `400` JSON validation error | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-005 | FR-02 | Partition | EP | DB sạch | Thiếu `password` | Controlled `400` JSON validation error | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-006 | FR-02 | Partition | EP/BVA | DB sạch | `email=""` | `400`; không truy vấn account | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-007 | FR-02 | Partition | EP | Seed user active | Password `abc` | `401` generic; đây là wrong credential, không phải password-policy test | AI-audited | PASS | — | Automated | — |
| TC-API-LOGIN-008 | FR-02 | Partition | Robustness | DB sạch | `email="not-an-email"` | Controlled 4xx; JSON; không 5xx/reflect input | AI-audited | PASS | — | Automated | — |
| TC-API-LOGIN-009 | FR-02 | Partition | EP | Seed user active | Email có whitespace | `401` generic; không tự trim khi spec không yêu cầu | AI-audited | PASS | — | Automated | — |
| TC-API-LOGIN-010 | FR-02 | Partition | Type partition | DB sạch | `email=null` | `400` validation error | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-011 | FR-02 | Partition | Type partition | DB sạch | `password=null` | `400` validation error | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-012 | FR-02 | Partition | Type partition | DB sạch | `email=123` | `400` validation error | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-013 | FR-02 | Partition | Type partition | DB sạch | `password={}` | `400` validation error | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-014 | FR-02 | Partition | Type partition | DB sạch | Body `[]` | `400` validation error | AI | FAIL | D-LOGIN-08 | Automated | — |
| TC-API-LOGIN-015 | FR-02 | Partition | Protocol robustness | DB sạch | Raw JSON thiếu Content-Type | Controlled `400` hoặc `415`; không 500 | AI-audited | PASS | — | Automated | — |
| TC-API-LOGIN-016 | FR-02 | Partition | EP | Seed user active | Credentials đúng + `rememberMe` | `200`; field vô hại bị bỏ qua | AI | PASS | — | Automated | — |
| TC-API-LOGIN-017 | FR-02 | State | State transition | Disposable user attempts=0 | Sai lần 1 | `401`; attempts tăng đúng 1, chưa khóa | AI | FAIL | D-LOGIN-01 | Automated | — |
| TC-API-LOGIN-018 | FR-02 | State | State/BVA | Disposable user attempts=1 | Sai lần 2 rồi login đúng | Sai lần 2 `401`; login đúng vẫn `200`, chưa khóa | AI | FAIL · CI canary | D-LOGIN-01 | Automated | — |
| TC-API-LOGIN-019 | FR-02 | State | State/BVA | Disposable user attempts=2 | Sai lần 3 | `401`; khóa đúng 30 giây | AI | FAIL | D-LOGIN-01 | Automated | — |
| TC-API-LOGIN-020 | FR-02 | State | State transition | User đang khóa | Login đúng trong lock | Không token; lỗi chung không tiết lộ trạng thái | AI | FAIL | D-LOGIN-07 | Automated | — |
| TC-API-LOGIN-021 | FR-02 | State | Temporal BVA | User vừa khóa | Chờ 29 giây, login đúng | Vẫn bị từ chối; không token | AI | PASS | — | Automated | — |
| TC-API-LOGIN-022 | FR-02 | State | Temporal BVA | User vừa khóa | Chờ 31 giây, login đúng | `200`; reset attempts/lock | AI | FAIL | D-LOGIN-02 | Automated | — |
| TC-API-LOGIN-023 | FR-02 | State | State transition | Disposable user | Sai 2 lần rồi login đúng | `200`; reset chuỗi sai | AI | FAIL | D-LOGIN-01 | Automated | — |
| TC-API-LOGIN-024 | FR-02 | State | State transition | Case 023 thành công | Sai một lần sau reset | `401`; chưa khóa | AI | FAIL | D-LOGIN-01 | Blocked | Đã chạy trong `05-timed-assert` và có assertion Newman thật, nhưng tiền đề của case không tồn tại trên SUT: D-LOGIN-06 khiến không bao giờ đạt được trạng thái reset sau lock. Blocked có bằng chứng, không phải giả định. |
| TC-API-LOGIN-025 | SEC-05 | Security | SQLi | DB sạch | SQLi ở email | `401`; không bypass/không đổi DB | AI-audited | PASS | — | Automated | — |
| TC-API-LOGIN-026 | SEC-05 | Security | SQLi | DB sạch | SQLi ở password | `401`; không bypass | AI | PASS | — | Automated | — |
| TC-API-LOGIN-027 | SEC-04 | Security | XSS/non-reflection | DB sạch | XSS ở email | 4xx; không reflect payload | AI | PASS | — | Automated | — |
| TC-API-LOGIN-028 | SEC-01 | Security | Sensitive-data exposure | Seed user active | Login đúng | `user` không có `password` | AI | FAIL | D-LOGIN-03 | Automated | — |
| TC-API-LOGIN-029 | SEC-01 | Security | Negative schema | Seed user active | Login đúng | Không có auth fields nội bộ | AI | FAIL | D-LOGIN-03 | Automated | — |
| TC-API-LOGIN-030 | SEC-03 | Security | Mass assignment | Seed role=user | Body thêm `role="admin"` | Token/user vẫn role=user | AI | PASS | — | Automated | — |
| TC-API-LOGIN-031 | SEC-02 | Security | Token usability | Seed user active | Login rồi `GET /api/users/me` | Cả hai `200`, đúng user | AI | PASS | — | Automated | — |
| TC-API-LOGIN-032 | FR-02 | Security | Enumeration | User đang khóa | Login đúng | Cùng public error contract, không lộ “locked” | AI | FAIL | D-LOGIN-07 | Automated | — |
| TC-API-LOGIN-033 | FR-02 | Schema | JSON Schema | Seed user active | Login đúng | `token` non-empty; `user.id/email/role` đúng kiểu | AI-audited | PASS | — | Automated | — |
| TC-API-LOGIN-034 | FR-02 | Schema | Header assertion | Seed user active | Login đúng | Content-Type là JSON | AI | PASS | — | Automated | — |
| TC-API-LOGIN-035 | FR-02 | Schema | JSON Schema | Seed user active | Wrong password | `401`; `error:string`, không tiết lộ account | AI-audited | PASS | — | Automated | — |
| TC-API-LOGIN-036 | SEC-01 | Schema | Negative schema | Seed user active | Login đúng | Có token/user; cho metadata vô hại; cấm field nhạy cảm | AI-audited | FAIL | D-LOGIN-03 | Automated | — |
| TC-API-LOGIN-037 | FR-02 | State | Sequence/state | Disposable user | Sai 2 lần rồi đúng | `401,401,200`; không khóa sớm | Human | FAIL | D-LOGIN-01 | Automated | — |
| TC-API-LOGIN-038 | FR-02 | State | Temporal BVA | User vừa khóa | Chờ 35 giây rồi đúng | `200`; lock hết hạn | Human | FAIL | D-LOGIN-02 | Automated | — |
| TC-API-LOGIN-039 | SEC-01 | Security | Negative schema | Seed user active | Login đúng | Không field nhạy cảm ở root/user | Human | FAIL | D-LOGIN-03 | Automated | — |
| TC-API-LOGIN-040 | SEC-02 | Security | JWT claims | Seed user active | Decode token | Có `iat/exp`; TTL ≤24h | Human | FAIL | D-LOGIN-05 | Automated | — |
| TC-API-LOGIN-041 | FR-02 | State | Residual-state | Lock đã hết hạn | Sai 1 lần rồi đúng | `401,200`; không khóa lại | Human | FAIL | D-LOGIN-06 | Automated | Chạy trong `05-timed-assert` sau khi chờ lock 180s hết hạn: sai một lần nhận `401`, nhưng đăng nhập đúng ngay sau đó nhận `403` — counter không reset. |
| TC-API-LOGIN-042 | SEC-02 | Security | JWT forgery | Biết source secret | Token tự ký gọi admin API | `401/403` | Human | FAIL | D-LOGIN-05 | Automated | Chạy trong `04-jwt-cases`: tự ký JWT bằng secret công khai ở `server.js:9`, gọi `GET /api/admin/orders` nhận `200` — token giả được chấp nhận. |
## Coverage summary

| Nguồn | Partition | State | Security | Schema | Tổng |
| :--- | ---: | ---: | ---: | ---: | ---: |
| AI sau audit | 16 | 8 | 8 | 4 | 36 |
| Human mở rộng | 0 | 3 | 3 | 0 | 6 |
| **Tổng** | **16** | **11** | **11** | **4** | **42** |
