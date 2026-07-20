# Báo cáo Phân tích State Transition Testing — FR-03

Tài liệu này trình bày chi tiết quy trình áp dụng kỹ thuật kiểm thử **State Transition Testing** cho chức năng **FR-03: Quên mật khẩu & Đặt lại mật khẩu** của hệ thống EShop.

---

## # Requirement Summary

**Chức năng:** Quên mật khẩu & Đặt lại mật khẩu (2 bước)

**Requirement ID:** FR-03

**Module:** Quản lý Tài khoản (Authentication & Authorization)

**Mô tả:**
- **Bước 1 — Lấy mã OTP:** Người dùng nhập địa chỉ Email đã đăng ký. Hệ thống sinh mã OTP **6 chữ số ngẫu nhiên** và hiển thị trực tiếp trên màn hình (môi trường demo). Giao diện phải hiển thị **chỉ báo bước** "Bước 1 / 2" và có nút **Quay lại đăng nhập**.
- **Bước 2 — Đặt lại mật khẩu:** Người dùng nhập OTP, Mật khẩu mới, và Xác nhận mật khẩu mới. Mật khẩu mới phải tuân thủ điều kiện FR-01. Hai trường mật khẩu phải khớp nhau. OTP chỉ hợp lệ cho email đã yêu cầu.

**User Roles:** Người dùng chưa đăng nhập (Guest / Unauthenticated User)

**Initial State:** S0 — Trang đăng nhập (Login Page)

**States:**
- S0: Trang đăng nhập (Initial)
- S1: Màn hình Bước 1/2 — Yêu cầu OTP (Intermediate)
- S2: Màn hình Bước 2/2 — Đặt lại mật khẩu (Intermediate)
- S3: Đặt lại mật khẩu thành công (Final)

**Final States:** S3

**Actions / Events:**
- A1: Chọn "Quên mật khẩu"
- A2: Nhập email đã đăng ký & gửi yêu cầu OTP
- A3: Nhập email chưa đăng ký & gửi yêu cầu OTP
- A4: Chọn "Quay lại đăng nhập"
- A5: Gửi OTP đúng + Mật khẩu mạnh hợp lệ + Xác nhận khớp
- A6: Gửi OTP sai (không đúng mã)
- A7: Gửi mật khẩu mới không hợp lệ (không đủ mạnh theo FR-01)
- A8: Gửi xác nhận mật khẩu không khớp với mật khẩu mới
- A9: Gửi OTP của email khác (OTP không khớp với phiên hiện tại)

**Business Rules:**
- OTP gồm 6 chữ số ngẫu nhiên, sinh cho từng email riêng biệt.
- Mật khẩu mới phải đáp ứng: tối thiểu 8 ký tự, 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 ký tự đặc biệt.
- Xác nhận mật khẩu phải khớp với mật khẩu mới.
- OTP chỉ hợp lệ cho email đã yêu cầu, không thể dùng cho email khác.
- Giao diện phải hiển thị chỉ báo bước "Bước X / 2".

**Expected Results:**
- Chuyển tiếp đúng giao diện qua từng bước.
- Cập nhật mật khẩu mới thành công khi nhập đúng thông tin.
- Báo lỗi và giữ nguyên trạng thái khi nhập sai OTP hoặc mật khẩu không hợp lệ.

**Missing Rules:**
- Đặc tả không định nghĩa thông báo lỗi cụ thể khi nhập email chưa đăng ký ở Bước 1.
- Đặc tả không định nghĩa hành vi hệ thống sau khi người dùng đặt lại mật khẩu thành công (tự chuyển hướng về trang đăng nhập hay hiển thị nút để người dùng tự bấm).
- Đặc tả không định nghĩa hành vi khi tái sử dụng OTP đã dùng.

---

## # State Identification

| ID | State | Type | Description |
| -- | ----- | ---- | ----------- |
| **S0** | Login Page (Trang đăng nhập) | Initial | Trạng thái bắt đầu. Người dùng chưa đăng nhập. |
| **S1** | Step 1 - Request OTP (Màn hình Yêu cầu OTP) | Intermediate | Màn hình Bước 1/2. Người dùng nhập email để nhận OTP. Hiển thị chỉ báo "Bước 1 / 2" và nút "Quay lại đăng nhập". |
| **S2** | Step 2 - Reset Password (Màn hình Đặt lại mật khẩu) | Intermediate | Màn hình Bước 2/2. Người dùng nhập OTP, mật khẩu mới, xác nhận mật khẩu. |
| **S3** | Password Reset Completed (Đặt lại mật khẩu thành công) | Final | Workflow hoàn tất. Mật khẩu đã được cập nhật thành công. |

