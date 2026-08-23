# Screenshots — GitHub Issues (bug)

Chụp mỗi Issue trên GitHub (https://github.com/trngnneee/eshop-sut/issues) rồi lưu vào **đúng tên** dưới đây.
Mỗi ảnh nên thấy: tiêu đề `[BUG][…]`, labels, và phần Steps/Expected/Actual.

| File cần lưu | Issue | Tiêu đề |
|--------------|:-----:|---------|
| `issue-440-cancel-shipping.png`       | #440 | User hủy được đơn shipping |
| `issue-441-empty-body.png`            | #441 | Body rỗng tạo record null |
| `issue-442-error-html.png`            | #442 | Lỗi trả HTML thay vì JSON |
| `issue-443-id-no-validation.png`      | #443 | Không validate kiểu :id |
| `issue-444-id-non-canonical.png`      | #444 | id không canonical |
| `issue-445-jwt-forge.png`             | #445 | Secret JWT hardcode / forge |
| `issue-446-nosniff.png`               | #446 | Thiếu X-Content-Type-Options |
| `issue-447-name-over-255.png`         | #447 | name > 255 ký tự |
| `issue-448-no-validation.png`         | #448 | POST/PUT không validate FR-15 |
| `issue-449-no-op-not-found.png`       | #449 | PUT/DELETE not-found no-op |
| `issue-450-not-found-200.png`         | #450 | GET id không tồn tại → 200 {} |
| `issue-451-order-read-no-auth.png`    | #451 | IDOR đọc đơn không token |
| `issue-452-price-type.png`            | #452 | price string với id chẵn |
| `issue-453-crud-no-auth.png`          | #453 | CRUD sản phẩm không auth |
| `issue-454-put-null-fields.png`       | #454 | PUT null hóa field |
| `issue-455-repeated-search.png`       | #455 | Param search lặp |
| `issue-456-sql-error-html.png`        | #456 | Lỗi SQL trả HTML + leak |
| `issue-457-sqli-wildcard.png`         | #457 | SQLi / wildcard bypass |
| `issue-458-unicode-search.png`        | #458 | Search Unicode không nhất quán |
| `issue-459-union-leak.png`            | #459 | SQLi UNION lộ credential |

> Có thể thay 20 ảnh riêng bằng **1 ảnh tổng** trang Issues (thấy đủ 20 issue open) + vài ảnh chi tiết bug Critical — tùy thời gian. Tối thiểu nên có ảnh các bug **Critical/P0** (#440, #445, #451, #453, #448, #454, #457, #459).
