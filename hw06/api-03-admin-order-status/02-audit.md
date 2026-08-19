# API-3 — Human-review worksheet for AI-generated order-status cases

> Oracle: FR-10/FR-12/FR-18, API specification, `backend/server.js` và `docs/hw06/02-sut-defect-catalog.md` §3.

## Bảng audit 100% test case AI sinh

| TC ID | Nhãn | Lý do review | Hành động sửa |
| :--- | :--- | :--- | :--- |
| TC-API-ORDER-STATUS-001 | VALID | Ô ma trận pending → pending được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-002 | VALID | Ô ma trận pending → confirmed được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-003 | VALID | Ô ma trận pending → shipping được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-004 | VALID | Ô ma trận pending → delivered được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-005 | VALID | Ô ma trận pending → canceled được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-006 | VALID | Ô ma trận confirmed → pending được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-007 | VALID | Ô ma trận confirmed → confirmed được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-008 | VALID | Ô ma trận confirmed → shipping được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-009 | VALID | Ô ma trận confirmed → delivered được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-010 | VALID | Ô ma trận confirmed → canceled được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-011 | VALID | Ô ma trận shipping → pending được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-012 | VALID | Ô ma trận shipping → confirmed được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-013 | VALID | Ô ma trận shipping → shipping được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-014 | VALID | Ô ma trận shipping → delivered được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-015 | INVALID | FR-10 cho phép Admin hủy đơn shipping; AI đã mô tả hiện thực lỗi thay vì đặc tả. | Sửa expected thành 200; cần báo D-ADM-03 khi SUT trả 400. |
| TC-API-ORDER-STATUS-016 | VALID | Ô ma trận delivered → pending được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-017 | VALID | Ô ma trận delivered → confirmed được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-018 | VALID | Ô ma trận delivered → shipping được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-019 | VALID | Ô ma trận delivered → delivered được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-020 | VALID | Ô ma trận delivered → canceled được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-021 | VALID | Ô ma trận canceled → pending được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-022 | VALID | Ô ma trận canceled → confirmed được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-023 | VALID | Ô ma trận canceled → shipping được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-024 | INVALID | canceled là terminal state; AI đã tin whitelist hiện tại của SUT và cho phép hồi sinh đơn. | Sửa expected thành 400; không được chuyển terminal canceled sang delivered. |
| TC-API-ORDER-STATUS-025 | VALID | Ô ma trận canceled → canceled được đối chiếu trực tiếp với FR-10. | Giữ nguyên. |
| TC-API-ORDER-STATUS-026 | VALID | Defect catalog và API contract yêu cầu order không tồn tại trả 404. | Giữ nguyên oracle 404. |
| TC-API-ORDER-STATUS-027 | INCOMPLETE | API spec không quy định riêng 400 hay 404 cho id âm; ý tưởng boundary đúng nhưng status chưa có oracle. | Sửa thành controlled 4xx; không 5xx và ghi actual status khi execute. |
| TC-API-ORDER-STATUS-028 | INVALID | Không được coi chuỗi tùy ý là order id hợp lệ; expected AI không bám schema path parameter. | Sửa thành 400/404 controlled error. |
| TC-API-ORDER-STATUS-029 | VALID | Body API yêu cầu status; thiếu field phải bị từ chối. | Giữ nguyên. |
| TC-API-ORDER-STATUS-030 | INVALID | API công bố đúng 5 giá trị lowercase; không có yêu cầu normalize. | Sửa thành 400; không cập nhật. |
| TC-API-ORDER-STATUS-031 | VALID | FR-12/SEC-03 yêu cầu JWT hợp lệ cho /api/admin/*. | Giữ nguyên. |
| TC-API-ORDER-STATUS-032 | VALID | authenticateToken từ chối token sai chữ ký. | Giữ nguyên. |
| TC-API-ORDER-STATUS-033 | INVALID | FR-12/SEC-03 yêu cầu role=admin, không chỉ token tồn tại. | Sửa thành 403; tạo bug role escalation nếu SUT cho phép. |
| TC-API-ORDER-STATUS-034 | INCOMPLETE | Endpoint admin phải chặn user role trước; ownership rule chưa được API spec mô tả riêng. | Assert 403 do role; nếu admin thì quyền toàn hệ thống là hợp lệ. |
| TC-API-ORDER-STATUS-035 | INCOMPLETE | Spec chỉ nêu endpoint/body, chưa công bố exact response schema; không được tự bịa object. | Hạ thành tối thiểu message:string nếu response có message. |
| TC-API-ORDER-STATUS-036 | INCOMPLETE | API spec không quy định exact error fields; chỉ status + controlled JSON là oracle chắc chắn. | Không assert duy nhất message; kiểm tra JSON và error/message có nội dung. |
| TC-API-ORDER-STATUS-037 | VALID | API JSON phải trả application/json. | Sửa expected thành application/json. |
| TC-API-ORDER-STATUS-038 | INCOMPLETE | API spec không công bố full response nhưng security boundary cấm lộ credential. | Giữ negative security assertion, không yêu cầu exact field whitelist. |

## Phiên bản expected sau audit cho case cần sửa

| TC ID | Expected đã chốt |
| :--- | :--- |
| TC-API-ORDER-STATUS-015 | 200; transition shipping → canceled được chấp nhận |
| TC-API-ORDER-STATUS-024 | 400; từ chối transition canceled → delivered |
| TC-API-ORDER-STATUS-027 | Controlled 4xx; không 5xx |
| TC-API-ORDER-STATUS-028 | Controlled 4xx; không cập nhật order |
| TC-API-ORDER-STATUS-030 | 400; invalid state transition |
| TC-API-ORDER-STATUS-033 | 403; không cập nhật |
| TC-API-ORDER-STATUS-034 | 403 với user token |
| TC-API-ORDER-STATUS-035 | 200; message:string |
| TC-API-ORDER-STATUS-036 | 400; controlled JSON error |
| TC-API-ORDER-STATUS-038 | Không có password/token/secret nội bộ |

## Thống kê audit

| Nhãn | Số case | Tỷ lệ |
| :--- | ---: | ---: |
| VALID | 28 | 73.68% |
| INVALID | 5 | 13.16% |
| INCOMPLETE | 5 | 13.16% |
| **Tổng đã audit** | **38/38** | **100%** |

## HUMAN checkpoint — bắt buộc trước khi sang Postman

- [ ] Tôi đã đối chiếu đủ 38 dòng, đặc biệt đủ 25 ô state matrix.
- [ ] Tôi đồng ý hoặc đã chỉnh lại nhãn/lý do cho case INVALID/INCOMPLETE.
- [ ] Tôi hiểu vì sao expected phải theo đặc tả, không sửa để khớp bug của SUT.

**Reviewed by:** Đặng Đăng Khoa
**Student ID:** `23127207`  
**Reviewed at:** 11:36 19-08-2026
**Signature / confirmation:** Đã duyệt

## Agent pre-review (không thay thế Human sign-off)

- [x] Đã kiểm tra đủ 25/25 ô của ma trận state transition.
- [x] Đã đối chiếu hai ô có chênh lệch SUT/đặc tả: `shipping → canceled` và `canceled → delivered`.
- [x] Đã kiểm tra 38/38 case đều có đúng một nhãn và mọi INVALID/INCOMPLETE đều có hành động sửa.
- [x] Đã kiểm tra thống kê: 28 VALID, 5 INVALID, 5 INCOMPLETE.

**Agent review time:** `2026-08-19T10:46:00+07:00`  
**Human sign-off:** Còn thiếu — không tự giả mạo chữ ký người học.
