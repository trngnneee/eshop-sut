# TC-ST-FORGOT-PASSWORD-E2E-001

## Test Case ID
TC-ST-FORGOT-PASSWORD-E2E-001

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03, FR-01

## Testing Technique
State Transition Testing

## Coverage Type
End-to-End Test (Happy Path)

## Covered State(s)
S0 (Trang đăng nhập), S1 (Bước 1 - Yêu cầu OTP), S2 (Bước 2 - Đặt lại mật khẩu), S3 (Đặt lại mật khẩu thành công)

## Covered Transition(s)
T1 (S0 → S1), T2 (S1 → S2), T4 (S2 → S3)

## Covered switch sequence, if applicable
E2E-001: T1 → T2 → T4 (S0 → S1 → S2 → S3)

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị trang đăng nhập (S0).
- Tài khoản `test@eshop.com` đã được đăng ký trong hệ thống với mật khẩu cũ.

## Test Data
| Parameter | Value |
| --- | --- |
| Email đã đăng ký | test@eshop.com |
| OTP | Mã OTP 6 chữ số hiển thị trên màn hình |
| Mật khẩu mới | NewPass123! |
| Xác nhận mật khẩu mới | NewPass123! |

## Test Steps
1. Truy cập trang đăng nhập (S0).
2. Nhấn nút "Quên mật khẩu" (A1) → Hệ thống chuyển sang màn hình Bước 1/2 (S1).
3. Nhập email `test@eshop.com` và nhấn gửi yêu cầu OTP (A2) → Hệ thống sinh OTP và chuyển sang màn hình Bước 2/2 (S2). Ghi lại mã OTP.
4. Nhập OTP hợp lệ vừa nhận, Mật khẩu mới `NewPass123!`, Xác nhận mật khẩu mới `NewPass123!`, và nhấn xác nhận (A5) → Hệ thống đặt lại mật khẩu thành công (S3).
5. Thử đăng nhập lại bằng mật khẩu mới `NewPass123!` để xác nhận mật khẩu đã được cập nhật.

## Expected Result
- Sau bước 2: Màn hình Bước 1/2 (S1) hiển thị đúng với chỉ báo "Bước 1 / 2" và nút "Quay lại đăng nhập".
- Sau bước 3: Mã OTP 6 chữ số được hiển thị. Màn hình Bước 2/2 (S2) hiển thị đúng với chỉ báo "Bước 2 / 2".
- Sau bước 4: Hệ thống thông báo đặt lại mật khẩu thành công. Workflow kết thúc tại S3.
- Sau bước 5: Đăng nhập thành công bằng mật khẩu mới `NewPass123!`.
- Toàn bộ luồng nghiệp vụ từ S0 đến S3 hoàn tất không có lỗi.

## Final State
S3 (Đặt lại mật khẩu thành công)

## Risk Level
High

## Actual Result
Luồng E2E từ S0 → S1 → S2 → S3 thực hiện được. Tất cả transitions T1, T2, T4 đều được đi qua. Tuy nhiên, tại T2: OTP được sinh ra chỉ có **4 chữ số** thay vì 6 chữ số theo đặc tả. Luồng E2E hoàn tất nhưng không đạt chuẩn về OTP. Đăng nhập bằng mật khẩu mới sau reset: thành công.

## Status
FAIL

## Bug Reference
BUG-FR03-001 — OTP sinh ra 4 chữ số thay vì 6 chữ số
