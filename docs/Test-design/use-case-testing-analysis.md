# Báo cáo Phân tích Use Case Testing

## FR-03: Quên mật khẩu & Đặt lại mật khẩu

---

# Requirement Summary

**Chức năng:** Quên mật khẩu & Đặt lại mật khẩu (2 bước)

**Requirement ID:** FR-03

**Module:** Authentication & Authorization

**Actor:** Guest (Người dùng chưa đăng nhập)

**Secondary Actor:** Email Service (trong môi trường thực gửi qua Email; trong môi trường demo: hiển thị trực tiếp trên màn hình)

**Goal:** Khôi phục quyền truy cập tài khoản khi người dùng quên mật khẩu

**Scope:** Hệ thống EShop (Frontend Web, Backend API)

**Preconditions:**
1. Người dùng chưa đăng nhập.
2. Tài khoản email của người dùng đã được đăng ký và tồn tại trong hệ thống.
3. Người dùng ở màn hình Quên mật khẩu (Bước 1).

**Trigger:** Người dùng nhập email và nhấn nút gửi yêu cầu OTP (Bước 1).

**Main Flow:**
1. (Bước 1) Người dùng nhập địa chỉ Email đã đăng ký.
2. Hệ thống sinh mã OTP 6 chữ số ngẫu nhiên và gửi qua Email (trong demo: hiển thị trực tiếp trên màn hình).
3. Giao diện hiển thị chỉ báo bước (Step Indicator) "Bước 1 / 2" và nút Quay lại đăng nhập.
4. (Bước 2) Người dùng nhập OTP, Mật khẩu mới, và Xác nhận mật khẩu mới.
5. Hệ thống xác minh OTP và các điều kiện mật khẩu mới.
6. Hệ thống cập nhật mật khẩu mới thành công và chuyển hướng người dùng về màn hình đăng nhập.

**Alternative Flows:**
- AF-01: Quay lại đăng nhập từ Bước 1.

**Exception Flows:**
- EF-01: Email chưa đăng ký trong hệ thống.
- EF-02: OTP không hợp lệ (sai mã).
- EF-03: OTP dùng cho email khác (cross-email).
- EF-04: Mật khẩu mới không đủ mạnh.
- EF-05: Mật khẩu mới và Xác nhận mật khẩu mới không khớp.

**Postconditions:**
- Thành công: Mật khẩu được cập nhật; người dùng có thể đăng nhập bằng mật khẩu mới.
- Thất bại: Mật khẩu cũ được giữ nguyên; hệ thống hiển thị thông báo lỗi phù hợp trên màn hình hiện tại.

