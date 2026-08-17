# Báo Cáo Tổng Kết Kiểm Thử - EShop SUT

## 1. Mục đích tài liệu

Tài liệu này tổng hợp các hoạt động kiểm thử đã thực hiện trên repository `trngnneee/eshop-sut` cho bốn nhánh cá nhân `HW2-Bao`, `HW3-Bao`, `HW4-Bao` và `HW5-Bao`. Báo cáo được viết theo cấu trúc Test Summary Report của SoftwareTestingHelp: nêu mục đích, tổng quan ứng dụng, phạm vi kiểm thử, số liệu thực thi, loại kiểm thử, môi trường/công cụ, bài học kinh nghiệm, khuyến nghị, thực hành tốt, tiêu chí kết thúc và kết luận.

Theo yêu cầu, phần lỗi chỉ tính các GitHub issue trong repository có tác giả là tài khoản `giabao1509`. Các bug report nội bộ trong từng nhánh vẫn được dùng như bằng chứng phụ, nhưng số lượng lỗi chính trong báo cáo này bám theo GitHub issue.

## 2. Tổng quan ứng dụng

EShop SUT là hệ thống thương mại điện tử demo phục vụ môn Kiểm thử phần mềm. Hệ thống gồm backend API, frontend web khách hàng, frontend quản trị và ứng dụng mobile. Các chức năng chính bao gồm đăng ký/đăng nhập, xem/tìm kiếm sản phẩm, giỏ hàng, thanh toán, mã giảm giá, lịch sử đơn hàng, quản lý sản phẩm, quản lý người dùng và một số luồng mobile.

| Mục | Giá trị |
|---|---|
| Repository | `https://github.com/trngnneee/eshop-sut` |
| Các nhánh được tổng hợp | `HW2-Bao`, `HW3-Bao`, `HW4-Bao`, `HW5-Bao` |
| Sinh viên | Nguyễn Thanh Gia Bảo - `23127158` |
| Công nghệ chính | Node.js, Express, SQLite, React/Vite, React Native/Expo |
| Backend URL dùng trong HW5 | `http://localhost:3000` |

## 3. Phạm vi kiểm thử

### 3.1 Trong phạm vi

| Nhánh | Commit cuối được kiểm tra | Phạm vi kiểm thử chính | Bằng chứng chính |
|---|---|---|---|
| `HW2-Bao` | `640918f` | Thiết kế và thực thi kiểm thử thủ công bằng Domain Testing, Boundary Value Analysis, Decision Table/Pairwise, State Transition và Use Case Testing. | `23127158/Test Summary Report.md`, `docs/main-report/main-report.md`, test case và bug artifacts. |
| `HW3-Bao` | `2262d7f` | Kiểm thử GUI checklist, usability evaluation với 7 người tham gia, kiểm tra cross-browser/cross-platform. | `hw03_gui_checklist/eshop_selected_screens/main_report.md`, screenshot, video, session notes và bug reports. |
| `HW4-Bao` | `5b4410d` | Tự động hóa kiểm thử Playwright cho FR-05, FR-11 và FR-19 trên Chromium, Firefox và WebKit. | `hw04-automation/docs/report.md`, Playwright HTML report, test script và bug reports. |
| `HW5-Bao` | `ea85636` | Kiểm thử hiệu năng bằng JMeter với Load, Stress, Spike và Soak/Endurance test. | `23127158/README.md`, `23127158/reports/HW05_Main_Report.md`, JTL, HTML report và ảnh evidence. |

### 3.2 Ngoài phạm vi

Các nhánh không thuộc mẫu `HWX-Bao` với `2 <= X <= 5` không được tổng hợp. Pull request, commit từ nhánh khác và GitHub issue không phải do `giabao1509` tạo không được tính vào defect summary.

### 3.3 Hạng mục chưa kiểm thử trong báo cáo này

