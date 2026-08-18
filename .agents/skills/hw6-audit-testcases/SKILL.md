---
name: hw6-audit-testcases
description: >
  Chuẩn bị khung tài liệu audit cho từng API trong HW6 – API Testing (EShop SUT).
  Bước audit (VALID/INVALID/INCOMPLETE) phải do con người thực hiện.
  AI chỉ tạo sườn bảng audit và ghi nhận thông tin cần thiết.
---

# Skill: hw6-audit-testcases

## Mục tiêu

Tạo **khung tài liệu audit** cho test cases đã được AI sinh ra, sẵn sàng để sinh viên tự điền nhãn VALID / INVALID / INCOMPLETE và lý do vào.

> ⚠️ **Lưu ý quan trọng:** Việc đánh nhãn audit (VALID / INVALID / INCOMPLETE) và viết reasoning **phải do con người thực hiện**. AI KHÔNG tự đánh nhãn audit. AI chỉ tạo khung bảng và điền thông tin cấu trúc từ các TC đã sinh.

---

## Thông tin đầu vào

Agent phải xác định rõ:

| Mục | Giá trị |
|:----|:--------|
| `API_NUMBER`  | 1, 2, hoặc 3 |
| `POOL`        | A / B / C |
| `TC_FILE`     | `submissions/test_cases_apiN.md` |
| `REPORT_FILE` | `submissions/MainReport.md` |

---

## Các bước thực hiện

### Bước 1 — Đọc các test cases đã sinh

Đọc `submissions/test_cases_apiN.md` và thu thập:
- Danh sách TC ID và mô tả của tất cả test cases trong mục DP, ST, SEC, SV
- Ghi nhận số lượng từng loại

### Bước 2 — Tạo bảng audit trong TC file

Điền cột **Audit** trong mỗi bảng của `test_cases_apiN.md` bằng placeholder `*(cần review)*`:

```markdown
| TC-A-DP-01 | [mô tả hiện có] | [input hiện có] | [expected hiện có] | [phân vùng] | *(cần review)* | |
```

Agent chỉ điền cột Audit bằng `*(cần review)*`, KHÔNG tự đánh VALID/INVALID/INCOMPLETE.

### Bước 3 — Tạo bảng tóm tắt audit sườn

Trong `test_cases_apiN.md`, thêm section mới **## Kết quả Audit (do người review)**:

```markdown
## Kết quả Audit (do người review)

> ⚠️ Bảng này phải được điền bởi sinh viên sau khi xem xét từng TC.

| Nhãn | Số lượng | Tỷ lệ | Lý do phổ biến |
|:-----|:---------|:------|:---------------|
| VALID | *(điền)* | % | *(điền)* |
| INVALID | *(điền)* | % | *(điền)* |
| INCOMPLETE | *(điền)* | % | *(điền)* |
| **Tổng** | | 100% | |

### Các TC cần sửa (INVALID / INCOMPLETE)

| TC ID | Nhãn | Lý do | Nội dung sửa |
|:------|:-----|:------|:-------------|
| *(điền)* | *(điền)* | *(điền)* | *(điền)* |
```

### Bước 4 — Cập nhật MainReport.md

Trong section 2.2 / 3.2 / 4.2 (Bước 2: Kiểm tra Audit) của `MainReport.md`:
- Đặt nội dung placeholder nhắc nhở sinh viên điền:

```markdown
### X.2. Bước 2: Kiểm tra (Audit)

> ⚠️ **Phần này do sinh viên tự điền sau khi review từng TC.**
> Xem chi tiết tại file: `test_cases_apiN.md`

| Nhãn | Số lượng | Tỷ lệ |
|:-----|:---------|:------|
| VALID | *(điền sau review)* | % |
| INVALID | *(điền sau review)* | % |
| INCOMPLETE | *(điền sau review)* | % |

**Nhận xét tổng quan về chất lượng output AI:** *(sinh viên tự viết)*
```

---

## Cập nhật tài liệu (BẮT BUỘC)

Agent phải cập nhật:

1. **`test_cases_apiN.md`**:
   - Đảm bảo cột Audit trong mỗi bảng hiển thị `*(cần review)*`
   - Thêm section "Kết quả Audit (do người review)" ở cuối file

2. **`MainReport.md`**:
   - Điền section 2.2 / 3.2 / 4.2 với khung placeholder như trên

---

## Ràng buộc

- AI KHÔNG tự điền VALID / INVALID / INCOMPLETE
- AI KHÔNG tự viết reasoning cho bất kỳ TC nào
- AI KHÔNG tự sửa nội dung TC dựa trên phán đoán của mình
- Chỉ tạo cấu trúc sườn để người dùng điền vào

---

## Checklist hoàn thành

- [ ] Cột Audit trong tất cả bảng TC hiển thị `*(cần review)*`
- [ ] Section "Kết quả Audit (do người review)" đã được thêm vào `test_cases_apiN.md`
- [ ] Section 2.2/3.2/4.2 trong `MainReport.md` đã có khung placeholder
- [ ] Không có nhãn VALID/INVALID/INCOMPLETE nào do AI tự điền
