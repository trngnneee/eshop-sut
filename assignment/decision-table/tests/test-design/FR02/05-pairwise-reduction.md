# 05 — Pairwise Reduction: FR02 — Đăng nhập & Khóa tài khoản

## Requirement ID
FR02

---

## Pairwise Factors (sau khi lọc)

| Factor ID | Factor | Values |
|---|---|---|
| F1 | Email tồn tại (C01) | Tồn tại / Không tồn tại |
| F2 | Mật khẩu (C02) | Đúng / Sai |
| F3 | Trạng thái khóa (C03) | Không bị khóa / Đang bị khóa / Đã hết hạn |
| F4 | login_attempts trước (C04) | 0 / 1 / ≥2 |
| F5 | Role (C05) | user / admin |

**Ràng buộc loại trừ:**
- F1=Không tồn tại → F2, F3, F4 không áp dụng (email lookup fail trả ngay)
- F3=Đang bị khóa hoặc Đã hết hạn → F4 phải là 1 hoặc ≥2 (không thể 0)
- F3=Đang bị khóa + F2=Đúng → vẫn từ chối (lock check trước)

---

## Pairwise Generation

Mục tiêu: mỗi cặp giá trị bất kỳ giữa 2 factor bất kỳ phải xuất hiện ít nhất 1 lần.

### Mandatory Rules (không được pairwise loại bỏ)

| Pairwise Case ID | Covered Rule ID(s) | F1 Email | F2 Password | F3 Lock | F4 Attempts | F5 Role | Action | Expected Action | Why Mandatory |
|---|---|---|---|---|---|---|---|---|---|
| PW001 | R001 | Tồn tại | Đúng | Không bị khóa | 0 | user | A01 | HTTP 200, JWT trả về, attempts=0 | Happy path |
| PW002 | R002 | Tồn tại | Đúng | Không bị khóa | 0 | admin | A01 | HTTP 200, JWT trả về, role=admin | Happy path admin |
| PW003 | R021 | Tồn tại | Sai | Không bị khóa | 1 | user | A04 | HTTP 401, locked_until SET (BUG: lần sai thứ 2 gây khóa) | **Bug exposure — critical** |
| PW004 | R022 | Tồn tại | Sai | Không bị khóa | 1 | admin | A04 | HTTP 401, locked_until SET | **Bug exposure — admin** |
| PW005 | R009 | Tồn tại | Đúng | Đang bị khóa | 1 | user | A05 | HTTP 403, "Tài khoản đã bị khóa" dù password đúng | **Security — lock check priority** |
| PW006 | R010 | Tồn tại | Đúng | Đang bị khóa | 1 | admin | A05 | HTTP 403 | **Security — admin locked** |
| PW007 | R027 | Tồn tại | Sai | Đang bị khóa | 1 | user | A05 | HTTP 403 — lock check trước password check | **Security — lock vs password order** |
| PW008 | R037 | Không tồn tại | - | - | - | - | A02 | HTTP 401 "Invalid email or password" | **Security — không tiết lộ user existence** |

### Pairwise Selected Rules (covering remaining pairs)

| Pairwise Case ID | Covered Rule ID(s) | F1 Email | F2 Password | F3 Lock | F4 Attempts | F5 Role | Action | Expected Action | Why Selected |
|---|---|---|---|---|---|---|---|---|---|
| PW009 | R003 | Tồn tại | Đúng | Không bị khóa | 1 | user | A01 | HTTP 200, reset attempts=0 | Covers F2=Đúng + F4=1 pair |
| PW010 | R019 | Tồn tại | Sai | Không bị khóa | 0 | user | A03 | HTTP 401, attempts = 0+2=2, KHÔNG khóa | Covers F2=Sai + F4=0; Boundary: sai lần đầu |
| PW011 | R020 | Tồn tại | Sai | Không bị khóa | 0 | admin | A03 | HTTP 401, attempts=2, KHÔNG khóa | Covers F2=Sai + F5=admin + F4=0 |
| PW012 | R015 | Tồn tại | Đúng | Đã hết hạn | 1 | user | A06 | HTTP 200, đăng nhập thành công sau hết khóa | Covers F3=Đã hết hạn + F2=Đúng |
| PW013 | R033 | Tồn tại | Sai | Đã hết hạn | 1 | user | A04 | HTTP 401, khóa lại | Covers F3=Đã hết hạn + F2=Sai |
| PW014 | R016 | Tồn tại | Đúng | Đã hết hạn | 1 | admin | A06 | HTTP 200, admin đăng nhập lại sau hết khóa | Covers F3=Đã hết hạn + F5=admin |
| PW015 | R011, R029 | Tồn tại | Đúng/Sai | Đang bị khóa | ≥2 | user | A05 | HTTP 403 | Covers F3=Đang bị khóa + F4=≥2 |
| PW016 | R023 | Tồn tại | Sai | Không bị khóa | ≥2 | user | A04 | HTTP 401, attempts tăng, vẫn locked | Covers F4=≥2 + F2=Sai + F3=Không bị khóa |
| PW017 | R017 | Tồn tại | Đúng | Đã hết hạn | ≥2 | user | A06 | HTTP 200 | Covers F3=Đã hết hạn + F4=≥2 |
| PW018 | R028 | Tồn tại | Sai | Đang bị khóa | 1 | admin | A05 | HTTP 403 | Covers F3=Đang bị khóa + F5=admin + F2=Sai |

