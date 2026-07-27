## Title
[Major] Field Email dùng type=text trên các form

## Description
Cả 3 form dùng `type="text"` cho ô email.

## Steps to Reproduce
1. Mở `/register`.
2. Nhập `abc` vào ô email và submit.

## Expected Result
Ô email dùng `type="email"`, chặn định dạng sai.

## Actual Result
- (GUI-IA02-02) Field email dùng type: {"/register":"text","/login":"text","/forgot-password":"text"} — đang là "text" thay vì "email", không chặn định dạng sai ở tầng trình duyệt.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-02

## Requirement
FR-22 (input type)

## Severity
Major — Không validate định dạng email phía client; bàn phím mobile không tối ưu.

## Screenshot
![GUI-IA02-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965711/eshop-hw03/gui-checklist/GUI-IA02-02.png)