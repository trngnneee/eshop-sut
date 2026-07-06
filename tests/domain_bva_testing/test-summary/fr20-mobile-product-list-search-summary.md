# FR-20 - Mobile Product List & Search

## Nguồn yêu cầu

README.md, dòng 233-236:

- Mobile phải có chức năng Xem sản phẩm.

Yêu cầu chi tiết liên quan:

- README.md, dòng 73-79: danh sách sản phẩm, tìm kiếm theo tên, loading, empty state, hiển thị từ khóa an toàn.
- `api_specification.md`, dòng 80-82: endpoint `GET /api/products` và query tùy chọn `?search=keyword`.
- `frontend-mobile/App.js`, dòng 84-111: mobile gọi `GET /api/products?search=${query}` khi tải danh sách hoặc tìm kiếm.
- `frontend-mobile/App.js`, dòng 455-532: mobile render card sản phẩm, ô tìm kiếm, loading, danh sách và số lượng kết quả.

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | FR-20 mobile kế thừa hành vi chi tiết của FR-05 cho phần xem danh sách và tìm kiếm sản phẩm. | FR-20 chỉ liệt kê nhóm chức năng mobile, còn FR-05 mô tả rule cụ thể cho sản phẩm. |
| A2 | Search keyword rỗng là hợp lệ và dùng để lấy toàn bộ danh sách sản phẩm. | `api_specification.md` mô tả query `search` là tùy chọn. |
| A3 | Mobile dùng `GET /api/products?search=keyword` để tìm theo tên sản phẩm. | Được thể hiện trực tiếp trong `frontend-mobile/App.js`. |
| A4 | BVA dùng miền độ dài search keyword từ `0` đến `255` ký tự; `256` ký tự là vượt giới hạn kiểm thử. | README/API không nêu max length, nên đặt một giới hạn kiểm thử rõ ràng để áp dụng BVA. |
| A5 | Dữ liệu seed có ít nhất 5 sản phẩm mẫu. | `backend/database.js` seed các sản phẩm dùng để đối chiếu kết quả. |

## Input / Output Variables

| Variable | Loại | Ghi chú |
| :--- | :--- | :--- |
| `search` | User input | Từ khóa tìm kiếm nhập trong ô `Tìm kiếm...`. |
| `products` | API response / UI state | Mảng sản phẩm trả về từ `GET /api/products`. |
| `loadingProducts` | UI state | Điều khiển trạng thái `Đang tải...`. |
| `errorHtml` | UI state | Lỗi/string từ backend phải được hiển thị an toàn, không render HTML. |
| `imageUrl`, `name`, `price` | Product fields | Dữ liệu bắt buộc hiển thị trên card sản phẩm. |
| Endpoint/API | Interface | `GET /api/products`, `GET /api/products?search=keyword`. |
| Final UI state | Expected output | Danh sách, số lượng kết quả, empty state hoặc thông báo lỗi an toàn. |

## Equivalence Partitions

| Class ID | Domain Class | Representative Values | Expected Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| L-VALID-01 | Tải toàn bộ danh sách sản phẩm | `search = ""` | Accepted | Search query là tùy chọn. |
| L-VALID-02 | Card sản phẩm đủ field | `imageUrl`, `name`, `price` | Accepted | FR-05 yêu cầu hiển thị ảnh, tên và giá. |
| L-VALID-03 | Trạng thái loading | Request đang pending | Accepted | FR-05 yêu cầu hiển thị loading khi tải dữ liệu. |
| S-VALID-01 | Tìm kiếm khớp một phần tên | `iPhone` | Accepted | Search theo tên sản phẩm. |
| S-VALID-02 | Tìm kiếm chữ thường | `samsung` | Accepted | Từ khóa người dùng nhập thường không cố định chữ hoa/thường. |
| S-VALID-03 | Từ khóa rỗng sau lần search | `""` | Accepted | Xóa search phải quay lại toàn bộ danh sách. |
| S-INVALID-01 | Từ khóa đặc biệt không khớp | `@@@###` | Handled safely | Không được crash hoặc trả dữ liệu sai phạm vi. |
| E-EMPTY-01 | Không có kết quả | `ZZZ_NOT_FOUND_2026` | Empty state | FR-05 yêu cầu empty state phù hợp. |
| X-INVALID-01 | Từ khóa chứa script tag | `<script>alert(1)</script>` | Rendered safely | Từ khóa tìm kiếm phải hiển thị an toàn. |
| X-INVALID-02 | Từ khóa chứa HTML event handler | `<img src=x onerror=alert(1)>` | Rendered safely | Không được render HTML/event handler. |
| X-INVALID-03 | Payload SQL injection | `%' OR '1'='1` | Rejected / handled safely | Search chỉ được tìm theo tên sản phẩm, không broaden query. |

