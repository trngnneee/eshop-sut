# 07 — State Transition & N-Switch Testing: FR02 — Đăng nhập & Khóa tài khoản

Tài liệu này thiết kế các kịch bản kiểm thử dựa trên mô hình trạng thái (State Transition Testing) áp dụng kỹ thuật phủ N-Switch (N-Switch Coverage) cho tính năng Đăng nhập & Khóa tài khoản (FR02).

---

## 1. Định nghĩa Trạng thái và Sự kiện (States & Events)

### 1.1. Các trạng thái (States)
Dựa trên đặc tả và mã nguồn hiện tại của SUT, chúng ta định nghĩa các trạng thái của hệ thống/tài khoản như sau:

| State ID | Tên trạng thái | Mô tả chi tiết | Dữ liệu DB liên quan |
|---|---|---|---|
| **Guest** | Chưa đăng nhập | Người dùng là khách vãng lai, chưa được cấp JWT hoặc token không hợp lệ. | N/A |
| **Checking** | Đang kiểm tra đăng nhập | Trạng thái chuyển tiếp khi người dùng gửi yêu cầu login, hệ thống đang xử lý xác thực. | N/A |
| **UnknownEmail** | Email không tồn tại | Trạng thái tạm thời khi email đăng nhập không tìm thấy trong CSDL. | N/A |
| **A0** | Hoạt động (attempts = 0) | Tài khoản không bị khóa, số lần đăng nhập sai là 0. | `login_attempts = 0`, `locked_until = NULL` |
| **A1** | Hoạt động (attempts = 1) | Tài khoản không bị khóa, đã đăng nhập sai 1 lần. | `login_attempts = 1`, `locked_until = NULL` |
| **A2** | Hoạt động (attempts = 2) | Tài khoản không bị khóa, đã đăng nhập sai 2 lần. | `login_attempts = 2`, `locked_until = NULL` |
| **Locked** | Đang bị khóa | Tài khoản bị tạm khóa, từ chối mọi yêu cầu đăng nhập kể cả đúng mật khẩu. | `login_attempts >= 3`, `locked_until > NOW` |
| **LockExpired** | Hết hạn khóa | Thời gian khóa đã trôi qua, nhưng các trường trong DB chưa được reset tự động. | `login_attempts >= 3`, `locked_until <= NOW` |
| **Authenticated** | Đã đăng nhập | Đăng nhập thành công, nhận được mã JWT token hợp lệ. | N/A |

### 1.2. Các sự kiện & Điều kiện chuyển đổi (Events & Guards)
- `E_Valid_Login`: Gửi yêu cầu đăng nhập với email đúng và mật khẩu đúng.
- `E_Invalid_Password`: Gửi yêu cầu đăng nhập với email đúng nhưng mật khẩu sai.
- `E_Invalid_Email`: Gửi yêu cầu đăng nhập với email không tồn tại trên hệ thống.
- `E_Timeout`: Thời gian trôi qua vượt quá thời gian khóa (180 giây).
- `E_Reset_Password`: Đặt lại mật khẩu thành công (thông qua luồng forgot & reset password).
- `E_Logout`: Gửi yêu cầu đăng xuất hoặc token JWT bị hủy/hết hạn.

---

## 2. Ma trận chuyển trạng thái (State Transition Matrix)

Bảng dưới đây mô tả trạng thái tiếp theo dựa trên trạng thái hiện tại và sự kiện kích hoạt.
*(Ghi chú: [E] đại diện cho hành vi kỳ vọng - Spec, [A] đại diện cho hành vi thực tế có bug `attempts += 2`)*

