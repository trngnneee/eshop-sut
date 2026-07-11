# FR-22: Quên mật khẩu & Đặt lại mật khẩu trên Mobile (2 bước)

**Phân hệ:** Mobile App (React Native + Expo)  
**Liên quan:** FR-03 (cùng nghiệp vụ trên Web), FR-01 (quy tắc mật khẩu mạnh), FR-20 (phạm vi tính năng Mobile), FR-22 README (Form Requirements: Step Indicator, inline error, …)

---

## Mô tả yêu cầu (cho báo cáo)

Người dùng trên ứng dụng Mobile có thể khôi phục mật khẩu qua quy trình **hai bước**, tương đương FR-03 trên Frontend Web:

### Bước 1 — Lấy mã OTP

- Người dùng truy cập màn hình Quên mật khẩu từ màn hình Đăng nhập và nhập **Email đã đăng ký**.
- Hệ thống sinh mã OTP **6 chữ số ngẫu nhiên** và gửi qua Email (trong môi trường demo: **hiển thị trực tiếp trên màn hình**).
- Giao diện phải hiển thị **chỉ báo bước (Step Indicator)** — ví dụ: "Bước 1 / 2".
- Có nút **Quay lại đăng nhập**.

### Bước 2 — Đặt lại mật khẩu

- Người dùng nhập **OTP**, **Mật khẩu mới**, và **Xác nhận mật khẩu mới**.
- Mật khẩu mới phải tuân thủ điều kiện như FR-01 (tối thiểu 8 ký tự; có chữ hoa, chữ thường, chữ số và ký tự đặc biệt `@`, `$`, `!`, `%`, `*`, `?`, `&`).
- Hai trường mật khẩu phải khớp nhau.
- OTP chỉ hợp lệ cho email đã yêu cầu, không thể dùng cho email khác.
- Sau khi đặt lại thành công, người dùng được chuyển về màn hình Đăng nhập.

---

## Biến đầu vào (Domain Testing)

| Biến | Bước | Lớp tương đương chính |
| :--- | :--- | :--- |
| Email | 1 | Rỗng, sai format, chưa đăng ký, hợp lệ |
| OTP | 2 | Rỗng, non-numeric, sai độ dài, sai giá trị, đúng, gắn email khác |
| Mật khẩu mới | 2 | Rỗng, ngắn, thiếu hoa/thường/số/đặc biệt, hợp lệ |
| Xác nhận mật khẩu | 2 | Rỗng, không khớp, khớp |
| UI | 1–2 | Step Indicator, Quay lại đăng nhập |

---

## Bộ test case Domain Testing

| ID | Kịch bản |
| :--- | :--- |
| TC-MFORGOT-001 | Happy path — toàn bộ dữ liệu hợp lệ |
| TC-MFORGOT-002 … 004 | Email Bước 1: rỗng, sai format, chưa đăng ký |
| TC-MFORGOT-005 … 010 | OTP Bước 2: rỗng, non-numeric, độ dài, sai giá trị, cross-email |
| TC-MFORGOT-011 … 016 | Mật khẩu mới: rỗng, ngắn, thiếu thành phần |
| TC-MFORGOT-017 … 018 | Xác nhận mật khẩu: rỗng, không khớp |
| TC-MFORGOT-019 … 020 | UI: Step Indicator, Quay lại đăng nhập |
| TC-MFORGOT-021 … 044 | BVA — Email, OTP, Password, Confirm boundaries |
| TC-MFORGOT-SUP-001 … 007 | GAP remediation — API, UI structure, FR-22 |
