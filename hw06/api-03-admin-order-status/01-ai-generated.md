# API-3 — AI-generated test cases for `PUT /api/admin/orders/:id/status`

> Output thô trước audit. Ma trận state 5×5 được liệt kê đầy đủ theo thứ tự pending, confirmed, shipping, delivered, canceled.

## P1 — Phân tích input và state

| Input/state | Kiểu/vị trí | Oracle/partition |
| :--- | :--- | :--- |
| `Authorization` | Header Bearer JWT | thiếu, sai chữ ký, user role, admin role |
| `:id` | Path parameter | số nguyên tồn tại, không tồn tại, âm, chuỗi |
| `status` | JSON body string enum | 5 lowercase states, thiếu, sai kiểu, sai casing |
| Order state | DB state | 5×5 transitions; delivered/canceled terminal |

## P2–P5 — Ma trận và case bổ sung

| TC ID | Nhóm | Tiêu đề | Preconditions | Test data | Expected result theo output AI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-ORDER-STATUS-001 | State | pending → pending | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='pending'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-002 | State | pending → confirmed | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='confirmed'` | 200; transition hợp lệ |
| TC-API-ORDER-STATUS-003 | State | pending → shipping | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='shipping'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-004 | State | pending → delivered | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='delivered'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-005 | State | pending → canceled | Admin JWT; order hiện ở trạng thái `pending` | `PUT /api/admin/orders/:id; status='canceled'` | 200; transition hợp lệ |
| TC-API-ORDER-STATUS-006 | State | confirmed → pending | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='pending'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-007 | State | confirmed → confirmed | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-008 | State | confirmed → shipping | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='shipping'` | 200; transition hợp lệ |
| TC-API-ORDER-STATUS-009 | State | confirmed → delivered | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='delivered'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-010 | State | confirmed → canceled | Admin JWT; order hiện ở trạng thái `confirmed` | `PUT /api/admin/orders/:id; status='canceled'` | 200; transition hợp lệ |
| TC-API-ORDER-STATUS-011 | State | shipping → pending | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='pending'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-012 | State | shipping → confirmed | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-013 | State | shipping → shipping | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='shipping'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-014 | State | shipping → delivered | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='delivered'` | 200; transition hợp lệ |
| TC-API-ORDER-STATUS-015 | State | shipping → canceled | Admin JWT; order hiện ở trạng thái `shipping` | `PUT /api/admin/orders/:id; status='canceled'` | 400; invalid transition |
| TC-API-ORDER-STATUS-016 | State | delivered → pending | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='pending'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-017 | State | delivered → confirmed | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-018 | State | delivered → shipping | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='shipping'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-019 | State | delivered → delivered | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='delivered'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-020 | State | delivered → canceled | Admin JWT; order hiện ở trạng thái `delivered` | `PUT /api/admin/orders/:id; status='canceled'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-021 | State | canceled → pending | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='pending'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-022 | State | canceled → confirmed | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='confirmed'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-023 | State | canceled → shipping | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='shipping'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-024 | State | canceled → delivered | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='delivered'` | 200; cập nhật thành công |
| TC-API-ORDER-STATUS-025 | State | canceled → canceled | Admin JWT; order hiện ở trạng thái `canceled` | `PUT /api/admin/orders/:id; status='canceled'` | 400; transition không hợp lệ |
| TC-API-ORDER-STATUS-026 | Partition | Order id không tồn tại | Admin JWT | `id=999999; status='confirmed'` | 200; cập nhật |
| TC-API-ORDER-STATUS-027 | Partition | Order id âm | Admin JWT | `id=-1; status='confirmed'` | 400; id không hợp lệ |
| TC-API-ORDER-STATUS-028 | Partition | Order id là chuỗi không số | Admin JWT | `id='abc'; status='confirmed'` | 200; server cast id |
| TC-API-ORDER-STATUS-029 | Partition | Thiếu status | Admin JWT | `Body={}` | 200; giữ nguyên trạng thái |
| TC-API-ORDER-STATUS-030 | Partition | Status sai enum/hoa | Admin JWT | `status='DELIVERED'` | 200; normalize thành delivered |
| TC-API-ORDER-STATUS-031 | Security | Không có token | Order tồn tại | `Không gửi Authorization` | 401 |
| TC-API-ORDER-STATUS-032 | Security | Token sai chữ ký | Order tồn tại | `Bearer invalid.token` | 403 |
| TC-API-ORDER-STATUS-033 | Security | User thường gọi endpoint admin | User JWT; order tồn tại | `Bearer userToken; status='confirmed'` | 200; chỉ cần JWT |
| TC-API-ORDER-STATUS-034 | Security | User A sửa order của user B | User JWT; order B tồn tại | `Bearer userToken; id=orderB` | 403 vì khác chủ đơn |
| TC-API-ORDER-STATUS-035 | Schema | Response success có message string | Admin JWT; transition hợp lệ | `status='confirmed'` | 200; message là object |
| TC-API-ORDER-STATUS-036 | Schema | Response lỗi transition | Admin JWT; transition invalid | `status='delivered' từ pending` | 400; body chỉ có message |
| TC-API-ORDER-STATUS-037 | Schema | Content-Type JSON | Admin JWT; transition hợp lệ | `status='confirmed'` | text/html cũng chấp nhận |
| TC-API-ORDER-STATUS-038 | Schema | Không lộ secret hoặc credential | Admin JWT; transition hợp lệ | `status='confirmed'` | Response có thể trả token/password |

## Thống kê output AI

| Nhóm | Số lượng |
| :--- | ---: |
| State transition matrix | 25 |
| Domain partition/BVA | 5 |
| Security | 4 |
| Schema | 4 |
| **Tổng** | **38** |
