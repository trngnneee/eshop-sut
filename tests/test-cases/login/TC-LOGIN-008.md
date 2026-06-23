# TC-LOGIN-008: Kiểm tra cấu hình Rate Limiting ngăn chặn brute force mật độ cao

## Requirement ID
SEC-02

## Module / Test type / Technique
Login / Security / Rate Limiting / Stress Testing

## Preconditions
- Máy chủ Backend đang chạy.

## Test data
- Gửi liên tiếp 15 request đăng nhập trong vòng 1 giây.

## Test steps
1. Sử dụng script hoặc công cụ gửi 15 yêu cầu đăng nhập liên tiếp với tần suất cao tới `/api/login`.
2. Kiểm tra mã trạng thái HTTP trả về của các request cuối cùng.

## Expected result
- Hệ thống phải kích hoạt Rate Limiting và trả về lỗi `HTTP 429 Too Many Requests` khi phát hiện tần suất yêu cầu vượt quá giới hạn.

## Status / Related bugs
Failed / #10
