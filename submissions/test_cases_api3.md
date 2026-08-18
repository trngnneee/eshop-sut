# Test Cases – API 3 (Pool C)

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**Feature:** *(FR-1x – Tên feature)*  
**Endpoint:** `METHOD /path/to/endpoint`

---

## Tổng quan

| Mục | Giá trị |
|:---|:---|
| **API** | *(tên API)* |
| **Pool** | C |
| **Tổng TC (AI sinh)** | *(≥ 35)* |
| **TC tự thêm** | *(≥ 5)* |
| **Tổng TC** | *(cập nhật)* |

---

## Phân loại test cases

### A. Domain Partition Tests

| TC ID | Mô tả | Input | Expected Output | Phân vùng | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-C-DP-01 | | | | | VALID/INVALID/INCOMPLETE | |
| TC-C-DP-02 | | | | | | |
| TC-C-DP-03 | | | | | | |
| TC-C-DP-04 | | | | | | |
| TC-C-DP-05 | | | | | | |

### B. State Transition Tests (Admin)

| TC ID | Mô tả | Trạng thái hiện tại | Sự kiện (Admin) | Trạng thái kỳ vọng | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-C-ST-01 | | | | | | |
| TC-C-ST-02 | | | | | | |
| TC-C-ST-03 | | | | | | |

### C. Security Tests (SEC-01 – SEC-07) – Access Control

| TC ID | Mô tả | Loại tấn công | Input | Expected | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-C-SEC-01 | Truy cập không có token | Unauthorized | | 401 | | |
| TC-C-SEC-02 | Truy cập với user thường | Role Escalation | | 403 | | |
| TC-C-SEC-03 | IDOR – xem dữ liệu admin khác | IDOR | | 403/404 | | |

### D. Schema Validation Tests

| TC ID | Mô tả | Field kiểm tra | Expected schema | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|
| TC-C-SV-01 | | | | | |
| TC-C-SV-02 | | | | | |

### E. Test Cases tự thêm (Extend – ≥ 5)

| TC ID | Mô tả | Loại | Lý do AI bỏ sót | Expected | Kết quả |
|:---|:---|:---|:---|:---|:---|
| TC-C-EXT-01 | | | | | |
| TC-C-EXT-02 | | | | | |
| TC-C-EXT-03 | | | | | |
| TC-C-EXT-04 | | | | | |
| TC-C-EXT-05 | | | | | |

---

## Kết quả thực thi (Execute)

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | | % |
| FAIL | | % |
| **Tổng** | | 100% |

*(Screenshot Newman / Postman Console đính kèm tại đây)*
