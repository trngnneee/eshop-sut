I use AI tools for the following tasks:

### Sửa Postman collection để tự lấy token đăng nhập

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 03:25:03 +07
- **Your prompt**:

  Tạo một API login để lấy token sẵn trong Postman collection.

- **The AI output**:

  Đã cập nhật `API-testing/build_common_postman_collection.js` để sinh folder `Auth - Get Tokens` ở đầu Postman collection, gồm request login admin lưu `adminToken` và request login user lưu `userToken` vào collection variables. Đã regenerate `API-testing/eshop_api.postman_collection.json` để các request admin coupon dùng token lấy sẵn trong collection.

### Sửa Postman collection để gán mã số sinh viên bằng Pre-request Script

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 03:36:59 +07
- **Your prompt**:

  Vậy hãy đổi lại sử dụng pre-request script để gán header mã số sinh viên.

- **The AI output**:

  Đã cập nhật `API-testing/build_common_postman_collection.js` để thêm collection-level Pre-request Script tự lấy `studentId` từ biến Postman và upsert header `X-Student-Id` trước mỗi request. Đã bỏ header `X-Student-Id` hard-code khỏi từng request, regenerate `API-testing/eshop_api.postman_collection.json`, và sửa workflow để Newman dùng environment file thay vì truyền `studentId` qua CLI.

### Thêm data-driven run cho Postman collection

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 03:42:26 +07
- **Your prompt**:

  Vậy hãy thêm data-driven cho collection này đi.

- **The AI output**:

  Đã thêm request data-driven `DP-DD - Áp dụng coupon bằng iteration data` vào đúng suite `FR-09 Apply Coupon > domain partitions`, dùng biến từ iteration data (`couponCode`, `totalAmount`, `userId`, `expectedStatus`, `expectedHasDiscount`). Đã tạo file `API-testing/data/apply_coupon_data.csv` gồm các dòng dữ liệu positive/negative cho apply-coupon, regenerate `API-testing/eshop_api.postman_collection.json`, và cập nhật `API-testing/README.md`.

### Tách Postman collection theo từng API

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 04:12:06 +07
- **Your prompt**:

  Tôi muốn tách ra 3 collection riêng ứng với 3 API để dễ quản lý.

- **The AI output**:

  Đã cập nhật `API-testing/build_common_postman_collection.js` để ngoài collection tổng `eshop_api.postman_collection.json` còn sinh thêm 3 collection riêng: `forgot_password.postman_collection.json`, `apply_coupon.postman_collection.json`, và `admin_coupons.postman_collection.json`. Đã cập nhật GitHub Actions workflow để chạy 3 collection riêng và upload các report HTML theo glob `API-testing/newman-*-report.html`; đồng thời cập nhật `API-testing/README.md` với lệnh Newman cho từng collection.

### Refactor apply-coupon collection sang data-driven

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 18:15:00 +07
- **Your prompt**:

  bạn hãy refactor file collection apply_coupon thử đi

- **The AI output**:

  Đã refactor `API-testing/apply_coupon.postman_collection.json` thành collection data-driven một request, chạy 49 test case qua `data/apply-coupon.test-data.json`, gồm 42 case AI-generated và 7 case human-extended `HT-APPLY-EXT-001..007`. Mỗi row dùng `testCaseId` để trace test case và field `assertions` để bật các assert sâu riêng như SQL leak, XSS echo, công thức `final_amount`, exact calculation, money bounds, preview no-side-effect, và chống client tự gửi `discount_amount`/`final_amount`. Đã thêm `API-testing/build_apply_coupon_data_driven_collection.js`, cập nhật `npm run apply`, và sửa README command tương ứng.

### Chuẩn hóa expectedStatus của apply-coupon theo CSV review

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 18:56:00 +07
- **Your prompt**:

  hiện file data có một số chỗ response code đang bị mơ hồ kìa hãy viết lại chuẩn theo file csv đi

- **The AI output**:

  Đã cập nhật builder `API-testing/build_apply_coupon_data_driven_collection.js` để đọc `API-testing/apply-coupon/test_cases_master.csv` và đồng bộ `expectedStatus`/`expectedResult` cho 49 row trong `data/apply-coupon.test-data.json`. Các status mơ hồ như `400 hoặc 404`, `200 hoặc 400`, `429 sau N...` đã được thay bằng mã cụ thể theo CSV; case BLOCKED giữ `N/A`. Đồng thời chỉnh một số request body đã được CSV audit chốt theo seed data như `EXPIRED`, `SAVE10` boundary, và public apply-coupon auth cases.