**Business Rules:**
- BR-01: Mã OTP phải là 6 chữ số ngẫu nhiên.
- BR-02: OTP chỉ hợp lệ cho email đã yêu cầu, không thể dùng cho email khác.
- BR-03: Mật khẩu mới phải tuân thủ điều kiện mạnh như FR-01: tối thiểu 8 ký tự, có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số, và 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`).
- BR-04: Hai trường mật khẩu mới và xác nhận mật khẩu mới phải khớp nhau.
- BR-05: Giao diện phải hiển thị chỉ báo bước (Step Indicator) - ví dụ: "Bước 1 / 2" và "Bước 2 / 2".
- BR-06: Phải có nút "Quay lại đăng nhập" ở Bước 1.
- BR-07: OTP phải đủ entropy (tối thiểu 6 chữ số), có thời hạn và vô hiệu hóa sau khi dùng (SEC-07).

**Expected Results:**
- Gửi OTP thành công cho email hợp lệ và chuyển sang Bước 2.
- Từ chối gửi OTP với email không tồn tại.
- Đặt lại mật khẩu thành công khi OTP khớp và mật khẩu mới hợp lệ.
- Từ chối đổi mật khẩu khi OTP sai, OTP chéo email, mật khẩu mới yếu, hoặc mật khẩu xác nhận không khớp.

**Missing Rules:** Đặc tả không định nghĩa thời gian hết hạn OTP cụ thể (chỉ ghi "có thời hạn").

---

# Actor Identification

## Actors

| Actor ID | Actor | Type | Description |
| -------- | ----- | ---- | ----------- |
| ACT-01 | Guest (Unauthenticated User) | Primary Actor | Người dùng chưa đăng nhập thực hiện quy trình khôi phục mật khẩu |
| ACT-02 | Email Service | Secondary Actor | Hệ thống phụ gửi mã OTP qua email (hoặc hiển thị trực tiếp trong demo) |

---

# Use Case Identification

## Use Cases

| Use Case ID | Use Case | Actor | Goal | Priority |
| ----------- | -------- | ----- | ---- | -------- |
| UC-01 | Yêu cầu OTP Đặt lại mật khẩu (Bước 1) | Guest | Nhận mã OTP để bắt đầu quy trình đặt lại mật khẩu | High |
| UC-02 | Đặt lại mật khẩu bằng OTP (Bước 2) | Guest | Cập nhật mật khẩu mới bằng cách nhập OTP hợp lệ và mật khẩu mới | High |
| UC-03 | Quay lại đăng nhập từ màn hình Quên mật khẩu | Guest | Hủy quy trình đặt lại mật khẩu và quay về đăng nhập | Medium |

---

# Precondition, Trigger, and Postcondition Identification

## Use Case Conditions

| Use Case ID | Precondition | Trigger | Success Postcondition | Failure Postcondition |
| ----------- | ------------ | ------- | --------------------- | --------------------- |
| UC-01 | Khách hàng chưa đăng nhập và đang ở màn hình Quên mật khẩu Bước 1 | Nhập email và bấm nút lấy OTP | OTP được sinh và hiển thị; UI chuyển sang Bước 2/2 | Hiển thị lỗi; không sinh OTP; người dùng vẫn ở Bước 1 |
| UC-02 | Có mã OTP hợp lệ được sinh; người dùng đang ở Bước 2 | Nhập OTP, mật khẩu mới, xác nhận và bấm đặt lại | Mật khẩu được cập nhật; người dùng có thể đăng nhập bằng mật khẩu mới | Hiển thị lỗi; mật khẩu không đổi; hệ thống giữ nguyên ở Bước 2 |
| UC-03 | Người dùng ở màn hình Bước 1 của Quên mật khẩu | Bấm nút "Quay lại đăng nhập" | Hệ thống chuyển hướng người dùng về màn hình đăng nhập | Đặc tả không định nghĩa quy tắc này. |

---

# Main Flow Identification

## Main Flow

| Use Case ID | Step ID | Actor / System | Step Description | Expected Result |
| ----------- | ------- | -------------- | ---------------- | --------------- |
| UC-01 | MF-01 | Actor | Truy cập màn hình Quên mật khẩu | Giao diện Bước 1/2 hiển thị với chỉ báo bước "Bước 1 / 2" và nút Quay lại đăng nhập |
| UC-01 | MF-02 | Actor | Nhập địa chỉ email đã đăng ký (`test@eshop.com`) | Trường email được điền |
| UC-01 | MF-03 | Actor | Nhấn nút "Lấy mã OTP" | Request gửi lên backend |
| UC-01 | MF-04 | System | Xác minh email tồn tại và sinh OTP | Email tồn tại trong hệ thống |
| UC-01 | MF-05 | System | Gửi/hiển thị OTP 6 chữ số và chuyển giao diện | OTP hiển thị trên màn hình; UI chuyển sang Bước 2/2 |
| UC-02 | MF-06 | Actor | Nhập mã OTP hợp lệ nhận được | Trường OTP được điền |
| UC-02 | MF-07 | Actor | Nhập Mật khẩu mới mạnh và Xác nhận mật khẩu mới | Hai trường mật khẩu được điền trùng khớp |
| UC-02 | MF-08 | Actor | Nhấn nút "Đặt lại mật khẩu" | Request gửi lên backend |
| UC-02 | MF-09 | System | Xác minh OTP hợp lệ và mật khẩu thỏa mãn | OTP và mật khẩu hợp lệ |
| UC-02 | MF-10 | System | Cập nhật mật khẩu trong CSDL và báo thành công | Mật khẩu được đổi thành công; thông báo hiển thị; chuyển sang đăng nhập |

---

# Alternative Flow Identification

## Alternative Flows

| Flow ID | Use Case ID | Start Step | Condition | Flow Steps | Expected Result |
| ------- | ----------- | ---------- | --------- | ---------- | --------------- |
| AF-01 | UC-01 | MF-01 | Người dùng không muốn tiếp tục khôi phục mật khẩu | Người dùng nhấn nút "Quay lại đăng nhập" | Hệ thống đóng quy trình quên mật khẩu và quay về trang đăng nhập |

---

# Exception Flow Identification

## Exception Flows

| Flow ID | Use Case ID | Start Step | Exception Condition | Flow Steps | Expected Result |
| ------- | ----------- | ---------- | ------------------- | ---------- | --------------- |
| EF-01 | UC-01 | MF-04 | Email nhập vào không tồn tại trong hệ thống | Hệ thống từ chối yêu cầu và báo lỗi | Hiển thị thông báo email không tồn tại; không sinh OTP; giữ nguyên Bước 1 |
| EF-02 | UC-02 | MF-09 | Người dùng nhập sai OTP | Hệ thống từ chối đổi mật khẩu | Hiển thị lỗi OTP không đúng; mật khẩu không đổi; giữ nguyên Bước 2 |
| EF-03 | UC-02 | MF-09 | Người dùng nhập OTP thuộc về email khác | Hệ thống từ chối đổi mật khẩu | Hiển thị lỗi OTP không đúng; mật khẩu không đổi; giữ nguyên Bước 2 |
| EF-04 | UC-02 | MF-09 | Mật khẩu mới nhập vào không đủ mạnh theo FR-01 | Hệ thống từ chối đổi mật khẩu | Hiển thị lỗi mật khẩu yếu; mật khẩu không đổi; giữ nguyên Bước 2 |
| EF-05 | UC-02 | MF-09 | Xác nhận mật khẩu mới không khớp mật khẩu mới | Hệ thống từ chối đổi mật khẩu | Hiển thị lỗi không khớp mật khẩu; mật khẩu không đổi; giữ nguyên Bước 2 |

---

# Use Case Scenario Table

## Use Case Scenario Table

| Scenario ID | Use Case ID | Actor | Flow Type | Flow ID | Scenario Description | Expected Result | Risk |
| ----------- | ----------- | ----- | --------- | ------- | -------------------- | --------------- | ---- |
| SC-UC01-001 | UC-01 | Guest | Main Flow | MF | Khôi phục mật khẩu thành công bằng OTP hợp lệ và mật khẩu mạnh | Mật khẩu được cập nhật thành công | High |
| SC-UC01-002 | UC-01 | Guest | Alternative Flow | AF-01 | Nhấn nút quay lại từ Bước 1 | Quay về màn hình đăng nhập | Medium |
| SC-UC01-003 | UC-01 | Guest | Exception Flow | EF-01 | Gửi OTP với email chưa đăng ký | Từ chối, báo lỗi email không tồn tại | High |
| SC-UC02-001 | UC-02 | Guest | Exception Flow | EF-02 | Đặt lại mật khẩu với OTP sai | Từ chối, báo lỗi OTP không đúng | High |
| SC-UC02-002 | UC-02 | Guest | Exception Flow | EF-03 | Đặt lại mật khẩu dùng OTP của email khác | Từ chối, báo lỗi OTP không đúng | High |
| SC-UC02-003 | UC-02 | Guest | Exception Flow | EF-04 | Đặt lại mật khẩu với mật khẩu mới yếu | Từ chối, báo lỗi mật khẩu yếu | High |
| SC-UC02-004 | UC-02 | Guest | Exception Flow | EF-05 | Đặt lại mật khẩu với mật khẩu xác nhận không khớp | Từ chối, báo lỗi mật khẩu không khớp | High |

---

# Actor × Use Case Matrix

## Actor × Use Case Matrix

| Actor / Use Case | UC-01 (Lấy OTP) | UC-02 (Đặt lại mật khẩu) | UC-03 (Quay lại đăng nhập) |
| ---------------- | --------------- | ------------------------- | -------------------------- |
| Guest | Allowed | Allowed | Allowed |
| Email Service | Supporting | Supporting | Not Applicable |

---

# Risk Analysis

## Risk Analysis

| Scenario ID | Risk | Reason |
| ----------- | ---- | ------ |
| SC-UC01-001 | High | Quy trình thành công khôi phục quyền truy cập, ảnh hưởng trực tiếp đến bảo mật xác thực |
| SC-UC01-002 | Medium | Điều hướng UI, rủi ro thấp |
| SC-UC01-003 | High | Email không tồn tại phải được xử lý đúng để tránh làm rò rỉ danh sách tài khoản |
| SC-UC02-001 | High | OTP sai phải bị từ chối nghiêm ngặt để chống Brute Force mã OTP |
| SC-UC02-002 | High | OTP chéo email là lỗi logic phân quyền nghiêm trọng nếu xảy ra |
| SC-UC02-003 | High | Chính sách mật khẩu mạnh (FR-01) phải được tuân thủ để tránh tài khoản dễ bị hack |
| SC-UC02-004 | High | Xác nhận mật khẩu không khớp phải bị chặn để tránh đổi mật khẩu nhầm |

---

# Main Flow Test Mapping

## Main Flow Test Mapping

| Use Case ID | Main Flow | Scenario ID | Test Case |
| ----------- | --------- | ----------- | --------- |
| UC-01 | Steps MF-01 → MF-05 | SC-UC01-001 (Bước 1) | TC-UC-FORGOT-PASSWORD-001 |
| UC-02 | Steps MF-06 → MF-10 | SC-UC01-001 (Bước 2) | TC-UC-FORGOT-PASSWORD-001 |

---

# Alternative Flow Test Mapping

## Alternative Flow Test Mapping

| Flow ID | Use Case ID | Scenario ID | Test Case |
| ------- | ----------- | ----------- | --------- |
| AF-01 | UC-01 | SC-UC01-002 | TC-UC-FORGOT-PASSWORD-002 |

---

# Exception Flow Test Mapping

## Exception Flow Test Mapping

| Flow ID | Use Case ID | Scenario ID | Test Case |
| ------- | ----------- | ----------- | --------- |
| EF-01 | UC-01 | SC-UC01-003 | TC-UC-FORGOT-PASSWORD-003 |
| EF-02 | UC-02 | SC-UC02-001 | TC-UC-FORGOT-PASSWORD-004 |
| EF-03 | UC-02 | SC-UC02-002 | TC-UC-FORGOT-PASSWORD-005 |
| EF-04 | UC-02 | SC-UC02-003 | TC-UC-FORGOT-PASSWORD-006 |
| EF-05 | UC-02 | SC-UC02-004 | TC-UC-FORGOT-PASSWORD-007 |

---

# Precondition Coverage

## Precondition Coverage

| Use Case ID | Precondition | Covered By Test Case |
| ----------- | ------------ | -------------------- |
| UC-01 | Guest đang ở màn hình đăng nhập, email test@eshop.com tồn tại | TC-UC-FORGOT-PASSWORD-001 |
| UC-02 | Có mã OTP hợp lệ; UI đang ở Bước 2 | TC-UC-FORGOT-PASSWORD-001, TC-UC-FORGOT-PASSWORD-004, TC-UC-FORGOT-PASSWORD-005, TC-UC-FORGOT-PASSWORD-006, TC-UC-FORGOT-PASSWORD-007 |
| UC-03 | Guest đang ở màn hình Quên mật khẩu Bước 1 | TC-UC-FORGOT-PASSWORD-002 |

---

# Postcondition Coverage

## Postcondition Coverage

| Use Case ID | Postcondition | Covered By Test Case |
| ----------- | ------------- | -------------------- |
| UC-01 | OTP 6 số được tạo, hiển thị; UI chuyển sang Bước 2/2 | TC-UC-FORGOT-PASSWORD-001 |
| UC-01 | Báo lỗi email không tồn tại; không sinh OTP; giữ nguyên Bước 1 | TC-UC-FORGOT-PASSWORD-003 |
| UC-02 | Đổi mật khẩu thành công và có thể đăng nhập bằng mật khẩu mới | TC-UC-FORGOT-PASSWORD-001 |
| UC-02 | Đổi mật khẩu bị từ chối; giữ nguyên Bước 2; mật khẩu không đổi | TC-UC-FORGOT-PASSWORD-004, TC-UC-FORGOT-PASSWORD-005, TC-UC-FORGOT-PASSWORD-006, TC-UC-FORGOT-PASSWORD-007 |
| UC-03 | Quay về màn hình đăng nhập | TC-UC-FORGOT-PASSWORD-002 |

---

# Actor Coverage

## Actor Coverage

| Actor | Use Case ID | Access | Covered By Test Case |
| ----- | ----------- | ------ | -------------------- |
| Guest | UC-01 | Allowed | TC-UC-FORGOT-PASSWORD-001, TC-UC-FORGOT-PASSWORD-003 |
| Guest | UC-02 | Allowed | TC-UC-FORGOT-PASSWORD-001, TC-UC-FORGOT-PASSWORD-004, TC-UC-FORGOT-PASSWORD-005, TC-UC-FORGOT-PASSWORD-006, TC-UC-FORGOT-PASSWORD-007 |
| Guest | UC-03 | Allowed | TC-UC-FORGOT-PASSWORD-002 |

---

# Business Rule Coverage

## Business Rule Coverage

| Business Rule ID | Business Rule | Scenario ID | Covered By Test Case |
| ---------------- | ------------- | ----------- | -------------------- |
| BR-01 | Mã OTP phải là 6 chữ số ngẫu nhiên | SC-UC01-001 | TC-UC-FORGOT-PASSWORD-001 |
| BR-02 | OTP chỉ hợp lệ cho email đã yêu cầu | SC-UC02-002 | TC-UC-FORGOT-PASSWORD-005 |
| BR-03 | Mật khẩu mới mạnh theo quy chuẩn FR-01 | SC-UC01-001, SC-UC02-003 | TC-UC-FORGOT-PASSWORD-001, TC-UC-FORGOT-PASSWORD-006 |
| BR-04 | Hai trường mật khẩu phải khớp nhau | SC-UC01-001, SC-UC02-004 | TC-UC-FORGOT-PASSWORD-001, TC-UC-FORGOT-PASSWORD-007 |
| BR-05 | Giao diện phải hiển thị Step Indicator "Bước 1 / 2" | SC-UC01-001 | TC-UC-FORGOT-PASSWORD-001 |
| BR-06 | Phải có nút "Quay lại đăng nhập" ở Bước 1 | SC-UC01-002 | TC-UC-FORGOT-PASSWORD-002 |
| BR-07 | OTP có thời hạn và vô hiệu hóa sau khi dùng (SEC-07) | SC-UC01-001 | TC-UC-FORGOT-PASSWORD-001 |

---

# Final Test Case Mapping

## Final Test Case Mapping

| Test Case ID | Use Case ID | Actor | Flow Type | Flow ID | Scenario ID | Status | Coverage Type |
| ------------ | ----------- | ----- | --------- | ------- | ----------- | ------ | ------------- |
| TC-UC-FORGOT-PASSWORD-001 | UC-01, UC-02 | Guest | Main Flow | MF | SC-UC01-001 | **FAIL** | Main Flow |
| TC-UC-FORGOT-PASSWORD-002 | UC-03 | Guest | Alternative Flow | AF-01 | SC-UC01-002 | **FAIL** | Alternative Flow |
| TC-UC-FORGOT-PASSWORD-003 | UC-01 | Guest | Exception Flow | EF-01 | SC-UC01-003 | **PASS** | Exception Flow |
| TC-UC-FORGOT-PASSWORD-004 | UC-02 | Guest | Exception Flow | EF-02 | SC-UC02-001 | **FAIL** | Exception Flow |
| TC-UC-FORGOT-PASSWORD-005 | UC-02 | Guest | Exception Flow | EF-03 | SC-UC02-002 | **FAIL** | Exception Flow |
| TC-UC-FORGOT-PASSWORD-006 | UC-02 | Guest | Exception Flow | EF-04 | SC-UC02-003 | **PASS** | Exception Flow |
| TC-UC-FORGOT-PASSWORD-007 | UC-02 | Guest | Exception Flow | EF-05 | SC-UC02-004 | **FAIL** | Exception Flow |

---

# Test Case Count Summary

## Test Case Count Summary

| Test Group | Count |
| ---------- | ----- |
| Main Flow Test Cases | 1 |
| Alternative Flow Test Cases | 1 |
| Exception Flow Test Cases | 5 |
| Additional Precondition Test Cases | 0 |
| Additional Postcondition Test Cases | 0 |
| Additional Actor Coverage Test Cases | 0 |
| Additional Business Rule Test Cases | 0 |
| **Total Test Cases** | **7** |

---

# Coverage Summary

| Coverage Type | Required | Covered | Coverage |
| ------------- | -------- | ------- | -------- |
| Use Case Coverage | 3 Use Cases | 3 Use Cases | 100% |
| Main Flow Coverage | 1 Main Flow | 1 Main Flow | 100% |
| Alternative Flow Coverage | 1 Alternative Flow | 1 Alternative Flow | 100% |
| Exception Flow Coverage | 5 Exception Flows | 5 Exception Flows | 100% |
| Actor Coverage | 1 Actor | 1 Actor | 100% |
| Precondition Coverage | 3 Preconditions | 3 Preconditions | 100% |
| Postcondition Coverage | 5 Postconditions | 5 Postconditions | 100% |
| Business Rule Coverage | 7 Business Rules | 7 Business Rules | 100% |

> **Giải thích:** Đạt 100% Coverage về mặt thiết kế test case, nhưng khi thực thi thực tế, có **5/7** test case bị **FAIL** do các lỗi nghiêm trọng về cả UI (thiếu trường nhập liệu, thiếu chỉ báo bước, thiếu nút quay lại) lẫn Logic (validator regex bị sai lệch hoàn toàn, OTP chỉ sinh ra 4 chữ số thay vì 6 chữ số).
