## Title
[Major] Regex số điện thoại từ chối số VN bắt đầu bằng 0

## Description
Regex `/^[1-9][0-9]{8,9}$/` (Profile.jsx:44) loại số bắt đầu bằng 0, mâu thuẫn chính placeholder "0912345678".

## Steps to Reproduce
1. Đăng nhập, mở `/profile`.
2. Nhập `0912345678` vào ô SĐT, bấm Cập nhật.

## Expected Result
Số `0912345678` được chấp nhận.

## Actual Result
- (GUI-IA02-06) Nhập SĐT hợp lệ "0912345678" bị từ chối: "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số." — regex yêu cầu số đầu 1-9 nên loại số VN bắt đầu bằng 0, mâu thuẫn với placeholder.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-06

## Requirement
FR-22 (format constraints: phone)

## Severity
Major — Người dùng nhập SĐT hợp lệ vẫn bị chặn — không cập nhật được hồ sơ.

## Screenshot
![GUI-IA02-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965717/eshop-hw03/gui-checklist/GUI-IA02-06.png)