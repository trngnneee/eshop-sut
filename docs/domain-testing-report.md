# Tóm tắt yêu cầu

- **Chức năng:** Trạng thái Đơn hàng (Order State Machine) — Phân hệ Mobile
- **Requirement ID:** FR-10, FR-20
- **Module:** MOBILE-ORDER
- **Mô tả:** Đơn hàng trên hệ thống EShop có 5 trạng thái: `pending`, `confirmed`, `shipping`, `delivered`, `canceled`. Trên phân hệ Mobile (React Native), User có thể hủy đơn hàng chỉ khi trạng thái là `pending` hoặc `confirmed`. Trạng thái `delivered` và `canceled` là trạng thái kết thúc (Final State) — không được phép chuyển sang bất kỳ trạng thái nào khác. Khi đơn hàng ở `shipping`, User không được phép tự hủy — chỉ Admin mới có thể thao tác.
- **Phạm vi kiểm thử:** Chỉ kiểm thử giao diện (UI Testing) trên ứng dụng Mobile. Không kiểm thử trực tiếp API.
- **Input (UI):** Trạng thái hiện tại của đơn hàng hiển thị trên mobile, nút Hủy đơn hàng, dialog xác nhận, trạng thái xác thực (đã đăng nhập / chưa đăng nhập).
- **Ràng buộc:**
  - User chỉ hủy được đơn ở trạng thái `pending` hoặc `confirmed` (FR-20).
  - Trạng thái `delivered` và `canceled` là Final States — không chuyển đổi được (FR-10).
  - Đơn `shipping` — User không được tự hủy, chỉ Admin (FR-10).
  - User chỉ thao tác được trên đơn hàng của chính mình (FR-11).
  - Trạng thái phải hiển thị tiếng Việt và phân biệt màu sắc (FR-11).
  - Nút hủy phải dùng màu đỏ (nút nguy hiểm) theo FR-21.
- **Quy tắc validation (UI):**
  - Nút Hủy chỉ hiển thị khi trạng thái cho phép (pending, confirmed).
  - Nút Hủy ẩn khi trạng thái không cho phép (shipping, delivered, canceled).
  - Phải có dialog xác nhận trước khi hủy.
  - Trạng thái cập nhật ngay sau khi hủy thành công.

---

# Sơ đồ chuyển đổi trạng thái (State Machine)

```
                 [Admin xác nhận]          [Admin giao hàng]      [Admin hoàn tất]
  ┌──────────┐ ─────────────────► ┌───────────┐ ──────────────► ┌──────────┐ ──────────► ┌───────────┐
  │ pending  │                    │ confirmed │                  │ shipping │             │ delivered │
  └──────────┘                    └───────────┘                  └──────────┘             └───────────┘
       │                               │
       │ [User/Admin hủy]              │ [User/Admin hủy]
       ▼                               ▼
  ┌──────────┐                    ┌──────────┐
  │ canceled │                    │ canceled │
  └──────────┘                    └──────────┘
```

**Quy tắc hủy đơn trên Mobile (FR-20):**
- `pending` → `canceled` ✓ (User được phép — nút Hủy hiển thị)
- `confirmed` → `canceled` ✓ (User được phép — nút Hủy hiển thị)
- `shipping` → `canceled` ✗ (User KHÔNG được phép — nút Hủy ẩn)
- `delivered` → bất kỳ ✗ (Final State — nút Hủy ẩn)
- `canceled` → bất kỳ ✗ (Final State — nút Hủy ẩn)

---

# Giải thích Domain Testing

Domain Testing được áp dụng để phân tích toàn bộ các miền giá trị đầu vào hợp lệ và không hợp lệ cho chức năng Hủy đơn hàng trên phân hệ Mobile (FR-10 + FR-20). Phạm vi kiểm thử tập trung vào **giao diện người dùng (UI)** trên ứng dụng mobile, không kiểm thử trực tiếp API.

