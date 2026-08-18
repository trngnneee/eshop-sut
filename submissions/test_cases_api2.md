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

### A. Domain Partition & Boundary Value Tests (EP & BVA)

| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload (Params/Body) | Expected HTTP Status & Output | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-B-DP-01 | | | | | | *(cần review)* | |
| TC-B-DP-02 | | | | | | *(cần review)* | |
| TC-B-DP-03 | | | | | | *(cần review)* | |
| TC-B-DP-04 | | | | | | *(cần review)* | |
| TC-B-DP-05 | | | | | | *(cần review)* | |

### B. State Transition & Lifecycle Tests

| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-B-ST-01 | Chuyển trạng thái sang Confirmed | pending | PUT /status (confirmed) | confirmed | 200 OK | *(cần review)* | |
| TC-B-ST-02 | Chuyển trạng thái sang Shipping | confirmed | PUT /status (shipping) | shipping | 200 OK | *(cần review)* | |
| TC-B-ST-03 | Chuyển trạng thái sang Delivered | shipping | PUT /status (delivered) | delivered | 200 OK | *(cần review)* | |
| TC-B-ST-04 | Hủy đơn hàng khi đang pending | pending | PUT /cancel | cancelled | 200 OK | *(cần review)* | |
| TC-B-ST-05 | Hủy đơn khi đã delivered (Invalid) | delivered | PUT /cancel | delivered (unchanged) | 400 Bad Request | *(cần review)* | |

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
