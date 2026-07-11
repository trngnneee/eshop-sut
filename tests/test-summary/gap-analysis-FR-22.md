# Gap Analysis — FR-22: Quên mật khẩu & Đặt lại mật khẩu trên Mobile

**Module:** FORGOT-MOBILE · **Skills audited:** Domain Testing (Skill-01) + BVA (Skill-02)  
**AI output reviewed:** `tests/test-cases/forgot-mobile/FR-22-requirement.md`, `TC-MFORGOT-001.md` … `TC-MFORGOT-020.md`  
**Spec source:** `README.md` FR-03 (nghiệp vụ gốc), FR-01 (quy tắc mật khẩu), FR-20 (phân hệ Mobile), FR-22 (form standards), SEC-07 (OTP)

> **Lưu ý đối chiếu README:** `README.md` có **FR-03** (Quên mật khẩu Web) và **FR-22** (Form Requirements: Step Indicator, inline error, …). Bộ test Mobile áp dụng **FR-03** (nghiệp vụ 2 bước) kết hợp **FR-22** (chuẩn form) trên Mobile App. **FR-20** liệt kê phân hệ Mobile nhưng **không nêu rõ** “Quên mật khẩu” — ghi trong báo cáo là phạm vi mở rộng / ánh xạ từ FR-03.

---

## Expected Coverage Checklist — FR-22 (≡ FR-03 trên Mobile)

### Input Variables
- [x] Email (Bước 1) — `TC-MFORGOT-002` … `004`, `001`
- [x] OTP (Bước 2) — `TC-MFORGOT-005` … `010`
- [x] Mật khẩu mới (Bước 2) — `TC-MFORGOT-011` … `016`
- [x] Xác nhận mật khẩu (Bước 2) — `TC-MFORGOT-017` … `018`, `001`

### Sub-domains / Equivalence Classes
- [x] Email: rỗng, sai format, chưa đăng ký, hợp lệ
- [x] OTP: rỗng, non-numeric, sai độ dài, sai giá trị, đúng, gắn email khác
- [x] Mật khẩu: rỗng, ngắn, thiếu hoa/thường/số/đặc biệt, hợp lệ
- [x] Xác nhận: rỗng, không khớp, khớp
- [x] UI: Step Indicator, Quay lại đăng nhập

### Boundary Points
- [ ] Email @ min− … max+ — **❌ Missing** (web có `TC-FORGOT-021` … `026`; mobile chưa mirror)
- [ ] OTP length @ 5 / 6 / 7 — **⚠️ Partial** (`TC-MFORGOT-007`–`008` EP only; thiếu BVA on-point 6 chữ số)
- [ ] Password @ 7 … 51 chars — **❌ Missing**
- [ ] Confirm password @ 7 … 51 — **❌ Missing**

### Business Rules (FR-03 / FR-01)
- [x] OTP chỉ hợp lệ cho email đã yêu cầu (`TC-MFORGOT-010`)
- [ ] Demo: OTP **hiển thị trực tiếp trên màn hình** — **❌ Missing** (TC-001 ghi chú fallback API; không có TC assert UI demo)
- [ ] OTP đúng **6 chữ số** (label + API) — **❌ Missing** (SUT Mobile label “Mã OTP (4 số)”)
- [ ] OTP một lần / vô hiệu sau reset (SEC-07) — **❌ Missing**
- [ ] Backend validate mật khẩu FR-01 — **❌ Missing**
- [ ] Hai trường mật khẩu khớp — **⚠️ Partial** (TC-017/018 có nhưng **UI Mobile không có** trường xác nhận)

### Mobile / Cross-requirement
- [ ] FR-20: chức năng Quên mật khẩu nằm trong phạm vi Mobile — **⚠️ Implicit** (không có trong danh sách FR-20)
- [ ] FR-22: trường bắt buộc có `*` — **❌ Missing**
- [ ] FR-22: lỗi **trên** nút submit — **❌ Missing** (Mobile dùng `Alert.alert`, không inline)
- [ ] FR-22: Step Indicator form 2 bước — **⚠️ Covered by TC-019** nhưng SUT thiếu
- [ ] FR-22: `type="email"` / `type="password"` — **⚠️ N/A HTML**; thiếu TC tương đương Mobile (`keyboardType`, `secureTextEntry`)
- [ ] FR-21: nhất quán tiếng Việt trên màn hình Forgot — **❌ Missing** (Login Mobile còn “Sign In”, “Username”)

### Execution & Traceability
- [ ] Tất cả TC đều `Not Run` — **❌ Missing**
- [ ] `traceability-matrix.md` chưa có dòng FR-22 — **❌ Missing**
- [ ] Không có E2E / Maestro / Detox cho Mobile Forgot — **❌ Missing**

---

## SUT Observations (đối chiếu `frontend-mobile/App.js`)