## Boundary Values

| Field | Boundary Type | Value | Expected Status | Test Case |
| :--- | :--- | :--- | :--- | :--- |
| `search` | Min | `0` ký tự | Accepted | FR20-S-BVA-TC01 |
| `search` | Min+1 | `1` ký tự | Accepted | FR20-S-BVA-TC02 |
| `search` | Min+2 | `2` ký tự | Accepted | FR20-S-BVA-TC03 |
| `search` | Nominal | `20` ký tự | Accepted | FR20-S-BVA-TC04 |
| `search` | Max-1 | `254` ký tự | Accepted | FR20-S-BVA-TC05 |
| `search` | Max | `255` ký tự | Accepted | FR20-S-BVA-TC06 |
| `search` | Max+1 | `256` ký tự | Rejected / handled safely | FR20-S-BVA-TC07 |

## Generated Test Case Index

| TC ID | Class / Boundary | Technique | Expected Status |
| :--- | :--- | :--- | :--- |
| FR20-L-TC01 | L-VALID-01 | Equivalence Partitioning | Accepted |
| FR20-L-TC02 | L-VALID-02 | Equivalence Partitioning | Accepted |
| FR20-L-TC03 | L-VALID-03 | Equivalence Partitioning | Accepted |
| FR20-S-TC01 | S-VALID-01 | Equivalence Partitioning | Accepted |
| FR20-S-TC02 | S-VALID-02 | Equivalence Partitioning | Accepted |
| FR20-S-TC03 | S-VALID-03 | Equivalence Partitioning | Accepted |
| FR20-S-TC04 | S-INVALID-01 | Equivalence Partitioning | Handled safely |
| FR20-E-TC01 | E-EMPTY-01 | Equivalence Partitioning | Empty state |
| FR20-X-TC01 | X-INVALID-01 | Equivalence Partitioning / Security | Rendered safely |
| FR20-X-TC02 | X-INVALID-02 | Equivalence Partitioning / Security | Rendered safely |
| FR20-X-TC03 | X-INVALID-03 | Equivalence Partitioning / Security | Rejected / handled safely |
| FR20-S-BVA-TC01 | `search` Min | Boundary Value Analysis | Accepted |
| FR20-S-BVA-TC02 | `search` Min+1 | Boundary Value Analysis | Accepted |
| FR20-S-BVA-TC03 | `search` Min+2 | Boundary Value Analysis | Accepted |
| FR20-S-BVA-TC04 | `search` Nominal | Boundary Value Analysis | Accepted |
| FR20-S-BVA-TC05 | `search` Max-1 | Boundary Value Analysis | Accepted |
| FR20-S-BVA-TC06 | `search` Max | Boundary Value Analysis | Accepted |
| FR20-S-BVA-TC07 | `search` Max+1 | Boundary Value Analysis | Rejected / handled safely |

## Generated Artifacts

| Artifact | Path |
| :--- | :--- |
| JSON config | `tests/test-configs/fr20-mobile-product-list-search-config.json` |
| Test cases | `tests/test-cases/mobile_product_list_search/` |
| Test run template | `tests/test-runs/fr20-mobile-product-list-search-test-run.md` |
| Traceability matrix | `tests/test-summary/traceability-matrix.md` |

## Count Summary

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC |
| :--- | ---: | ---: | ---: |
| Product List Display | 3 | 0 | 3 |
| Search Keyword | 4 | 7 | 11 |
| Empty Search Result | 1 | 0 | 1 |
| Search Safety | 3 | 0 | 3 |
| **Tổng** | **11** | **7** | **18** |
