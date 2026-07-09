# 04 — Rule Filtering: FR02 — Đăng nhập & Khóa tài khoản

## Requirement ID
FR02

---

## Filtering Table

| Rule ID | C01 | C02 | C03 | C04 | Decision | Reason |
|---|---|---|---|---|---|---|
| R006 | Tồn tại | Đúng | Không bị khóa | ≥2 | **Remove — Impossible** | Với bug `+2`: attempts=0→2 chưa khóa, attempts=1→3 đã khóa. Không thể có trạng thái attempts≥2 + NOT LOCKED sau lần sai (trừ khi được reset, nhưng reset chỉ xảy ra khi login thành công). Trường hợp thực tế: attempts=2 sau 1 lần sai (bug), tiếp theo chỉ có thể là locked hoặc login thành công. |
| R007 | Tồn tại | Đúng | Đang bị khóa | 0 | **Remove — Impossible** | `login_attempts = 0` không bao giờ đạt ngưỡng ≥3 để bị khóa. Không tồn tại trạng thái locked với attempts=0. |
| R008 | Tồn tại | Đúng | Đang bị khóa | 0 | **Remove — Impossible** | Như R007 (admin variant). |
| R013 | Tồn tại | Đúng | Đã hết hạn | 0 | **Remove — Impossible** | attempts=0 không bao giờ bị khóa → không thể hết hạn khóa. |
| R014 | Tồn tại | Đúng | Đã hết hạn | 0 | **Remove — Impossible** | Như R013 (admin variant). |
| R024 | Tồn tại | Sai | Không bị khóa | ≥2 | **Remove — Impossible** | Với bug +2: nếu attempts bắt đầu từ 1 → sau sai thứ 2 attempts=3 → locked. Attempts≥2 với NOT LOCKED không xảy ra trong luồng bình thường sau khi đã qua 1 lần sai (ngoại trừ nếu DB được can thiệp trực tiếp). Giữ để test nhưng đánh dấu impossible. |
| R025 | Tồn tại | Sai | Đang bị khóa | 0 | **Remove — Impossible** | attempts=0 không bao giờ bị locked. |
| R026 | Tồn tại | Sai | Đang bị khóa | 0 | **Remove — Impossible** | Như R025 (admin). |
| R031 | Tồn tại | Sai | Đã hết hạn | 0 | **Remove — Impossible** | attempts=0 không bao giờ bị locked → không có trạng thái expired lock với attempts=0. |
| R032 | Tồn tại | Sai | Đã hết hạn | 0 | **Remove — Impossible** | Như R031 (admin). |
| R038 | Không tồn tại | - | - | - | **Remove — Redundant** | Gộp vào R037. Tất cả trường hợp email không tồn tại đều cho cùng kết quả. |

---

## Rules to Keep

| Rule ID | C01 | C02 | C03 | C04 | C05 | Lý do giữ |
|---|---|---|---|---|---|---|
| R001 | Tồn tại | Đúng | Không bị khóa | 0 | user | Happy path — user |
| R002 | Tồn tại | Đúng | Không bị khóa | 0 | admin | Happy path — admin |
| R003 | Tồn tại | Đúng | Không bị khóa | 1 | user | Đúng password sau 1 lần sai |
| R004 | Tồn tại | Đúng | Không bị khóa | 1 | admin | Admin đúng password sau 1 lần sai |
| R005 | Tồn tại | Đúng | Không bị khóa | ≥2 | user | Giữ để test edge case (DB manipulation / hệ thống spec bình thường) |
| R009 | Tồn tại | Đúng | Đang bị khóa | 1 | user | **Bắt buộc giữ — security**: đúng password trong khi bị khóa phải vẫn bị từ chối |
| R010 | Tồn tại | Đúng | Đang bị khóa | 1 | admin | **Bắt buộc giữ — security**: admin bị khóa |
| R011 | Tồn tại | Đúng | Đang bị khóa | ≥2 | user | Locked với nhiều lần sai |
| R012 | Tồn tại | Đúng | Đang bị khóa | ≥2 | admin | Locked admin |
| R015 | Tồn tại | Đúng | Đã hết hạn | 1 | user | Hết khóa → đăng nhập lại được |
| R016 | Tồn tại | Đúng | Đã hết hạn | 1 | admin | Admin hết khóa |
| R017 | Tồn tại | Đúng | Đã hết hạn | ≥2 | user | Nhiều lần sai, hết khóa |
| R018 | Tồn tại | Đúng | Đã hết hạn | ≥2 | admin | Admin, nhiều lần sai, hết khóa |
| R019 | Tồn tại | Sai | Không bị khóa | 0 | user | Sai lần 1 — chưa khóa (BUG: attempts = 2 không phải 1) |
| R020 | Tồn tại | Sai | Không bị khóa | 0 | admin | Admin sai lần 1 |
| R021 | Tồn tại | Sai | Không bị khóa | 1 | user | **Sai lần 2 → bị khóa (BUG: theo spec phải là lần 3)** — critical |
| R022 | Tồn tại | Sai | Không bị khóa | 1 | admin | Admin bị khóa sau lần sai thứ 2 |
| R023 | Tồn tại | Sai | Không bị khóa | ≥2 | user | Tiếp tục sai (trường hợp spec bình thường hoặc DB can thiệp) |
| R027 | Tồn tại | Sai | Đang bị khóa | 1 | user | **Bắt buộc giữ — security**: lock check trước password check |
| R028 | Tồn tại | Sai | Đang bị khóa | 1 | admin | Admin bị khóa, sai password |
| R029 | Tồn tại | Sai | Đang bị khóa | ≥2 | user | Locked, tiếp tục sai |
| R030 | Tồn tại | Sai | Đang bị khóa | ≥2 | admin | Admin locked, tiếp tục sai |
| R033 | Tồn tại | Sai | Đã hết hạn | 1 | user | Hết khóa → sai → bị khóa lại |
| R034 | Tồn tại | Sai | Đã hết hạn | 1 | admin | Admin: hết khóa → sai → khóa lại |
| R035 | Tồn tại | Sai | Đã hết hạn | ≥2 | user | Tiếp tục sai sau hết khóa |
| R036 | Tồn tại | Sai | Đã hết hạn | ≥2 | admin | Admin tiếp tục sai |
| R037 | Không tồn tại | - | - | - | - | **Bắt buộc giữ — security**: email không tồn tại không được tiết lộ thông tin |

---

## Tổng kết sau lọc

| Category | Count |
|---|---|
| Removed — Impossible | 10 |
| Removed — Redundant | 1 |
| Kept — Valid | 27 |

> **Mandatory Rules không được loại bỏ dù pairwise không chọn:**
> - R009, R010 — security: locked account với đúng password
> - R021, R022 — bug exposure: bị khóa sau lần sai thứ 2
> - R027, R028 — security: lock check trước password check
> - R037 — security: email không tồn tại
