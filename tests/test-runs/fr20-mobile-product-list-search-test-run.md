# Test Run - FR-20 Mobile Product List & Search

__Ngày thực hiện__: [dd/mm/yyyy]  
__Người thực hiện__: [Tên người test]  
__Môi trường thử nghiệm__: [Local API backend http://localhost:3000, Expo/Frontend Mobile on iOS/Android simulator or real device]

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Product List Display | 3 | 0 | 3 | 3 | 0 |
| Search Keyword | 4 | 7 | 11 | 11 | 0 |
| Empty Search Result | 1 | 0 | 1 | 1 | 0 |
| Search Safety | 3 | 0 | 3 | 2 | 1 |
| **Tổng** | **11** | **7** | **18** | **17** | **1** |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR20-L-TC01](../test-cases/mobile_product_list_search/FR20-L-TC01.md) | Mobile Product List & Search - Product List Display | Đặng Trường Nguyên | Passed | None | Danh sách sản phẩm được hiển thị đúng cách. |
| [FR20-L-TC02](../test-cases/mobile_product_list_search/FR20-L-TC02.md) | Mobile Product List & Search - Product List Display | Đặng Trường Nguyên | Passed | None | Danh sách sản phẩm được hiển thị đúng cách. |
| [FR20-L-TC03](../test-cases/mobile_product_list_search/FR20-L-TC03.md) | Mobile Product List & Search - Product List Display | Đặng Trường Nguyên | Passed | None | `Đang tải...` được hiển thị khi danh sách đang tải, sau khi tải xong thì danh sách sản phẩm sẽ được hiển thị thay thế cho nó. |
| [FR20-S-TC01](../test-cases/mobile_product_list_search/FR20-S-TC01.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Sản phẩm có từ khóa `Iphone` được hiển thị. |
| [FR20-S-TC02](../test-cases/mobile_product_list_search/FR20-S-TC02.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Sản phẩm có từ khóa `Samsung` được hiển thị. |
| [FR20-S-TC03](../test-cases/mobile_product_list_search/FR20-S-TC03.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Danh sách toàn bộ sản phẩm được hiển thị. |
| [FR20-S-TC04](../test-cases/mobile_product_list_search/FR20-S-TC04.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Không sản phẩm nào được hiển thị. |
| [FR20-E-TC01](../test-cases/mobile_product_list_search/FR20-E-TC01.md) | Mobile Product List & Search - Empty Search Result | Đặng Trường Nguyên | Passed | None | Không sản phẩm nào được hiển thị. |
| [FR20-X-TC01](../test-cases/mobile_product_list_search/FR20-X-TC01.md) | Mobile Product List & Search - Search Safety | Đặng Trường Nguyên | Passed | None | Không sản phẩm nào được hiển thị, không script nào được thực thi. |
| [FR20-X-TC02](../test-cases/mobile_product_list_search/FR20-X-TC02.md) | Mobile Product List & Search - Search Safety | Đặng Trường Nguyên | Passed | None | Không sản phẩm nào được hiển thị, không script nào được thực thi. |
| [FR20-X-TC03](../test-cases/mobile_product_list_search/FR20-X-TC03.md) | Mobile Product List & Search - Search Safety | Đặng Trường Nguyên | Failed | BUG-FR20-X-01 - SQL injection qua từ khóa tìm kiếm trả về toàn bộ danh sách sản phẩm | Danh sách toàn bộ sản phẩm được hiển thị. |
| [FR20-S-BVA-TC01](../test-cases/mobile_product_list_search/FR20-S-BVA-TC01.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Danh sách toàn bộ sản phẩm được hiển thị. |
| [FR20-S-BVA-TC02](../test-cases/mobile_product_list_search/FR20-S-BVA-TC02.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Danh sách sản phẩm có từ khóa `i` được hiển thị. |
| [FR20-S-BVA-TC03](../test-cases/mobile_product_list_search/FR20-S-BVA-TC03.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Danh sách sản phẩm có từ khóa `ip` được hiển thị. |
| [FR20-S-BVA-TC04](../test-cases/mobile_product_list_search/FR20-S-BVA-TC04.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Không sản phẩm nào với từ khóa `iphone pro max query` được hiển thị.` |
| [FR20-S-BVA-TC05](../test-cases/mobile_product_list_search/FR20-S-BVA-TC05.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Không sản phẩm nào với từ khóa `(254 chữ a)` được hiển thị. |
| [FR20-S-BVA-TC06](../test-cases/mobile_product_list_search/FR20-S-BVA-TC06.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Danh sách sản phẩm có từ khóa `(255 chữ a)` được hiển thị. |
| [FR20-S-BVA-TC07](../test-cases/mobile_product_list_search/FR20-S-BVA-TC07.md) | Mobile Product List & Search - Search Keyword | Đặng Trường Nguyên | Passed | None | Danh sách sản phẩm có từ khóa `(256 chữ a)` được hiển thị. |

## Defect Log

Sau khi chạy test, cập nhật các test case `Fail` vào bảng dưới đây hoặc map sang bug report riêng.

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR20-X-01 | FR20-X-TC03 | SQL injection qua từ khóa tìm kiếm làm API trả về toàn bộ danh sách sản phẩm. | High | Open | Actual: danh sách toàn bộ sản phẩm được hiển thị. Evidence bổ sung sau. |