1. **Xác định input cần kiểm thử:** Trạng thái hiện tại (current_status), Hiển thị nút Hủy (visibility), Quyền sở hữu đơn (ownership), Trạng thái xác thực (auth), Hiển thị trạng thái bằng tiếng Việt (localization), Phân biệt màu sắc trạng thái (color), Thông tin đơn hàng trên UI.
2. **Xác định miền giá trị của input:** Được mô tả chi tiết trong bảng Domain Analysis bên dưới.
3. **Xác định dữ liệu hợp lệ:** User đã đăng nhập, đơn hàng thuộc user, trạng thái pending hoặc confirmed (nút Hủy hiển thị), trạng thái hiển thị tiếng Việt + màu sắc phân biệt.
4. **Xác định dữ liệu không hợp lệ:** Chưa đăng nhập (không truy cập được), trạng thái shipping/delivered/canceled (nút Hủy ẩn), trạng thái hiển thị sai tiếng Việt hoặc không phân biệt màu.
5. **Xác định các trường hợp cần kiểm thử:** Tạo test case bao phủ toàn bộ các domain trên, kiểm tra hành vi UI cho mỗi trạng thái đơn hàng.

## Domain Analysis Table

| Biến | Domain | Loại giá trị | Khoảng giá trị | Mô tả |
|---|---|---|---|---|
| Trạng thái hiện tại (current_status) | Order State | Enum | pending, confirmed, shipping, delivered, canceled | Trạng thái hiện tại quyết định nút Hủy hiển thị hay ẩn trên mobile. |
| Hiển thị nút Hủy (visibility) | UI Action | Boolean | Hiển thị / Ẩn | Mobile chỉ hiển thị nút Hủy khi trạng thái cho phép (pending, confirmed). |
| Trạng thái xác thực (auth) | Authentication | Boolean | Đã đăng nhập / Chưa đăng nhập | User chưa đăng nhập không truy cập được Lịch sử đơn hàng. |
| Quyền sở hữu đơn hàng (ownership) | Authorization | Boolean | Chủ đơn / Không phải chủ đơn | Mobile chỉ hiển thị đơn hàng của user hiện tại. |
| Hiển thị trạng thái (localization) | Display Text | Enum | Tiếng Việt cho 5 trạng thái | FR-11 quy định trạng thái phải dịch sang tiếng Việt rõ ràng. |
| Màu sắc trạng thái (color) | Display Color | Enum | 5 màu phân biệt cho 5 trạng thái | FR-11 quy định mỗi trạng thái phải có màu sắc riêng biệt. |
| Thông tin đơn hàng (UI) | Display Data | Composite | Mã đơn, Ngày đặt, Tổng tiền (₫), Trạng thái | FR-11 quy định hiển thị đầy đủ 4 thông tin. |

---

# Giải thích Boundary Value Analysis

Kỹ thuật BVA được áp dụng cho biên trạng thái cho phép hủy trên Mobile — đây là biên quan trọng nhất khi kiểm thử UI.

> **Lưu ý:** BVA cho order_id (giá trị biên 0, 1, 2, 999999, "abc") đã được loại bỏ vì thuộc phạm vi kiểm thử API, không phải UI. Trên giao diện mobile, User không thể nhập order_id thủ công.

## BVA: Trạng thái cho phép hủy trên Mobile (State Boundary)

| Boundary | Trạng thái | Nút Hủy trên Mobile | Test Case | Mô tả |
|---|---|---|---|---|
| Biên dưới (cho phép) | pending | ✓ Hiển thị | TC-MOBILE-ORDER-001, TC-009 | Trạng thái đầu tiên cho phép hủy — nút Hủy hiển thị. |
| Biên trên (cho phép) | confirmed | ✓ Hiển thị | TC-MOBILE-ORDER-002, TC-010 | Trạng thái cuối cùng cho phép hủy — nút Hủy hiển thị. |
| Vượt biên (không cho phép) | shipping | ✗ Ẩn | TC-MOBILE-ORDER-003, TC-006 | Trạng thái đầu tiên KHÔNG cho phép hủy — nút Hủy ẩn. |
| Final State 1 | delivered | ✗ Ẩn | TC-MOBILE-ORDER-004, TC-007 | Trạng thái kết thúc — nút Hủy ẩn. |
| Final State 2 | canceled | ✗ Ẩn | TC-MOBILE-ORDER-005, TC-008 | Trạng thái kết thúc — nút Hủy ẩn. |

- *Lý do:* Biên giữa `confirmed` (nút Hủy hiển thị) và `shipping` (nút Hủy ẩn) là ranh giới quan trọng nhất. Nếu logic hiển thị nút bị lỗi ở đây, User có thể hủy đơn đang giao gây thiệt hại nghiệp vụ. Final States cần kiểm tra kỹ để đảm bảo giao diện không hiển thị bất kỳ thao tác thay đổi trạng thái nào.