| Hạng mục | Lý do |
|---|---|
| Các nhánh của thành viên khác | Yêu cầu chỉ tổng hợp `HW2-Bao` đến `HW5-Bao`. |
| Trạng thái sửa lỗi sau khi issue được mở | Các issue hiện đang mở; báo cáo này không xác nhận lỗi đã được sửa nếu chưa có bằng chứng đóng issue hoặc lần chạy hồi quy. |
| Kiểm thử production/staging thật | Các bài tập chủ yếu thực hiện trên môi trường local và evidence trong repository. |
| Kiểm thử bảo mật chuyên sâu độc lập | Một số lỗi security được phát hiện qua functional/automation testing, nhưng không có security audit chuyên dụng. |

## 4. Chỉ số kiểm thử

### 4.1 Tổng hợp chỉ số theo template

#### 4.1.1 Số test case kế hoạch so với đã thực thi

| Nhánh | Loại hạng mục kiểm thử | Kế hoạch | Đã thực thi | Tỷ lệ thực thi |
|---|---|---:|---:|---:|
| `HW2-Bao` | Test case thủ công | 118 | 118 | 100% |
| `HW3-Bao` | Tiêu chí GUI checklist | 52 | 52 | 100% |
| `HW4-Bao` | Test case tự động Playwright | 45 | 45 | 100% |
| `HW5-Bao` | Kịch bản kiểm thử hiệu năng | 4 | 4 | 100% |
| **Tổng hạng mục kiểm thử chính** |  | **219** | **219** | **100%** |

Ghi chú: HW3 còn có 7 phiên đánh giá usability với người tham gia thật. Các phiên này được tính riêng ở mục chi tiết vì đây là phiên đánh giá trải nghiệm, không phải test case truyền thống.

#### 4.1.2 Số test case đạt/không đạt

| Nhánh | Hạng mục kiểm thử | Đạt | Không đạt / vấn đề quan sát | Tỷ lệ đạt |
|---|---|---:|---:|---:|
| `HW2-Bao` | Test case thủ công | 73 | 45 | 61,86% |
| `HW3-Bao` | Tiêu chí GUI checklist | 31 | 21 | 59,62% |
| `HW4-Bao` | Test case tự động Playwright | 32 | 13 | 71,11% |
| `HW5-Bao` | Kịch bản kiểm thử hiệu năng | 4 | 0 lỗi chức năng | 100% |
| **Tổng hạng mục kiểm thử chính** |  | **140** | **79** | **63,93%** |

#### 4.1.3 Tổng defect theo trạng thái và mức độ nghiêm trọng

| Mức độ nghiêm trọng | Đang mở | Đã đóng | Tổng |
|---|---:|---:|---:|
| Critical | 8 | 0 | 8 |
| Major | 22 | 0 | 22 |
| Minor | 17 | 0 | 17 |
| **Tổng cộng** | **47** | **0** | **47** |

Nguồn: 47 GitHub issue trong repository `trngnneee/eshop-sut` có author `giabao1509`. Mức độ nghiêm trọng được trích từ trường `Severity / Priority` trong body của từng issue; trạng thái hiện tại của toàn bộ 47 issue là `đang mở`.

#### 4.1.4 Phân bố defect theo module

| Phân hệ / chủ đề | Critical | Major | Minor | Tổng |
|---|---:|---:|---:|---:|
| Danh sách/tìm kiếm sản phẩm | 2 | 4 | 8 | 14 |
| Lịch sử đơn hàng / trạng thái đơn / đơn hàng mobile | 1 | 2 | 3 | 6 |
| Quản lý người dùng / phân quyền admin | 4 | 3 | 0 | 7 |
| Giỏ hàng / giao diện thanh toán | 0 | 2 | 2 | 4 |
| Quản lý sản phẩm admin / CSV / form UX | 1 | 8 | 2 | 11 |
| Mobile / cross-platform | 0 | 1 | 1 | 2 |
| Hiệu năng | 0 | 2 | 1 | 3 |
| **Tổng cộng** | **8** | **22** | **17** | **47** |

Các bảng trên là phần tổng hợp chính theo bước 4 - chỉ số kiểm thử của template. Các mục bên dưới giữ lại số liệu chi tiết theo nhánh/kịch bản để hỗ trợ truy vết.

### 4.2 Chỉ số nhánh và commit