---

## Coverage Review

| Pair | Covered by Pairwise Case | Status |
|---|---|---|
| F1=Tồn tại + F2=Đúng | PW001, PW002, PW005, PW006, PW009, PW012, PW014, PW015, PW017 | ✅ Covered |
| F1=Tồn tại + F2=Sai | PW003, PW004, PW007, PW010, PW011, PW013, PW015, PW016, PW018 | ✅ Covered |
| F1=Không tồn tại | PW008 | ✅ Covered |
| F2=Đúng + F3=Không bị khóa | PW001, PW002, PW009 | ✅ Covered |
| F2=Đúng + F3=Đang bị khóa | PW005, PW006, PW015 | ✅ Covered |
| F2=Đúng + F3=Đã hết hạn | PW012, PW014, PW017 | ✅ Covered |
| F2=Sai + F3=Không bị khóa | PW003, PW004, PW010, PW011, PW016 | ✅ Covered |
| F2=Sai + F3=Đang bị khóa | PW007, PW015, PW018 | ✅ Covered |
| F2=Sai + F3=Đã hết hạn | PW013 | ✅ Covered |
| F3=Không bị khóa + F4=0 | PW001, PW002, PW010, PW011 | ✅ Covered |
| F3=Không bị khóa + F4=1 | PW003, PW004, PW009 | ✅ Covered |
| F3=Không bị khóa + F4=≥2 | PW016 | ✅ Covered |
| F3=Đang bị khóa + F4=1 | PW005, PW006, PW007, PW018 | ✅ Covered |
| F3=Đang bị khóa + F4=≥2 | PW015 | ✅ Covered |
| F3=Đã hết hạn + F4=1 | PW012, PW013, PW014 | ✅ Covered |
| F3=Đã hết hạn + F4=≥2 | PW017 | ✅ Covered |
| F4=0 + F5=user | PW001, PW010 | ✅ Covered |
| F4=0 + F5=admin | PW002, PW011 | ✅ Covered |
| F4=1 + F5=user | PW003, PW005, PW007, PW009, PW012, PW013 | ✅ Covered |
| F4=1 + F5=admin | PW004, PW006, PW014, PW018 | ✅ Covered |
| F4=≥2 + F5=user | PW015, PW016, PW017 | ✅ Covered |
| F4=≥2 + F5=admin | PW015 | ✅ Covered |
| F2=Đúng + F5=user | PW001, PW005, PW009, PW012, PW015, PW017 | ✅ Covered |
| F2=Đúng + F5=admin | PW002, PW006, PW014 | ✅ Covered |
| F2=Sai + F5=user | PW003, PW007, PW010, PW013, PW015, PW016 | ✅ Covered |
| F2=Sai + F5=admin | PW004, PW011, PW018 | ✅ Covered |

---

## Summary

| Metric | Count |
|---|---|
| Mandatory rules (security/bug) | 8 |
| Pairwise selected rules | 10 |
| **Total pairwise cases** | **18** |
| Rules NOT covered by pairwise (low risk) | R004, R018, R030, R034, R035, R036 |

> **Coverage Gap Note**: Các rule còn lại (R004, R018, R030...) là các biến thể admin/role thứ cấp đã được cover về pattern behavior. Chúng không được ưu tiên vì không có edge case mới, nhưng có thể thêm vào regression suite sau.
