# Tóm tắt yêu cầu

- **Chức năng:** Quản lý Người dùng (Admin)
- **Requirement ID:** FR-19
- **Module:** USERMGMT
- **Mô tả:** Admin có thể xem danh sách tất cả người dùng trong hệ thống (không lộ mật khẩu). Admin có thể xóa bất kỳ người dùng nào, ngoại trừ không được phép xóa chính tài khoản Admin đang đăng nhập.
- **Input:** JWT Token của Admin (để xác thực và phân quyền), `user_id` của người dùng cần xóa.
- **Ràng buộc:**
  - Chỉ tài khoản có `role = 'admin'` mới có quyền truy cập.
  - Mật khẩu tuyệt đối không được lộ trong danh sách.
  - Không được xóa tài khoản Admin đang đăng nhập.
- **Quy tắc validation:**
  - Yêu cầu JWT Token hợp lệ với `role = 'admin'`.
  - `user_id` phải là số nguyên dương và tồn tại trong CSDL.
  - `user_id` mục tiêu không được trùng với `user_id` của Admin đang thực hiện yêu cầu.

---

# Giải thích Domain Testing

Domain Testing được áp dụng để phân tích toàn bộ các miền giá trị đầu vào hợp lệ và không hợp lệ của FR-19.

1. **Xác định input cần kiểm thử:** Trạng thái xác thực (Authentication), phân quyền (Role), `user_id` mục tiêu xóa, số lượng người dùng trong hệ thống.
2. **Xác định miền giá trị của input:** Được mô tả chi tiết trong bảng Domain Analysis bên dưới.
3. **Xác định dữ liệu hợp lệ:** Admin đã đăng nhập, token hợp lệ, xóa user khác (không phải chính mình), user_id tồn tại.
4. **Xác định dữ liệu không hợp lệ:** Chưa đăng nhập, token hết hạn, role = user cố truy cập, xóa chính mình, user_id không tồn tại, user_id kiểu dữ liệu sai.
5. **Xác định các trường hợp cần kiểm thử:** Tạo test case bao phủ toàn bộ các domain và boundary trên.

## Domain Analysis Table

| Biến | Domain | Loại giá trị | Khoảng giá trị | Mô tả |
|---|---|---|---|---|
| Trạng thái xác thực | Authentication | Boolean | Đã đăng nhập, Chưa đăng nhập | Kiểm soát quyền truy cập trang/API Admin. |
| Vai trò người dùng (Role) | Authorization | Enum | admin, user | Chỉ `admin` mới có quyền xem và xóa người dùng. |
| user_id mục tiêu xóa | Identity | Integer | >= 1 (hợp lệ), 0 (biên dưới), âm (không hợp lệ), không tồn tại, chuỗi | Xác định người dùng bị xóa. |
| Quan hệ self-delete | Ownership | Boolean | user_id = admin_id (cấm), user_id ≠ admin_id (cho phép) | Ràng buộc không được tự xóa bản thân. |
| Số lượng người dùng | Count | Integer | 0, 1, >= 2 | Điều kiện biên cho hiển thị danh sách. |
| JWT Token | Token Validity | Enum | Hợp lệ, Hết hạn, Không có, Giả mạo | Kiểm soát khả năng thực hiện thao tác. |
| Trường mật khẩu trong response | Data Exposure | Boolean | Có lộ, Không lộ | Kiểm tra bảo mật dữ liệu nhạy cảm. |

---

# Giải thích Boundary Value Analysis

Kỹ thuật BVA được áp dụng cho các biến số có giá trị biên rõ ràng trong FR-19:

## BVA 1: Số lượng người dùng trong hệ thống (hiển thị danh sách)

- **Minimum boundary:** 0 người dùng (ngoài Admin).
- **Boundary 0 (min):** Kiểm tra empty state khi không có user nào khác — TC-USERMGMT-005.
- **Boundary 1 (min+1):** Kiểm tra hiển thị đúng với đúng 1 user — TC-USERMGMT-006.
- **Large dataset:** Kiểm tra hiển thị với nhiều user (50+) — TC-USERMGMT-011.
- *Lý do:* Đảm bảo logic render danh sách và empty state hoạt động chính xác ở các biên.

## BVA 2: user_id mục tiêu xóa

