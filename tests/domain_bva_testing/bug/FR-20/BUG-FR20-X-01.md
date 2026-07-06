## BUG-FR20-X-01 - SQL injection qua từ khóa tìm kiếm trả về toàn bộ danh sách sản phẩm

**GitHub issue title:** `[BUG][FR-20][Mobile Product Search][Security] SQL injection qua từ khóa tìm kiếm trả về toàn bộ danh sách sản phẩm`

**GitHub issue:** [#146](https://github.com/trngnneee/eshop-sut/issues/146)

**Labels:** `type: bug`, `status: new`, `found-by: test-case`, `security`

## Found by Test Case

- `FR20-X-TC03`
- Path: `eshop-sut/tests/test-cases/mobile_product_list_search/FR20-X-TC03.md`

## Requirement liên quan

- `FR-20`
- Mobile có chức năng xem sản phẩm.
- Hành vi danh sách/tìm kiếm sản phẩm kế thừa `FR-05`: thanh tìm kiếm tìm theo tên sản phẩm.
- Search payload không được làm truy vấn trả về toàn bộ sản phẩm ngoài tiêu chí tên sản phẩm.
- Source: `eshop-sut/README.md`
- Source: `eshop-sut/api_specification.md`

## Severity / Priority

Critical / P0

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser/Runtime**: Expo mobile app on simulator or real device
- **URL**: `http://localhost:3000/api/products?search=%25'%20OR%20'1'%3D'1`
- **Build/Commit**: Latest

## Steps to reproduce

1. Chạy backend API và mobile app.
2. Bảo đảm database có nhiều sản phẩm seed để phát hiện trường hợp kết quả bị broaden.
3. Mở màn hình `Danh sách sản phẩm` trên mobile app.
4. Nhập `%' OR '1'='1` vào ô tìm kiếm.
5. Bấm `Tìm`.
6. Quan sát danh sách sản phẩm được trả về/hiển thị.

## Expected result

- Backend xử lý từ khóa bằng parameterized query hoặc escape an toàn.
- Payload SQL-like không làm truy vấn trả về toàn bộ sản phẩm ngoài tiêu chí tên sản phẩm.
- Mobile app không hiển thị dữ liệu sai phạm vi.

## Actual result

- Danh sách toàn bộ sản phẩm được hiển thị.

## Technical note

- Route `GET /api/products` hiện build SQL bằng string interpolation với `searchQuery`, nên payload SQL-like có thể làm điều kiện `LIKE` bị broaden.
- Code path: `eshop-sut/backend/server.js`

## Evidence

<img width="946" height="2047" alt="Image" src="https://github.com/user-attachments/assets/851d7ff2-7fcd-4ff5-adb2-0fd43fcc5510" />