| Nhánh | Số commit | SHA cuối | Ngày commit cuối | Trạng thái bảo vệ nhánh |
|---|---:|---|---|---|
| `HW2-Bao` | 35 | `640918f7db01e9b70004c4a7097a012ad16b019e` | 2026-07-20 | Không bảo vệ |
| `HW3-Bao` | 23 | `2262d7f032f1ab5acf0d9e60712c84f829ae0cb2` | 2026-08-02 | Không bảo vệ |
| `HW4-Bao` | 26 | `5b4410d726a05f206751709e100f4a036e795255` | 2026-08-09 | Không bảo vệ |
| `HW5-Bao` | 31 | `ea856363e02cf3f59386dfe27e9006e93d47fe18` | 2026-08-16 | Không bảo vệ |
| **Tổng cộng** | **115** |  |  |  |

### 4.3 Số lượng test case kế hoạch và đã thực thi

| Nhánh | Đơn vị đo | Kế hoạch / thiết kế | Đã thực thi | Ghi chú |
|---|---|---:|---:|---|
| `HW2-Bao` | Test case thủ công thuộc phần Nguyễn Thanh Gia Bảo | 118 | 118 | Bao phủ FR03, FR05, FR10, FR11, FR19, FR20. |
| `HW3-Bao` | Tiêu chí GUI checklist | 52 | 52 | Vượt yêu cầu tối thiểu 40 tiêu chí. |
| `HW3-Bao` | Phiên usability | 7 người tham gia | 7 phiên | Tính điểm SUS và tổng hợp pain point. |
| `HW4-Bao` | Unique automated test case | 45 | 45 | Chạy trên Chromium, Firefox và WebKit. |
| `HW5-Bao` | Scenario hiệu năng | 4 | 4 | Load, Stress, Spike, Soak/Endurance. |

### 4.4 Kết quả pass/fail

| Nhánh | Đơn vị đo | Đạt | Không đạt / vấn đề quan sát | Tỷ lệ đạt |
|---|---|---:|---:|---:|
| `HW2-Bao` | Test case thủ công | 73 | 45 | 61,86% |
| `HW3-Bao` | GUI checklist items | 31 | 21 | 59,62% |
| `HW3-Bao` | Usability sessions | N/A | SUS trung bình 50,4/100, Grade F/Poor | N/A |
| `HW4-Bao` | Unique automated test case | 32 | 13 | 71,11% |
| `HW5-Bao` | Scenario hiệu năng | 4 | 0 lỗi chức năng; 3 performance issues | 100% theo lỗi chức năng |

### 4.5 Chi tiết tự động hóa HW4

| Chức năng | TC duy nhất | Đạt | Không đạt | Trình duyệt |
|---|---:|---:|---:|---|
| FR-05 Danh sách và tìm kiếm sản phẩm | 17 | 7 | 10 | Chromium, Firefox, WebKit |
| FR-11 Xem lịch sử đơn hàng | 14 | 14 | 0 | Chromium, Firefox, WebKit |
| FR-19 Quản lý người dùng admin | 14 | 11 | 3 | Chromium, Firefox, WebKit |
| **Tổng cộng** | **45** | **32** | **13** | 3 trình duyệt |

### 4.6 Chi tiết hiệu năng HW5

| Kịch bản | Số mẫu | Tỷ lệ lỗi | p95 | p99 | Thông lượng |
|---|---:|---:|---:|---:|---:|
| Load | 16.714 | 0,0% | 6,0 ms | 9,0 ms | 35,061 req/s |
| Stress | 107.203 | 0,0% | 8,0 ms | 13,0 ms | 179,655 req/s |
| Spike | 88.157 | 0,0% | 10,0 ms | 16,0 ms | 184,866 req/s |
| Soak / Endurance | 189.818 | 0,0% | 40,0 ms | 71,0 ms | 218,751 req/s |
| **Tổng cộng** | **401.892** |  |  |  |  |

### 4.7 Tổng hợp defect theo trạng thái và nhánh

