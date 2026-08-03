# Bằng Chứng Thực Nghiệm Usability (Usability Session Evidence)

Tài liệu này tổng hợp toàn bộ kế hoạch kiểm thử, chuẩn bị công cụ đo lường và bằng chứng thực nghiệm của quá trình đánh giá Usability với **7 người tham gia thực tế** đối với chức năng Web Admin.

---

## 1. Kịch Bản Kiểm Thử (Task Scenario)

- **Mục tiêu đánh giá:** Khảo sát hành vi của quản trị viên khi thực hiện nhập liệu hàng loạt (Import CSV) chứa cả dữ liệu hợp lệ/không hợp lệ, khả năng tự phục hồi sau lỗi và xem sản phẩm được thêm.
- **Tài nguyên chuẩn bị:** 
  - File dữ liệu lỗi: [import_i.csv](./usability-testing-csv/import_i.csv) (Thiếu trường tên sản phẩm ở dòng 2)
  - File dữ liệu chuẩn: [import_v .csv](./usability-testing-csv/import_v.csv) (Dữ liệu hợp lệ đầy đủ)
  - Tài khoản Admin kiểm thử: `admin@eshop.com` / `Admin123!`
- **Kịch bản giao cho người dùng (Goal-oriented Scenario):**
  > "Bạn đang đóng vai trò là một Quản trị viên (Admin) mới tiếp nhận quản lý cửa hàng trực tuyến EShop. Bạn được giao nhiệm vụ nhập một danh sách các sản phẩm mới vào hệ thống từ các file dữ liệu sẵn có. Sau khi nhập thành công từng file, có thể lướt xuống dưới để kiểm tra lại danh sách sản phẩm. Lưu ý: Nếu có lỗi ở bất kỳ dòng nào, toàn bộ import phải được rollback hay nói cách khác không có sản phẩm nào từ file lỗi được import thành công.

---

## 2. Bảng Danh Sách 7 Người Tham Gia (Table of 7 Participants)

*Thông tin liên hệ bắt buộc phải che 4 chữ số ở giữa để bảo vệ quyền riêng tư, nhưng vẫn đảm bảo tính xác thực.*

| STT | Họ và Tên | Đối tượng | Số điện thoại / Zalo (Masked) | Phương thức liên lạc chính | Trạng thái buổi test |
|---|---|---|---|---|---|
| **1** | `Võ Ngọc Bích Trâm` | IT (HCMUS) | `0982.xxx.701` | Điện thoại | Hoàn  (Pilot) |
| **2** | `Nguyễn Thanh Gia Bảo` | IT (HCMUS) | `0358.xxx.739` | Điện thoại | Hoàn thành |
| **3** | `Phan Yến Anh` | Non-IT (UEH) | `0795.xxx.339` | Điện thoại | Hoàn thành |
| **4** | `Đặng Trường Nguyên` | IT (HCMUS) | `0911.xxx.029` | Điện thoại | Hoàn thành |
| **5** | `Trương Lý Khải` | IT (HCMUS) | `0903.xxx.744` | Điện thoại | Hoàn thành |
| **6** | `Nguyễn Vũ Thiên Tú` | Non-IT (UEH) | `0977.xxx.246` | Điện thoại | Hoàn thành |
| **7** | `Lê Trương Bảo Ngọc` | IT (HCMUS) | `0907.xxx.390` | Điện thoại | Hoàn thành |

---

## 3. Ghi Chép Quan Sát & Kết Quả Từng Buổi Test (Observation Notes)

### Buổi test số 1 (Participant 1 - Pilot Session) - Võ Ngọc Bích Trâm
- **Thời gian hoàn thành tác vụ (Time on Task):** `02:35`
- **Ghi chép hành vi & Tương tác (Observation Table):**