| Trạng thái hiện tại | E_Valid_Login | E_Invalid_Password | E_Invalid_Email | E_Timeout | E_Reset_Password | E_Logout |
|---|---|---|---|---|---|---|
| **Guest** | Checking | Checking | Checking | - | - | - |
| **Checking** | [E] A0/A1/A2 $\rightarrow$ Authenticated<br>[A] A0/A2 $\rightarrow$ Authenticated | [E] A0 $\rightarrow$ A1<br>[E] A1 $\rightarrow$ A2<br>[E] A2 $\rightarrow$ Locked<br>[A] A0 $\rightarrow$ A2 (bug)<br>[A] A2 $\rightarrow$ Locked | UnknownEmail | - | - | - |
| **UnknownEmail** | - | - | - | - | - | Guest (trả về lỗi) |
| **A0** | Authenticated | [E] A1 / [A] A2 (bug) | Guest (trả về lỗi) | - | - | - |
| **A1** | Authenticated | [E] A2 / [A] Locked (bug)| Guest (trả về lỗi) | - | - | - |
| **A2** | Authenticated | Locked | Guest (trả về lỗi) | - | - | - |
| **Locked** | Locked (HTTP 403) | Locked (HTTP 403) | Guest (trả về lỗi) | LockExpired | A0 (Mở khóa ngay) | - |
| **LockExpired**| Authenticated | Locked | Guest (trả về lỗi) | - | - | - |
| **Authenticated**| - | - | - | - | - | Guest |

---

## 3. Thiết kế Phủ 0-Switch (0-Switch Coverage - 1-Hop Paths)

Mục tiêu của 0-Switch là kiểm thử **từng chuyển dịch trạng thái đơn lẻ** (mỗi mũi tên trong State Diagram) ít nhất một lần.

### 3.1. Danh sách các chuyển dịch cần phủ (Spec vs Buggy SUT)

| ID Chuyển dịch | Trạng thái nguồn | Sự kiện | Trạng thái đích (Spec - Kỳ vọng) | Trạng thái đích (SUT thực tế - Buggy) | Ghi chú kiểm thử |
|---|---|---|---|---|---|
| **T01** | Guest | Submit login form | Checking | Checking | Gọi API `POST /api/login` |
| **T02** | Checking | Email không tồn tại | UnknownEmail | UnknownEmail | Nhận HTTP 401 |
| **T03** | UnknownEmail | Hết vòng xử lý | Guest | Guest | Quay lại trang login với thông báo lỗi |
| **T04** | Checking | Đúng credentials lúc attempts = 0 | Authenticated | Authenticated | Nhận HTTP 200 + JWT |
| **T05** | Checking | Sai password lần 1 (từ A0) | **A1** | **A2** (Bug!) | Do bug `attempts += 2` nên nhảy cóc qua A1 lên A2 |
| **T06** | Checking | Đúng credentials lúc attempts = 1 | Authenticated | Authenticated (Nếu DB được seed attempts=1) | Reset attempts = 0 |
| **T07** | Checking | Sai password lần 2 (từ A1) | **A2** | **Locked** (Bug!) | Nếu xuất phát từ A1, lần sai tiếp theo sẽ khóa luôn |
| **T08** | Checking | Đúng credentials lúc attempts = 2 | Authenticated | Authenticated | Reset attempts = 0 |
| **T09** | Checking | Sai password lần 3 (từ A2) | **Locked** | **Locked** | Khóa tài khoản trong 180s |
| **T10** | Locked | Đăng nhập khi đang khóa | Locked | Locked | Trả về HTTP 403, không đổi attempts |
| **T11** | Locked | Đợi qua 180 giây | LockExpired | LockExpired | Thời gian thực tế trôi qua |
| **T12** | LockExpired | Đúng credentials | Authenticated | Authenticated | Reset attempts = 0, unlock |
| **T13** | LockExpired | Sai credentials | Locked | Locked | Tái khóa thêm 180 giây |
| **T14** | Authenticated | Click đăng xuất | Guest | Guest | Xóa JWT ở client |
| **T15** | Locked | Reset mật khẩu thành công | **A0** | **Locked** (Bug!) | Lỗi **BUG-FR02-A-17**: Reset password thành công không mở khóa tài khoản |

### 3.2. Thiết kế kịch bản test phủ 0-Switch

Để phủ toàn bộ 15 chuyển dịch trên với số lượng test case tối ưu nhất, ta xây dựng các kịch bản sau:

