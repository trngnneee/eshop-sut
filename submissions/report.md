# HW06 – Báo cáo Kiểm thử API

**Khoa Công nghệ Thông tin (FIT) – Trường Đại học Khoa học Tự nhiên TP.HCM (HCMUS)**  
**CS423 / CSC13003 – Kiểm thử Phần mềm (AI-augmented · 2026)**

---

## Thông tin sinh viên

| Trường | Giá trị |
|:---|:---|
| **Họ và tên:** | Phan Quốc Thịnh |
| **MSSV:** | 23127486 |
| **Lớp:** | 23KTPM3 |
| **Ngày:** | *(cập nhật khi nộp)* |

---

## 1. Giới thiệu

*(Mô tả ngắn về bài tập, hệ thống SUT EShop, và 3 API được chọn.)*

### 1.1. Hệ thống cần kiểm thử (SUT)

- **Tên:** EShop – Ứng dụng thương mại điện tử demo
- **Repository:** https://github.com/ttbhanh/eshop-sut

### 1.2. Các API được chọn

| Pool | Feature | Endpoint | Mô tả |
|:---|:---|:---|:---|
| Pool A | *(FR-0x)* | `...` | *(mô tả)* |
| Pool B | *(FR-0x)* | `...` | *(mô tả)* |
| Pool C | *(FR-1x)* | `...` | *(mô tả)* |

### 1.3. Công cụ sử dụng

- *(Tên AI tool, Postman, Newman, ...)*

---

## 2. API 1 – Pool A: *(Tên Feature)*

> **Endpoint:** `METHOD /path/to/endpoint`  
> **Feature:** FR-0x – *(Tên)*

### 2.1. Bước 1: Sinh test cases bằng AI (Generate)

*(Mô tả cách prompt AI từng bước – không dùng một prompt tổng quát)*

**Prompt 1:**
```
(dán prompt ở đây)
```

**Output AI (tóm tắt):**
*(tóm tắt output, chi tiết trong AI_Audit.md)*

**Số test cases AI sinh ra:** *(≥ 35)*

### 2.2. Bước 2: Kiểm tra (Audit)

*(Nhãn từng test case: VALID / INVALID / INCOMPLETE + lý do)*

> Chi tiết xem file: `test_cases_api1.md`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| VALID | | % |
| INVALID | | % |
| INCOMPLETE | | % |

### 2.3. Bước 3: Bổ sung (Extend)

*(Thêm ≥ 5 test cases mà AI bỏ sót, giải thích lý do AI bỏ sót)*

| TC ID | Mô tả | Lý do AI bỏ sót |
|:---|:---|:---|
| TC-A-EXT-01 | | |
| TC-A-EXT-02 | | |
| TC-A-EXT-03 | | |
| TC-A-EXT-04 | | |
| TC-A-EXT-05 | | |

### 2.4. Bước 4: Thực thi (Execute)

- **Công cụ:** Postman + Newman
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Kết quả:** *(PASS/FAIL, screenshot)*

> Newman report: `newman_report.html`

### 2.5. Bước 5: Báo cáo Bug

*(Các bug phát hiện được, kèm link GitHub Issues)*

| Bug ID | Mô tả | Severity | Link Issue |
|:---|:---|:---|:---|
| BUG-A-01 | | | |

---

## 3. API 2 – Pool B: *(Tên Feature)*

> **Endpoint:** `METHOD /path/to/endpoint`  
> **Feature:** FR-0x – *(Tên)*

### 3.1. Bước 1: Sinh test cases bằng AI (Generate)

*(Mô tả cách prompt AI từng bước)*

### 3.2. Bước 2: Kiểm tra (Audit)

> Chi tiết xem file: `test_cases_api2.md`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| VALID | | % |
| INVALID | | % |
| INCOMPLETE | | % |

### 3.3. Bước 3: Bổ sung (Extend)

| TC ID | Mô tả | Lý do AI bỏ sót |
|:---|:---|:---|
| TC-B-EXT-01 | | |
| TC-B-EXT-02 | | |
| TC-B-EXT-03 | | |
| TC-B-EXT-04 | | |
| TC-B-EXT-05 | | |

### 3.4. Bước 4: Thực thi (Execute)

- **Công cụ:** Postman + Newman
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Kết quả:** *(PASS/FAIL, screenshot)*

### 3.5. Bước 5: Báo cáo Bug

| Bug ID | Mô tả | Severity | Link Issue |
|:---|:---|:---|:---|
| BUG-B-01 | | | |

---

## 4. API 3 – Pool C: *(Tên Feature)*

> **Endpoint:** `METHOD /path/to/endpoint`  
> **Feature:** FR-1x – *(Tên)*

### 4.1. Bước 1: Sinh test cases bằng AI (Generate)

*(Mô tả cách prompt AI từng bước)*

### 4.2. Bước 2: Kiểm tra (Audit)

> Chi tiết xem file: `test_cases_api3.md`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| VALID | | % |
| INVALID | | % |
| INCOMPLETE | | % |

### 4.3. Bước 3: Bổ sung (Extend)

| TC ID | Mô tả | Lý do AI bỏ sót |
|:---|:---|:---|
| TC-C-EXT-01 | | |
| TC-C-EXT-02 | | |
| TC-C-EXT-03 | | |
| TC-C-EXT-04 | | |
| TC-C-EXT-05 | | |

### 4.4. Bước 4: Thực thi (Execute)

- **Công cụ:** Postman + Newman
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Kết quả:** *(PASS/FAIL, screenshot)*

### 4.5. Bước 5: Báo cáo Bug

| Bug ID | Mô tả | Severity | Link Issue |
|:---|:---|:---|:---|
| BUG-C-01 | | | |

---

## 5. Các tính năng Postman đã sử dụng

*(Liệt kê các tính năng Postman được dùng trong bài)*

| Tính năng | Mô tả sử dụng |
|:---|:---|
| Workspaces | |
| Collections | |
| Variables | |
| Environments | |
| Data-driven runs (Collection Runner) | |
| Pre-request Scripts | |
| Test Scripts | |
| Monitors | |
| Mock Servers | |

---

## 6. Tích hợp CI/CD

*(Tóm tắt ngắn – chi tiết trong `cicd_report.md`)*

- **Pipeline:** GitHub Actions
- **Run 1 (all PASS):** *(link)*
- **Run 2 (có test FAIL):** *(link)*

---

## 7. Agent Skill – AI-driven Test Generator

*(Tóm tắt – chi tiết trong `agent_skill.md`)*

---

## 8. Phụ lục

- **Phụ lục A – AI Audit Report:** xem `AI_Audit.md`
- **Phụ lục B – AI Critique:** xem `AI_Critique.md`
- **Phụ lục C – Bug Report:** xem `bug_report.md`
- **Phụ lục D – CI/CD Report:** xem `cicd_report.md`
- **Phụ lục E – Git Commit Log:** xem `git_commit_log.txt`