| Nhánh tương ứng | Quy tắc tính defect | Số GitHub issue | Trạng thái |
|---|---|---:|---|
| `HW2-Bao` | Issue do `giabao1509` tạo trong giai đoạn 2026-06-25 đến 2026-06-28 | 19 | 19 đang mở |
| `HW3-Bao` | Issue do `giabao1509` tạo trong giai đoạn 2026-07-30 đến 2026-08-02 | 22 | 22 đang mở |
| `HW4-Bao` | Issue do `giabao1509` tạo ngày 2026-08-09 | 3 | 3 đang mở |
| `HW5-Bao` | Issue do `giabao1509` tạo ngày 2026-08-16 | 3 | 3 đang mở |
| **Tổng cộng** |  | **47** | **47 đang mở** |

### 4.8 Phân bố defect theo module/chủ đề

| Phân hệ / chủ đề | Issue liên quan | Số lượng |
|---|---|---:|
| Danh sách/tìm kiếm sản phẩm | #25, #26, #27, #28, #29, #30, #53, #60, #250, #260, #261, #299, #330, #331 | 14 |
| Order history / order state / mobile order | #64, #65, #154, #155, #332, #412 | 6 |
| User management / admin authorization | #147, #148, #149, #150, #151, #152, #153 | 7 |
| Cart / checkout UI | #249, #252, #262, #283 | 4 |
| Admin product / CSV / form UX | #251, #253, #254, #255, #256, #257, #258, #263, #284, #289, #290 | 11 |
| Mobile / cross-platform | #264, #300 | 2 |
| Hiệu năng | #410, #411, #412 | 3 |
| **Tổng cộng** |  | **47** |

## 5. Các loại kiểm thử đã thực hiện

| Nhánh | Loại kiểm thử | Mô tả |
|---|---|---|
| `HW2-Bao` | Kiểm thử chức năng thủ công theo kỹ thuật thiết kế test | Thiết kế và chạy test case bằng Domain Testing, BVA, Decision Table/Pairwise, State Transition và Use Case Testing để kiểm tra các yêu cầu chức năng trọng yếu. |
| `HW3-Bao` | Kiểm thử GUI và usability | Dùng GUI checklist để kiểm tra giao diện, sau đó thực hiện usability evaluation với 7 người tham gia và tính SUS score. |
| `HW3-Bao` | Kiểm thử cross-browser/cross-platform | Kiểm tra một số màn hình/luồng trên trình duyệt và mobile để phát hiện khác biệt hiển thị/trải nghiệm. |
| `HW4-Bao` | Kiểm thử tự động hồi quy | Dùng Playwright để chạy lại các test case cho FR-05, FR-11 và FR-19 trên nhiều trình duyệt. |
| `HW4-Bao` | Kiểm thử API/UI kết hợp | Một số test kiểm tra cả hành vi UI và API, đặc biệt ở quyền admin và dữ liệu lịch sử đơn hàng. |
| `HW5-Bao` | Kiểm thử hiệu năng | Dùng JMeter để chạy Load, Stress, Spike và Soak/Endurance test trên workflow mua hàng và đọc lịch sử đơn hàng. |

## 6. Môi trường và công cụ kiểm thử

| Nhóm | Môi trường / công cụ |
|---|---|
| Quản lý mã nguồn | GitHub repository `trngnneee/eshop-sut`, các nhánh `HW2-Bao` đến `HW5-Bao`. |
| Thiết kế test thủ công | Markdown test case, checklist, bug-report template, AI-assisted test design artifacts. |
| GUI/usability | GUI checklist workbook, screenshot/video evidence, session notes, SUS scoring. |
| Tự động hóa | Playwright, Chromium, Firefox, WebKit, Playwright HTML reporter. |
| Hiệu năng | Apache JMeter 5.6.3, raw `.jtl`, JMeter HTML dashboard, screenshot theo dõi resource. |
| SUT local | Backend Node.js/Express/SQLite; trong HW5 chạy tại `http://localhost:3000`. |

## 7. Tổng hợp lỗi

### 7.1 Danh sách issue theo nhánh