#### **TC-0-SWITCH-01: Happy Path & Logout**
- **Đường đi:** Guest $\rightarrow$ Checking $\rightarrow$ A0 $\rightarrow$ Authenticated $\rightarrow$ Guest.
- **Mục tiêu phủ:** T01, T04, T14.
- **Các bước:**
  1. Từ trang `/login`, nhập tài khoản hợp lệ (attempts = 0).
  2. Kiểm tra đăng nhập thành công (Authenticated).
  3. Nhấn nút Đăng xuất $\rightarrow$ Quay lại trang `/login` (Guest).

#### **TC-0-SWITCH-02: Sai email đăng nhập**
- **Đường đi:** Guest $\rightarrow$ Checking $\rightarrow$ UnknownEmail $\rightarrow$ Guest.
- **Mục tiêu phủ:** T01, T02, T03.
- **Các bước:**
  1. Nhập email không tồn tại trong DB, mật khẩu bất kỳ.
  2. Xác nhận nhận HTTP 401 với thông báo "Invalid email or password".

#### **TC-0-SWITCH-03: Sai mật khẩu liên tiếp & Khóa tài khoản (Kỳ vọng/Spec)**
- **Đường đi:** Guest $\rightarrow$ Checking $\rightarrow$ A0 $\rightarrow$ A1 $\rightarrow$ A2 $\rightarrow$ Locked $\rightarrow$ Locked $\rightarrow$ LockExpired $\rightarrow$ Authenticated.
- **Mục tiêu phủ:** T05, T07, T09, T10, T11, T12.
- **Ghi chú chạy thực tế:** Do bug nhảy cóc attempts, kịch bản này trên SUT thực tế sẽ rẽ sang hướng khác (Xem phần 3.3). 
- **Các bước:**
  1. Đăng nhập sai mật khẩu lần 1 $\rightarrow$ State A1.
  2. Đăng nhập sai mật khẩu lần 2 $\rightarrow$ State A2.
  3. Đăng nhập sai mật khẩu lần 3 $\rightarrow$ State Locked (nhận thông báo khóa tài khoản).
  4. Cố đăng nhập lần nữa khi đang khóa $\rightarrow$ Vẫn báo khóa (HTTP 403).
  5. Chờ hết 180s $\rightarrow$ State LockExpired.
  6. Đăng nhập bằng mật khẩu đúng $\rightarrow$ Đăng nhập thành công (Authenticated).

#### **TC-0-SWITCH-04: Sai mật khẩu sau khi hết hạn khóa**
- **Đường đi:** LockExpired $\rightarrow$ Locked.
- **Mục tiêu phủ:** T13.
- **Các bước:**
  1. Đưa tài khoản vào trạng thái LockExpired (sai 3 lần, đợi qua 180s).
  2. Đăng nhập bằng mật khẩu SAI.
  3. Kiểm tra xem tài khoản có bị khóa lại lập tức hay không (Locked, nhận HTTP 401/403).

#### **TC-0-SWITCH-05: Đặt lại mật khẩu khi đang bị khóa**
- **Đường đi:** Locked $\rightarrow$ A0.
- **Mục tiêu phủ:** T15.
- **Các bước:**
  1. Đăng nhập sai mật khẩu liên tiếp để tài khoản bị khóa (Locked).
  2. Thực hiện đặt lại mật khẩu thành công qua API `/api/forgot-password` và `/api/reset-password`.
  3. Đăng nhập bằng mật khẩu mới $\rightarrow$ Phải thành công ngay lập tức (A0 $\rightarrow$ Authenticated).

---

### 3.3. Đường chạy thực tế trên Buggy SUT (Hành vi thực tế)
Vì bug tại backend, các chuyển dịch trạng thái thực tế sẽ diễn ra như sau:
1. Đăng nhập sai lần 1: `A0 --(T_fail)--> A2` (Tài khoản lưu `login_attempts = 2` ngay từ lần sai thứ nhất).
2. Đăng nhập sai lần 2: `A2 --(T_fail)--> Locked` (Tài khoản bị khóa ngay lập tức vì `attempts = 4 >= 3`).
3. Đặt lại mật khẩu thành công: Mật khẩu được đổi, nhưng `login_attempts` vẫn bằng 4 và `locked_until` không đổi. Khi đăng nhập bằng mật khẩu mới $\rightarrow$ Vẫn báo lỗi khóa HTTP 403 (Không chuyển dịch sang `A0` mà giữ nguyên `Locked`).

