# Test Cases — Bảng tổng (Master Summary)

**Họ và tên:** Đặng Trường Nguyên · **MSSV:** 23127438 · **Ngày cập nhật:** 23/08/2026
**SUT:** EShop backend `http://localhost:3000` · **Scope:** 3 API (FR-05/06, FR-10, FR-15)

> Tổng hợp toàn bộ test case của 3 API sau khi đã: (a) AI sinh ở Bước 2, (b) audit VALID/INVALID/INCOMPLETE ở Bước 3
> (xem `docs/ai-testcase-audit.md`), (c) **extend** thêm case tự nghĩ ở Bước 4 (xem `docs/extended-cases.md`).
> Mọi "Actual" đều đã probe cURL live trên `localhost:3000` (backup + restore `database.sqlite`).

---

## 1. Tổng số test case

| API | Endpoint | Base (Bước 2, sau audit) | Extend (Bước 4) 🆕 | **Tổng** |
|-----|----------|--------------------------|---------------------|----------|
| **API-1** | `GET /api/products/:id` (+ `?search=`) | 83 | 2 (TC-P1-084, 085) | **85** |
| **API-2** | `PUT /api/orders/:id/cancel` | 57 | 2 (TC-O2-058, 059) | **59** |
| **API-3** | `POST /api/products` + `PUT /api/products/:id` | 72 | 3 (TC-P3-074, 075, 076) | **75** |
| | | | **Tổng cộng** | **219** |

> Ghi chú số học: AI sinh 212 (Bước 2) − 1 (TC-P3-048 gộp vào 057 ở audit) + 1 (TC-P3-073 bù ở audit) + 7 (extend Bước 4) = **219**.

---

## 2. Chi tiết theo nhóm kỹ thuật

### API-1 — 85 case
| Nhóm | File | Số case | TC-ID |
|------|------|---------|-------|
| Equivalence Partitioning + BVA | `API-1_TestCases.md` | 44 | 001–044 |
| Security (SEC-04/05) | `API-1_Security_TestCases.md` | 14 | 045–058 |
| Schema validation | `API-1_Schema_TestCases.md` | 16 | 059–074 |
| Negative / Contract | `API-1_Negative_Contract_TestCases.md` | 9 | 075–083 |
| **Extend** 🆕 | `docs/extended-cases.md` | 2 | 084–085 |

### API-2 — 59 case
| Nhóm | File | Số case | TC-ID |
|------|------|---------|-------|
| Phân hoạch `:id` + ownership | `API-2_TestCases.md` | 15 | 001–015 |
| State Transition (FR-10) | `API-2_StateTransition_TestCases.md` | 9 | 016–024 |
| Security (auth/forge/IDOR) | `API-2_Security_TestCases.md` | 13 | 025–037 |
| Schema validation | `API-2_Schema_TestCases.md` | 11 | 038–048 |
| Negative / Contract | `API-2_Negative_Contract_TestCases.md` | 9 | 049–057 |
| **Extend** 🆕 | `docs/extended-cases.md` | 2 | 058–059 |

### API-3 — 75 case
| Nhóm | File | Số case | TC-ID |
|------|------|---------|-------|
| Input Validation (Partition+BVA) | `API-3_TestCases.md` | 48* | 001–047, 073 |
| Security (auth/role/forge/XSS) | `API-3_Security_TestCases.md` | 13 | 049–061 |
| Schema validation | `API-3_Schema_TestCases.md` | 11 | 062–072 |
| **Extend** 🆕 | `docs/extended-cases.md` | 3 | 074–076 |

*TC-P3-048 đã gộp vào TC-P3-057 (dòng gạch còn giữ để giải thích khoảng trống ID); TC-P3-073 bù lại.

---

## 3. Bảy case Extend (Bước 4) — case AI sinh-từ-spec dễ bỏ sót

| TC-ID | Case | Actual (đã probe) | Expected | Nhóm lý do |
|-------|------|-------------------|----------|-----------|
| **TC-P1-084** | `GET /api/products/2.0` (id chẵn, không canonical) | price = `"28000000"` (**string**) | `400` / price number | [API] affinity + `id%2` chồng nhau |
| **TC-P1-085** | `?search=%` | trả **cả 5** sản phẩm (bypass filter) | `200` + array rỗng | [API] nối chuỗi `'%%%'` |
| **TC-O2-058** | `GET /api/orders/:id` **không token** | `200`, lộ đơn người khác (`shipping_address`...) | `401`/`403` | [Prompt] endpoint liền kề — BUG-06 |
| **TC-O2-059** | double-cancel **song song** | ⚠ probe được `200`+`400` (xem note) | 1×`200`, 1×`400` | [Model] race read-check-write |
| **TC-P3-074** | `DELETE /api/products/99999` | `200 "Product deleted"` im lặng | `404` | [API] không kiểm `this.changes` |
| **TC-P3-075** | 2 sản phẩm **trùng tên** | cả 2 `200 created` (2 record) | ràng buộc/cảnh báo | [API] thiếu `UNIQUE(name)` |
| **TC-P3-076** | `POST price:true` (boolean) | `200 created` | `400` | [Model] hiếm ai thử boolean |

