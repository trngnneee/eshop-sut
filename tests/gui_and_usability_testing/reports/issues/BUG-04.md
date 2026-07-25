## Title
[Major] Lộ lỗi SQL kỹ thuật của backend ra giao diện

## Description
Tìm kiếm với ký tự đặc biệt khiến backend trả về nguyên khối HTML lỗi và frontend render trực tiếp (Home.jsx:69-73).

## Steps to Reproduce
1. Mở `/`.
2. Tìm với từ khoá `'` (một dấu nháy đơn).

## Expected Result
Hiển thị thông báo thân thiện ("Có lỗi xảy ra, thử lại sau"), không lộ SQL/stack.

## Actual Result
- (GUI-IA04-14) Tìm với từ khoá "'" hiển thị nguyên khối lỗi kỹ thuật "Database Error / SQLITE_ERROR" ra UI — lộ chi tiết backend thay vì thông báo thân thiện.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-14

## Requirement
Heuristic (error feedback)

## Severity
Major — Lộ thông tin nội bộ (SQLITE_ERROR) hỗ trợ tấn công; trải nghiệm kém.

## Screenshot
![GUI-IA04-14](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965773/eshop-hw03/gui-checklist/GUI-IA04-14.png)