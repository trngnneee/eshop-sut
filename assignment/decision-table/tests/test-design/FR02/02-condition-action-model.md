# 02 — Condition / Action Model: FR02 — Đăng nhập & Khóa tài khoản

## Requirement ID
FR02

---

## Condition Table

| Condition ID | Condition / Factor | Values | Source / Reason | Risk |
|---|---|---|---|---|
| C01 | Email tồn tại trong hệ thống | Tồn tại / Không tồn tại | BR01: Lookup email trước khi kiểm tra password | High |
| C02 | Mật khẩu nhập vào | Đúng / Sai | BR03, BR04: Kết quả so sánh password | High |
| C03 | Trạng thái khóa tài khoản (`locked_until`) | Không bị khóa / Đang bị khóa (chưa hết hạn) / Đã hết hạn khóa | BR02, BR06: Kiểm tra thời điểm khóa | High |
| C04 | Số lần thất bại hiện tại (`login_attempts` trước khi cộng) | 0 / 1 / ≥2 (đã ở ngưỡng hoặc vượt) | BR04, BR05: Tính toán ngưỡng khóa (cộng +2 do bug) | High |
| C05 | Role của tài khoản | user / admin | JWT payload: role quyết định quyền truy cập sau login | Medium |

---

## Condition Values Detail

### C01 — Email tồn tại
| Value | Mô tả |
|---|---|
| Tồn tại | Email có trong bảng `users` |
| Không tồn tại | Email không có trong DB → trả 401 ngay |

### C02 — Mật khẩu
| Value | Mô tả |
|---|---|
| Đúng | `user.password === req.body.password` |
| Sai | Không khớp |

### C03 — Trạng thái khóa
| Value | Mô tả | Điều kiện kỹ thuật |
|---|---|---|
| Không bị khóa | `locked_until IS NULL` | Cho phép tiếp tục kiểm tra password |
| Đang bị khóa | `locked_until NOT NULL` và `NOW < locked_until` | Trả 403 ngay lập tức |
| Đã hết hạn khóa | `locked_until NOT NULL` và `NOW >= locked_until` | Hệ thống **không** auto-reset, nhưng điều kiện `new Date() < new Date(locked_until)` trả `false` → cho phép qua |

### C04 — login_attempts (trước khi cộng)
| Value | Sau khi cộng +2 (bug) | Có bị khóa? |
|---|---|---|
| 0 | 2 | Không (2 < 3) |
| 1 | 3 | Có (3 >= 3) ← **khóa sau lần thất bại thứ 2 thay vì thứ 3** |
| ≥2 | ≥4 | Có |

### C05 — Role
| Value | Quyền sau khi đăng nhập thành công |
|---|---|
| user | Truy cập tài nguyên user thông thường |
| admin | Truy cập admin panel |

---

## Action Table

| Action ID | Action / Expected Behavior | HTTP Status | Khi nào triggered |
|---|---|---|---|
| A01 | Đăng nhập thành công — trả JWT token, reset `login_attempts = 0`, `locked_until = NULL` | 200 | C01=Tồn tại, C02=Đúng, C03=Không bị khóa hoặc Đã hết hạn |
| A02 | Từ chối — Email không tồn tại | 401 | C01=Không tồn tại |
| A03 | Từ chối — Sai mật khẩu, cộng `login_attempts`, KHÔNG khóa | 401 | C01=Tồn tại, C02=Sai, C03=Không bị khóa, C04 sau cộng < 3 |
| A04 | Từ chối — Sai mật khẩu, cộng `login_attempts`, SET `locked_until` | 401 | C01=Tồn tại, C02=Sai, C03=Không bị khóa, C04 sau cộng >= 3 |
| A05 | Từ chối — Tài khoản đang bị khóa (dù password đúng hay sai) | 403 | C01=Tồn tại, C03=Đang bị khóa |
| A06 | Đăng nhập thành công sau khi hết hạn khóa — như A01 | 200 | C01=Tồn tại, C02=Đúng, C03=Đã hết hạn khóa |

---

## Constraints và Assumptions

| ID | Constraint / Assumption |
|---|---|
| CON01 | Kiểm tra `locked_until` được thực hiện **trước** khi kiểm tra password |
| CON02 | `login_attempts += 2` là lỗi trong code — tài khoản bị khóa sau 2 lần sai thay vì 3 lần |
| CON03 | Khi tài khoản đang bị khóa, API không tiếp tục kiểm tra password (lock check đứng trước) |
| CON04 | JWT không có expiry được set trong code (`jwt.sign` không có options) — token tồn tại vô thời hạn |
