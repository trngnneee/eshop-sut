# API-3 — Danh sách test case chốt cho `PUT /api/admin/orders/:id/status`

> 38 case AI sau audit + 6 case human extension. 25 dòng đầu là đầy đủ ma trận 5×5.

| TC ID | Requirement | Nhóm | Kỹ thuật | Preconditions | Method + Endpoint / Test data | Expected | Nguồn | Kỳ vọng chạy | Bug ID | Execution | Lý do |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-ORDER-STATUS-001 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='pending'` | 400; từ chối transition pending → pending | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-002 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='confirmed'` | 200; transition pending → confirmed được chấp nhận | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-003 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='shipping'` | 400; từ chối transition pending → shipping | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-004 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='delivered'` | 400; từ chối transition pending → delivered | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-005 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='canceled'` | 200; transition pending → canceled được chấp nhận | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-006 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='pending'` | 400; từ chối transition confirmed → pending | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-007 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; từ chối transition confirmed → confirmed | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-008 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='shipping'` | 200; transition confirmed → shipping được chấp nhận | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-009 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='delivered'` | 400; từ chối transition confirmed → delivered | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-010 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='canceled'` | 200; transition confirmed → canceled được chấp nhận | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-011 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='pending'` | 400; từ chối transition shipping → pending | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-012 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; từ chối transition shipping → confirmed | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-013 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='shipping'` | 400; từ chối transition shipping → shipping | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-014 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='delivered'` | 200; transition shipping → delivered được chấp nhận | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-015 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='canceled'` | 200; transition shipping → canceled được chấp nhận | AI/audit | FAIL | D-ADM-03 | Automated | — |
| TC-API-ORDER-STATUS-016 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='pending'` | 400; từ chối transition delivered → pending | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-017 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; từ chối transition delivered → confirmed | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-018 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='shipping'` | 400; từ chối transition delivered → shipping | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-019 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='delivered'` | 400; từ chối transition delivered → delivered | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-020 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='canceled'` | 400; từ chối transition delivered → canceled | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-021 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='pending'` | 400; từ chối transition canceled → pending | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-022 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; từ chối transition canceled → confirmed | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-023 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='shipping'` | 400; từ chối transition canceled → shipping | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-024 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='delivered'` | 400; từ chối transition canceled → delivered | AI/audit | FAIL | D-ADM-02 | Automated | — |
| TC-API-ORDER-STATUS-025 | FR-10/FR-12/FR-18 | State | State-transition | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='canceled'` | 400; từ chối transition canceled → canceled | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-026 | FR-10/FR-12/FR-18 | Partition | EP | Admin JWT | `id=999999; status='confirmed'` | 404; {error:'Order not found'} | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-027 | FR-10/FR-12/FR-18 | Partition | BVA | Admin JWT | `id=-1; status='confirmed'` | Controlled 4xx; không 5xx | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-028 | FR-10/FR-12/FR-18 | Partition | EP/type | Admin JWT | `id='abc'; status='confirmed'` | Controlled 4xx; không cập nhật order | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-029 | FR-10/FR-12/FR-18 | Partition | EP | Admin JWT | `Body={}` | 400; lỗi transition/validation | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-030 | FR-10/FR-12/FR-18 | Partition | EP/type | Admin JWT | `status='DELIVERED'` | 400; invalid state transition | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-031 | FR-10/FR-12/FR-18 | Security | Security | Order tồn tại | `Không gửi Authorization` | 401; không cập nhật | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-032 | FR-10/FR-12/FR-18 | Security | Security | Order tồn tại | `Bearer invalid.token` | 403; không cập nhật | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-033 | FR-10/FR-12/FR-18 | Security | Security/role | User JWT; order tồn tại | `Bearer userToken; status='confirmed'` | 403; không cập nhật | AI/audit | FAIL | D-ADM-01 | Automated | — |
| TC-API-ORDER-STATUS-034 | FR-10/FR-12/FR-18 | Security | Security/IDOR | User JWT; order B tồn tại | `Bearer userToken; id=orderB` | 403 với user token | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-035 | FR-10/FR-12/FR-18 | Schema | Schema | Admin JWT; transition hợp lệ | `status='confirmed'` | 200; message:string | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-036 | FR-10/FR-12/FR-18 | Schema | Schema | Admin JWT; transition invalid | `status='delivered' từ pending` | 400; controlled JSON error | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-037 | FR-10/FR-12/FR-18 | Schema | Schema | Admin JWT; transition hợp lệ | `status='confirmed'` | Content-Type application/json | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-038 | FR-10/FR-12/FR-18 | Schema | Schema/security | Admin JWT; transition hợp lệ | `status='confirmed'` | Không có password/token/secret nội bộ | AI/audit | PASS | — | Automated | — |
| TC-API-ORDER-STATUS-039 | FR-10/FR-12/FR-18 | Extension | State/security | User thường có JWT; order tồn tại; PUT status=confirmed | `Role escalation bằng user token` | 403; không cập nhật order | Human | FAIL | D-ADM-01 | Automated | — |
| TC-API-ORDER-STATUS-040 | FR-10/FR-12/FR-18 | Extension | State/security | User A dùng token sửa order của user B | `Cross-user order mutation` | 403; user không có quyền admin | Human | FAIL | D-ADM-01 | Automated | — |
| TC-API-ORDER-STATUS-041 | FR-10/FR-12/FR-18 | Extension | State/security | Admin thử canceled→delivered rồi kiểm tra dữ liệu delivered/dashboard | `Canceled không hồi sinh và dashboard không tăng doanh thu` | 400; không tăng delivered revenue | Human | FAIL | D-ADM-02 | Blocked | SUT không có Dashboard/revenue API để quan sát hậu điều kiện doanh thu; transition canceled→delivered được phủ riêng bởi TC-024. |
| TC-API-ORDER-STATUS-042 | FR-10/FR-12/FR-18 | Extension | State/security | Admin JWT; order shipping; status=canceled | `Admin hủy đơn shipping` | 200; order chuyển canceled | Human | FAIL | D-ADM-03 | Automated | — |
| TC-API-ORDER-STATUS-043 | FR-10/FR-12/FR-18 | Extension | State/security | User JWT; order shipping; PUT /api/orders/:id/cancel | `User không hủy order shipping qua endpoint user` | 400; user không được hủy shipping | Human | FAIL | D-ADM-08 | Automated | — |
| TC-API-ORDER-STATUS-044 | FR-10/FR-12/FR-18 | Extension | State/security | Admin JWT; status=['delivered'] hoặc {value:'delivered'} | `Status sai kiểu dữ liệu` | 400; phân biệt type invalid với transition invalid | Human | FAIL | D-ADM-06 | Automated | — |

## Summary

| Nguồn | Số lượng |
| :--- | ---: |
| AI-generated sau audit | 38 |
| Human extension | 6 |
| **Tổng** | **44** |
