# Gap Analysis — FR-03: Quên mật khẩu & Đặt lại mật khẩu

**Module:** FORGOT · **Skills audited:** Domain Testing (Skill-01) + BVA (Skill-02)  
**AI output reviewed:** `tests/test-cases/forgot/TC-FORGOT-001.md` … `TC-FORGOT-020.md`  
**Spec source:** `README.md` FR-03, FR-01 (password rules), FR-22 (form standards)

---

## Expected Coverage Checklist — FR-03

### Input Variables
- [x] Email (Bước 1)
- [x] OTP (Bước 2)
- [x] Mật khẩu mới (Bước 2)
- [x] Xác nhận mật khẩu (Bước 2)

### Sub-domains / Equivalence Classes
- [x] Email: rỗng, sai format, chưa đăng ký, hợp lệ
- [x] OTP: rỗng, non-numeric, sai độ dài, sai giá trị, đúng, gắn email khác
- [x] Mật khẩu: rỗng, ngắn, thiếu hoa/thường/số/đặc biệt, hợp lệ
- [x] Xác nhận: rỗng, không khớp, khớp
- [x] UI: Step Indicator, Quay lại đăng nhập

### Boundary Points
- [ ] Email @ min− … max+ — **❌ Missing** (BVA TC 021–026 not committed)
- [ ] OTP length @ 5 / 6 / 7 — **⚠️ Partial** (DT 007–008 only; no dedicated 6-digit on-point BVA file)
- [ ] Password @ 7 … 51 chars — **❌ Missing** (BVA not in repo)
- [ ] Confirm password @ 7 … 51 — **❌ Missing**

### Business Rules
- [x] OTP chỉ hợp lệ cho email đã yêu cầu (TC-FORGOT-010)
- [x] Demo: OTP hiển thị trên màn hình — **⚠️ Partial** (no TC asserting exact 6-digit OTP from API)
- [ ] OTP chỉ dùng một lần / vô hiệu sau khi reset — **❌ Missing**
- [ ] Backend validate mật khẩu FR-01 — **❌ Missing**
- [ ] Email `type="email"` (FR-22) — **❌ Missing**
- [ ] Cross-boundary password pairs (min/min, max/max, mismatch at boundary) — **❌ Missing**

---

## Gap Catalogue

### GAP-01
- **Category:** Missing TC (BVA suite)
- **Item missed:** Toàn bộ BVA Email / Password / Confirm (TC-FORGOT-021 … 044)
- **Root cause:** □ Prompt quality · ☑ Spec complexity (BVA deferred) · □ AI limitation
- **Severity:** High
- **Remediation:** Re-apply Skill-02; commit BVA files or `TC-FORGOT-SUP-006` … `SUP-008`

### GAP-02
- **Category:** Missing variable / rule
- **Item missed:** OTP phải đúng **6 chữ số** (kiểm tra response API + label UI)
- **Root cause:** ☑ AI limitation — AI ghi 6 chữ số trong expected nhưng không có TC API-level
- **Severity:** High
- **Remediation:** `TC-FORGOT-SUP-001`

### GAP-03
- **Category:** Missing business rule
- **Item missed:** Backend không validate độ mạnh mật khẩu khi reset
- **Root cause:** ☑ Spec complexity — rule suy ra từ FR-01 nhưng không lặp trong FR-03
- **Severity:** High
- **Remediation:** `TC-FORGOT-SUP-002`

### GAP-04
- **Category:** Missing TC (cross-requirement)
- **Item missed:** Email input `type="email"` theo FR-22
- **Root cause:** ☑ Prompt quality — session chỉ trigger FR-03, không gộp FR-22
- **Severity:** Medium
- **Remediation:** `TC-FORGOT-SUP-003`

### GAP-05
- **Category:** Missing business rule
- **Item missed:** OTP một lần — token phải vô hiệu sau reset thành công
- **Root cause:** ☑ Spec complexity — implicit security rule
- **Severity:** Medium
- **Remediation:** `TC-FORGOT-SUP-004`

### GAP-06
- **Category:** Other
- **Item missed:** TC ID trong `tests/e2e/forgot-password.spec.js` **không khớp** markdown TC (cùng ID, khác kịch bản)
- **Root cause:** ☑ Prompt quality / quy trình — automation tạo song song không đồng bộ ID
- **Severity:** High (traceability broken)
- **Remediation:** Đồng bộ spec E2E với `tests/test-cases/forgot/` hoặc đổi ID automation

---

## Gap Summary Table

| Gap ID | Category | Severity | Variable / Rule | Root Cause | Remediation TC |
|--------|----------|----------|-----------------|------------|----------------|
| GAP-01 | Missing TC | High | BVA boundaries | Spec complexity | TC-FORGOT-021+ or SUP-006+ |
| GAP-02 | Missing rule | High | OTP 6 digits | AI limitation | TC-FORGOT-SUP-001 |
| GAP-03 | Missing rule | High | Server password validation | Spec complexity | TC-FORGOT-SUP-002 |
| GAP-04 | Missing TC | Medium | FR-22 email type | Prompt quality | TC-FORGOT-SUP-003 |
| GAP-05 | Missing rule | Medium | OTP one-time use | Spec complexity | TC-FORGOT-SUP-004 |
| GAP-06 | Other | High | TC ID mismatch | Process | Sync E2E ↔ markdown |

---

## AI Critique Paragraph

The AI-generated domain suite for FR-03 achieved broad equivalence-class coverage for the four main inputs and two UI requirements, but exhibited a consistent pattern of **stopping at the feature boundary** rather than tracing inherited rules. Password strength was copied from FR-01 in prose only; no supplementary case targeted server-side enforcement on `POST /api/reset-password`, which allowed a critical defect to surface only during execution. OTP testing treated “wrong length” as invalid input classes yet never pinned the **exact six-digit contract** against the backend generator, so the SUT’s four-digit implementation was under-specified in tests until execution. The largest process gap was **ID drift**: Playwright reused `TC-FORGOT-001`–`018` with different scenarios than the markdown files, breaking traceability for HW02. BVA cases (021–044) were designed in chat but not persisted, leaving length boundaries uncommitted. Root causes were dominated by **spec complexity** (implicit cross-feature rules) and **missing human review of ID conventions**. Future sessions should: (1) paste FR-01 + FR-22 constraints into the FR-03 prompt, (2) require one API-level OTP assertion, and (3) generate automation only after markdown TC IDs are frozen.
