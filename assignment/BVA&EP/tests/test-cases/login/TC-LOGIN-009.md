# TC-LOGIN-009: Kiểm tra trạng thái tải (Loading State) và disable nút bấm khi đang đăng nhập

## Requirement ID
FR-21, FR-24

## Module / Test type / Technique
Login / UI/UX / Usability Testing

## Preconditions
- Người dùng ở trang Đăng nhập.

## Test data
- Thông tin đăng nhập hợp lệ.

## Test steps
1. Nhập thông tin đăng nhập hợp lệ.
2. Bấm nút Đăng nhập và quan sát trạng thái của nút bấm cũng như toàn bộ form trong lúc yêu cầu API đang được gửi đi.

## Expected result
- Giao diện phải hiển thị chỉ báo tải (ví dụ: quay vòng loading, hiển thị text "Đang đăng nhập...") và **vô hiệu hóa (disable) nút Đăng nhập** để tránh người dùng click đúp gửi nhiều yêu cầu trùng lặp.

## Status / Related bugs
Fail / #41
