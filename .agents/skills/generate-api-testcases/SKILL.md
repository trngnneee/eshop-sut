---
name: generate-api-testcases
description: >
  Hướng dẫn AI sinh test cases cho một API cụ thể trong HW6 – API Testing (EShop SUT).
  Skill này điều khiển AI đi qua từng bước kỹ thuật (domain partition, state transition,
  security, schema validation) và ghi kết quả vào các file Markdown tương ứng.
---

# Skill: generate-api-testcases

## Mục tiêu

Sinh **≥ 35 test cases** cho từng API được chọn từ EShop SUT, bao phủ đầy đủ 4 kỹ thuật:
- **Domain Testing (EP & BVA)** – phân lớp tương đương và phân tích giá trị biên (cô lập lỗi, phủ lớp hợp lệ)
- **State Transition & Lifecycle** – chuyển trạng thái nghiệp vụ (FR-10), auth/session state, vòng đời CRUD
- **Security** – SEC-01 đến SEC-07 (SQL Injection, IDOR, role escalation, v.v.)
- **Schema Validation** – kiểm tra response shape khớp với spec (bao gồm nullable fields)

---

## Thông tin đầu vào (Agent phải xác định trước khi chạy)

Agent phải xác định rõ:

| Mục | Giá trị |
|:----|:--------|
| `API_NUMBER`   | 1, 2, hoặc 3 (tương ứng Pool A, B, C) |
| `POOL`         | A / B / C |
| `FEATURE`      | FR-xy – tên tính năng |
| `ENDPOINT`     | `METHOD /path` |
| `OUTPUT_FILE`  | `submissions/test_cases_apiN.md` |
| `REPORT_FILE`  | `submissions/MainReport.md` |

---

## Các bước thực hiện

### Bước 1 — Đọc API Specification

Đọc file `api_specification.md` tại root của project EShop SUT.
Trích xuất cho endpoint đã chọn:
- Tất cả tham số (path / query / body) và kiểu dữ liệu
- Response schema (các field, kiểu, ràng buộc)
- Security requirements liên quan (SEC-01 – SEC-07)
- Các trạng thái nếu là state machine (FR-10)

### Bước 2 — Sinh Domain Partition & Boundary Value Tests (Prompt riêng biệt)

Áp dụng kỹ thuật **Phân lớp tương đương (EP)** và **Phân tích giá trị biên (BVA)** theo các nguyên tắc:
- Xác định toàn bộ biến đầu vào/đầu ra của endpoint đang xét, phân chia các lớp **Hợp lệ (Valid)** và **Không hợp lệ (Invalid)** cùng các giá trị biên (chiến lược 2 điểm hoặc 3 điểm).
- **Phủ lớp hợp lệ:** Kết hợp nhiều giá trị hợp lệ trong cùng 1 test case để tối ưu độ bao phủ.
- **Cô lập lỗi (Error Isolation):** Mỗi test case không hợp lệ/biên lỗi chỉ chứa **duy nhất 1 giá trị sai**, tất cả các biến còn lại phải giữ giá trị đại diện hợp lệ.

**Mẫu prompt gửi cho AI:**

```
Dựa trên API spec của endpoint [ENDPOINT], hãy áp dụng kỹ thuật Domain Testing (Equivalence Partitioning & Boundary Value Analysis) để thiết kế test cases theo các quy tắc sau:

1. Phân tích biến: Liệt kê tất cả tham số đầu vào/ra, xác định các lớp tương đương Hợp lệ (Valid EP), Không hợp lệ (Invalid EP: sai kiểu, chuỗi rỗng, vượt ngưỡng, ký tự đặc biệt,...) và các giá trị biên (BVA 2-point/3-point).
2. Nguyên tắc tạo Test Case:
* Valid Cases: Kết hợp tối đa các lớp hợp lệ vào cùng 1 test case.
* Invalid / Boundary Cases (Cô lập lỗi): Mỗi test case chỉ chứa DUY NHẤT 1 giá trị không hợp lệ hoặc 1 giá trị biên lỗi; toàn bộ các tham số còn lại bắt buộc phải dùng giá trị đại diện hợp lệ.
* Đảm bảo phủ hết tất cả các EP và BVA đã xác định.


Xuất kết quả theo định dạng bảng:
| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload (Params/Body) | Expected HTTP Status & Output |

API Spec:
[dán spec endpoint]

```

### Bước 3 — Sinh State Transition & Lifecycle Tests (Prompt riêng biệt)

Áp dụng kỹ thuật **Kiểm thử chuyển trạng thái (State Transition Testing)** cho các endpoint có vòng đời hoặc ràng buộc trạng thái:
- **Nhận diện loại trạng thái:** - *State Machine nghiệp vụ:* Đơn hàng (FR-10: pending → confirmed → shipping → delivered / canceled).
  - *Session/Auth State:* Unauthenticated → Authenticated → Locked (sai $N$ lần) → Token Expired/Revoked.
  - *Resource Lifecycle (CRUD):* Non-existent (404) → Created (201) → Active/Updated (200) → Deleted/Archived → Re-access (404/410).
- **Bao phủ chuyển trạng thái:**
  - *Hợp lệ (Valid transitions):* Luồng chính (Happy path), các nhánh rẽ và luồng hủy hợp lệ.
  - *Không hợp lệ (Invalid transitions / N-switch):* Thao tác sai thứ tự, chuyển trạng thái từ trạng thái kết thúc (terminal state), hoặc gọi API khi chưa thỏa mãn trạng thái tiên quyết.

**Mẫu prompt gửi cho AI:**