| Nhánh tương ứng | GitHub issue |
|---|---|
| `HW2-Bao` | #25, #26, #27, #28, #29, #30, #53, #60, #64, #65, #147, #148, #149, #150, #151, #152, #153, #154, #155 |
| `HW3-Bao` | #249, #250, #251, #252, #253, #254, #255, #256, #257, #258, #259, #260, #261, #262, #263, #264, #283, #284, #289, #290, #299, #300 |
| `HW4-Bao` | #330, #331, #332 |
| `HW5-Bao` | #410, #411, #412 |

### 7.2 Chi tiết issue

| Issue | Nhánh | Tóm tắt | Trạng thái |
|---|---|---|---|
| [#25](https://github.com/trngnneee/eshop-sut/issues/25) | HW2 | Giá sản phẩm không hiển thị đúng định dạng tiền tệ Việt Nam | Đang mở |
| [#26](https://github.com/trngnneee/eshop-sut/issues/26) | HW2 | Hình ảnh sản phẩm lỗi không hiển thị nội dung thay thế | Đang mở |
| [#27](https://github.com/trngnneee/eshop-sut/issues/27) | HW2 | Trang hiển thị màn hình trắng khi đang tải dữ liệu | Đang mở |
| [#28](https://github.com/trngnneee/eshop-sut/issues/28) | HW2 | Không hiển thị thông báo khi danh sách sản phẩm trống | Đang mở |
| [#29](https://github.com/trngnneee/eshop-sut/issues/29) | HW2 | Trang chủ chứa nhiều hơn một thẻ h1 | Đang mở |
| [#30](https://github.com/trngnneee/eshop-sut/issues/30) | HW2 | Trang kết quả tìm kiếm chứa nhiều hơn một thẻ h1 | Đang mở |
| [#53](https://github.com/trngnneee/eshop-sut/issues/53) | HW2 | Chức năng tìm kiếm không sanitize input dẫn đến XSS vulnerability | Đang mở |
| [#60](https://github.com/trngnneee/eshop-sut/issues/60) | HW2 | Chức năng tìm kiếm không xử lý input đặc biệt dẫn đến SQL Injection vulnerability | Đang mở |
| [#64](https://github.com/trngnneee/eshop-sut/issues/64) | HW2 | API lịch sử đơn hàng bỏ qua tham số phân trang | Đang mở |
| [#65](https://github.com/trngnneee/eshop-sut/issues/65) | HW2 | API xem chi tiết đơn hàng không yêu cầu xác thực người dùng | Đang mở |
| [#147](https://github.com/trngnneee/eshop-sut/issues/147) | HW2 | User thường có thể truy cập API quản lý người dùng của Admin | Đang mở |
| [#148](https://github.com/trngnneee/eshop-sut/issues/148) | HW2 | Admin có thể tự xóa chính tài khoản đang đăng nhập | Đang mở |
| [#149](https://github.com/trngnneee/eshop-sut/issues/149) | HW2 | API xóa người dùng trả về thành công khi user_id không tồn tại | Đang mở |
| [#150](https://github.com/trngnneee/eshop-sut/issues/150) | HW2 | API xóa người dùng chấp nhận user_id không hợp lệ và trả về thành công | Đang mở |
| [#151](https://github.com/trngnneee/eshop-sut/issues/151) | HW2 | Trang quản lý người dùng không có phân trang khi hiển thị nhiều tài khoản | Đang mở |
| [#152](https://github.com/trngnneee/eshop-sut/issues/152) | HW2 | User thường có thể xóa tài khoản khác thông qua API Admin | Đang mở |
| [#153](https://github.com/trngnneee/eshop-sut/issues/153) | HW2 | Xóa người dùng có dữ liệu liên quan nhưng không xử lý dữ liệu liên kết | Đang mở |
| [#154](https://github.com/trngnneee/eshop-sut/issues/154) | HW2 | Trạng thái đơn hàng không có màu sắc phân biệt trên ứng dụng Mobile | Đang mở |
| [#155](https://github.com/trngnneee/eshop-sut/issues/155) | HW2 | Không hiển thị dialog xác nhận trước khi hủy đơn hàng trên Mobile | Đang mở |
| [#249](https://github.com/trngnneee/eshop-sut/issues/249) | HW3 | Nhãn tổng tiền hiển thị "Tổng tạm tính" thay vì "Tổng cộng" | Đang mở |
| [#250](https://github.com/trngnneee/eshop-sut/issues/250) | HW3 | Ô số lượng chi tiết sản phẩm không chặn giá trị âm, thập phân hoặc chữ | Đang mở |
| [#251](https://github.com/trngnneee/eshop-sut/issues/251) | HW3 | Form thêm/sửa sản phẩm không đánh dấu ký tự (*) cho các trường bắt buộc | Đang mở |
| [#252](https://github.com/trngnneee/eshop-sut/issues/252) | HW3 | Không có hộp thoại xác nhận khi xóa sản phẩm khỏi giỏ hàng | Đang mở |
| [#253](https://github.com/trngnneee/eshop-sut/issues/253) | HW3 | Form Admin không kiểm tra độ dài Tên sản phẩm và hiển thị lỗi bằng alert | Đang mở |
| [#254](https://github.com/trngnneee/eshop-sut/issues/254) | HW3 | Form Admin cho phép lưu Giá sản phẩm rỗng, 0 hoặc số âm mà không chặn ở giao diện | Đang mở |
| [#255](https://github.com/trngnneee/eshop-sut/issues/255) | HW3 | Không có hộp thoại xác nhận trước khi xóa sản phẩm | Đang mở |
| [#256](https://github.com/trngnneee/eshop-sut/issues/256) | HW3 | Form Admin thiếu xem trước ảnh và kiểm tra định dạng URL ảnh sản phẩm | Đang mở |
| [#257](https://github.com/trngnneee/eshop-sut/issues/257) | HW3 | Import sản phẩm từ CSV không kiểm tra định dạng file | Đang mở |
| [#258](https://github.com/trngnneee/eshop-sut/issues/258) | HW3 | Phân tích CSV sai khi trường nội dung có chứa dấu phẩy trong dấu ngoặc kép | Đang mở |
| [#259](https://github.com/trngnneee/eshop-sut/issues/259) | HW3 | Thiếu breadcrumb điều hướng trên trang chi tiết sản phẩm và trang giỏ hàng | Đang mở |
| [#260](https://github.com/trngnneee/eshop-sut/issues/260) | HW3 | Khi sản phẩm không tồn tại, UI hiển thị chuỗi debug thô thay vì thông báo lỗi thân thiện | Đang mở |
| [#261](https://github.com/trngnneee/eshop-sut/issues/261) | HW3 | Nút "Thêm vào giỏ hàng" yêu cầu bấm 2 lần mới có phản hồi | Đang mở |
| [#262](https://github.com/trngnneee/eshop-sut/issues/262) | HW3 | Giao diện giỏ hàng trống thiếu hình minh họa hoặc icon trực quan | Đang mở |
| [#263](https://github.com/trngnneee/eshop-sut/issues/263) | HW3 | Khi sửa một sản phẩm, danh sách admin cập nhật đè tên của tất cả sản phẩm khác | Đang mở |
| [#264](https://github.com/trngnneee/eshop-sut/issues/264) | HW3 | Khi API sản phẩm lỗi, màn hình hiển thị lỗi thô và không có nút Thử lại | Đang mở |
| [#283](https://github.com/trngnneee/eshop-sut/issues/283) | HW3 | Trang Giỏ hàng thiếu điều khiển tăng/giảm và không cho phép chỉnh sửa số lượng | Đang mở |
| [#284](https://github.com/trngnneee/eshop-sut/issues/284) | HW3 | Ô nhập Giá sản phẩm không tự động loại bỏ khoảng trắng và thông báo lỗi không rõ ràng | Đang mở |
| [#289](https://github.com/trngnneee/eshop-sut/issues/289) | HW3 | Giao diện thiếu chỉ báo Chế độ Sửa khi bấm nút Sửa sản phẩm | Đang mở |
| [#290](https://github.com/trngnneee/eshop-sut/issues/290) | HW3 | Form Admin thiếu thông báo phản hồi sau khi thêm hoặc sửa sản phẩm thành công | Đang mở |
| [#299](https://github.com/trngnneee/eshop-sut/issues/299) | HW3 | Badge số lượng trên navbar không cập nhật ngay sau khi thêm sản phẩm vào giỏ | Đang mở |
| [#300](https://github.com/trngnneee/eshop-sut/issues/300) | HW3 | Ảnh sản phẩm trên Expo Go không có alt text mô tả tên sản phẩm | Đang mở |
| [#330](https://github.com/trngnneee/eshop-sut/issues/330) | HW4 | Tìm kiếm không xử lý khoảng trắng đầu/cuối | Đang mở |
| [#331](https://github.com/trngnneee/eshop-sut/issues/331) | HW4 | Ảnh sản phẩm thiếu alt text mô tả | Đang mở |
| [#332](https://github.com/trngnneee/eshop-sut/issues/332) | HW4 | Đơn đang giao vẫn hiển thị nút hủy trong lịch sử | Đang mở |
| [#410](https://github.com/trngnneee/eshop-sut/issues/410) | HW5 | Spike peak 500 users làm tail latency tăng mạnh | Đang mở |
| [#411](https://github.com/trngnneee/eshop-sut/issues/411) | HW5 | Soak 300 users vượt latency guardrail dù không có lỗi | Đang mở |
| [#412](https://github.com/trngnneee/eshop-sut/issues/412) | HW5 | My Orders tail latency tăng dưới tải cao | Đang mở |

## 8. Bài học kinh nghiệm

1. HW2 cho thấy các kỹ thuật thiết kế test thủ công vẫn rất hữu ích để phát hiện khoảng trống chức năng, đặc biệt ở search, authorization, order history và mobile order.
2. HW3 cho thấy một hệ thống có thể chạy được về mặt chức năng nhưng vẫn tạo trải nghiệm kém nếu thiếu feedback, confirmation dialog, empty state, breadcrumb hoặc chỉ báo trạng thái rõ ràng. Điểm SUS 50,4/100 là dấu hiệu cần cải thiện UX.
3. HW4 cho thấy automation giúp xác nhận lỗi lặp lại trên nhiều trình duyệt và tách lỗi API/security khỏi lỗi selector/timing.
4. HW5 cho thấy error rate 0,0% không đủ để kết luận hệ thống hoàn toàn ổn; các chỉ số p95/p99 và peak-window latency vẫn cần được theo dõi.

## 9. Khuyến nghị

1. Ưu tiên xử lý các issue bảo mật và phân quyền: role bypass, self-delete, order detail authentication, XSS và SQL injection.
2. Chuẩn hóa regression suite cho FR-05, FR-11 và FR-19 vì các nhóm chức năng này xuất hiện lỗi xuyên suốt nhiều bài.
3. Bổ sung test case tự động tương ứng với từng GitHub issue đang mở để có thể xác nhận lỗi đã được sửa ở lần chạy sau.
4. Sửa các lỗi UX có ảnh hưởng cao: thao tác xóa không xác nhận, thiếu success feedback, thiếu edit-mode indicator, thiếu quantity control và empty state nghèo nàn.
5. Duy trì bộ performance guardrail từ HW5: error rate, p95/p99, throughput, Spike peak/recovery window, Checkout latency và My Orders latency.
6. Sau khi sửa lỗi, cần cập nhật trạng thái issue trên GitHub để báo cáo sau có thể phân biệt rõ lỗi đang mở, đã sửa, trùng lặp hoặc tạm hoãn.

## 10. Thực hành tốt

1. Artifact được tách theo nhánh bài tập, giúp truy vết phạm vi và evidence dễ hơn.
2. HW4 và HW5 có bằng chứng thực thi rõ ràng: Playwright HTML report, JMeter JTL, JMeter HTML report và screenshot resource.
3. Các bài sau có audit/human review cho output do AI hỗ trợ, giảm rủi ro dùng nhầm kết luận chưa kiểm chứng.
4. Bug/performance issue được liên kết với GitHub issue, giúp stakeholder theo dõi trạng thái sau khi báo cáo.
5. Cùng một SUT được kiểm tra bằng nhiều góc nhìn: chức năng, GUI, usability, automation và performance.

## 11. Tiêu chí kết thúc

| Tiêu chí | Kết quả | Ghi chú |
|---|---|---|
| Các nhánh `HW2-Bao` đến `HW5-Bao` tồn tại và đọc được | Đạt | GitHub branch API trả về đủ 4 nhánh. |
| Có evidence kiểm thử cho từng nhánh | Đạt | Các report, test case, screenshot, JTL và HTML report tồn tại trong repository. |
| Test case/scenario chính đã được thực thi | Đạt | HW2, HW3, HW4 và HW5 đều có kết quả thực thi. |
| Defect summary chỉ tính issue do `giabao1509` tạo | Đạt | Tìm thấy 47 GitHub issue phù hợp. |
| Không còn defect Critical/Major đang mở | Không đạt | Nhiều issue về bảo mật, phân quyền, UX và hiệu năng vẫn đang mở. |
| Sẵn sàng production/go-live | Không đạt | Báo cáo đủ cho mục tiêu học phần, nhưng SUT chưa nên coi là production-ready. |

## 12. Kết luận / phê duyệt

Các nhánh `HW2-Bao`, `HW3-Bao`, `HW4-Bao` và `HW5-Bao` cung cấp một bộ evidence kiểm thử khá rộng cho EShop SUT: từ thiết kế test thủ công, kiểm thử GUI/usability, automation đa trình duyệt đến kiểm thử hiệu năng. Về mặt học phần, các artifact đã thể hiện được quá trình kiểm thử, kết quả thực thi, lỗi phát hiện và đề xuất cải thiện.

Tuy nhiên, xét theo tiêu chí chất lượng sản phẩm, hệ thống chưa đạt điều kiện phát hành vì vẫn còn 47 GitHub issue do `giabao1509` tạo đang ở trạng thái mở. Trong đó có các vấn đề nghiêm trọng về phân quyền admin, khả năng tự xóa tài khoản, XSS, SQL injection, xác thực chi tiết đơn hàng, lỗi GUI/UX và tail latency dưới tải cao.

Kết luận: chấp nhận báo cáo như một test summary report cho phạm vi bài tập `HW2-Bao` đến `HW5-Bao`, nhưng chưa khuyến nghị phát hành sản phẩm nếu chưa sửa hoặc chính thức defer các issue quan trọng.

## 13. Định nghĩa, từ viết tắt

| Thuật ngữ | Ý nghĩa |
|---|---|
| SUT | System Under Test - hệ thống được kiểm thử |
| TC | Test Case |
| FR | Functional Requirement - yêu cầu chức năng |
| BVA | Boundary Value Analysis - phân tích giá trị biên |
| DT | Decision Table - bảng quyết định |
| PT | Pairwise Testing - kiểm thử cặp |
| ST | State Transition Testing - kiểm thử chuyển trạng thái |
| UC | Use Case Testing - kiểm thử theo ca sử dụng |
| SUS | System Usability Scale - thang đo usability |
| JTL | File log kết quả thô của JMeter |
| p95 / p99 | Percentile 95 / 99 của thời gian phản hồi |

## 14. Nguồn tham chiếu

- Repository được kiểm tra: `https://github.com/trngnneee/eshop-sut`
- Nhánh được tổng hợp: `HW2-Bao`, `HW3-Bao`, `HW4-Bao`, `HW5-Bao`
- GitHub issue filter: repository `trngnneee/eshop-sut`, issue author `giabao1509`
- Template tham chiếu: SoftwareTestingHelp - Test Summary Report Template, gồm các nhóm nội dung: mục đích tài liệu, tổng quan ứng dụng, phạm vi kiểm thử, chỉ số kiểm thử, loại kiểm thử đã thực hiện, môi trường và công cụ, bài học kinh nghiệm, khuyến nghị, thực hành tốt, tiêu chí kết thúc, kết luận/phê duyệt và định nghĩa/từ viết tắt.