### Đối chiếu apply-coupon report với CSV và bug reports

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 19:07:00 +07
- **Your prompt**:

  Hãy so sánh kết quả của file apply-coupon-report-1.html với kết quả trong file apply-coupon/test-case-master.csv để xem có chỗ nào lệch không, nếu có thì sửa theo file html report. Sau đó đối chiếu các bug report và thống kê cho tôi những chỗ lệch đã sửa

- **The AI output**:

  Đã thêm script đối chiếu `API-testing/sync_apply_coupon_csv_with_report.js`, parse `API-testing/apply-coupon-report-1.html`, cập nhật `API-testing/apply-coupon/test_cases_master.csv` theo kết quả report, và đối chiếu các bug report `BUG-APPLY-COUPON-*.md`. Kết quả sửa chính: `TC-APPLY-COUPON-SEC-009` đổi `Status` từ `PASS` sang `FAIL`; bug tương ứng đã được bao phủ bởi `BUG-APPLY-COUPON-001-negative-discount-calculation.md`. Đồng thời quote lại field `Notes` của `HT-APPLY-EXT-007` vì có dấu phẩy để CSV không bị lệch cột.

### Sửa apply-coupon test cases dùng coupon ngoài seed data

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 19:17:00 +07
- **Your prompt**:

  Hiện tại trong file csv có một số cái incomplete và invalid bởi vì khi test thì nó apply coupon không tồn tại trong seed data vì vậy bạn hãy sửa những chô mà apply coupon không tồn tại đó thành coupon tồn tại. Bạn hãy đọc file README.md ở thư mục root đế biết rõ đặc tả hệ thống.

- **The AI output**:

  Đã đọc root `README.md` và xác nhận coupon seed hợp lệ cho FR-09 là `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`. Đã cập nhật `API-testing/apply-coupon/test_cases_master.csv`, `API-testing/data/apply-coupon.test-data.json`, và regenerate `API-testing/apply_coupon.postman_collection.json` để thay các case từng dùng coupon ngoài seed bằng coupon seed tương ứng. Các case state transition hết hạn/xóa/flash sale dùng `EXPIRED`; các case min-order/quota/parameter tampering/auth dùng `SAVE10`. Đồng thời sửa lại auth cases theo README.md vì FR-09 yêu cầu JWT hợp lệ.

### Đồng bộ Status CSV apply-coupon theo report mới

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 19:23:00 +07
- **Your prompt**:

  Đọc file apply-coupon-report.html vừa chạy và kiểm tra xem file csv có chỗ nào bị lệch status không nếu có thì đổi theo html và thống kê cho tôi biết

- **The AI output**:

  Đã cập nhật `API-testing/sync_apply_coupon_csv_with_report.js` để nhận tên report qua CLI và giữ các case `BLOCKED`/`expected_status=N/A` ở trạng thái blocked. Đã chạy đối chiếu `API-testing/apply-coupon-report.html` với `API-testing/apply-coupon/test_cases_master.csv`: report có 49 test cases, 31 failed, 1 skipped/blocked. Có 1 lệch status đã sửa: `TC-APPLY-COUPON-ST-008` đổi từ `FAIL` sang `PASS`; chạy lại script xác nhận không còn lệch status.

### Thêm auto-login lấy userToken cho apply-coupon collection

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 19:35:00 +07
- **Your prompt**:

  oke làm vậy đi

- **The AI output**:

  Đã cập nhật `API-testing/build_apply_coupon_data_driven_collection.js` để pre-request script tự gọi `POST /api/login` bằng seed user `test@eshop.com` / `Test1234!` khi iteration row dùng `authorization: "Bearer {{userToken}}"` và chưa có `userToken`. Token được lưu vào collection variable rồi gắn vào header `Authorization`; các row có `authorization` rỗng vẫn chạy không token để giữ no-auth/security cases. Đã regenerate `API-testing/apply_coupon.postman_collection.json`, giữ 49 rows trong `API-testing/data/apply-coupon.test-data.json`, cập nhật `API-testing/README.md`, và chạy `npm run apply` xác nhận auto-login hoạt động trong Newman report.

### Đối chiếu bug reports apply-coupon với danh sách test case

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 19:39:00 +07
- **Your prompt**:

  check lại các bug report coi có khớp với danh sách test case không