---

## 4. Thiết kế Phủ 1-Switch (1-Switch Coverage - 2-Hop Paths)

Mục tiêu của 1-Switch là phủ tất cả **cặp chuyển dịch liên tiếp** (độ dài chuỗi chuyển dịch = 2 transitions).
Ví dụ: $S_1 \xrightarrow{T_a} S_2 \xrightarrow{T_b} S_3$.

### 4.1. Danh sách các cặp chuyển dịch 1-Switch hợp lệ (Theo thiết kế Spec)

Chúng ta liệt kê các cặp chuyển dịch tiêu biểu và quan trọng nhất đối với logic nghiệp vụ FR02:

1. **Cặp đăng nhập xen kẽ (Reset bộ đếm):**
   - Chuỗi: `A0 --(Sai lần 1)--> A1 --(Đúng)--> Authenticated`
   - Chuỗi: `A1 --(Sai lần 2)--> A2 --(Đúng)--> Authenticated`
   - Ý nghĩa: Xác minh bộ đếm thất bại được xóa sạch khi có 1 lần thành công xen giữa.

2. **Cặp chuyển tiếp khóa:**
   - Chuỗi: `A1 --(Sai lần 2)--> A2 --(Sai lần 3)--> Locked`
   - Chuỗi: `A2 --(Sai lần 3)--> Locked --(Đăng nhập lại)--> Locked`
   - Chuỗi: `A2 --(Sai lần 3)--> Locked --(Chờ thời gian)--> LockExpired`

3. **Cặp xử lý sau khóa:**
   - Chuỗi: `Locked --(Chờ thời gian)--> LockExpired --(Đăng nhập đúng)--> Authenticated`
   - Chuỗi: `Locked --(Chờ thời gian)--> LockExpired --(Đăng nhập sai)--> Locked`

4. **Cặp Reset mật khẩu:**
   - Chuỗi: `Locked --(Reset mật khẩu)--> A0 --(Đăng nhập đúng)--> Authenticated`
   - Chuỗi: `Locked --(Reset mật khẩu)--> A0 --(Đăng nhập sai lần 1)--> A1`

5. **Cặp Đăng xuất:**
   - Chuỗi: `LockExpired --(Đăng nhập đúng)--> Authenticated --(Đăng xuất)--> Guest`

---

### 4.2. Thiết kế kịch bản test phủ 1-Switch

#### **TC-1-SWITCH-01: Đăng nhập đúng xen kẽ (Reset bộ đếm)**
- **Kịch bản:**
  1. Tài khoản đang ở trạng thái bình thường (A0).
  2. Đăng nhập SAI lần 1 $\rightarrow$ Chuyển sang A1.
  3. Đăng nhập ĐÚNG mật khẩu $\rightarrow$ Chuyển sang Authenticated.
  4. Thực hiện Đăng xuất $\rightarrow$ Chuyển sang Guest (DB lưu `login_attempts = 0`).
  5. Đăng nhập SAI 2 lần liên tiếp.
  6. **Kết quả mong đợi:** Tài khoản không bị khóa (vì lần đúng ở bước 3 đã xóa bộ đếm cũ).

#### **TC-1-SWITCH-02: Chu kỳ khóa và mở khóa tự động**
- **Kịch bản:**
  1. Tài khoản đăng nhập sai 3 lần liên tiếp: `A0 -> A1 -> A2 -> Locked`.
  2. Cố gắng đăng nhập ngay lập tức bằng mật khẩu đúng: `Locked -> Locked` (bị từ chối HTTP 403).
  3. Đợi hết 180s: `Locked -> LockExpired`.
  4. Đăng nhập bằng mật khẩu đúng: `LockExpired -> Authenticated` (thành công, reset DB).