---

# Danh sách Test Case

| TC ID | Mô tả | Kỹ thuật | Loại |
|---|---|---|---|
| TC-MOBILE-ORDER-001 | User hủy đơn `pending` thành công trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-002 | User hủy đơn `confirmed` thành công trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-003 | User KHÔNG thể hủy đơn `shipping` trên mobile | Domain Testing | Negative |
| TC-MOBILE-ORDER-004 | User KHÔNG thể hủy đơn `delivered` (Final State) | Domain Testing | Negative |
| TC-MOBILE-ORDER-005 | User KHÔNG thể hủy đơn `canceled` (Final State) | Domain Testing | Negative |
| TC-MOBILE-ORDER-006 | Mobile ẩn nút hủy khi trạng thái = `shipping` | Domain Testing | Negative |
| TC-MOBILE-ORDER-007 | Mobile ẩn nút hủy khi trạng thái = `delivered` | Domain Testing | Negative |
| TC-MOBILE-ORDER-008 | Mobile ẩn nút hủy khi trạng thái = `canceled` | Domain Testing | Negative |
| TC-MOBILE-ORDER-009 | Mobile hiển thị nút hủy khi trạng thái = `pending` | Domain Testing | Positive |
| TC-MOBILE-ORDER-010 | Mobile hiển thị nút hủy khi trạng thái = `confirmed` | Domain Testing | Positive |
| TC-MOBILE-ORDER-011 | Sau khi hủy, trạng thái cập nhật thành `canceled` trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-012 | Sau khi hủy, đơn không thể hủy lại (Final State) | Domain Testing | Negative |
| TC-MOBILE-ORDER-013 | User chưa đăng nhập không thể truy cập Lịch sử đơn hàng | Domain Testing | Negative |
| TC-MOBILE-ORDER-014 | Hiển thị trạng thái `pending` bằng tiếng Việt trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-015 | Hiển thị trạng thái `confirmed` bằng tiếng Việt trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-016 | Hiển thị trạng thái `shipping` bằng tiếng Việt trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-017 | Hiển thị trạng thái `delivered` bằng tiếng Việt trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-018 | Hiển thị trạng thái `canceled` bằng tiếng Việt trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-019 | Mỗi trạng thái có màu sắc phân biệt trên mobile | Domain Testing | Positive |
| TC-MOBILE-ORDER-020 | Lịch sử đơn hàng chỉ hiển thị đơn của user hiện tại | Domain Testing | Positive |
| TC-MOBILE-ORDER-021 | Hiển thị đầy đủ thông tin: Mã đơn, Ngày đặt, Tổng tiền, Trạng thái | Domain Testing | Positive |
| TC-MOBILE-ORDER-022 | Dialog xác nhận trước khi hủy đơn trên mobile | Domain Testing | Positive |

---

# Coverage Summary

- **Domain Coverage:** 100% — Bao phủ toàn bộ 7 miền giá trị: Trạng thái đơn hàng (5 trạng thái: pending / confirmed / shipping / delivered / canceled), Hiển thị nút Hủy (hiển thị / ẩn theo từng trạng thái), Xác thực (đã đăng nhập / chưa đăng nhập), Quyền sở hữu (chỉ xem đơn của mình), Hiển thị tiếng Việt (5 trạng thái × tiếng Việt), Màu sắc phân biệt (5 trạng thái × 5 màu), Thông tin đơn hàng (Mã đơn, Ngày đặt, Tổng tiền, Trạng thái).
- **Boundary Coverage:** 100% — BVA cho biên trạng thái cho phép hủy trên mobile: pending ✓ (nút Hủy hiển thị), confirmed ✓ (nút Hủy hiển thị), shipping ✗ (nút Hủy ẩn — biên quan trọng), delivered ✗ (Final State), canceled ✗ (Final State).
- **Positive Test Cases:** TC-001, TC-002, TC-009, TC-010, TC-011, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022 (14 test cases).
- **Negative Test Cases:** TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-012, TC-013 (8 test cases).
- **Tổng số test case:** 22.
- **Phạm vi:** Tất cả test case chỉ kiểm thử giao diện (UI) trên phân hệ Mobile. Không kiểm thử trực tiếp API.