```
Dựa trên API spec của endpoint [ENDPOINT], hãy áp dụng kỹ thuật State Transition Testing để thiết kế test cases theo các yêu cầu sau:

1. Xác định mô hình trạng thái: Nhận diện thực thể/phiên làm việc (Order, Session/Auth, Resource CRUD), liệt kê tất cả State (trạng thái) và Event/Action (gọi endpoint này).
2. Xây dựng kịch bản chuyển đổi:
* Chuyển đổi hợp lệ (Valid Transition): Gọi endpoint khi thực thể ở đúng trạng thái cho phép.
* Chuyển đổi không hợp lệ (Invalid Transition): Gọi endpoint khi thực thể ở trạng thái không hợp lệ hoặc đã ở trạng thái kết thúc (Terminal state) để kiểm tra việc từ chối chuyển trạng thái.
* Kịch bản chuỗi (State Sequence): Kiểm tra tính toàn vẹn của dữ liệu và mã phản hồi sau khi chuyển trạng thái thành công.

Xuất kết quả theo định dạng bảng:
| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code |

API Spec:
[dán spec endpoint]

```

### Bước 4 — Sinh Security Tests (Prompt riêng biệt)

Sinh test case cho từng loại tấn công trong SEC-01 – SEC-07:
- SQL Injection vào các input fields
- IDOR – truy cập resource của user khác
- Role Escalation – user thường gọi admin API
- Missing/Invalid Authorization header
- Token forgery / expired token
- Rate limiting (brute force lockout)
- Sensitive data exposure trong response

Mẫu prompt:

```
Đối với endpoint [ENDPOINT], hãy sinh test cases bảo mật cho từng
loại sau: SQL Injection, IDOR, Role Escalation, Missing Auth,
Expired Token. Với mỗi loại, cung cấp:
[TC ID | Mô tả | Loại tấn công | Input | Expected Response]
```

### Bước 5 — Sinh Schema Validation Tests (Prompt riêng biệt)

Xác minh response shape:
- Tất cả field trong spec có tồn tại trong response không?
- Kiểu dữ liệu (string / number / boolean / array) đúng không?
- Nullable fields được xử lý đúng không?
- Status code đúng không?

Mẫu prompt:

```
Dựa vào response schema của [ENDPOINT] trong API spec, hãy sinh
test cases Schema Validation để kiểm tra:
- Đủ các field theo spec
- Kiểu dữ liệu chính xác, các giá trị đặc biệt (Nullable fields) được xử lý đúng
- HTTP status code đúng
Bảng: [TC ID | Mô tả | Field kiểm tra | Expected schema]
```

### Bước 6 — Tổng hợp và đánh số TC ID

Đặt TC ID theo convention:
- Domain:   `TC-[A/B/C]-DP-01`, `TC-[A/B/C]-DP-02`, ...
- State:    `TC-[A/B/C]-ST-01`, ...
- Security: `TC-[A/B/C]-SEC-01`, ...
- Schema:   `TC-[A/B/C]-SV-01`, ...

Đảm bảo tổng ≥ 35 test cases.

---

## Cập nhật tài liệu (BẮT BUỘC)

Sau khi sinh xong test cases, agent PHẢI cập nhật các file sau:

### 1. Cập nhật `test_cases_apiN.md` (OUTPUT_FILE)

- Cập nhật bảng **Tổng quan**: tên API, tổng số TC AI sinh
- Điền tất cả test cases vào bảng A (DP), B (ST), C (SEC), D (SV)
- **Để trống cột Audit** – do con người review, AI không điền
- **Để trống phần E** (Test Cases tự thêm)

### 2. Cập nhật `MainReport.md` (REPORT_FILE)

Trong section tương ứng API N (mục 2/3/4):
- Điền endpoint và tên feature
- Copy nguyên văn từng prompt (cả 4 bước: Domain EP/BVA, State Transition, Security, Schema) vào các code block
- Ghi tóm tắt output: số lượng TC theo từng loại
- Ghi tổng số TC AI sinh ra

Format mẫu:

```markdown
### X.1. Bước 1: Sinh test cases bằng AI (Generate)

**Prompt 1 – Domain Testing (EP & BVA):**
```
[copy nguyên văn prompt]
```

**Output AI 1 (tóm tắt):**
AI sinh ra X test cases domain EP & BVA.

**Prompt 2 – State Transition & Lifecycle:**
```
[copy nguyên văn prompt]
```

**Output AI 2 (tóm tắt):**
AI sinh ra Y test cases state transition.

**Prompt 3 – Security Tests:**
```
[copy nguyên văn prompt]
```

**Output AI 3 (tóm tắt):**
AI sinh ra Z test cases security.

**Prompt 4 – Schema Validation:**
```
[copy nguyên văn prompt]
```

**Output AI 4 (tóm tắt):**
AI sinh ra W test cases schema validation.

**Số test cases AI sinh ra:** [tổng] (DP/BVA: X | ST: Y | SEC: Z | SV: W)
```

---

## Ràng buộc

- KHÔNG dùng một prompt tổng quát ("generate all test cases for this API")
- Mỗi kỹ thuật PHẢI có prompt riêng biệt được ghi lại vào MainReport.md
- Cột Audit trong bảng test cases để TRỐNG – AI không tự đánh giá
- Không giả mạo kết quả – chỉ ghi những gì AI thực sự sinh ra
- Tuân theo TC ID convention đã quy định

---

## Checklist hoàn thành

Agent tự kiểm tra trước khi kết thúc:

- [ ] `test_cases_apiN.md` có ≥ 35 TC trong các mục DP + ST + SEC + SV
- [ ] 4 loại test (DP/BVA, ST, SEC, SV) đều có mặt
- [ ] TC ID đặt đúng convention
- [ ] Cột Audit để trống
- [ ] `MainReport.md` đã cập nhật: prompt nguyên văn 4 bước + tóm tắt output + tổng số TC
