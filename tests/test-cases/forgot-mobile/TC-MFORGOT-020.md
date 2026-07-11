# TC-MFORGOT-020: Kiểm thử nút Quay lại đăng nhập

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Người dùng đang ở màn hình Quên Mật Khẩu trên Mobile App (Bước 1 hoặc Bước 2)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| (Không áp dụng) | — |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu.
2. Tìm và bấm nút "Quay lại đăng nhập".
3. (Tùy chọn) Lặp lại sau khi chuyển sang Bước 2.

## Expected result
- Hệ thống điều hướng người dùng về màn hình Đăng nhập trên Mobile App.

## Sub-domains covered
SD-UI02 (nút quay lại đăng nhập)

## Type
Valid

## Status / Related bugs
Fail / #9