| Điểm đặc tả (FR-03) | Triển khai Mobile hiện tại | TC AI bắt được? |
|---------------------|----------------------------|-----------------|
| OTP 6 chữ số, demo hiển thị trên màn hình | Message chung, **không** hiển thị OTP; label “4 số” | ⚠️ Một phần (TC-001 có ghi chú API) |
| Step Indicator “Bước 1/2” | Không có | ✅ TC-019 |
| Nút “Quay lại đăng nhập” | Chỉ “← Quay lại” (về Bước 1); Bước 1 không có về Login | ✅ TC-020 |
| Xác nhận mật khẩu mới | Không có trường | ⚠️ TC-017/018 (có lưu ý, thiếu TC cấu trúc) |
| Mật khẩu FR-01 (ký tự đặc biệt `@$!%*?&`) | Regex `[^A-Za-z\d]` — rộng hơn đặc tả | ❌ Không |
| Validate email rỗng / format Bước 1 | Gọi API trực tiếp, lỗi qua Alert | ⚠️ TC-002/003 (expected web-style) |

---

## Gap Catalogue

### GAP-01
- **Category:** Missing TC (BVA suite)
- **Item missed:** Toàn bộ BVA Email / OTP / Password / Confirm cho Mobile (`TC-MFORGOT-021` … tương đương `TC-FORGOT-021` … `044`)
- **Root cause:** ☑ Spec complexity (BVA deferred) · ☑ AI limitation — clone EP từ web, không port BVA
- **Severity:** High
- **Remediation:** Re-apply Skill-02; tạo `TC-MFORGOT-021` … `044` hoặc `TC-MFORGOT-SUP-006` … `SUP-008`

### GAP-02
- **Category:** Missing variable / rule
- **Item missed:** OTP phải đúng **6 chữ số** — kiểm tra response API + **label UI Mobile** (“4 số” vs đặc tả)
- **Root cause:** ☑ AI limitation — suite kế thừa expected 6 số từ web, không có TC Mobile-specific cho label
- **Severity:** High
- **Remediation:** `TC-MFORGOT-SUP-001` (API + assert text “Mã OTP (6 số)” trên màn hình)

### GAP-03
- **Category:** Missing business rule
- **Item missed:** Demo FR-03 — OTP phải **hiển thị trên màn hình** (Mobile hiện message chung)
- **Root cause:** ☑ AI limitation — TC-001 thêm fallback API thay vì TC assert hành vi demo
- **Severity:** High
- **Remediation:** `TC-MFORGOT-SUP-002` — sau Bước 1, `messageBox` phải chứa mã OTP 6 chữ số

### GAP-04
- **Category:** Missing business rule
- **Item missed:** Backend không validate độ mạnh mật khẩu khi reset (`POST /api/reset-password`)
- **Root cause:** ☑ Spec complexity — rule suy ra từ FR-01, không lặp trong FR-03
- **Severity:** High
- **Remediation:** `TC-MFORGOT-SUP-003` (có thể dùng chung API với `TC-FORGOT-SUP-002`, ghi rõ platform Mobile)

### GAP-05
- **Category:** Missing business rule
- **Item missed:** OTP một lần — token vô hiệu sau reset (SEC-07)
- **Root cause:** ☑ Spec complexity — rule ngầm / SEC
- **Severity:** Medium
- **Remediation:** `TC-MFORGOT-SUP-004`

### GAP-06
- **Category:** Missing TC (structural / UI)
- **Item missed:** Bước 2 **thiếu trường Xác nhận mật khẩu** — lỗi triển khai so với FR-03, không có TC kiểm tra **sự tồn tại** trường
- **Root cause:** ☑ AI limitation — TC-017/018 giả định trường có; chỉ thêm lưu ý markdown, không có TC “field present”
- **Severity:** High
- **Remediation:** `TC-MFORGOT-SUP-005` — assert có 2 `TextInput` `secureTextEntry` hoặc label “Xác nhận mật khẩu”

### GAP-07
- **Category:** Missing TC (cross-requirement)
- **Item missed:** FR-22 — lỗi validation phải hiển thị **trên** nút submit (Mobile dùng `Alert.alert` popup)
- **Root cause:** ☑ Prompt quality — không map FR-22 sang pattern React Native
- **Severity:** Medium
- **Remediation:** `TC-MFORGOT-SUP-006` — kích hoạt lỗi yếu mật khẩu; kiểm tra **không** dùng Alert, có inline `errorBoxText` phía trên nút

### GAP-08
- **Category:** Missing TC (Mobile-specific)
- **Item missed:** Regex client Mobile chấp nhận ký tự đặc biệt **ngoài** tập FR-01 (`@$!%*?&`)
- **Root cause:** ☑ AI limitation — EP “thiếu đặc biệt” dùng `Test1234` nhưng không test ký tự đặc biệt **không hợp lệ** theo FR-01
- **Severity:** Medium
- **Remediation:** `TC-MFORGOT-SUP-007` — mật khẩu `Test1234#` (hoặc ký tự ngoài whitelist) phải bị từ chối nếu tuân FR-01 chặt

### GAP-09
- **Category:** Missing TC (spec traceability)
- **Item missed:** FR-20 không liệt kê Quên mật khẩu — thiếu TC hoặc ghi chú phạm vi trong báo cáo
- **Root cause:** ☑ Spec complexity — README không có FR-22; FR-20 thiếu mục
- **Severity:** Low (tài liệu)
- **Remediation:** Ghi rõ trong báo cáo: FR-22 = FR-03 @ Mobile; đề xuất bổ sung README

