# 01 — Requirement Analysis: FR02 — Đăng nhập & Khóa tài khoản

## Requirement ID
FR02

## Feature Summary
Người dùng (User/Admin) đăng nhập vào hệ thống EShop bằng email và mật khẩu.  
Nếu nhập sai mật khẩu **3 lần trở lên**, tài khoản bị khóa trong **3 phút** (180 giây).  
Trong thời gian bị khóa, mọi lần đăng nhập đều bị từ chối, dù mật khẩu đúng.

> **Lưu ý bug đã xác định trong source code:**  
> Tại `server.js` dòng 54: `const newAttempts = user.login_attempts + 2;`  
> Thay vì `+ 1`. Điều này khiến tài khoản bị khóa sớm hơn dự kiến (sau 2 lần thay vì 3 lần).

---

## Actors and Permissions

| Actor | Quyền |
|---|---|
| Guest (chưa đăng nhập) | Truy cập trang login, gửi yêu cầu đăng nhập |
| User | Đăng nhập → nhận JWT token, truy cập tài khoản |
| Admin | Đăng nhập → nhận JWT token, truy cập admin panel |

---

## Entry Points

| Type | Path / Endpoint |
|---|---|
| UI Route (Web) | `/login` |
| UI Route (Admin) | `/admin/login` (dùng cùng API) |
| API Endpoint | `POST /api/login` |

---

## Preconditions

- Server đang chạy tại `http://localhost:3000`
- Database đã được khởi tạo và seeded (có tài khoản `test@eshop.com` / `Test1234!` và `admin@eshop.com` / `Admin123!`)
- Người dùng chưa đăng nhập (chưa có JWT token hợp lệ)

---

## Postconditions

| Kết quả | Trạng thái |
|---|---|
| Đăng nhập thành công | JWT token được trả về, `login_attempts` reset về 0, `locked_until` = NULL |
| Sai mật khẩu (< ngưỡng khóa) | `login_attempts` tăng lên, trả về HTTP 401 |
| Đạt ngưỡng khóa | `locked_until` được set = `NOW + 3 phút`, trả về HTTP 401 |
| Tài khoản đang bị khóa | Trả về HTTP 403, thông báo "Tài khoản đã bị khóa" |
| Email không tồn tại | Trả về HTTP 401 "Invalid email or password" |

---

## Data Entities Affected

| Entity | Columns |
|---|---|
| `users` | `login_attempts`, `locked_until` (đọc và ghi) |
| JWT Token | Sinh ra từ `user.id` + `user.role` khi đăng nhập thành công |

---

## Business Rules (từ source code)

| ID | Rule |
|---|---|
| BR01 | Email phải tồn tại trong DB mới kiểm tra mật khẩu |
| BR02 | Nếu `locked_until` tồn tại và `NOW < locked_until` → từ chối ngay (HTTP 403) |
| BR03 | Nếu mật khẩu đúng → reset `login_attempts = 0`, `locked_until = NULL`, trả JWT |
| BR04 | Nếu mật khẩu sai → `login_attempts += 2` *(bug: nên là +1)* |
| BR05 | Nếu `login_attempts >= 3` sau khi cập nhật → set `locked_until = NOW + 180s` |
| BR06 | Tài khoản tự mở khóa sau 3 phút (không cần thao tác thủ công) |

---

## In-Scope

- Đăng nhập với email đúng / sai
- Đăng nhập với mật khẩu đúng / sai
- Kiểm tra trạng thái khóa tài khoản (`locked_until`)
- Đếm số lần thất bại (`login_attempts`)
- Xác minh lock period (3 phút)
- Đăng nhập thành công với role User và Admin

---

## Out-of-Scope

- Chức năng Quên mật khẩu (FR03)
- Chức năng Đăng ký (FR01)
- Đăng xuất (logout)
- Quản lý user từ Admin panel
- OAuth / SSO

---

## Assumptions (cần xác nhận)

| ID | Assumption | Risk |
|---|---|---|
| ASM01 | `login_attempts += 2` là **bug** (nên là +1). Test case cần phản ánh **hành vi thực tế** (bug) và **hành vi mong đợi** (spec) | High |
| ASM02 | Không có CAPTCHA hay rate-limit tầng HTTP hiện tại | Medium |
| ASM03 | Mật khẩu được lưu dạng plaintext trong DB (bug bảo mật — nằm ngoài scope FR02) | Low |
| ASM04 | Sau khi hết thời gian khóa, `locked_until` không được reset tự động cho đến lần đăng nhập thành công tiếp theo | Medium |
