# Gap Analysis — FR-15: Quản lý Sản phẩm (Product CRUD)

**Module:** PRODUCT · **Skills audited:** Domain Testing (Skill-01) + BVA (Skill-02)  
**AI output reviewed:** `tests/test-cases/product/TC-PRODUCT-001.md` … `TC-PRODUCT-011.md`, `TC-PRODUCT-020.md` … `TC-PRODUCT-032.md`  
**Spec source:** `README.md` FR-15; tham chiếu chéo FR-12 (access control), FR-21 (định dạng tiền), FR-22 (form standards)

---

## Expected Coverage Checklist — FR-15

### Input Variables
- [x] Tên sản phẩm
- [x] Giá
- [x] Danh mục (`category_id` / dropdown)
- [—] Mô tả, `imageUrl` — không có ràng buộc trong FR-15 (ngoài phạm vi)

### CRUD Operations
- [x] Thêm — `TC-PRODUCT-001`
- [x] Xem — `TC-PRODUCT-002`
- [x] Sửa — `TC-PRODUCT-009`, `TC-PRODUCT-010`
- [x] Xóa — `TC-PRODUCT-011`

### Sub-domains / Equivalence Classes
- [x] Tên: rỗng, hợp lệ (EP + BVA)
- [x] Giá: rỗng, 0, âm, không phải số, dương (EP + BVA)
- [x] Danh mục: không chọn (EP)
- [x] Danh mục: chọn từ danh sách có sẵn (EP — ngụ ý trong TC hợp lệ)
- [ ] Danh mục: `category_id` không tồn tại / không thuộc danh sách — **✅** `TC-PRODUCT-SUP-001`
- [ ] Tên chỉ gồm khoảng trắng — **✅** `TC-PRODUCT-SUP-008`

### Boundary Points
- [x] Tên @ 0, 1, 2, 254, 255, 256 — `TC-PRODUCT-020` … `025`
- [x] Giá @ −1, 0, 1, 2, 0.01 — `TC-PRODUCT-026` … `030`
- [x] Cross-boundary Sửa: Tên 256, Giá 0 — `TC-PRODUCT-031`, `032`
- [ ] Giá @ 0.001 (giữa 0 và 0.01) — **⚠️ Partial** (chỉ có 0 và 0.01; thiếu điểm giữa nếu SUT làm tròn)
- [ ] Cross-boundary Sửa **hợp lệ** (Tên 255 / Giá 1 trên form Sửa) — **✅** `TC-PRODUCT-SUP-009`, `SUP-010`

### Business Rules
- [x] Khi Sửa, chỉ sản phẩm đó thay đổi — `TC-PRODUCT-010`
- [ ] FR-12: chỉ Admin truy cập CRUD / API `POST|PUT|DELETE /api/products` — **✅** `TC-PRODUCT-SUP-002` … `004`
- [ ] FR-22: trường bắt buộc có ký hiệu `*` — **✅** `TC-PRODUCT-SUP-005`
- [ ] FR-22: thông báo lỗi **trên** nút Submit — **✅** `TC-PRODUCT-SUP-006`
- [ ] FR-21: Giá hiển thị ký hiệu `₫` và phân cách hàng nghìn trên UI Admin — **✅** `TC-PRODUCT-SUP-011`
- [ ] Backend validate đồng bộ với UI (API-level) — **✅** `TC-PRODUCT-SUP-007`
- [ ] Xóa sản phẩm có dialog xác nhận — **⚠️ N/A** (không nêu trong FR-15; có thể tham chiếu FR-24 cho consistency)

### Execution & Traceability
- [ ] Tất cả TC đều `Not Run` — **❌ Missing** (chưa thực thi / chưa ghi kết quả)
- [ ] `traceability-matrix.md` chưa có dòng FR-15 — **❌ Missing**
- [x] `tests/e2e/admin-product.spec.js` khớp ID markdown — **✅ Done** (24 TC + 11 SUP)

---

## Gap Catalogue

### GAP-01
- **Category:** Missing variable / rule
- **Item missed:** Danh mục với `category_id` không tồn tại hoặc không thuộc danh sách có sẵn (phân vùng không hợp lệ ngoài “không chọn”)
- **Root cause:** ☑ Spec complexity — UI dropdown có thể che phân vùng này; cần TC API hoặc thao tác trực tiếp
- **Severity:** Medium
- **Remediation:** `TC-PRODUCT-SUP-001` — `POST /api/products` với `category_id: 99999` (admin JWT)

### GAP-02
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-12 — user thường / không token không được tạo-sửa-xóa sản phẩm
- **Root cause:** ☑ Prompt quality — session FR-15 giới hạn phạm vi, bỏ access control khỏi markdown
- **Severity:** High (bảo mật Admin)
- **Remediation:** `TC-PRODUCT-SUP-002` … `SUP-004` (UI chặn user; API 401/403) hoặc map sang suite FR-12

### GAP-03
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-22 — nhãn Tên / Giá / Danh mục bắt buộc phải có `*`
- **Root cause:** ☑ Prompt quality — không gộp FR-22 vào prompt FR-15
- **Severity:** Medium
- **Remediation:** `TC-PRODUCT-SUP-005`

### GAP-04
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-22 — thông báo lỗi validation xuất hiện **trên** nút Submit
- **Root cause:** ☑ Prompt quality
- **Severity:** Medium
- **Remediation:** `TC-PRODUCT-SUP-006` (kích hoạt lỗi bằng TC-003 hoặc TC-008, kiểm tra vị trí DOM)

