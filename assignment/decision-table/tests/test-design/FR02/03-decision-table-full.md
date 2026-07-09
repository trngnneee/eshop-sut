# 03 — Full Decision Table: FR02 — Đăng nhập & Khóa tài khoản

## Requirement ID
FR02

---

## Điều kiện và giá trị

| Condition | Values |
|---|---|
| C01 — Email tồn tại | Tồn tại (E) / Không tồn tại (NE) |
| C02 — Mật khẩu | Đúng (OK) / Sai (FAIL) |
| C03 — Trạng thái khóa | Không bị khóa (UL) / Đang bị khóa (LK) / Đã hết hạn (EX) |
| C04 — login_attempts (trước khi cộng) | 0 (A0) / 1 (A1) / ≥2 (A2+) |
| C05 — Role | user / admin |

**Tổng lý thuyết** = 2 × 2 × 3 × 3 × 2 = **72 rules**  
(Sau loại bỏ impossible/redundant còn lại hữu ích)

---

## Decision Table

| Rule ID | C01 Email | C02 Password | C03 Lock Status | C04 Attempts (before) | C05 Role | Action | Expected Result | HTTP | Validity | Reason |
|---|---|---|---|---|---|---|---|---|---|---|
| R001 | Tồn tại | Đúng | Không bị khóa | 0 | user | A01 | Đăng nhập thành công, trả JWT, reset attempts=0 | 200 | Valid | Happy path — user |
| R002 | Tồn tại | Đúng | Không bị khóa | 0 | admin | A01 | Đăng nhập thành công, trả JWT, reset attempts=0 | 200 | Valid | Happy path — admin |
| R003 | Tồn tại | Đúng | Không bị khóa | 1 | user | A01 | Đăng nhập thành công, reset attempts=0 (giải phóng lock counter) | 200 | Valid | Đúng password sau 1 lần sai |
| R004 | Tồn tại | Đúng | Không bị khóa | 1 | admin | A01 | Đăng nhập thành công, reset attempts=0 | 200 | Valid | Admin đúng password sau 1 lần sai |
| R005 | Tồn tại | Đúng | Không bị khóa | ≥2 | user | A01 | Đăng nhập thành công, reset attempts=0 | 200 | Valid | Đúng password sau nhiều lần sai (nhưng chưa bị khóa — impossible với bug +2) |
| R006 | Tồn tại | Đúng | Không bị khóa | ≥2 | admin | A01 | Đăng nhập thành công | 200 | Impossible | Với bug +2: attempts 0→2 đã khóa, attempts ≥2 + UL không tồn tại |
| R007 | Tồn tại | Đúng | Đang bị khóa | 0 | user | A05 | Từ chối: "Tài khoản đã bị khóa" | 403 | Impossible | Nếu locked → attempts phải >= 3; attempts=0 không bao giờ bị lock |
| R008 | Tồn tại | Đúng | Đang bị khóa | 0 | admin | A05 | Từ chối: "Tài khoản đã bị khóa" | 403 | Impossible | Như R007 |
| R009 | Tồn tại | Đúng | Đang bị khóa | 1 | user | A05 | Từ chối: "Tài khoản đã bị khóa" | 403 | Valid | Tài khoản bị khóa — password đúng nhưng vẫn từ chối |
| R010 | Tồn tại | Đúng | Đang bị khóa | 1 | admin | A05 | Từ chối: "Tài khoản đã bị khóa" | 403 | Valid | Admin bị khóa — dù đúng password |
| R011 | Tồn tại | Đúng | Đang bị khóa | ≥2 | user | A05 | Từ chối: "Tài khoản đã bị khóa" | 403 | Valid | Locked, đúng password, nhiều lần sai trước |
| R012 | Tồn tại | Đúng | Đang bị khóa | ≥2 | admin | A05 | Từ chối: "Tài khoản đã bị khóa" | 403 | Valid | Locked admin, đúng password |
| R013 | Tồn tại | Đúng | Đã hết hạn | 0 | user | A06 | Đăng nhập thành công sau hết hạn khóa | 200 | Impossible | attempts=0 không bao giờ bị lock → hết hạn không xảy ra |
| R014 | Tồn tại | Đúng | Đã hết hạn | 0 | admin | A06 | Đăng nhập thành công sau hết hạn khóa | 200 | Impossible | Như R013 |
| R015 | Tồn tại | Đúng | Đã hết hạn | 1 | user | A06 | Đăng nhập thành công sau hết hạn khóa, reset attempts=0 | 200 | Valid | Hết 3 phút → đăng nhập lại được |
| R016 | Tồn tại | Đúng | Đã hết hạn | 1 | admin | A06 | Đăng nhập thành công sau hết hạn khóa | 200 | Valid | Admin hết hạn khóa |
| R017 | Tồn tại | Đúng | Đã hết hạn | ≥2 | user | A06 | Đăng nhập thành công sau hết hạn khóa | 200 | Valid | Nhiều lần sai, hết khóa, đúng password |
| R018 | Tồn tại | Đúng | Đã hết hạn | ≥2 | admin | A06 | Đăng nhập thành công sau hết hạn khóa | 200 | Valid | Admin |
| R019 | Tồn tại | Sai | Không bị khóa | 0 | user | A03 | Từ chối 401, attempts = 0+2 = 2 (BUG: nên 1), KHÔNG khóa | 401 | Valid | Sai lần 1 — chưa đủ ngưỡng khóa |
| R020 | Tồn tại | Sai | Không bị khóa | 0 | admin | A03 | Từ chối 401, attempts = 2, KHÔNG khóa | 401 | Valid | Admin sai lần 1 |
| R021 | Tồn tại | Sai | Không bị khóa | 1 | user | A04 | Từ chối 401, attempts = 1+2 = 3 → SET locked_until = NOW+180s | 401 | Valid | **Sai lần 2 → bị khóa (BUG: theo spec nên là lần 3)** |
| R022 | Tồn tại | Sai | Không bị khóa | 1 | admin | A04 | Từ chối 401, attempts = 3 → SET locked_until | 401 | Valid | Admin bị khóa sau lần sai thứ 2 |
| R023 | Tồn tại | Sai | Không bị khóa | ≥2 | user | A04 | Từ chối 401, attempts ≥4, locked_until đã set (hoặc set lại) | 401 | Valid | Tiếp tục sai sau khi đã qua ngưỡng khóa (không UL) |
| R024 | Tồn tại | Sai | Không bị khóa | ≥2 | admin | A04 | Từ chối 401, attempts ≥4 | 401 | Impossible | Với bug +2: nếu attempts=1 đã lock, attempts≥2+UL không xảy ra |
| R025 | Tồn tại | Sai | Đang bị khóa | 0 | user | A05 | Từ chối 403 — tài khoản bị khóa | 403 | Impossible | attempts=0 không thể bị locked |
| R026 | Tồn tại | Sai | Đang bị khóa | 0 | admin | A05 | Từ chối 403 | 403 | Impossible | Như R025 |
| R027 | Tồn tại | Sai | Đang bị khóa | 1 | user | A05 | Từ chối 403 — kiểm tra lock trước, không cộng attempts | 403 | Valid | Sai password trong khi đang bị khóa — lock check có priority |
| R028 | Tồn tại | Sai | Đang bị khóa | 1 | admin | A05 | Từ chối 403 | 403 | Valid | Admin bị khóa, thử sai password |
| R029 | Tồn tại | Sai | Đang bị khóa | ≥2 | user | A05 | Từ chối 403 | 403 | Valid | Nhiều lần sai, đang khóa |
| R030 | Tồn tại | Sai | Đang bị khóa | ≥2 | admin | A05 | Từ chối 403 | 403 | Valid | Admin, nhiều lần sai, đang khóa |
| R031 | Tồn tại | Sai | Đã hết hạn | 0 | user | A03 | Từ chối 401, attempts = 2, KHÔNG khóa lại | 401 | Impossible | attempts=0 không thể từng bị lock |
| R032 | Tồn tại | Sai | Đã hết hạn | 0 | admin | A03 | Từ chối 401 | 401 | Impossible | Như R031 |
| R033 | Tồn tại | Sai | Đã hết hạn | 1 | user | A04 | Từ chối 401, attempts = 3 → khóa lại | 401 | Valid | Hết khóa, thử lại → bị khóa lại |
| R034 | Tồn tại | Sai | Đã hết hạn | 1 | admin | A04 | Từ chối 401, khóa lại | 401 | Valid | Admin hết khóa, sai password → bị khóa lại |
| R035 | Tồn tại | Sai | Đã hết hạn | ≥2 | user | A04 | Từ chối 401, tăng attempts, khóa lại | 401 | Valid | Tiếp tục sai sau hết khóa |
| R036 | Tồn tại | Sai | Đã hết hạn | ≥2 | admin | A04 | Từ chối 401, tăng attempts | 401 | Valid | Admin tiếp tục sai |
| R037 | Không tồn tại | - | - | - | - | A02 | Từ chối 401 "Invalid email or password" | 401 | Valid | Email không có trong DB |
| R038 | Không tồn tại | - | - | - | - | A02 | Redundant | 401 | Redundant | Gộp vào R037 |

---

## Summary

| Category | Count |
|---|---|
| Tổng lý thuyết | 72 |
| Valid | 24 |
| Impossible | 10 |
| Redundant | 1 |
| Không tồn tại (C01=NE) gộp thành 1 rule | Xem R037 |

> **Ghi chú Bug BR04**: Do `login_attempts += 2` thay vì `+= 1`:
> - Sai lần 1: attempts đi từ 0 → 2 (chưa khóa)
> - Sai lần 2: attempts đi từ 1 → 3 → **bị khóa** (theo spec phải là sai lần 3 mới khóa)
> - Điều này làm một số rule trở thành Impossible trong thực tế
