Title: [BUG][Import][Backend] Cho phép lưu trữ SQL Injection payload trong trường imageUrl

## Found by Test Case
[TC-IMPORT-030](../test-cases/import/TC-IMPORT-030.md)

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
       {"name": "Imported SQLi Image", "price": 100000, "description": "Mô tả", "imageUrl": "' OR 1=1 --", "category_id": 1}
     ]
   }
   ```

## Expected result
- Hệ thống từ chối import các chuỗi SQL Injection payload nguy hiểm trong imageUrl, trả về HTTP 400.

## Actual result
- Hệ thống trả về HTTP 200 OK và lưu trữ chuỗi `' OR 1=1 --` nguyên bản vào CSDL.

## Evidence
![Phản hồi API thành công](../bugs-screenshots/BUG-IMPORT-020a.png)
![Dữ liệu lưu trữ trong database](../bugs-screenshots/BUG-IMPORT-020b.png)
---
*Nhãn (Labels) cần gắn:* `type: bug, module: backend, severity: major, priority: P2, status: new, found-by: test-case`
