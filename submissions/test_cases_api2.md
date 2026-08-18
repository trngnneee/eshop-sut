# Test Cases – API 2 (Pool B)

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**Feature:** *(FR-0x – Tên feature)*  
**Endpoint:** `METHOD /path/to/endpoint`

---

## Tổng quan

| Mục | Giá trị |
|:---|:---|
| **API** | *(tên API)* |
| **Pool** | B |
| **Tổng TC (AI sinh)** | *(≥ 35)* |
| **TC tự thêm** | *(≥ 5)* |
| **Tổng TC** | *(cập nhật)* |

---

## Phân loại test cases

### A. Domain Partition Tests

| TC ID | Mô tả | Input | Expected Output | Phân vùng | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-B-DP-01 | | | | | VALID/INVALID/INCOMPLETE | |
| TC-B-DP-02 | | | | | | |
| TC-B-DP-03 | | | | | | |
| TC-B-DP-04 | | | | | | |
| TC-B-DP-05 | | | | | | |

### B. State Transition Tests

| TC ID | Mô tả | Trạng thái hiện tại | Sự kiện | Trạng thái kỳ vọng | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-B-ST-01 | | pending | confirm | confirmed | | |
| TC-B-ST-02 | | confirmed | ship | shipping | | |
| TC-B-ST-03 | | shipping | deliver | delivered | | |
| TC-B-ST-04 | | pending | cancel | cancelled | | |
| TC-B-ST-05 | | delivered | cancel | *(không hợp lệ)* | | |

### C. Security Tests (SEC-01 – SEC-07)

| TC ID | Mô tả | Loại tấn công | Input | Expected | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-B-SEC-01 | | SQL Injection | | | | |
| TC-B-SEC-02 | | IDOR | | | | |
| TC-B-SEC-03 | | Role Escalation | | | | |

### D. Schema Validation Tests

| TC ID | Mô tả | Field kiểm tra | Expected schema | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|
| TC-B-SV-01 | | | | | |
| TC-B-SV-02 | | | | | |

### E. Test Cases tự thêm (Extend – ≥ 5)

| TC ID | Mô tả | Loại | Lý do AI bỏ sót | Expected | Kết quả |
|:---|:---|:---|:---|:---|:---|
| TC-B-EXT-01 | | | | | |
| TC-B-EXT-02 | | | | | |
| TC-B-EXT-03 | | | | | |
| TC-B-EXT-04 | | | | | |
| TC-B-EXT-05 | | | | | |

---

## Kết quả thực thi (Execute)

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | | % |
| FAIL | | % |
| **Tổng** | | 100% |

*(Screenshot Newman / Postman Console đính kèm tại đây)*
