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

### Refactor Postman/Newman sang luồng data-driven chính

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 04:18:07 +07
- **Your prompt**:

  Oke và bây giờ sửa theo một hướng clean, data driven hơn. Sẽ có một file json chứa các thông tin của test-case: `test-data.json` -> Postman Collection -> đọc từng record ở mỗi iteration -> gửi request tương ứng -> assert expected result -> Newman report.

- **The AI output**:

  Đã cập nhật `API-testing/build_common_postman_collection.js` để sinh `API-testing/data/test-data.json` chứa các record test case và `API-testing/eshop_data_driven.postman_collection.json` chứa một request runner đọc từng record qua iteration data. Hai record đầu trong `test-data.json` đăng nhập seed admin/user và lưu `adminToken`/`userToken`; các record sau gửi request theo `method`, `path`, `headers`, `body` và assert theo `expectedStatus`. Đã sửa workflow CI để chạy collection data-driven bằng `--iteration-data API-testing/data/test-data.json` và xuất `newman-eshop-api-report.html`; cập nhật README theo flow mới.
