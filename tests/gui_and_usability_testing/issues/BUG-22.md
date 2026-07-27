## Title
[Major] Label không gắn với input (thiếu htmlFor/id)

## Description
Không `<label>` nào trên 4 form có `htmlFor` gắn với `id` input.

## Steps to Reproduce
1. Mở một form bất kỳ.
2. Click vào chữ nhãn (vd "Mật khẩu").

## Expected Result
Click nhãn → focus vào ô input tương ứng.

## Actual Result
- (GUI-GAP-04) Không label nào trên các form (Đăng nhập/Đăng ký/Quên MK/Hồ sơ) có thuộc tính htmlFor/for gắn với input — click nhãn không focus vào ô, screen reader không đọc được tên field (WCAG 1.3.1, 4.1.2).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-GAP-04

## Requirement
Heuristic / WCAG (label association)

## Severity
Major — Click nhãn không focus ô nhập; screen reader không đọc được tên field (WCAG 1.3.1/4.1.2).

## Screenshot
![GUI-GAP-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965685/eshop-hw03/gui-checklist/GUI-GAP-04.png)