**Tổng số States:** 4

---

## # Action / Event Identification

| ID | Action / Event | Description |
| -- | -------------- | ----------- |
| **A1** | Chọn "Quên mật khẩu" | Người dùng nhấn liên kết/nút quên mật khẩu tại trang đăng nhập (S0). |
| **A2** | Nhập email đã đăng ký & gửi yêu cầu OTP | Người dùng cung cấp email hợp lệ đã đăng ký và nhấn gửi yêu cầu OTP. |
| **A3** | Nhập email chưa đăng ký & gửi yêu cầu OTP | Người dùng nhập email chưa tồn tại trong hệ thống và nhấn gửi. |
| **A4** | Chọn "Quay lại đăng nhập" | Người dùng nhấn nút quay lại trang đăng nhập (có ở Bước 1). |
| **A5** | Gửi OTP đúng + Mật khẩu mạnh hợp lệ + Xác nhận khớp | Người dùng điền đầy đủ thông tin hợp lệ và nhấn xác nhận đặt lại mật khẩu. |
| **A6** | Gửi OTP sai | Người dùng nhập mã OTP sai (không khớp với mã đã sinh). |
| **A7** | Gửi mật khẩu mới không hợp lệ (yếu) | Mật khẩu mới không thỏa mãn tiêu chuẩn độ mạnh theo FR-01. |
| **A8** | Gửi xác nhận mật khẩu không khớp | Trường xác nhận mật khẩu không trùng với mật khẩu mới. |
| **A9** | Gửi OTP của email khác | Sử dụng mã OTP hợp lệ nhưng được sinh ra cho một email khác. |

**Tổng số Actions:** 9

---

## # State Transition Table using States × Actions

**Số dòng bảng = 4 States × 9 Actions = 36 dòng**

