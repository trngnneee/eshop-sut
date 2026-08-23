# Human-Extended Test Cases - Admin Coupons

File này liệt kê các test case do người kiểm thử bổ sung sau khi audit bộ test do AI sinh. Các case này chỉ nằm trong scope chạy hiện tại: `POST /api/admin/coupons`.

## Added Test Cases

- Tổng số case bổ sung: 7
- ID range: `HT-ADMIN-EXT-001` đến `HT-ADMIN-EXT-007`
- Trọng tâm: security, hidden state transitions của coupon creation, input normalization, và business invariants có thể gây lỗi downstream ở apply-coupon.
- Lý do bổ sung: bộ AI-generated ban đầu bao phủ nhiều partition cơ bản của body và auth chung, nhưng chưa đi sâu vào duplicate race/replay, case-insensitive uniqueness, thiếu một số required field, ràng buộc integer, fixed discount gây negative final amount, và JWT tampering cụ thể.

| ID | Category | Title | Preconditions | Request | Expected Result |
| --- | --- | --- | --- | --- | --- |
| HT-ADMIN-EXT-001 | StateTransition, Security | Hai request tạo cùng một code đồng thời chỉ được tạo một coupon | Admin có JWT hợp lệ; coupon code `RACEADMIN01` chưa tồn tại; runner có thể gửi hai request gần như đồng thời | `POST /api/admin/coupons` với cùng body `RACEADMIN01` ở cả hai request | Chỉ một request được tạo coupon thành công; request còn lại phải bị từ chối duplicate, không tạo hai coupon cùng code. |
| HT-ADMIN-EXT-002 | DomainPartition | Thiếu `max_uses_per_user` khi tạo coupon | Admin có JWT hợp lệ | `POST /api/admin/coupons` không có field `max_uses_per_user` | API từ chối vì FR-17 đánh dấu `max_uses_per_user` là field bắt buộc; không tự default âm thầm. |
| HT-ADMIN-EXT-003 | Security | Coupon fixed không được có discount lớn hơn ngưỡng/tổng có thể áp dụng | Admin có JWT hợp lệ; coupon code `FIXOVER01` chưa tồn tại | `POST /api/admin/coupons` với `type=fixed`, `discount_value=500000`, `min_order_amount=100000` | API từ chối để tránh tạo coupon có thể làm `final_amount` âm ở downstream apply-coupon/checkout. |
| HT-ADMIN-EXT-004 | DomainPartition, Security | Code có khoảng trắng đầu/cuối không được lưu thành coupon khác | Admin có JWT hợp lệ; coupon code `TRIMADMIN` chưa tồn tại | `POST /api/admin/coupons` với `code=" TRIMADMIN "` | API phải trim và lưu canonical code hoặc từ chối input; không được tạo coupon có code chứa khoảng trắng gây nhầm lẫn. |
| HT-ADMIN-EXT-005 | StateTransition, Security | Duplicate code khác hoa/thường với seed coupon không được tạo | Admin có JWT hợp lệ; seed đã có `SAVE10` | `POST /api/admin/coupons` với `code="save10"` | API từ chối hoặc normalize để không có hai coupon chỉ khác casing, tránh bypass uniqueness/lookup confusion. |
| HT-ADMIN-EXT-006 | DomainPartition | `max_uses_per_user` là số thập phân bị từ chối | Admin có JWT hợp lệ; coupon code `DECIMALUSE` chưa tồn tại | `POST /api/admin/coupons` với `max_uses_per_user=1.5` | API từ chối vì số lần dùng/người phải là integer >= 1. |
| HT-ADMIN-EXT-007 | Security | JWT payload tự sửa role thành admin nhưng signature sai bị từ chối | Có token user bị chỉnh payload role=`admin` nhưng signature không hợp lệ | `POST /api/admin/coupons` với forged token | API trả 401/403 và không tạo coupon; không được tin role trong payload nếu signature không hợp lệ. |

## Why The AI Missed Them

| Added Test Case | Why AI Missed It |
| --- | --- |
| HT-ADMIN-EXT-001 | AI đã có duplicate test theo kiểu tuần tự, nhưng chưa nghĩ tới race condition khi hai request cùng code đến gần như đồng thời. Đây là giới hạn thường gặp vì model sinh single-request tests nhiều hơn multi-request/concurrency tests. |
| HT-ADMIN-EXT-002 | AI kiểm nhiều required field như `code`, nhưng bỏ sót `max_uses_per_user` dù FR-17 ghi field này là bắt buộc. Thiếu sót đến từ domain partition chưa duyệt đủ từng field bắt buộc một cách máy móc. |
| HT-ADMIN-EXT-003 | AI kiểm `discount_value > 100` cho percent, nhưng chưa tách business invariant riêng của fixed coupon. Đây là model limitation khi dùng cùng tư duy percent cho mọi loại discount mà chưa xét hậu quả `final_amount` âm ở API liên quan. |
| HT-ADMIN-EXT-004 | AI đã kiểm code rỗng/whitespace, nhưng chưa kiểm khoảng trắng đầu/cuối quanh một code hợp lệ. Đây là boundary normalization phổ biến nhưng dễ bị bỏ qua nếu prompt chỉ nhắc empty/whitespace chung chung. |
| HT-ADMIN-EXT-005 | AI kiểm duplicate exact-match, nhưng chưa kiểm duplicate sau normalization/case folding. Thiếu sót đến từ prompt chưa yêu cầu xem xét uniqueness theo canonical form của coupon code. |
| HT-ADMIN-EXT-006 | AI kiểm `max_uses_per_user=0`, nhưng chưa kiểm số thập phân. Đây là lỗi domain partition còn nông: biết ràng buộc `>= 1` nhưng chưa tách kiểu integer khỏi number nói chung. |
| HT-ADMIN-EXT-007 | AI có case user thường dùng JWT hợp lệ và token sai định dạng, nhưng chưa kiểm token bị chỉnh payload role. Đây là security gap do model kiểm auth theo nhóm lớn, chưa phân biệt malformed token với tampered signed token. |
