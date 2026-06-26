Title: [BUG][Import][Backend] Cho phép lưu trữ SQL Injection payload trong trường description

## Found by Test Case
[TC-IMPORT-028](../test-cases/import/TC-IMPORT-028.md)

## Requirement liên quan
FR-16: Import Sản phẩm từ CSV (Bảo mật SQL Injection)

## Severity / Priority
Major / P2

## Environment
Backend API & CSDL SQLite

## Steps to reproduce
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Gửi API POST đến `/api/admin/import-products` chứa:
   ```json
   {
     "products": [
       {"name": "Imported SQLi Desc", "price": 100000, "description": "' OR 1=1 --", "imageUrl": "", "category_id": 1}
     ]
   }
   ```

## Expected result
- Hệ thống từ chối import payload SQL Injection nguy hiểm hoặc xử lý chuỗi an toàn bằng parameterized query (để không bị lỗi cấu trúc dữ liệu), trả về HTTP 400.

## Actual result
- Hệ thống trả về HTTP 200 OK và lưu chuỗi `' OR 1=1 --` nguyên bản vào CSDL.

## Evidence
![Phản hồi API thành công](../bugs-screenshots/BUG-IMPORT-018a.png)
![Dữ liệu lưu trữ trong database](../bugs-screenshots/BUG-IMPORT-018b.png)
---
*Nhãn (Labels) cần gắn:* `type: bug, module: backend, severity: major, priority: P2, status: new, found-by: test-case`
