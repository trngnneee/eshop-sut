Title: [BUG][Import][Backend] Cho phép lưu trữ payload SQL Injection vào trường tên hoặc giá sản phẩm

## Found by Test Case
[TC-IMPORT-017](../test-cases/import/TC-IMPORT-017.md)

## Requirement liên quan
FR-16: Import Sản phẩm từ CSV (Đảm bảo an toàn dữ liệu)

## Severity / Priority
Critical / P1

## Environment
Backend API & CSDL SQLite

## Steps to reproduce
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Gửi API POST đến `/api/admin/import-products` chứa SQL Injection payload trong trường price:
   ```json
   {
     "products": [
       {"name": "Imported Product", "price": "' OR 1=1 --", "description": "Mô tả", "imageUrl": "", "category_id": 1}
     ]
   }
   ```

## Expected result
- Hệ thống từ chối import, trả về HTTP 400 Bad Request vì trường price chứa giá trị không hợp lệ.

## Actual result
- Hệ thống trả về HTTP 200 OK và lưu trực tiếp chuỗi lệnh `"' OR 1=1 --"` vào cột price của CSDL SQLite.

## Evidence
![Ảnh chụp minh chứng](../bugs-screenshots/BUG-IMPORT-010.png)
---
*Nhãn (Labels) cần gắn:* `type: bug, module: backend, severity: critical, priority: P1, status: new, found-by: test-case`