| Row | Current State | Action / Event | Valid / Invalid | Next State | Result / Expected Behavior |
| --- | ------------- | -------------- | --------------- | ---------- | -------------------------- |
| 1 | S0 | A1 | **Valid** | S1 | Chuyển sang màn hình Bước 1/2 (S1). |
| 2 | S0 | A2 | Invalid | S0 | Từ chối Action. S0 không có form gửi OTP. Giữ nguyên S0. |
| 3 | S0 | A3 | Invalid | S0 | Từ chối Action. Giữ nguyên S0. |
| 4 | S0 | A4 | Invalid | S0 | Từ chối Action. Đã ở trang đăng nhập rồi. Giữ nguyên S0. |
| 5 | S0 | A5 | Invalid | S0 | Từ chối Action. Không có form xác nhận mật khẩu ở S0. Giữ nguyên S0. |
| 6 | S0 | A6 | Invalid | S0 | Từ chối Action. Giữ nguyên S0. |
| 7 | S0 | A7 | Invalid | S0 | Từ chối Action. Giữ nguyên S0. |
| 8 | S0 | A8 | Invalid | S0 | Từ chối Action. Giữ nguyên S0. |
| 9 | S0 | A9 | Invalid | S0 | Từ chối Action. Giữ nguyên S0. |
| 10 | S1 | A1 | Invalid | S1 | Từ chối Action. Đang ở Bước 1, không thể bấm "Quên mật khẩu" lại. Giữ nguyên S1. |
| 11 | S1 | A2 | **Valid** | S2 | Hệ thống sinh OTP 6 chữ số và chuyển sang màn hình Bước 2/2 (S2). |
| 12 | S1 | A3 | **Invalid** | S1 | Từ chối Action hoặc báo lỗi. Không sinh OTP. Giữ nguyên S1. *"Đặc tả không định nghĩa quy tắc này."* |
| 13 | S1 | A4 | **Valid** | S0 | Điều hướng người dùng quay về trang đăng nhập (S0). |
| 14 | S1 | A5 | Invalid | S1 | Từ chối Action. Chưa ở Bước 2. Giữ nguyên S1. |
| 15 | S1 | A6 | Invalid | S1 | Từ chối Action. Chưa ở Bước 2. Giữ nguyên S1. |
| 16 | S1 | A7 | Invalid | S1 | Từ chối Action. Chưa ở Bước 2. Giữ nguyên S1. |
| 17 | S1 | A8 | Invalid | S1 | Từ chối Action. Chưa ở Bước 2. Giữ nguyên S1. |
| 18 | S1 | A9 | Invalid | S1 | Từ chối Action. Chưa ở Bước 2. Giữ nguyên S1. |
| 19 | S2 | A1 | Invalid | S2 | Từ chối Action. Giữ nguyên S2. |
| 20 | S2 | A2 | Invalid | S2 | Từ chối Action. Không thể gửi yêu cầu OTP mới từ Bước 2. Giữ nguyên S2. *"Đặc tả không định nghĩa quy tắc này."* |
| 21 | S2 | A3 | Invalid | S2 | Từ chối Action. Giữ nguyên S2. |
| 22 | S2 | A4 | Invalid | S2 | Từ chối Action. Đặc tả không định nghĩa nút "Quay lại" ở Bước 2. Giữ nguyên S2. *"Đặc tả không định nghĩa quy tắc này."* |
| 23 | S2 | A5 | **Valid** | S3 | Đặt lại mật khẩu thành công. Workflow kết thúc (S3). |
| 24 | S2 | A6 | **Invalid** | S2 | Báo lỗi OTP không hợp lệ. Giữ nguyên S2. |
| 25 | S2 | A7 | **Invalid** | S2 | Báo lỗi mật khẩu không đủ mạnh. Giữ nguyên S2. |
| 26 | S2 | A8 | **Invalid** | S2 | Báo lỗi xác nhận mật khẩu không khớp. Giữ nguyên S2. |
| 27 | S2 | A9 | **Invalid** | S2 | Báo lỗi OTP không hợp lệ (không khớp với email). Giữ nguyên S2. |
| 28 | S3 | A1 | Invalid | S3 | Từ chối Action. Workflow đã kết thúc. Giữ nguyên S3. |
| 29 | S3 | A2 | Invalid | S3 | Từ chối Action. Giữ nguyên S3. |
| 30 | S3 | A3 | Invalid | S3 | Từ chối Action. Giữ nguyên S3. |
| 31 | S3 | A4 | Invalid | S3 | Từ chối Action. Giữ nguyên S3. *"Đặc tả không định nghĩa quy tắc này."* |
| 32 | S3 | A5 | Invalid | S3 | Từ chối Action. OTP cũ đã hết hiệu lực. Giữ nguyên S3. *"Đặc tả không định nghĩa quy tắc này."* |
| 33 | S3 | A6 | Invalid | S3 | Từ chối Action. Giữ nguyên S3. |
| 34 | S3 | A7 | Invalid | S3 | Từ chối Action. Giữ nguyên S3. |
| 35 | S3 | A8 | Invalid | S3 | Từ chối Action. Giữ nguyên S3. |
| 36 | S3 | A9 | Invalid | S3 | Từ chối Action. Giữ nguyên S3. |

---

## # Transition List

| Transition ID | Current State | Action / Event | Next State | Valid / Invalid | Result |
| ------------- | ------------- | -------------- | ---------- | --------------- | ------ |
| **T1** | S0 | A1 | S1 | Valid | Chuyển sang màn hình Bước 1/2 |
| **T2** | S1 | A2 | S2 | Valid | Sinh OTP, chuyển sang màn hình Bước 2/2 |
| **T3** | S1 | A4 | S0 | Valid | Quay lại trang đăng nhập |
| **T4** | S2 | A5 | S3 | Valid | Đặt lại mật khẩu thành công |
| **T5** | S1 | A3 | S1 | Invalid | Từ chối — email chưa đăng ký, không sinh OTP |
| **T6** | S2 | A6 | S2 | Invalid | Từ chối — OTP sai |
| **T7** | S2 | A7 | S2 | Invalid | Từ chối — mật khẩu mới không đủ mạnh |
| **T8** | S2 | A8 | S2 | Invalid | Từ chối — xác nhận mật khẩu không khớp |
| **T9** | S2 | A9 | S2 | Invalid | Từ chối — OTP không khớp với email |