#### **TC-1-SWITCH-03: Tái khóa sau khi hết hạn khóa**
- **Kịch bản:**
  1. Tài khoản đăng nhập sai 3 lần liên tiếp và đợi hết 180s: `Locked -> LockExpired`.
  2. Gửi yêu cầu đăng nhập bằng mật khẩu SAI: `LockExpired -> Locked`.
  3. Cố gắng đăng nhập ngay lập tức: Kiểm tra xem tài khoản có bị khóa ngay lập tức và thiết lập thời gian khóa mới 180s hay không.

#### **TC-1-SWITCH-04: Đặt lại mật khẩu thành công & Reset bộ đếm**
- **Kịch bản:**
  1. Tài khoản đăng nhập sai 3 lần liên tiếp để bị khóa: `A2 -> Locked`.
  2. Gửi yêu cầu đặt lại mật khẩu và hoàn tất việc đặt lại mật khẩu mới: `Locked -> A0`.
  3. Thực hiện đăng nhập SAI lần 1 bằng mật khẩu mới: `A0 -> A1`.
  4. Kiểm tra xem tài khoản có chuyển sang trạng thái A1 thông thường hay bị khóa luôn (nếu bị khóa luôn là lỗi do không reset attempts).

---

## 5. Bảng ma trận truy vết ca kiểm thử (Traceability Matrix)

| Test Case ID | Test Type / Technique | Trạng thái nguồn | Chuỗi chuyển dịch phủ được | Chuyển dịch 0-Switch | Chuyển dịch 1-Switch | Status SUT hiện tại | Bug liên quan |
|---|---|---|---|---|---|---|---|
| **TC-0-SWITCH-01** | State Transition / 0-Switch | Guest | Guest $\rightarrow$ Checking $\rightarrow$ A0 $\rightarrow$ Authenticated $\rightarrow$ Guest | T01, T04, T14 | N/A | **Pass** | None |
| **TC-0-SWITCH-02** | State Transition / 0-Switch | Guest | Guest $\rightarrow$ Checking $\rightarrow$ UnknownEmail $\rightarrow$ Guest | T01, T02, T03 | N/A | **Pass** | None |
| **TC-0-SWITCH-03** | State Transition / 0-Switch | Guest | A0 $\rightarrow$ A1 $\rightarrow$ A2 $\rightarrow$ Locked $\rightarrow$ Locked $\rightarrow$ LockExpired $\rightarrow$ Authenticated | T05, T07, T09, T10, T11, T12 | N/A | **Fail** | **BUG-FR02-A-01**, **BUG-FR02-A-02** |
| **TC-0-SWITCH-04** | State Transition / 0-Switch | LockExpired | LockExpired $\rightarrow$ Locked | T13 | N/A | **Pass** | None |
| **TC-0-SWITCH-05** | State Transition / 0-Switch | Locked | Locked $\rightarrow$ A0 $\rightarrow$ Authenticated | T15, T04 | N/A | **Fail** | **BUG-FR02-A-17** |
| **TC-1-SWITCH-01** | State Transition / 1-Switch | A0 | A0 $\rightarrow$ A1 $\rightarrow$ Authenticated $\rightarrow$ Guest $\dots \rightarrow$ A2 | T05, T06, T14, T01, T08 | A0-A1-Authenticated, Authenticated-Guest-A2 | **Fail** (nhảy cóc qua A2) | **BUG-FR02-A-01** |
| **TC-1-SWITCH-02** | State Transition / 1-Switch | A0 | A2 $\rightarrow$ Locked $\rightarrow$ Locked $\rightarrow$ LockExpired $\rightarrow$ Authenticated | T09, T10, T11, T12 | A2-Locked-Locked, Locked-LockExpired-Authenticated | **Fail** | **BUG-FR02-A-02** |
| **TC-1-SWITCH-03** | State Transition / 1-Switch | Locked | Locked $\rightarrow$ LockExpired $\dots \rightarrow$ Locked | T11, T13 | Locked-LockExpired-Locked | **Fail** (thời gian khóa sai) | **BUG-FR02-A-02** |
| **TC-1-SWITCH-04** | State Transition / 1-Switch | Locked | Locked $\dots \rightarrow$ A0 $\dots \rightarrow$ A1 | T15, T05 | Locked-A0-A1 | **Fail** | **BUG-FR02-A-17** |