> **⚠ Đính chính TC-O2-059 (race condition):** khi probe lại (23/08), 2 request song song trả **`200` + `400`** (SUT serialize
> đúng nhờ event-loop Node + sqlite3), **không** phải "cả 2 đều 200" như ghi ban đầu trong `extended-cases.md`. Cửa sổ race
> (read-check-write không atomic) **tồn tại về lý thuyết** nhưng **không tái hiện ổn định** trên SQLite. → Nên hạ mức phát hiện
> này xuống **observation/nghi vấn**, không khẳng định là bug chắc chắn. Cần sửa lại dòng TC-O2-059 trong `extended-cases.md`.

---

## 4. Test Summary (cho README bài nộp)

| Chỉ số | Giá trị |
|--------|---------|
| Số API | 3 |
| Test case **AI sinh** (Bước 2) | 212 |
| Test case **tự thêm/extend** (audit + Bước 4) | 8 (TC-P3-073 + 7 extend) |
| Test case **gộp/bỏ** (audit) | 1 (TC-P3-048) |
| **Tổng test case hiệu lực** | **219** |
| Test case **đã execute** (probe live) | 219 / 219 |
| Test case **kỳ vọng PASS** (SUT làm đúng spec) | ~145 |
| Test case **kỳ vọng FAIL = lộ bug** (VALID-but-FAIL) | ~74 |
| **Số bug đã verify** | **20** (BUG-01→18, 20, 21; trừ BUG-19 đã hạ thành OBS-01) |
| Cờ SEC-04 (stored/reflected XSS vector — kiểm chéo UI) | 1 nhóm |
| Bug ngoài scope (nêu 1 dòng) | 5 (login lockout, users/me role, OTP, admin canceled→delivered, plaintext pw) |

> Con số PASS/FAIL là **ước lượng** từ cột verdict trong Phụ lục mỗi file; số chính xác lấy từ **Newman report** sau khi
> chạy collection (Bước 6) — sẽ cập nhật lại ô này bằng số thật của Newman.

---

## 5. Ánh xạ Bug ↔ Test case (dùng cho Bug report §8)

| Bug | Severity | API | Test case tiêu biểu |
|-----|----------|-----|---------------------|
| BUG-01 | Major | API-1 | TC-P1-004/005/020/062/063/070, TC-P1-084 |
| BUG-02 | Major | API-1 | TC-P1-006/007/065 |
| BUG-03 | **Critical** | API-1 | TC-P1-045/046/047 |
| BUG-04 | Major | API-1 | TC-P1-050/051/052/053 |
| BUG-05 | **Critical** | API-2 | TC-O2-018/023/041 |
| BUG-06 | **Critical** | API-2 (adjacent) | TC-O2-058 🆕 |
| BUG-07 | **Critical** | API-3 | TC-P3-049/050/052/053/054/055/070 |
| BUG-08 | **Critical** | API-3 | TC-P3-004/005/011/012/021/025/030/068 |
| BUG-09 | Major | API-3 | TC-P3-031 |
| BUG-10 | Major | API-3 | TC-P3-006/007 |
| BUG-11 | **Critical** | API-3 | TC-P3-034/042 |
| BUG-12 | Major | API-3 | TC-P3-035/069, TC-P3-074 🆕 |
| BUG-13 | **Critical** | API-2/3 | TC-O2-032/033, TC-P3-051 |
| BUG-14 | Minor | API-1 | TC-P1-012/015/016/017/018, TC-P1-084 |
| BUG-15 | Minor | API-1/2/3 | TC-P1-025/075, TC-O2-009/049/050/051/053, TC-P3-043/044/045 |
| BUG-16 | Major | API-1 | TC-P1-038 |
| BUG-17 | Major | API-1 | TC-P1-040/041/042, TC-P1-085 🆕 |
| BUG-18 | Minor | API-1 | TC-P1-044 |
| BUG-20 | **Critical** | API-1 | TC-P1-048/049 |
| BUG-21 | Minor | API-1 | TC-P1-056 |

> Thêm quan sát: **TC-P3-075** (thiếu `UNIQUE(name)`) và **TC-P3-076** (price boolean) là biến thể của BUG-08
> (thiếu validation) — có thể gộp vào BUG-08 hoặc tách bug phụ tuỳ mức chi tiết bug report.
