# TC-ST-FORGOT-PASSWORD-E2E-002

## Test Case ID
TC-ST-FORGOT-PASSWORD-E2E-002

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03, FR-01

## Testing Technique
State Transition Testing

## Coverage Type
End-to-End Test (Alternative Path - Quay lại rồi đặt lại thành công)

## Covered State(s)
S0 (Trang đăng nhập), S1 (Bước 1 - Yêu cầu OTP), S2 (Bước 2 - Đặt lại mật khẩu), S3 (Đặt lại mật khẩu thành công)

## Covered Transition(s)
T1 (S0 → S1), T3 (S1 → S0), T1 (S0 → S1), T2 (S1 → S2), T4 (S2 → S3)

## Covered switch sequence, if applicable
E2E-002: T1 → T3 → T1 → T2 → T4 (S0 → S1 → S0 → S1 → S2 → S3)

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị trang đăng nhập (S0).
- Tài khoản `test@eshop.com` đã được đăng ký trong hệ thống.

## Test Data
| Parameter | Value |
| --- | --- |
| Email đã đăng ký | test@eshop.com |
| OTP | Mã OTP 6 chữ số hiển thị trên màn hình |
| Mật khẩu mới | NewPass456@ |
| Xác nhận mật khẩu mới | NewPass456@ |

## Test Steps
1. Tại trang đăng nhập (S0), nhấn nút "Quên mật khẩu" (A1) → Chuyển sang S1.
2. Tại màn hình Bước 1/2 (S1), nhấn nút "Quay lại đăng nhập" (A4) → Chuyển về S0.
3. Tại trang đăng nhập (S0), nhấn lại nút "Quên mật khẩu" (A1) → Chuyển sang S1.
4. Tại màn hình Bước 1/2 (S1), nhập email `test@eshop.com` và nhấn gửi yêu cầu OTP (A2) → Chuyển sang S2. Ghi lại mã OTP.
5. Tại màn hình Bước 2/2 (S2), nhập OTP hợp lệ, Mật khẩu mới `NewPass456@`, Xác nhận `NewPass456@`, nhấn xác nhận (A5) → Chuyển sang S3.
6. Thử đăng nhập bằng mật khẩu mới `NewPass456@` để xác nhận.

## Expected Result
- Sau bước 1: Hệ thống chuyển sang S1. T1 thực thi thành công.
- Sau bước 2: Hệ thống điều hướng về S0. T3 thực thi thành công.
- Sau bước 3: Hệ thống chuyển sang S1 lần nữa. T1 thực thi lại thành công.
- Sau bước 4: Hệ thống sinh OTP và chuyển sang S2. T2 thực thi thành công.
- Sau bước 5: Hệ thống đặt lại mật khẩu thành công và chuyển sang S3. T4 thực thi thành công.
- Sau bước 6: Đăng nhập thành công bằng mật khẩu mới `NewPass456@`.
- Luồng E2E với bước quay lại từ S0 → S1 → S0 → S1 → S2 → S3 hoàn tất.

## Final State
S3 (Đặt lại mật khẩu thành công)

## Risk Level
High

## Actual Result
Luồng E2E từ S0 → S1 → S0 → S1 → S2 → S3 thực hiện được. Tất cả 5 transitions T1, T3, T1, T2, T4 đều được đi qua. Tuy nhiên, tại T2: OTP được sinh ra chỉ có **4 chữ số** thay vì 6 chữ số. Luồng E2E hoàn tất nhưng không đạt chuẩn về OTP. Đăng nhập bằng mật khẩu mới: thành công.

## Status
FAIL

## Bug Reference
BUG-FR03-001 — OTP sinh ra 4 chữ số thay vì 6 chữ số
