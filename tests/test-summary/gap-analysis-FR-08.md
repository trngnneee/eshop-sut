# Gap Analysis — FR-08: Thanh toán (Checkout)

**Module:** CHECKOUT · **Skills audited:** Domain Testing (Skill-01) + BVA (Skill-02)  
**AI output reviewed:** `tests/test-cases/checkout/TC-CHECKOUT-001.md` … `TC-CHECKOUT-044.md`, `TC-CHECKOUT-SUP-001` … `SUP-006`  
**Spec source:** `README.md` FR-08; tham chiếu chéo FR-06, FR-07, FR-21, FR-23, SEC-02

---

## Expected Coverage Checklist — FR-08

### Input Variables
- [x] Trạng thái đăng nhập / JWT (Rule 1)
- [x] Trạng thái giỏ hàng (số mục, số loại, số lượng)
- [x] Tổng tiền hiển thị trên UI (Rule 2)
- [x] `total_amount` do client gửi lên API (Rule 4)
- [x] Danh sách sản phẩm đặt mua — tên, số lượng, thành tiền (Rule 3)

### Sub-domains / Equivalence Classes
- [x] Auth: chưa đăng nhập (giỏ + URL), token hết hạn, token không hợp lệ, không token, header sai định dạng, đã đăng nhập (user + admin)
- [x] Giỏ: trống, 1 loại, nhiều loại, gộp SP trùng (FR-07)
- [x] Tổng UI: tự động tính, không chỉnh sửa, sửa UI nhưng đơn phải đúng
- [x] `total_amount` API: âm, 0, thiếu, chuỗi, khớp cartTotal, lệch ±1, 1, 2×, thập phân, items rỗng, items không khớp giỏ
- [x] Hậu thanh toán: giỏ xóa, badge = 0, chặn thanh toán lần 2

### Boundary Points
- [x] Số lượng @ 1 / 2 / 3 / 10 / 99 — TC-CHECKOUT-010, 011, 034, 035, 040
- [x] Số loại SP @ 0 / 1 / 2 / 3 / 4 — TC-CHECKOUT-012, 013, 014, 036, 041
- [x] `total_amount` @ 0, cartTotal−1, cartTotal, cartTotal+1 — TC-CHECKOUT-015 … 018
- [x] `total_amount` @ −1, 1, 2×cartTotal, decimal — TC-CHECKOUT-038, 039, 042, 043
- [x] Đơn giá @ min (> 0) — TC-CHECKOUT-037
- [ ] Đơn giá @ max (sản phẩm giá cao nhất trong seed, ví dụ 45.000.000 ₫) — **❌ Missing**
- [ ] Số lượng @ min− (0) tại checkout — **⚠️ Partial** (không thể có qty=0 trong giỏ; chưa có TC FR-06 trước khi vào checkout)

### Business Rules (FR-08 verbatim)
- [x] Rule 1 — Chỉ user đã đăng nhập mới thanh toán (001, 002, 019, 020, SUP-001, SUP-002, SUP-005)
- [x] Rule 2 — Tổng tự động tính, không chỉnh sửa (004, 005, 026, 010–044)
- [x] Rule 3 — Hiển thị đầy đủ danh sách SP (003, 009, 021–025, 024)
- [x] Rule 4 — Backend tự tính lại; không tin `total_amount` client (015–018, 029–032, 038–043, SUP-003, SUP-004, SUP-006)
- [x] Rule 5 — Giỏ xóa sau thành công (007, 027, 028)

### Cross-requirement / Implicit
- [ ] FR-21 — Định dạng `₫` + phân cách hàng nghìn trên checkout — **⚠️ Partial** (nhắc trong 003/005; không có TC riêng)
- [ ] FR-21 — Đúng 1 thẻ `<h1>` trên trang Thanh toán — **❌ Missing**
- [ ] FR-23 — Breadcrumb bắt buộc ở trang Thanh toán — **❌ Missing**
- [ ] FR-09 — Mã giảm giá tại checkout ảnh hưởng `final_amount` gửi API — **❌ Missing** (thuộc FR-09; UI checkout đã có coupon nhưng không có TC FR-08/09)
- [ ] SEC-02 — Checkout API yêu cầu JWT — **x** (SUP-002, SUP-001)
- [ ] SEC-04 — Tên SP hiển thị an toàn trên checkout (không render HTML) — **❌ Missing**
- [ ] Server cart (`userCarts`) xóa sau checkout — **❌ Missing** (web dùng `CartContext` client; API có `userCarts` riêng)
- [ ] `shipping_address` lưu vào đơn hàng — **❌ Missing**
- [ ] FR-20 — Thanh toán trên Mobile — **❌ Missing** (ngoài phạm vi session web)

