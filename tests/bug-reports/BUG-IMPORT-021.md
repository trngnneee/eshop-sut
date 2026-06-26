Title: [BUG][Import][Backend] Lưu trữ mã độc XSS nguyên bản vào database trong cột price

## Found by Test Case
[TC-IMPORT-031](../test-cases/import/TC-IMPORT-031.md)

## Requirement liên quan
FR-16: Import Sản phẩm từ CSV (Kiểm tra kiểu dữ liệu)

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
       {"name": "Imported XSS Price", "price": "<script>alert('XSS_price')</script>", "description": "Mô tả", "imageUrl": "", "category_id": 1}
     ]
   }
   ```

## Expected result
- Hệ thống từ chối import vì `price` không phải là số dương hợp lệ, trả về HTTP 400.

## Actual result
- Hệ thống trả về HTTP 200 OK và lưu trữ mã độc `<script>alert('XSS_price')</script>` vào cột `price` trong CSDL.

## Evidence
![Phản hồi API thành công](../bugs-screenshots/BUG-IMPORT-021a.png)
![Dữ liệu lưu trữ trong database](../bugs-screenshots/BUG-IMPORT-021b.png)
---
*Nhãn (Labels) cần gắn:* `type: bug, module: backend, severity: major, priority: P2, status: new, found-by: test-case`