| Mốc thời gian | Quan sát | Màn hình / Bước |
|---|---|---|
| **00:00 - 00:23** | Người dùng đăng nhập thành công bằng tài khoản admin có sẵn. | Đăng nhập |
| **00:23 - 00:51** | Tìm thấy vùng "Import sản phẩm từ CSV". Chọn upload file `import_i.csv`. | Quản lý sản phẩm / Xem trước |
| **00:51 - 01:24** | Nhấp nút "Import 2 sản phẩm". Giao diện báo import có lỗi ở hàng 2. | Quản lý sản phẩm / Xem kết quả |
| **01:24 - 01:47** | Cuộn xuống phần danh sách sản phẩm bên dưới để đối chiếu. Người dùng phát hiện sản phẩm hợp lệ của `import_i.csv` vẫn được chèn vào danh sách. Người dùng thắc mắc: "Tôi thấy dòng hợp lệ vẫn được thêm vào danh sách. Đáng lẽ khi có lỗi ở bất cứ dòng nào thì toàn bộ import phải được rollback chứ?". Moderator ghi nhận ý kiến. | Quản lý sản phẩm / Kiểm tra danh sách |
| **01:47 - 02:19** | Chọn file `import_v.csv` để upload và nhấn nút Import. Hệ thống báo import thành công hoàn toàn. | Quản lý sản phẩm / Import lần 2 |
| **02:19 - 02:35** | Cuộn xuống dưới kiểm tra lại danh sách sản phẩm, xác nhận các sản phẩm mới đã xuất hiện đầy đủ. | Quản lý sản phẩm / Kiểm tra danh sách |

- **Khó khăn gặp phải (Friction points):**
  - Font chữ hiển thị trong bảng xem trước (preview table) của file CSV hơi nhỏ, gây khó khăn cho việc kiểm tra nhanh trước khi import.
- **Điểm đánh giá SUS:** `70`
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* Giao diện quản trị có bố cục rõ ràng, dễ hiểu.
  - *Error Recovery:* Hệ thống chỉ rõ vị trí dòng bị lỗi, giúp dễ dàng nhận biết vấn đề.
  - *Speed:* Tốc độ xử lý của các thao tác đều nhanh chóng.
  - *Trust:* Không chắc chắn dữ liệu đã lưu đúng chưa vì hệ thống thông báo import hoàn tất nhưng lại liệt kê lỗi ở dưới.