### Process / Traceability
- [ ] Traceability matrix — **❌ Missing** (`traceability-matrix.md` chưa có hàng FR-08)
- [ ] Test run / execution — **❌ Missing** (toàn bộ TC `Not Run`)
- [ ] Bug reports checkout — **❌ Missing** (chưa có `issue-011+` cho lỗi FR-08)
- [ ] E2E Playwright đồng bộ markdown TC — **⚠️ Deferred** (user: sẽ sửa `checkout.spec.js` sau)

---

## Gap Catalogue

### GAP-01
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-23 — Breadcrumb trên trang Thanh toán
- **Root cause:** ☑ Prompt quality — session chỉ trigger FR-08, không gộp FR-23
- **Severity:** Medium
- **Remediation:** `TC-CHECKOUT-SUP-007` hoặc TC GUI riêng

### GAP-02
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-21 — Một `<h1>` duy nhất; SUT hiện dùng `<h2>` cho tiêu đề checkout
- **Root cause:** ☑ Spec complexity — tiêu chuẩn GUI tách mục FR-21
- **Severity:** Low
- **Remediation:** `TC-CHECKOUT-SUP-008`

### GAP-03
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-21 — Kiểm tra định dạng tiền tệ `₫` + phân cách hàng nghìn trên tổng và từng dòng
- **Root cause:** ☑ AI limitation — kỳ vọng lẫn trong TC khác, không assert riêng
- **Severity:** Medium
- **Remediation:** `TC-CHECKOUT-SUP-009`

### GAP-04
- **Category:** Missing business rule
- **Item missed:** FR-09 tương tác — `final_amount` sau coupon được gửi làm `total_amount`; backend vẫn phải validate so với giỏ
- **Root cause:** ☑ Spec complexity — coupon thuộc FR-09; checkout UI đã tích hợp coupon
- **Severity:** High (khi test FR-08 trên trang checkout thực tế)
- **Remediation:** TC thuộc module COUPON/FR-09 hoặc `TC-CHECKOUT-SUP-010`

### GAP-05
- **Category:** Missing variable / rule
- **Item missed:** Giỏ phía server (`POST /api/cart`, `userCarts`) không được xóa sau checkout — chỉ test client `CartContext`
- **Root cause:** ☑ Spec complexity — web cart client-side vs API cart in-memory
- **Severity:** Medium
- **Remediation:** `TC-CHECKOUT-SUP-011`

### GAP-06
- **Category:** Missing TC (BVA)
- **Item missed:** Đơn giá @ max — sản phẩm giá cao (ví dụ MacBook 45.000.000 ₫ × qty 1)
- **Root cause:** ☑ AI limitation — chỉ thêm BVA price min (037)
- **Severity:** Low
- **Remediation:** `TC-CHECKOUT-045`

### GAP-07
- **Category:** Missing TC (security)
- **Item missed:** SEC-04 — Tên sản phẩm chứa HTML/script hiển thị escaped trên checkout
- **Root cause:** ☑ Prompt quality — SEC chỉ tham khảo, không đưa vào prompt FR-08
- **Severity:** Medium
- **Remediation:** `TC-CHECKOUT-SUP-012`

### GAP-08
- **Category:** Missing variable
- **Item missed:** `coupon_id` giả mạo trong body checkout
- **Root cause:** ☑ Spec complexity — field tồn tại trong `Checkout.jsx` nhưng không nằm trong FR-08 text
- **Severity:** Medium
- **Remediation:** `TC-CHECKOUT-SUP-013`

### GAP-09
- **Category:** Missing variable
- **Item missed:** `shipping_address` trên đơn hàng (API nhận field nhưng không có TC)
- **Root cause:** ☑ AI limitation — FR-08 không nhắc địa chỉ giao hàng
- **Severity:** Low
- **Remediation:** `TC-CHECKOUT-SUP-014` (nếu mở rộng spec)

### GAP-10
- **Category:** Other
- **Item missed:** Traceability matrix + test run + bug reports cho FR-08
- **Root cause:** ☑ Prompt quality / quy trình — mới có markdown TC, chưa execute
- **Severity:** High (HW traceability)
- **Remediation:** Cập nhật `traceability-matrix.md`, chạy test, ghi `issue-011+`

### GAP-11
- **Category:** Other
- **Item missed:** E2E `checkout.spec.js` chưa đồng bộ 50 markdown TC
- **Root cause:** ☑ Process — cố ý tách test case khỏi automation cũ
- **Severity:** High (khi nộp automation)
- **Remediation:** Viết lại E2E theo `TC-CHECKOUT-001` … `044`

---

## Gap Summary Table