**Tổng số Valid Transitions: 4 (T1, T2, T3, T4)**
**Tổng số Invalid Transitions (có định nghĩa hành vi): 5 (T5, T6, T7, T8, T9)**

---

## # State Transition Validation

### 1. Completeness (Tính đầy đủ)
- ✅ Tất cả 4 States đã được đưa vào bảng.
- ✅ Tất cả 9 Actions đã được kiểm tra với mỗi State (36 dòng đầy đủ).
- ✅ Tất cả 4 Valid Transitions đã được xác định.
- ✅ Tất cả 5 Invalid Transitions có định nghĩa hành vi đã được liệt kê. Các ô "Đặc tả không định nghĩa quy tắc này" đã được đánh dấu rõ ràng.
- ✅ Final State S3 đã được xác định.

### 2. Reachability (Khả năng tiếp cận)
- ✅ S1: Đạt được từ S0 qua T1.
- ✅ S2: Đạt được từ S1 qua T2.
- ✅ S3: Đạt được từ S2 qua T4.
- ✅ Không có State nào bị cô lập.

### 3. Dead-end State (Trạng thái cụt)
- ✅ S3 là Final State — đây là trạng thái cụt hợp lệ và mong đợi của workflow.
- ✅ Không có trạng thái trung gian nào bị rơi vào dead-end bất ngờ.

### 4. Consistency (Tính nhất quán)
- ✅ Không có Transition nào trùng lặp có kết quả mâu thuẫn.
- ✅ Mỗi cặp (Current State + Action) chỉ dẫn đến đúng một Next State duy nhất.

### 5. Missing Rule Check
- ⚠️ Đặc tả không định nghĩa thông báo lỗi cụ thể khi nhập email chưa đăng ký ở Bước 1 (T5).
- ⚠️ Đặc tả không định nghĩa nút "Gửi lại OTP" hoặc "Quay lại Bước 1" ở màn hình Bước 2 (Row 22).
- ⚠️ Đặc tả không định nghĩa hành vi sau khi đặt lại mật khẩu thành công tại S3 (tự chuyển hướng hay hiển thị nút).
- ⚠️ Đặc tả không định nghĩa hành vi khi tái sử dụng OTP cũ sau khi đặt lại thành công (Row 32).

---

## # Risk Analysis

| Transition ID | Risk | Reason |
| ------------- | ---- | ------ |
| **T1** (S0 → S1) | Low | Điều hướng UI từ trang đăng nhập sang trang quên mật khẩu. |
| **T2** (S1 → S2) | Medium | Hệ thống sinh mã OTP ngẫu nhiên và gửi/hiển thị. Liên quan đến luồng xác thực. |
| **T3** (S1 → S0) | Low | Điều hướng UI quay lại trang đăng nhập. |
| **T4** (S2 → S3) | High | Đặt lại mật khẩu thành công — thay đổi thông tin xác thực nhạy cảm. |
| **T5** (S1 → S1) | Medium | Email chưa đăng ký — hệ thống phải từ chối đúng cách, tránh rò rỉ thông tin. |
| **T6** (S2 → S2) | High | OTP sai — cơ chế bảo vệ chống lại brute-force OTP. |
| **T7** (S2 → S2) | Medium | Mật khẩu yếu — phải reject để đảm bảo người dùng đặt mật khẩu đủ an toàn. |
| **T8** (S2 → S2) | Medium | Xác nhận mật khẩu không khớp — phòng ngừa người dùng nhập nhầm. |
| **T9** (S2 → S2) | High | OTP của email khác — nguy cơ tấn công chiếm quyền reset mật khẩu của email khác. |

---

## # Dedicated Valid Transition Test Mapping

**Kiểm tra:** Tổng Valid Transitions = 4, Dedicated Test Cases = 4 → ✅ Hợp lệ (X = Y = 4)

| Transition ID | Current State | Action / Event | Next State | Dedicated Test Case |
| ------------- | ------------- | -------------- | ---------- | ------------------- |
| **T1** | S0 | A1 (Chọn "Quên mật khẩu") | S1 | TC-ST-FORGOT-PASSWORD-001 |
| **T2** | S1 | A2 (Nhập email đúng & gửi OTP) | S2 | TC-ST-FORGOT-PASSWORD-002 |
| **T3** | S1 | A4 (Chọn "Quay lại đăng nhập") | S0 | TC-ST-FORGOT-PASSWORD-003 |
| **T4** | S2 | A5 (Gửi OTP+mật khẩu hợp lệ) | S3 | TC-ST-FORGOT-PASSWORD-004 |