- **Liên kết bằng chứng:** [Link Drive Video Session 1](https://drive.google.com/file/d/1_eDBRoShbDevvvGxupqKQ7pgHaDXcCv6/view?usp=drive_link)

### Buổi test số 2 (Participant 2) - Nguyễn Thanh Gia Bảo
- **Thời gian hoàn thành tác vụ (Time on Task):** `01:34`
- **Ghi chép hành vi & Tương tác (Observation Table):**

| Mốc thời gian | Quan sát | Màn hình / Bước |
|---|---|---|
| **00:00 - 00:11** | Đăng nhập nhanh chóng, không gặp trở ngại. | Đăng nhập |
| **00:11 - 00:37** | Vào mục Sản phẩm, click chọn upload file `import_i.csv` và nhấn nút Import. | Quản lý sản phẩm / Xem trước |
| **00:37 - 00:59** | Nhấp nút Import, nhận kết quả thông báo thành công màu xanh lá nhưng bên dưới lại liệt kê lỗi màu đỏ. Người dùng: "Hộp màu xanh lá báo thành công nhưng vẫn hiển thị lỗi bên dưới làm tôi bối rối không biết có lỗi thật hay không". | Quản lý sản phẩm / Xem kết quả |
| **00:59 - 01:13** | Cuộn xuống dưới xem danh sách sản phẩm. Nhận thấy sản phẩm hợp lệ trong file lỗi vẫn được thêm vào hệ thống. Người dùng thắc mắc: "Tuii tưởng có lỗi thì không được lưu sản phẩm nào?". | Quản lý sản phẩm / Kiểm tra danh sách |
| **01:13 - 01:25** | Upload file hợp lệ `import_v.csv` rồi bấm nút Import. Hệ thống báo thành công đầy đủ. | Quản lý sản phẩm / Import lần 2 |
| **01:25 - 01:34** | Cuộn xuống dưới danh sách và xác nhận các sản phẩm mới đã xuất hiện. | Quản lý sản phẩm / Kiểm tra danh sách |

- **Khó khăn gặp phải (Friction points):**
  - Hộp thông báo màu xanh lá (biểu thị thành công) nhưng bên trong lại chứa chi tiết lỗi dòng màu đỏ khiến người dùng bối rối không rõ tác vụ đã hoàn thành trọn vẹn chưa.
- **Điểm đánh giá SUS:** `72.5`
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* Các thao tác đơn giản và quen thuộc, không cần tài liệu hướng dẫn.
  - *Error Recovery:* Nhận biết lỗi nhanh nhờ thông báo chi tiết vị trí lỗi.
  - *Speed:* Thời gian phản hồi tác vụ rất nhanh.
  - *Trust:* Lo ngại dữ liệu bị trùng lặp hoặc mất mát ở backend do import chạy nửa vời không rollback.
- **Liên kết bằng chứng:** [Link Drive Video Session 2](https://drive.google.com/file/d/1ZEw_L40uTdZ-6w9aEDTMiFzY0cWm4kbY/view?usp=drive_link)

### Buổi test số 3 (Participant 3) - Phan Yến Anh
- **Thời gian hoàn thành tác vụ (Time on Task):** `02:02`
- **Ghi chép hành vi & Tương tác (Observation Table):**

| Mốc thời gian | Quan sát | Màn hình / Bước |
|---|---|---|
| **00:00 - 00:27** | Đăng nhập hơi chậm do gõ phím cẩn thận từng ký tự. | Đăng nhập |
| **00:27 - 00:53** | Vào mục Sản phẩm, chọn upload file lỗi `import_i.csv` rồi nhấp Import. | Quản lý sản phẩm / Xem trước & Import |
| **00:53 - 01:16** | Giao diện hiển thị thông báo lỗi dòng 2. Người dùng cuộn xuống kiểm tra danh sách sản phẩm và phát hiện sản phẩm dòng 1 của file lỗi vẫn được chèn thành công. Người dùng thắc mắc: "Ủa, sao sản phẩm dòng đầu vẫn vào danh sách vậy?". Moderator ghi nhận ý kiến. | Quản lý sản phẩm / Xem kết quả |
| **01:16 - 01:48** | Chọn file chuẩn `import_v.csv` để upload, lướt qua bảng xem trước rồi bấm Import. | Quản lý sản phẩm / Import lần 2 |
| **01:48 - 02:02** | Kéo xuống dưới kiểm tra lại danh sách và thấy các sản phẩm mới đã hiển thị đầy đủ. | Quản lý sản phẩm / Kiểm tra danh sách |

- **Khó khăn gặp phải (Friction points):**
  - Bảng xem trước dữ liệu hiển thị chữ hơi nhỏ.
- **Điểm đánh giá SUS:** `70`
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* Thiết kế đơn giản và dễ hiểu.
  - *Error Recovery:* Ghi nhận được lỗi dòng dữ liệu bị thiếu một cách trực quan.
  - *Speed:* Hệ thống tải trang và import nhanh.
  - *Trust:* Khó nhận biết trạng thái thực tế của hệ thống nếu không kéo xuống kiểm tra thủ công.
- **Liên kết bằng chứng:** [Link Drive Video Session 3](https://drive.google.com/file/d/1dyAuPUGKiyRZofVH0cOefcCVfI1q6JLE/view?usp=drive_link)

### Buổi test số 4 (Participant 4) - Đặng Trường Nguyên
- **Thời gian hoàn thành tác vụ (Time on Task):** `00:46`
- **Ghi chép hành vi & Tương tác (Observation Table):**

| Mốc thời gian | Quan sát | Màn hình / Bước |
|---|---|---|
| **00:00 - 00:07** | Đăng nhập cực kì nhanh và chính xác. | Đăng nhập |
| **00:07 - 00:19** | Vào trang Sản phẩm, chọn file lỗi `import_i.csv` upload rồi nhấn Import ngay. | Quản lý sản phẩm / Xem trước & Import |
| **00:19 - 00:28** | Nhận thông báo lỗi hàng 2. Lập tức cuộn xuống kiểm tra danh sách và phát hiện sản phẩm dòng 1 đã được chèn vào. Người dùng: "Lỗi rollback giao dịch rồi, backend không dùng TRANSACTION đúng không?". Moderator ghi nhận phản hồi. | Quản lý sản phẩm / Xem kết quả |
| **00:28 - 00:39** | Chọn file hợp lệ `import_v.csv` để up đè lên và bấm Import. Import hoàn thành ngay lập tức. | Quản lý sản phẩm / Import lần 2 |
| **00:39 - 00:46** | Cuộn xuống kiểm tra danh sách sản phẩm để xác nhận các sản phẩm mới đã thêm thành công. | Quản lý sản phẩm / Kiểm tra danh sách |

- **Khó khăn gặp phải (Friction points):**
  - Không gặp trở ngại nào trong thao tác.
- **Điểm đánh giá SUS:** `85`
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* Giao diện trực quan nhưng cơ chế hoạt động thực tế chưa đồng bộ với thiết kế tính năng.
  - *Error Recovery:* Hệ thống báo lỗi chính xác và bắt lỗi tốt.
  - *Speed:* Phản hồi rất mượt mà.
  - *Trust:* Không tin cậy thiết kế hệ thống dữ liệu vì thiếu ràng buộc giao dịch (transaction/rollback).
- **Liên kết bằng chứng:** [Link Drive Video Session 4](https://drive.google.com/file/d/1My95yWCY_4YmH8UcAklR9-lu8C9oNOU4/view?usp=drive_link)

### Buổi test số 5 (Participant 5) - Trương Lý Khải
- **Thời gian hoàn thành tác vụ (Time on Task):** `01:55`
- **Ghi chép hành vi & Tương tác (Observation Table):**

| Mốc thời gian | Quan sát | Màn hình / Bước |
|---|---|---|
| **00:00 - 00:17** | Đăng nhập thành công. | Đăng nhập |
| **00:17 - 00:43** | Vào mục Sản phẩm, loay hoay tìm khu vực Import sản phẩm. Người dùng hỏi: "Nút Import ở đâu vậy?". Người dùng sau đó thấy phần Import ở phía trên danh sách sản phẩm. | Quản lý sản phẩm |
| **00:43 - 01:06** | Upload file lỗi `import_i.csv`, nhấn nút Import và hệ thống hiển thị thông báo "Hàng 2: Thiếu tên sản phẩm". | Quản lý sản phẩm / Import |
| **01:06 - 01:23** | Người dùng dừng lại suy nghĩ: "Hộp báo lỗi này không có nút để xóa đi, và tôi cũng không biết có sửa được dữ liệu trực tiếp trên bảng xem trước không". Người dùng kéo xuống và thấy sản phẩm hợp lệ của file lỗi đã được chèn vào. Nhưng có nhiều dòng sản phẩm trùng lặp, Moderator có giải thích đây là kết quả do các phiên kiểm thử trước, không phải do hệ thống nên người dùng tiếp tục. | Quản lý sản phẩm / Xem kết quả |
| **01:23 - 01:42** | Chọn file hợp lệ `import_v.csv`, xem qua preview rồi bấm nút Import. Hệ thống báo import hoàn tất thành công. | Quản lý sản phẩm / Import lần 2 |
| **01:42 - 01:55** | Cuộn xuống dưới cùng của danh sách sản phẩm để xác nhận các sản phẩm mới đã xuất hiện thành công. | Quản lý sản phẩm / Kiểm tra danh sách |

- **Khó khăn gặp phải (Friction points):**
  - Vị trí khu vực Import sản phẩm chưa đủ nổi bật trên màn hình quản lý.
  - Thiếu nút để xóa/hủy kết quả import hoặc file đã chọn, buộc người dùng phải chọn file khác đè lên.
  - Bảng xem trước không cho phép nhấp đúp để chỉnh sửa trực tiếp dữ liệu bị thiếu.
  - Moderator quên xóa sản phẩm từ phiên kiểm thử trước nên xuất hiện dòng sản phẩm bị trùng lặp.
- **Điểm đánh giá SUS:** `50`
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* Giao diện cần làm nổi bật các chức năng chính hơn nữa.
  - *Error Recovery:* Báo lỗi rõ vị trí nhưng thiếu các chức năng hỗ trợ sửa lỗi nhanh tại chỗ.
  - *Speed:* Hệ thống chạy ổn định, không bị trễ.
  - *Trust:* Bối rối vì thông báo thành công màu xanh lá lại đi kèm dòng báo lỗi chữ đỏ ở bên trong.
- **Liên kết bằng chứng:** [Link Drive Video Session 5](https://drive.google.com/file/d/13LPt6ndcqLb8iYGL18GO2cGp5EN0PVoh/view?usp=drive_link)

### Buổi test số 6 (Participant 6) - Nguyễn Vũ Thiên Tú
- **Thời gian hoàn thành tác vụ (Time on Task):** `01:46`
- **Ghi chép hành vi & Tương tác (Observation Table):**

| Mốc thời gian | Quan sát | Màn hình / Bước |
|---|---|---|
| **00:00 - 00:14** | Đăng nhập hệ thống bình thường. | Đăng nhập |
| **00:14 - 00:39** | Truy cập trang Sản phẩm, upload file lỗi `import_i.csv` rồi nhấn nút Import. | Quản lý sản phẩm / Import |
| **00:39 - 00:58** | Đọc thông báo kết quả có chữ lỗi màu đỏ nằm trong khung màu xanh lá. | Quản lý sản phẩm / Xem kết quả |
| **00:58 - 01:16** | Cuộn xuống dưới xem danh sách sản phẩm, nhận xét: "Sản phẩm dòng 1 của file lỗi vẫn bị chèn vào danh sách này, như vậy là không đúng khi file có dòng lỗi hả?". Moderator ghi nhận ý kiến. | Quản lý sản phẩm / Kiểm tra danh sách |
| **01:16 - 01:35** | Upload file chuẩn `import_v.csv`, kiểm tra bảng preview rồi nhấn nút Import sản phẩm. Hệ thống báo import thành công. | Quản lý sản phẩm / Import lần 2 |
| **01:35 - 01:46** | Kéo xuống dưới cùng xác nhận tất cả sản phẩm mới đã được chèn vào thành công. | Quản lý sản phẩm / Kiểm tra danh sách |

- **Khó khăn gặp phải (Friction points):**
  - Màu sắc thông báo import có lỗi dòng (chữ đỏ trong nền xanh lá) gây cảm giác không nhất quán về mặt thị giác.
- **Điểm đánh giá SUS:** `57.5`
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* Các thành phần giao diện rõ ràng, dễ đi theo mạch tác vụ.
  - *Error Recovery:* Hệ thống thông tin lỗi tốt.
  - *Speed:* Phản hồi nhanh chóng.
  - *Trust:* Không chắc chắn các dòng lỗi đã được lọc sạch hoàn toàn khỏi danh sách sản phẩm hay chưa.
- **Liên kết bằng chứng:** [Link Drive Video Session 6](https://drive.google.com/file/d/12ngTldmDNp9z0klDrvF_jNQ6ZC9bUX2r/view?usp=drive_link)

### Buổi test số 7 (Participant 7) - Lê Trương Bảo Ngọc
- **Thời gian hoàn thành tác vụ (Time on Task):** `01:03`
- **Ghi chép hành vi & Tương tác (Observation Table):**

| Mốc thời gian | Quan sát | Màn hình / Bước |
|---|---|---|
| **00:00 - 00:09** | Đăng nhập thành công nhanh chóng. | Đăng nhập |
| **00:09 - 00:26** | Truy cập mục Sản phẩm, upload file lỗi `import_i.csv`, nhấn nút Import. | Quản lý sản phẩm / Import & Xem kết quả |
| **00:26 - 00:38** | Cuộn xuống danh sách sản phẩm kiểm tra, phát hiện ra lỗi rollback và trao đổi với Moderator về việc này. Moderator ghi nhận. | Quản lý sản phẩm / Kiểm tra danh sách |
| **00:38 - 00:52** | Upload file chuẩn `import_v.csv`. Đọc kĩ danh sách sản phẩm hiển thị trong bảng xem trước trước khi nhấn Import. | Quản lý sản phẩm / Xem trước & Import |
| **00:52 - 01:03** | Kéo xuống dưới kiểm tra lại và thấy tất cả sản phẩm mới của file chuẩn đã hiển thị đầy đủ. | Quản lý sản phẩm / Kiểm tra danh sách |

- **Khó khăn gặp phải (Friction points):**
  - Cuộn trang preview sản phẩm có hiện tượng khựng nhẹ do danh sách hiển thị dài.
- **Điểm đánh giá SUS:** `70`
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* Giao diện đơn giản, dễ làm quen và thao tác.
  - *Error Recovery:* Thông tin lỗi dòng dữ liệu rõ ràng.
  - *Speed:* Các trang tải tương đối nhanh.
  - *Trust:* Cảm thấy thiếu nhất quán giữa thông điệp báo thành công của giao diện và kết quả thực tế.
- **Liên kết bằng chứng:** [Link Drive Video Session 7](https://drive.google.com/file/d/1qhM2eICyAQ5pQGWETkiuvAH-ndRnRqQx/view?usp=drive_link)

---

## 4. Kết Quả Thang Đo Usability (SUS / UEQ-S Score Sheet)

### 10 Phát biểu chuẩn System Usability Scale (SUS):
1. Tôi nghĩ rằng mình sẽ thích sử dụng hệ thống này thường xuyên.
2. Tôi thấy hệ thống phức tạp không cần thiết.
3. Tôi nghĩ hệ thống dễ sử dụng.
4. Tôi nghĩ rằng tôi sẽ cần sự hỗ trợ của một kỹ thuật viên để có thể sử dụng hệ thống này.
5. Tôi thấy các chức năng khác nhau trong hệ thống này được liên kết tốt.
6. Tôi nghĩ rằng có quá nhiều sự bất nhất trong hệ thống này.
7. Tôi hình dung rằng hầu hết mọi người sẽ học cách sử dụng hệ thống này rất nhanh.
8. Tôi thấy hệ thống rất cồng kềnh/khó sử dụng.
9. Tôi cảm thấy rất tự tin khi sử dụng hệ thống.
10. Tôi cần phải học rất nhiều thứ trước khi có thể bắt đầu sử dụng hệ thống này.

### Bảng tổng hợp điểm số của 7 người tham gia:

| Câu hỏi chuẩn SUS (Q1 - Q10) / UEQ-S | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Điểm Trung Bình |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Q1 (Tần suất sử dụng)** | 3 | 3 | 3 | 4 | 3 | 3 | 4 | 3.3 |
| **Q2 (Bất hợp lý/Phức tạp)** | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 2.1 |
| **Q3 (Dễ sử dụng)** | 4 | 4 | 4 | 5 | 3 | 3 | 4 | 3.9 |
| **Q4 (Cần hỗ trợ kỹ thuật)** | 2 | 1 | 2 | 1 | 4 | 2 | 2 | 2.0 |
| **Q5 (Tích hợp tốt)** | 3 | 4 | 4 | 4 | 3 | 3 | 3 | 3.4 |
| **Q6 (Sự bất nhất)** | 3 | 3 | 3 | 2 | 3 | 4 | 4 | 3.1 |
| **Q7 (Học nhanh)** | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 3.7 |
| **Q8 (Cồng kềnh/Khó dùng)** | 2 | 2 | 2 | 1 | 3 | 2 | 2 | 2.0 |
| **Q9 (Tự tin khi dùng)** | 3 | 4 | 3 | 4 | 3 | 2 | 3 | 3.1 |
| **Q10 (Cần học nhiều trước)** | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1.1 |
| **Điểm quy đổi SUS tổng cộng** | 70 | 72.5 | 70 | 85 | 50 | 57.5 | 70 | 67.8 |

*Công thức tính điểm SUS:*
- Với các câu hỏi số lẻ (1, 3, 5, 7, 9): `Điểm = Trả lời - 1`
- Với các câu hỏi số chẵn (2, 4, 6, 8, 10): `Điểm = 5 - Trả lời`
- `Điểm SUS của 1 người = (Tổng điểm 10 câu) x 2.5` (Thang điểm từ 0 đến 100).
- `Xếp loại điểm SUS trung bình:` >80.3: Excellent | 68 - 80.3: Good | 51 - 67.9: OK | <51: Poor.

---

## 5. Đánh Giá Khó Khăn & Phân Loại Theo Mức Độ Nghiêm Trọng

### 5.1. Lỗi Nghiêm Trọng / Chặn dòng tác vụ (Blockers)
- *Không ghi nhận*: Cả 7 người tham gia đều thực hiện thành công các mục tiêu của kịch bản kiểm thử (đăng nhập, upload file dữ liệu lỗi, nhận diện lỗi dòng, upload file dữ liệu chuẩn và kiểm tra danh sách sản phẩm mới).

### 5.2. Lỗi Lớn gây khó khăn lớn (Major Usability Issues)
1. **Không rollback giao dịch khi có dòng lỗi (Transaction Rollback Failure / Atomicity Broken):** Khi người dùng import file lỗi `import_i.csv` (dòng 1 hợp lệ, dòng 2 thiếu tên sản phẩm), hệ thống vẫn chèn sản phẩm hợp lệ của dòng 1 vào cơ sở dữ liệu và chỉ bỏ qua dòng 2. Theo thiết kế giao dịch nguyên tử (all-or-nothing), toàn bộ import phải được rollback để tránh tình trạng dữ liệu dở dang hoặc trùng lặp ở backend. Vấn đề này gây bối rối và làm giảm độ tin cậy của hệ thống đối với người dùng (P1, P2, P3, P4, P5, P6, P7 đều nhận thấy và thắc mắc).
2. **Thông điệp kết quả import thiếu nhất quán trực quan (Inconsistent Success Alert with Red Error Text):** Hộp cảnh báo kết quả import hiển thị nền màu xanh lá (success alert) nhưng nội dung bên trong lại hiển thị các dòng lỗi chi tiết màu đỏ. Điều này làm người dùng bối rối không biết tác vụ đã thực sự thành công hay thất bại (P2, P5, P6, P7 phản ánh).

### 5.3. Vấn đề Nhỏ / Thẩm mỹ (Minor/Cosmetic Issues)
1. **Khu vực Import sản phẩm chưa đủ nổi bật:** Khu vực upload và nhập file CSV nằm ở vị trí khó tìm thấy ngay lập tức đối với người dùng mới (P5 loay hoay mất hơn 30 giây để tìm kiếm).
2. **Thiếu nút xóa/hủy file đã chọn hoặc kết quả import cũ:** Sau khi import có lỗi, giao diện không cung cấp tùy chọn xóa/hủy file/kết quả cũ để làm sạch giao diện hoặc thử lại từ đầu, buộc người dùng phải chọn file khác đè lên (P5 phản ánh).
3. **Kích thước phông chữ của bảng xem trước (preview table) quá nhỏ:** Phông chữ hiển thị dữ liệu xem trước CSV rất nhỏ, gây khó khăn cho việc kiểm tra nhanh và đối chiếu thông tin trước khi bấm import (P1, P3 phản ánh).
4. **Bảng xem trước ở trạng thái Read-only:** Không cho phép người dùng click đúp hoặc chỉnh sửa trực tiếp các ô dữ liệu bị thiếu/lỗi trên bảng xem trước để sửa nhanh trước khi bấm Import (P5 đề xuất).
5. **Hiện tượng lag nhẹ khi cuộn bảng xem trước:** Đây là lỗi nhỏ có thể do mạng hoặc cấu hình máy, không ảnh hưởng đáng kể nên em sẽ không liệt kê vào bug report.