| Gap ID | Category | Severity | Variable / Rule | Root Cause | Remediation TC |
|--------|----------|----------|-----------------|------------|----------------|
| GAP-01 | Missing TC | Medium | FR-23 breadcrumb | Prompt quality | TC-CHECKOUT-SUP-007 |
| GAP-02 | Missing TC | Low | FR-21 single h1 | Spec complexity | TC-CHECKOUT-SUP-008 |
| GAP-03 | Missing TC | Medium | FR-21 currency format | AI limitation | TC-CHECKOUT-SUP-009 |
| GAP-04 | Missing rule | High | FR-09 coupon + total | Spec complexity | TC-CHECKOUT-SUP-010 / FR-09 suite |
| GAP-05 | Missing rule | Medium | Server cart clear | Spec complexity | TC-CHECKOUT-SUP-011 |
| GAP-06 | Missing BVA | Low | Price max boundary | AI limitation | TC-CHECKOUT-045 |
| GAP-07 | Missing security | Medium | SEC-04 XSS on list | Prompt quality | TC-CHECKOUT-SUP-012 |
| GAP-08 | Missing variable | Medium | coupon_id tamper | Spec complexity | TC-CHECKOUT-SUP-013 |
| GAP-09 | Missing variable | Low | shipping_address | AI limitation | TC-CHECKOUT-SUP-014 |
| GAP-10 | Other | High | Traceability / execution | Process | Matrix + test run + bugs |
| GAP-11 | Other | High | E2E ID sync | Process | Rewrite checkout.spec.js |

---

## FR-08 Rule → Test Case Mapping (Audit)

| # | Yêu cầu FR-08 | TC chính | Độ bao phủ |
|---|---------------|----------|------------|
| 1 | Chỉ user đã đăng nhập | 001, 002, 019, 020, SUP-001, SUP-002, SUP-005, 033 | **Đủ** (UI + API) |
| 2 | Tổng tự động, không sửa UI | 004, 005, 026, 010–044 | **Đủ** (SUT vi phạm: input `type=number` editable) |
| 3 | Danh sách SP đầy đủ | 003, 009, 021–025, 024, 013, 014, 036, 041 | **Đủ** |
| 4 | Backend tự tính lại total | 015–018, 029–032, 038–043, SUP-003, 004, 006 | **Đủ** (SUT vi phạm: lưu `total_amount` client) |
| 5 | Giỏ xóa sau thành công | 007, 027, 028 | **Đủ** (SUT vi phạm: `clearCart()` không gọi) |

---

## Known SUT Defects (chưa có bug report)

| # | Mô tả | Bằng chứng SUT | TC phát hiện khi chạy |
|---|--------|----------------|------------------------|
| D1 | Tổng tiền cho phép sửa trên UI | `Checkout.jsx` `input[type=number]` + `editableTotal` | 004, 026 |
| D2 | Giỏ client không xóa sau checkout | `handleCheckout` không gọi `clearCart()` | 007, 027 |
| D3 | Backend tin `total_amount` client | `server.js` `INSERT … total_amount` từ `req.body` | 015–018, SUP-003 |
| D4 | Backend bỏ qua `items` trong body | API không đọc `items` khi tính đơn | SUP-004, SUP-006 |
| D5 | `/checkout` không guard route | `App.jsx` không bảo vệ route | 019 |

→ Cần tạo `issue-011` … `issue-015` sau test run.

---

## AI Critique Paragraph

The checkout suite grew from an initial **under-scoped 21-case draft** (one scenario per FR-08 bullet) to **50 markdown files** after user feedback, and now provides solid **equivalence-class and BVA coverage** for authentication, cart shape, product-line display, client `total_amount` tampering, and post-checkout cart state. Against the **literal five sentences of FR-08**, rule-level coverage is complete; the remaining gaps are **cross-feature inheritance** (FR-21 currency/h1, FR-23 breadcrumb, FR-09 coupon on the same page) and **architecture blind spots** (client `CartContext` vs server `userCarts`, no line items in `orders` table). The AI correctly added supplementary API cases (SUP-003–006) for backend recalculation—matching the highest-risk FR-08 rule—but did not initially produce BVA until prompted, mirroring the FR-03 pattern in `gap-analysis-FR-03.md`. Duplicate empty-cart coverage (DT-008 vs BVA-012) is acceptable for technique separation. **No test has been executed** and **no traceability row or bug issue** exists yet, so defects D1–D5 are predicted from static code review, not run evidence. Root causes: **narrow initial prompt** (FR-08 only), **spec complexity** (coupon UI + dual cart stores), and **deferred automation**. Recommended next steps: (1) add SUP-007–010 for GUI/coupon gaps, (2) run manual or E2E against TC-004/007/016, (3) file bug reports, (4) extend matrix before Sprint test run.
