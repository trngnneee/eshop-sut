Title: [BUG][Import] Không đảm bảo tính giao dịch nguyên tử (Atomicity / Rollback)

## Found by Test Case
TC-IMPORT-009

## Requirement liên quan
FR-16: Import Sản phẩm từ CSV (Nếu có lỗi ở bất kỳ dòng nào, toàn bộ import phải được rollback)

## Severity / Priority
Critical / P0

## Environment
Backend Node.js API, SQLite Database

## Steps to reproduce
1. Admin đăng nhập và lấy JWT token.
2. Gửi API POST đến `/api/admin/import-products` với payload gồm 3 sản phẩm, trong đó dòng 2 có name rỗng:
   ```json
   {
     "products": [
       {"name": "SP Hợp Lệ 1", "price": 100000},
       {"name": "", "price": 120000},
       {"name": "SP Hợp Lệ 3", "price": 150000}
     ]
   }
   ```

## Expected result
- Hệ thống từ chối đăng ký và trả về HTTP 400.
- Giao dịch được rollback toàn bộ, không sản phẩm nào được lưu vào CSDL SQLite.

## Actual result
- Hệ thống trả về HTTP 200 OK.
- Hai sản phẩm "SP Hợp Lệ 1" và "SP Hợp Lệ 3" vẫn được insert thành công vào CSDL, chỉ bỏ qua dòng 2 bị lỗi. Ràng buộc all-or-nothing bị vi phạm.

## Evidence
![BUG-IMPORT-001 Screenshot](../bugs-screenshots/BUG-IMPORT-001.png)

## Cause analysis (Nguyên nhân)
Tại `backend/server.js` dòng 213-232:
Hệ thống duyệt qua mảng sản phẩm bằng `rows.forEach` và thực hiện `stmt.run` độc lập cho từng sản phẩm mà không đặt trong một Transaction (BEGIN/COMMIT) của SQLite. Bất kỳ dòng nào thành công sẽ được commit vĩnh viễn.

## Cách sửa đề xuất
Sử dụng giao dịch SQLite để thực hiện rollback khi có lỗi:
```javascript
db.serialize(() => {
  db.run('BEGIN TRANSACTION');
  // Thực hiện insert...
  // Nếu có lỗi: db.run('ROLLBACK');
  // Nếu thành công tất cả: db.run('COMMIT');
});
```

---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: admin`, `severity: critical`, `priority: P0`, `status: new`, `found-by: test-case`