### GAP-05
- **Category:** Missing business rule
- **Item missed:** Backend từ chối payload không hợp lệ khi bỏ qua UI (server-side validation)
- **Root cause:** ☑ AI limitation — suite tập trung UI form, không có assertion API
- **Severity:** High
- **Remediation:** `TC-PRODUCT-SUP-007` — `POST /api/products` name 256 chars / price 0 với admin token

### GAP-06
- **Category:** Other
- **Item missed:** TC ID trong `tests/e2e/admin-product.spec.js` **không khớp** markdown `tests/test-cases/product/`
- **Root cause:** ☑ Prompt quality / quy trình — automation tạo trước, markdown refactor sau với ID và kịch bản khác
- **Severity:** High (traceability broken)
- **Remediation:** ✅ Đã đồng bộ E2E (`001`–`032` + `SUP-001`–`011`)

### GAP-07
- **Category:** Missing TC (edge case)
- **Item missed:** Tên sản phẩm chỉ gồm khoảng trắng (`"   "`) — có thể vượt qua client nhưng không hợp lệ nghiệp vụ
- **Root cause:** ☑ AI limitation — EP “rỗng” không bao phủ whitespace-only
- **Severity:** Low
- **Remediation:** `TC-PRODUCT-SUP-008`

### GAP-08
- **Category:** Missing TC (BVA cross-context)
- **Item missed:** Form **Sửa** với giá trị biên **hợp lệ** (Tên 255 ký tự, Giá 1) — chỉ có cross-boundary **invalid** (031–032)
- **Root cause:** ☑ Spec complexity — BVA mặc định chỉ trên form Thêm
- **Severity:** Low
- **Remediation:** `TC-PRODUCT-SUP-009`, `SUP-010`

### GAP-09
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-21 — định dạng Giá `₫` + phân cách hàng nghìn trên danh sách / form Admin
- **Root cause:** ☑ Prompt quality — FR-15 không nhắc định dạng tiền; rule nằm ở FR-21
- **Severity:** Low
- **Remediation:** `TC-PRODUCT-SUP-011`

### GAP-10
- **Category:** Other
- **Item missed:** Traceability matrix và trạng thái thực thi cho 24 TC FR-15
- **Root cause:** ☑ Process — chưa chạy test, chưa cập nhật `traceability-matrix.md`
- **Severity:** Medium (HW02 deliverable)
- **Remediation:** Thực thi manual/E2E; thêm 24 dòng vào `traceability-matrix.md`

---

## Gap Summary Table

| Gap ID | Category | Severity | Variable / Rule | Root Cause | Remediation TC |
|--------|----------|----------|-----------------|------------|----------------|
| GAP-01 | Missing variable | Medium | `category_id` không hợp lệ | Spec complexity | TC-PRODUCT-SUP-001 |
| GAP-02 | Cross-requirement | High | FR-12 access control | Prompt quality | TC-PRODUCT-SUP-002 … 004 |
| GAP-03 | Cross-requirement | Medium | FR-22 required `*` | Prompt quality | TC-PRODUCT-SUP-005 |
| GAP-04 | Cross-requirement | Medium | FR-22 error position | Prompt quality | TC-PRODUCT-SUP-006 |
| GAP-05 | Missing rule | High | Server-side validation | AI limitation | TC-PRODUCT-SUP-007 |
| GAP-06 | Other | High | E2E ↔ markdown ID drift | Process | Sync E2E sau khi freeze ID |
| GAP-07 | Edge case | Low | Whitespace-only name | AI limitation | TC-PRODUCT-SUP-008 |
| GAP-08 | BVA cross-context | Low | Edit valid boundaries | Spec complexity | TC-PRODUCT-SUP-009 … 010 |
| GAP-09 | Cross-requirement | Low | FR-21 price format | Prompt quality | TC-PRODUCT-SUP-011 |
| GAP-10 | Process | Medium | Traceability / execution | Process | Run tests + matrix |

---

## Coverage Summary

| Kỹ thuật | Số TC | Trạng thái |
|----------|-------|------------|
| Domain Testing (EP) | 11 (`001`–`011`) | ✅ Đủ phân vùng chính cho 3 input + CRUD + rule sửa độc lập |
| BVA | 13 (`020`–`032`) | ✅ Đủ 6 điểm biên Tên; 5 điểm biên Giá; 2 cross-boundary Sửa (invalid) |
| Supplementary | 11 (`SUP-001`–`SUP-011`) | ✅ Đã commit + automation |
| **Tổng** | **35** | Chưa thực thi (`Not Run`) |

---

## AI Critique Paragraph

The FR-15 suite delivers solid **in-scope** coverage of FR-15 itself: all four CRUD verbs are represented, the three constrained inputs (Tên, Giá, Danh mục) have equivalence classes on the Add form, and BVA commits the full six-point name ladder (0→256) plus price boundaries around the `> 0` contract. Deliberately excluding FR-12 from markdown avoided spec creep but leaves a **high-severity integration gap** for Admin security that homework traceability may still expect. The largest process risk mirrors FR-03 (**GAP-06**): legacy Playwright file `admin-product.spec.js` still maps `TC-PRODUCT-001`–`016` to different scenarios (navigation, SEC tests, old BVA numbering), so automation must not be run against current markdown until IDs are reconciled. Category validation stops at “empty dropdown” and never tests a **non-existent `category_id`**, which UI-only testing often misses. Cross-cutting GUI rules from FR-22 (`*`, error placement) and FR-21 (₫ formatting) were not inherited—same “feature boundary” pattern seen in FR-03 vs FR-01/FR-22. Recommended next steps: (1) add `TC-PRODUCT-SUP-001` and `SUP-007` for server contracts, (2) freeze markdown IDs then rewrite E2E, (3) extend prompt with FR-12 + FR-22 snippets for Admin forms, (4) execute and populate `traceability-matrix.md`.
