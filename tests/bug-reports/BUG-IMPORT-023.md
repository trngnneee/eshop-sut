Title: [BUG][Import][Backend] Cho phép lưu trữ SQL Injection payload trong cột category_id

## Found by Test Case
[TC-IMPORT-033](../test-cases/import/TC-IMPORT-033.md)

## Requirement liên quan
FR-16: Import Sản phẩm từ CSV (Kiểm tra kiểu dữ liệu và Bảo mật SQL Injection)

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
       {"name": "Imported SQLi Cat", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": "' OR 1=1 --"}
     ]
   }
   ```

## Expected result
- Hệ thống từ chối import vì `category_id` không hợp lệ, trả về HTTP 400.

## Actual result
- Hệ thống trả về HTTP 200 OK và lưu trữ chuỗi payload SQL Injection nguyên bản vào cột `category_id` trong CSDL.

## Evidence
![Phản hồi API thành công](../bugs-screenshots/BUG-IMPORT-023a.png)
![Dữ liệu lưu trữ trong database](../bugs-screenshots/BUG-IMPORT-023b.png)
---
*Nhãn (Labels) cần gắn:* `type: bug, module: backend, severity: major, priority: P2, status: new, found-by: test-case`
