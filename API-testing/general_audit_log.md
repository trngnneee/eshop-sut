I use AI tools for the following tasks:

### Sửa Postman collection để tự lấy token đăng nhập

- **AI tool**: Codex (GPT-5)
- **Date and time**: 2026-08-23 03:25:03 +07
- **Your prompt**:

  Tạo một API login để lấy token sẵn trong Postman collection.

- **The AI output**:

  Đã cập nhật `API-testing/build_common_postman_collection.js` để sinh folder `Auth - Get Tokens` ở đầu Postman collection, gồm request login admin lưu `adminToken` và request login user lưu `userToken` vào collection variables. Đã regenerate `API-testing/eshop_api.postman_collection.json` để các request admin coupon dùng token lấy sẵn trong collection.