---

## # Invalid Transition Test Mapping

| Transition ID | Current State | Action / Event | Expected Behavior | Test Case |
| ------------- | ------------- | -------------- | ----------------- | --------- |
| **T5** | S1 | A3 (Email chưa đăng ký) | Từ chối Action, không sinh OTP, giữ S1. *"Đặc tả không định nghĩa thông báo lỗi cụ thể."* | TC-ST-FORGOT-PASSWORD-005 |
| **T6** | S2 | A6 (OTP sai) | Báo lỗi OTP không hợp lệ, giữ S2. | TC-ST-FORGOT-PASSWORD-006 |
| **T7** | S2 | A7 (Mật khẩu yếu) | Báo lỗi mật khẩu không đủ mạnh, giữ S2. | TC-ST-FORGOT-PASSWORD-007 |
| **T8** | S2 | A8 (Xác nhận không khớp) | Báo lỗi xác nhận mật khẩu không khớp, giữ S2. | TC-ST-FORGOT-PASSWORD-008 |
| **T9** | S2 | A9 (OTP của email khác) | Báo lỗi OTP không hợp lệ (không khớp với email), giữ S2. | TC-ST-FORGOT-PASSWORD-009 |

---

## # State Coverage

**Kiểm tra:** Tổng States = 4, Covered States = 4 → ✅ State Coverage = 100%

| State | Covered By Test Case |
| ----- | -------------------- |
| **S0** | TC-ST-FORGOT-PASSWORD-001, TC-ST-FORGOT-PASSWORD-003, TC-ST-FORGOT-PASSWORD-SW1-001, TC-ST-FORGOT-PASSWORD-SW1-002, TC-ST-FORGOT-PASSWORD-SW1-004, TC-ST-FORGOT-PASSWORD-SW2-001, TC-ST-FORGOT-PASSWORD-SW2-002, TC-ST-FORGOT-PASSWORD-E2E-001, TC-ST-FORGOT-PASSWORD-E2E-002 |
| **S1** | TC-ST-FORGOT-PASSWORD-001, TC-ST-FORGOT-PASSWORD-002, TC-ST-FORGOT-PASSWORD-003, TC-ST-FORGOT-PASSWORD-005, TC-ST-FORGOT-PASSWORD-SW1-001, TC-ST-FORGOT-PASSWORD-SW1-002, TC-ST-FORGOT-PASSWORD-SW1-003, TC-ST-FORGOT-PASSWORD-SW1-004, TC-ST-FORGOT-PASSWORD-SW2-001, TC-ST-FORGOT-PASSWORD-SW2-002, TC-ST-FORGOT-PASSWORD-SW2-003, TC-ST-FORGOT-PASSWORD-SW2-004, TC-ST-FORGOT-PASSWORD-E2E-001, TC-ST-FORGOT-PASSWORD-E2E-002 |
| **S2** | TC-ST-FORGOT-PASSWORD-002, TC-ST-FORGOT-PASSWORD-004, TC-ST-FORGOT-PASSWORD-006, TC-ST-FORGOT-PASSWORD-007, TC-ST-FORGOT-PASSWORD-008, TC-ST-FORGOT-PASSWORD-009, TC-ST-FORGOT-PASSWORD-SW1-001, TC-ST-FORGOT-PASSWORD-SW1-003, TC-ST-FORGOT-PASSWORD-SW2-001, TC-ST-FORGOT-PASSWORD-SW2-003, TC-ST-FORGOT-PASSWORD-E2E-001, TC-ST-FORGOT-PASSWORD-E2E-002 |
| **S3** | TC-ST-FORGOT-PASSWORD-004, TC-ST-FORGOT-PASSWORD-SW1-003, TC-ST-FORGOT-PASSWORD-SW2-001, TC-ST-FORGOT-PASSWORD-E2E-001, TC-ST-FORGOT-PASSWORD-E2E-002, TC-ST-FORGOT-PASSWORD-FINAL-001 |

---