- **The AI output**:

  Đã thêm script `API-testing/check_apply_coupon_bug_coverage.js` để parse `API-testing/Bug/BUG-APPLY-COUPON-*.md`, `API-testing/apply-coupon/test_cases_master.csv`, và `API-testing/apply-coupon-report.html`. Lần kiểm đầu phát hiện không có ID lạ và không có bug nào trỏ tới PASS/BLOCKED, nhưng còn 5 failed test cases chưa được bug report cover. Đã bổ sung `TC-APPLY-COUPON-DP-016`, `TC-APPLY-COUPON-SEC-009`, `HT-APPLY-EXT-006` vào bug 001 và tạo `BUG-APPLY-COUPON-008-missing-auth-and-user-binding.md` cho `TC-APPLY-COUPON-SEC-003`, `TC-APPLY-COUPON-SEC-004`. Chạy lại checker xác nhận 31 failed test cases đều được cover bởi 8 bug reports, không còn lệch.

### Refactor forgot-password collection sang data-driven

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 19:46:00 +07
- **Your prompt**:

  Hãy refactor lại collection forgot-password giống với collection apply-coupon. Cũng xem file forgot-password/test-case-master.csv làm chuẩn.

- **The AI output**:

  Đã refactor `API-testing/forgot_password.postman_collection.json` thành collection data-driven một request template, sinh từ `API-testing/forgot-password/test_cases_master.csv` qua `API-testing/build_forgot_password_data_driven_collection.js`. Đã tạo `API-testing/data/forgot-password.test-data.json` gồm 45 rows, mỗi row có `testCaseId`, method/path/body, `expectedStatus`, `setupFlow`, và `assertions` riêng cho OTP format, schema, user enumeration, cache header, GET method confusion, reset-password state flows, OTP reuse, OTP binding, và weak password. Đã cập nhật `npm run forgot` và README để chạy với `--iteration-data`. Chạy `npm run forgot` xác nhận collection mới chạy đủ 45 iterations / 67 requests / 201 assertions; còn 25 failures phản ánh behavior lệch CSV/spec. Đã restore seed password `test@eshop.com` về `Test1234!` sau khi chạy.

### Chuẩn hóa format data-driven forgot-password và apply-coupon

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 20:15:00 +07
- **Your prompt**:

  sao file data của forgot-password có 2 cái không cần là "reviewStatus": "PASS", và "notes": vậy hãy làm file data giữa forgot-passworf và apply-coupon đồng nhất với nhau đi. Những cái nào cần thiết thì giữ và thống nhất format

- **The AI output**:

  Đã cập nhật `API-testing/build_forgot_password_data_driven_collection.js` để file runtime `API-testing/data/forgot-password.test-data.json` chỉ xuất các field cần cho data-driven Newman giống `apply-coupon`: `testCaseId`, metadata request, `expectedStatus`, `expectedResult`, `secId`, `attackVector`, và `assertions`; giữ riêng `setupFlow` vì forgot-password cần chuẩn bị OTP/reset-password theo từng case. Đã loại các field audit/review như `reviewStatus`, `validationStatus`, `notes` khỏi JSON runtime, normalize `expectedStatus` về number khi là HTTP code, regenerate `API-testing/data/forgot-password.test-data.json` và `API-testing/forgot_password.postman_collection.json`, đồng thời sửa extract `secId` để đọc đúng `SEC-01..SEC-07` từ CSV master.

### Tạo collection data-driven cho admin-coupons

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 21:25:00 +07
- **Your prompt**:

  Hãy tạo file collection cho admin-coupons. Đọc file test_cases_master.csv để hiểu các test cases. Xem format của các file data của 2 api khác. Vì luồng này cần token để test nên nhớ setup để lấy token.

- **The AI output**:

  Đã tạo collection data-driven `API-testing/admin_coupons.postman_collection.json` cho `POST /api/admin/coupons`, sinh từ `API-testing/admin-coupons/test_cases_master.csv` qua script `API-testing/build_admin_coupons_data_driven_collection.js`. Đã tạo `API-testing/data/admin-coupons.test-data.json` đủ 49 rows, đồng nhất format runtime với `apply-coupon` và `forgot-password`, không đưa các field audit như `sourceFile`, `priority`, `reviewStatus`, `notes`, `Audit`, `Status` vào data JSON. Collection có pre-request script tự login admin/user qua `POST /api/login`, lưu `adminToken` và `userToken`, đồng thời sinh token hết hạn và forged token cho security cases. Các case ngoài scope được set skipped để Newman report hiện `skipped` thay vì fail; đã thêm script `npm run admin` trong `API-testing/package.json`.