| Boundary | Giá trị | Test Case | Mô tả |
|---|---|---|---|
| min-1 | 0 | TC-USERMGMT-016 | ID không hợp lệ (dưới biên thấp nhất) |
| min | 1 | TC-USERMGMT-017 | ID hợp lệ thấp nhất |
| min+1 | 2 | TC-USERMGMT-018 | ID hợp lệ kế tiếp |
| Không tồn tại | 999999 | TC-USERMGMT-009 | ID vượt quá max hiện tại |
| Kiểu sai | "abc" | TC-USERMGMT-010 | ID không phải số nguyên |

- *Lý do:* Giá trị biên của user_id thường tiết lộ lỗi validation và lỗi xử lý input trong backend.

---

# Danh sách Test Case

| TC ID | Mô tả | Kỹ thuật | Loại |
|---|---|---|---|
| TC-USERMGMT-001 | Admin xem danh sách người dùng khi đã đăng nhập | Domain Testing | Positive |
| TC-USERMGMT-002 | Danh sách không lộ mật khẩu (UI + API) | Domain Testing | Positive/Security |
| TC-USERMGMT-003 | User thường không thể truy cập trang Admin Users | Domain Testing | Negative |
| TC-USERMGMT-004 | Khách chưa đăng nhập không thể xem danh sách | Domain Testing | Negative |
| TC-USERMGMT-005 | Hiển thị empty state khi có 0 user (BVA min) | BVA | Boundary |
| TC-USERMGMT-006 | Hiển thị đúng khi có 1 user (BVA min+1) | BVA | Boundary |
| TC-USERMGMT-007 | Admin xóa thành công user thường | Domain Testing | Positive |
| TC-USERMGMT-008 | Admin KHÔNG thể tự xóa tài khoản đang đăng nhập | Domain Testing | Negative |
| TC-USERMGMT-009 | Xóa user với ID không tồn tại (999999) | Domain Testing | Negative |
| TC-USERMGMT-010 | Xóa user với ID kiểu không hợp lệ ("abc") | Domain Testing | Negative |
| TC-USERMGMT-011 | Hiển thị danh sách với nhiều user (50+) | BVA | Boundary |
| TC-USERMGMT-012 | Danh sách hiển thị đầy đủ thông tin cần thiết | Domain Testing | Positive |
| TC-USERMGMT-013 | Danh sách cập nhật ngay sau khi xóa (không reload) | Domain Testing | Positive |
| TC-USERMGMT-014 | Xóa user với JWT Token hết hạn bị từ chối | Domain Testing | Negative |
| TC-USERMGMT-015 | User thường cố gọi API xóa user bị từ chối (403) | Domain Testing | Negative |
| TC-USERMGMT-016 | Xóa user với user_id = 0 (BVA min-1) | BVA | Boundary |
| TC-USERMGMT-017 | Xóa user với user_id = 1 (BVA min) | BVA | Boundary |
| TC-USERMGMT-018 | Xóa user với user_id = 2 (BVA min+1) | BVA | Boundary |
| TC-USERMGMT-019 | API không trả về trường password trong response | Domain Testing | Positive/Security |
| TC-USERMGMT-020 | Xóa đúng mục tiêu, không ảnh hưởng tài khoản khác | Domain Testing | Positive |

---

# Coverage Summary

- **Domain Coverage:** 100% — Bao phủ toàn bộ 7 miền giá trị: Authentication (đã đăng nhập / chưa đăng nhập), Role (admin / user), user_id (hợp lệ / không tồn tại / kiểu sai), Self-delete (cấm / cho phép), Count (0 / 1 / nhiều), Token (hợp lệ / hết hạn / không có), Data Exposure (mật khẩu bị lộ / không lộ).
- **Boundary Coverage:** 100% — BVA cho số lượng user (0, 1, 50+) và BVA cho user_id (0, 1, 2, 999999, "abc").
- **Positive Test Cases:** TC-001, TC-002, TC-006, TC-007, TC-011, TC-012, TC-013, TC-017, TC-018, TC-019, TC-020 (11 test cases).
- **Negative Test Cases:** TC-003, TC-004, TC-008, TC-009, TC-010, TC-014, TC-015, TC-016 (8 test cases).
- **Security Test Cases:** TC-002, TC-015, TC-019 (3 test cases tập trung bảo mật).
- **Tổng số test case:** 20.