## # Transition Coverage

**Kiểm tra:** Tổng Transitions có thể kiểm thử = 9 (4 Valid + 5 Invalid có định nghĩa), Covered = 9 → ✅ Transition Coverage = 100%

| Transition ID | Valid / Invalid | Covered By Test Case |
| ------------- | --------------- | -------------------- |
| **T1** | Valid | TC-ST-FORGOT-PASSWORD-001 (Dedicated) + SW1-001, SW1-002, SW1-004, SW2-001, SW2-002, SW2-003, SW2-004, E2E-001, E2E-002 |
| **T2** | Valid | TC-ST-FORGOT-PASSWORD-002 (Dedicated) + SW1-001, SW1-003, SW2-001, SW2-003, E2E-001, E2E-002 |
| **T3** | Valid | TC-ST-FORGOT-PASSWORD-003 (Dedicated) + SW1-002, SW1-004, SW2-002, SW2-003, SW2-004, E2E-002 |
| **T4** | Valid | TC-ST-FORGOT-PASSWORD-004 (Dedicated) + SW1-003, SW2-001, E2E-001, E2E-002 |
| **T5** | Invalid | TC-ST-FORGOT-PASSWORD-005 |
| **T6** | Invalid | TC-ST-FORGOT-PASSWORD-006 |
| **T7** | Invalid | TC-ST-FORGOT-PASSWORD-007 |
| **T8** | Invalid | TC-ST-FORGOT-PASSWORD-008 |
| **T9** | Invalid | TC-ST-FORGOT-PASSWORD-009 |

---

## # 1-switch Coverage

**Kiểm tra:** Tổng 1-switch sequences = 4, Covered = 4 → ✅ 1-switch Coverage = 100%

| 1-switch ID | Transition Sequence | State Sequence | Covered By Test Case |
| ----------- | ------------------- | -------------- | -------------------- |
| **SW1-001** | T1 → T2 | S0 → S1 → S2 | TC-ST-FORGOT-PASSWORD-SW1-001 |
| **SW1-002** | T1 → T3 | S0 → S1 → S0 | TC-ST-FORGOT-PASSWORD-SW1-002 |
| **SW1-003** | T2 → T4 | S1 → S2 → S3 | TC-ST-FORGOT-PASSWORD-SW1-003 |
| **SW1-004** | T3 → T1 | S1 → S0 → S1 | TC-ST-FORGOT-PASSWORD-SW1-004 |

---

## # n-switch Coverage

**Kiểm tra (n=2):** Tổng 2-switch sequences = 4, Covered = 4 → ✅ n-switch Coverage = 100%

| n-switch ID | n Value | Transition Sequence | State Sequence | Covered By Test Case |
| ----------- | ------- | ------------------- | -------------- | -------------------- |
| **SW2-001** | 2 | T1 → T2 → T4 | S0 → S1 → S2 → S3 | TC-ST-FORGOT-PASSWORD-SW2-001 |
| **SW2-002** | 2 | T1 → T3 → T1 | S0 → S1 → S0 → S1 | TC-ST-FORGOT-PASSWORD-SW2-002 |
| **SW2-003** | 2 | T3 → T1 → T2 | S1 → S0 → S1 → S2 | TC-ST-FORGOT-PASSWORD-SW2-003 |
| **SW2-004** | 2 | T3 → T1 → T3 | S1 → S0 → S1 → S0 | TC-ST-FORGOT-PASSWORD-SW2-004 |

---

## # End-to-End Test Paths

**Kiểm tra:** Tổng E2E paths = 2, Covered = 2 → ✅ E2E Test Coverage = 100%

| E2E ID | Start State | Transition Path | Final State | Covered By Test Case |
| ------ | ----------- | --------------- | ----------- | -------------------- |
| **E2E-001** | S0 | T1 → T2 → T4 | S3 | TC-ST-FORGOT-PASSWORD-E2E-001 |
| **E2E-002** | S0 | T1 → T3 → T1 → T2 → T4 | S3 | TC-ST-FORGOT-PASSWORD-E2E-002 |

---

## # Final State Test

**Kiểm tra:** Tổng Final States = 1 (S3), Covered = 1 → ✅ Final State Test Coverage = 100%

