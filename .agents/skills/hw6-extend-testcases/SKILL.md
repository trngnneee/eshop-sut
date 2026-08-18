---
name: hw6-extend-testcases
description: >
  Hướng dẫn AI đề xuất khung cho phần "Extend" (Bổ sung Test Cases) trong HW6.
  AI phân tích các điểm yếu có thể bị bỏ sót, đề xuất danh sách ý tưởng,
  nhưng nội dung thực sự phải do sinh viên tự viết.
---

# Skill: hw6-extend-testcases

## Mục tiêu

Chuẩn bị phần **E – Test Cases tự thêm (Extend)** trong `test_cases_apiN.md`:
- AI phân tích các điểm yếu / blind spots trong test cases đã sinh
- AI đề xuất **danh sách ý tưởng** cho ≥ 5 test case mà AI có thể đã bỏ sót
- **Nội dung cụ thể** (input, expected output, reasoning) do sinh viên tự viết

> ⚠️ **Lưu ý:** Phần "Lý do AI bỏ sót" và nội dung chi tiết từng TC PHẢI do sinh viên tự viết.
> AI chỉ gợi ý hướng và tạo khung bảng sẵn sàng để điền.

---

## Thông tin đầu vào

| Mục | Giá trị |
|:----|:--------|
| `API_NUMBER`  | 1, 2, hoặc 3 |
| `POOL`        | A / B / C |
| `ENDPOINT`    | `METHOD /path` |
| `TC_FILE`     | `submissions/test_cases_apiN.md` |
| `REPORT_FILE` | `submissions/MainReport.md` |

---

## Các bước thực hiện

### Bước 1 — Phân tích điểm yếu của test cases hiện có

Đọc `test_cases_apiN.md` và xem xét:
- Các boundary value chưa được test (off-by-one, max length, v.v.)
- Các tổ hợp tham số phức tạp (combination testing)
- Các kịch bản race condition hoặc concurrent requests
- Các lỗi bảo mật nâng cao mà AI thường bỏ sót:
  - HTTP verb tampering
  - Mass assignment / parameter pollution
  - Timing attack trên authentication
  - Business logic bypass (ví dụ: apply coupon nhiều lần)
  - Cache poisoning
- Các trường hợp dữ liệu đặc biệt (Unicode, emoji, XSS trong fields)

### Bước 2 — Tạo danh sách gợi ý (Suggestions List)

AI tạo danh sách **≥ 8 ý tưởng** (để sinh viên chọn ≥ 5), mỗi ý tưởng gồm:
- **Loại TC**: (Security / Business Logic / Edge Case / v.v.)
- **Mô tả ngắn**: kịch bản cần test là gì
- **Lý do AI thường bỏ sót**: (prompt không đủ cụ thể / model limitations / đặc thù API)
- **Gợi ý input**: để sinh viên tham khảo (không bắt buộc)

Format danh sách gợi ý:

```markdown
### Gợi ý từ AI (sinh viên chọn ≥ 5 để thêm vào)

| # | Loại | Mô tả kịch bản | Lý do AI thường bỏ | Gợi ý input |
|:--|:-----|:---------------|:-------------------|:------------|
| 1 | Business Logic | Apply coupon nhiều lần với cùng user_id | AI không mô hình hóa trạng thái coupon đã dùng | code=SAVE10, user_id=1 (lần 2) |
| 2 | Security | HTTP Verb tampering: dùng PATCH thay vì PUT | AI không test HTTP method không chuẩn | PATCH /api/... |
| ... | ... | ... | ... | ... |
```

### Bước 3 — Cập nhật bảng Extend trong TC file

Trong `test_cases_apiN.md`, phần **E. Test Cases tự thêm (Extend)**:
- Thêm ≥ 5 hàng với TC ID đúng convention: `TC-[A/B/C]-EXT-01`, ...
- Điền cột **Mô tả** và **Loại** dựa trên gợi ý
- Để trống các cột: **Lý do AI bỏ sót**, **Expected**, **Kết quả** → sinh viên điền

```markdown
| TC-A-EXT-01 | [mô tả từ gợi ý] | [loại] | *(sinh viên điền)* | *(sinh viên điền)* | *(sau execute)* |
```

### Bước 4 — Cập nhật MainReport.md

Trong section 2.3 / 3.3 / 4.3 (Bước 3: Bổ sung) của `MainReport.md`:

```markdown
### X.3. Bước 3: Bổ sung (Extend)

> ℹ️ AI đề xuất các hướng bổ sung; nội dung chi tiết và lý do AI bỏ sót
> do sinh viên tự phân tích và điền.

**Phân tích điểm yếu của test suite hiện có:**
*(AI mô tả ngắn các blind spots đã phát hiện)*

**Danh sách TC bổ sung:**

| TC ID | Mô tả | Loại | Lý do AI bỏ sót |
|:------|:------|:-----|:----------------|
| TC-[X]-EXT-01 | *(điền)* | *(điền)* | *(sinh viên điền)* |
| TC-[X]-EXT-02 | *(điền)* | *(điền)* | *(sinh viên điền)* |
| TC-[X]-EXT-03 | *(điền)* | *(điền)* | *(sinh viên điền)* |
| TC-[X]-EXT-04 | *(điền)* | *(điền)* | *(sinh viên điền)* |
| TC-[X]-EXT-05 | *(điền)* | *(điền)* | *(sinh viên điền)* |
```

---

## Cập nhật tài liệu (BẮT BUỘC)

Agent phải cập nhật:

1. **`test_cases_apiN.md`**:
   - Phần E có ≥ 5 hàng với TC ID, Mô tả, Loại đã điền
   - Cột "Lý do AI bỏ sót", "Expected", "Kết quả" để trống

2. **`MainReport.md`**:
   - Section 2.3/3.3/4.3 có phân tích blind spots và bảng TC bổ sung sườn

---

## Ràng buộc

- AI KHÔNG tự viết "Lý do AI bỏ sót" – đây phải là phân tích của sinh viên
- AI KHÔNG tự điền "Expected Output" – sinh viên phải tự xác định
- AI chỉ cung cấp gợi ý hướng, không viết thay sinh viên

---

## Checklist hoàn thành

- [ ] `test_cases_apiN.md` phần E có ≥ 5 hàng TC với ID đúng convention
- [ ] Các cột cần sinh viên điền đều hiển thị placeholder rõ ràng
- [ ] `MainReport.md` section Extend đã có khung bảng và phân tích blind spots
- [ ] Danh sách gợi ý (≥ 8 ý tưởng) đã được tạo cho sinh viên tham khảo