### GAP-10
- **Category:** Other
- **Item missed:** Không có automation Mobile; toàn bộ `Not Run`; `traceability-matrix.md` chưa có FR-22
- **Root cause:** ☑ Process — mới tạo markdown, chưa thực thi / chưa cập nhật matrix
- **Severity:** Medium (HW02 deliverable)
- **Remediation:** Manual test trên Expo; thêm 20+ dòng vào `traceability-matrix.md`; cân nhắc Maestro/Detox sau khi freeze ID

### GAP-11
- **Category:** Other
- **Item missed:** Suite được **clone** từ `forgot/` web — bước điều hướng đã sửa nhưng **expected lỗi** vẫn theo web (inline form) thay vì hành vi Alert Mobile
- **Root cause:** ☑ AI limitation — copy-transform không điều chỉnh expected theo platform
- **Severity:** Medium
- **Remediation:** Review từng TC Invalid; tách expected: “từ chối + thông báo lỗi (Alert hoặc inline)” vs đặc tả FR-22

---

## Gap Summary Table

| Gap ID | Category | Severity | Variable / Rule | Root Cause | Remediation TC |
|--------|----------|----------|-----------------|------------|----------------|
| GAP-01 | Missing TC (BVA) | High | Length boundaries | Spec complexity + AI | TC-MFORGOT-021+ or SUP-006+ |
| GAP-02 | Missing rule | High | OTP 6 digits + UI label | AI limitation | TC-MFORGOT-SUP-001 |
| GAP-03 | Missing rule | High | Demo OTP on screen | AI limitation | TC-MFORGOT-SUP-002 |
| GAP-04 | Missing rule | High | Server password validation | Spec complexity | TC-MFORGOT-SUP-003 |
| GAP-05 | Missing rule | Medium | OTP one-time use | Spec complexity | TC-MFORGOT-SUP-004 |
| GAP-06 | Structural UI | High | Confirm-password field | AI limitation | TC-MFORGOT-SUP-005 |
| GAP-07 | Cross-requirement | Medium | FR-22 error placement | Prompt quality | TC-MFORGOT-SUP-006 |
| GAP-08 | Mobile-specific | Medium | FR-01 special-char whitelist | AI limitation | TC-MFORGOT-SUP-007 |
| GAP-09 | Spec traceability | Low | FR-20 scope | Spec complexity | Doc / README update |
| GAP-10 | Process | Medium | Execution + matrix | Process | Run tests + matrix |
| GAP-11 | Other | Medium | Platform-specific expected | AI limitation | Revise Invalid TC expected |

---

## Coverage Summary

| Kỹ thuật | Số TC | Trạng thái |
|----------|-------|------------|
| Domain Testing (EP) | 20 (`TC-MFORGOT-001`–`020`) | ✅ Đủ phân vùng chính (mirror FR-03 web) |
| BVA | 0 | ❌ Chưa port từ `TC-FORGOT-021` … `044` |
| Supplementary | 0 | ❌ Chưa có `TC-MFORGOT-SUP-*` |
| **Tổng** | **20** | Chưa thực thi (`Not Run`) |

---

## AI Critique Paragraph

The AI-generated FR-22 suite correctly mirrors the **equivalence-class structure** of the FR-03 web domain pack (20 TCs, same sub-domain IDs `SD-E01` … `SD-UI02`) and adapts navigation to Mobile (Đăng nhập → “Quên mật khẩu?”). Against `README.md`, however, it **inherits FR-03 expectations without reconciling the Mobile implementation**: the SUT omits Step Indicator, confirm-password, and on-screen OTP demo, while mislabeling OTP as four digits—yet the AI only added a soft API fallback in TC-001 instead of dedicated structural and label assertions (GAP-02, GAP-03, GAP-06). The same **feature-boundary pattern** seen in FR-03 gap analysis repeats: no supplementary API cases for six-digit OTP, server password validation, or one-time OTP (GAP-04, GAP-05); FR-22 was not translated to React Native semantics (Alert vs inline errors, `secureTextEntry` vs `type="password"`). BVA was not ported at all (GAP-01), leaving boundary coverage weaker than the web folder despite `TC-FORGOT-021`+ already existing. **Spec traceability** is fragile: README has no FR-22 entry and FR-20 does not list forgot-password (GAP-09). Process gaps include zero execution, no traceability matrix rows, and no Mobile automation (GAP-10). Root causes are **AI limitation** (web clone without platform/SUT diff), **spec complexity** (implicit FR-01/SEC-07/FR-22), and **missing BVA pass**. Recommended next steps: (1) add `TC-MFORGOT-SUP-001`–`007` before execution, (2) port or reference BVA boundaries, (3) run manual tests on Expo and record defects aligned with web issues #4–#10 where applicable, (4) update `traceability-matrix.md`, (5) freeze IDs before any Mobile E2E.