| Final State | Action After Final State | Expected Behavior | Covered By Test Case |
| ----------- | ------------------------ | ----------------- | -------------------- |
| **S3** | Tái sử dụng OTP cũ + Thử đăng nhập bằng mật khẩu cũ và mới | Từ chối OTP cũ; mật khẩu cũ không đăng nhập được; mật khẩu mới đăng nhập thành công | TC-ST-FORGOT-PASSWORD-FINAL-001 |

---

## # Final Test Case Mapping

| Test Case ID | Coverage Type | Covered Transitions | Risk |
| ------------ | ------------- | ------------------- | ---- |
| TC-ST-FORGOT-PASSWORD-001 | Dedicated Valid Transition | T1 | Low |
| TC-ST-FORGOT-PASSWORD-002 | Dedicated Valid Transition | T2 | Medium |
| TC-ST-FORGOT-PASSWORD-003 | Dedicated Valid Transition | T3 | Low |
| TC-ST-FORGOT-PASSWORD-004 | Dedicated Valid Transition | T4 | High |
| TC-ST-FORGOT-PASSWORD-005 | Invalid Transition | T5 | Medium |
| TC-ST-FORGOT-PASSWORD-006 | Invalid Transition | T6 | High |
| TC-ST-FORGOT-PASSWORD-007 | Invalid Transition | T7 | Medium |
| TC-ST-FORGOT-PASSWORD-008 | Invalid Transition | T8 | Medium |
| TC-ST-FORGOT-PASSWORD-009 | Invalid Transition | T9 | High |
| TC-ST-FORGOT-PASSWORD-SW1-001 | 1-switch Coverage | T1 → T2 | Medium |
| TC-ST-FORGOT-PASSWORD-SW1-002 | 1-switch Coverage | T1 → T3 | Low |
| TC-ST-FORGOT-PASSWORD-SW1-003 | 1-switch Coverage | T2 → T4 | High |
| TC-ST-FORGOT-PASSWORD-SW1-004 | 1-switch Coverage | T3 → T1 | Low |
| TC-ST-FORGOT-PASSWORD-SW2-001 | n-switch Coverage (n=2) | T1 → T2 → T4 | High |
| TC-ST-FORGOT-PASSWORD-SW2-002 | n-switch Coverage (n=2) | T1 → T3 → T1 | Low |
| TC-ST-FORGOT-PASSWORD-SW2-003 | n-switch Coverage (n=2) | T3 → T1 → T2 | Medium |
| TC-ST-FORGOT-PASSWORD-SW2-004 | n-switch Coverage (n=2) | T3 → T1 → T3 | Low |
| TC-ST-FORGOT-PASSWORD-E2E-001 | End-to-End Test (Happy Path) | T1 → T2 → T4 | High |
| TC-ST-FORGOT-PASSWORD-E2E-002 | End-to-End Test (Alternative Path) | T1 → T3 → T1 → T2 → T4 | High |
| TC-ST-FORGOT-PASSWORD-FINAL-001 | Final State Test | S3 (post-final) | High |

---

## # Test Case Count Summary

| Test Group | Count |
| ---------- | ----- |
| Dedicated valid Transition Test Cases | 4 |
| Invalid Transition Test Cases | 5 |
| Additional State Coverage Test Cases | 0 |
| 1-switch Test Cases | 4 |
| n-switch Test Cases (n=2) | 4 |
| End-to-End Test Cases | 2 |
| Final State Test Cases | 1 |
| **Total Test Cases** | **20** |

---

## # Coverage Summary

| Coverage Type | Required | Covered | Coverage |
| ------------- | -------- | ------- | -------- |
| State Coverage | 4 States | 4 States | **100%** |
| Transition Coverage | 9 Transitions (4 Valid + 5 Invalid) | 9 Transitions | **100%** |
| Dedicated Valid Transition Coverage | 4 valid Transitions | 4 Dedicated Test Cases | **100%** |
| Invalid Transition Coverage | 5 Invalid Transitions (có định nghĩa hành vi) | 5 Test Cases | **100%** |
| 1-switch Coverage | 4 sequences | 4 sequences | **100%** |
| n-switch Coverage (n=2) | 4 sequences | 4 sequences | **100%** |
| End-to-End Test | 2 paths | 2 paths | **100%** |
| Final State Test | 1 Final State | 1 Final State | **100%** |
