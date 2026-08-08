# FR-05 - Review Locator/Page Object

File page object: `hw04-automation/tests/pages/ProductListingPage.js`

## Locator Được Tạo

| Thành phần | Locator | Nhận xét review |
|---|---|---|
| Tiêu đề chính | `page.locator("h1").first()` | Dùng để kiểm tra tiêu đề chính. Không match theo text vì source UI hiện tại có dấu hiệu lỗi encoding tiếng Việt. |
| Tất cả thẻ h1 | `page.locator("h1")` | Phù hợp cho test đặc tả “trang chủ chỉ có đúng một thẻ h1”. |
| Form tìm kiếm | `page.locator("form").first()` | Chấp nhận được vì trang FR-05 hiện chỉ có một form tìm kiếm. |
| Ô tìm kiếm | `searchForm.locator('input[type="text"]').first()` | Tạm ổn. Nên thay bằng accessible label hoặc `data-testid` nếu app được cải thiện. |
| Nút tìm kiếm | `searchForm.locator('button[type="submit"]').first()` | Tốt hơn locator theo text vì text UI hiện tại có thể bị lỗi encoding. |
| Lưới sản phẩm | `page.locator(".grid").first()` | Tạm thời phụ thuộc class Tailwind; nên thêm `data-testid="product-grid"`. |
| Thẻ sản phẩm | CSS class của card sản phẩm | Fragile vì phụ thuộc class UI. Nên thêm `data-testid="product-card"`. |
| Thẻ sản phẩm theo tên | Card filter theo heading level 2 và tên sản phẩm | Tương đối ổn vì tên sản phẩm là nội dung nghiệp vụ. |
| Ảnh sản phẩm | `productCardByName(name).locator("img").first()` | Dùng được để assert `alt`, nhưng nên có alt text đúng theo đặc tả. |
| Giá sản phẩm | `productCardByName(name).locator("p.text-red-500").first()` | Fragile vì phụ thuộc class màu. Nên thêm `data-testid="product-price"`. |
| Link xem chi tiết | `productCardByName(name).locator('a[href^="/product/"]').first()` | Khá ổn vì dựa vào URL pattern của chức năng. |
| Nút thêm vào giỏ | `productCardByName(name).locator("button").last()` | Tạm thời được vì card hiện chỉ có một button. Nên thêm role/name ổn định hoặc `data-testid`. |
| Tóm tắt tìm kiếm | `page.locator("div.mb-4.text-gray-600").first()` | Fragile vì phụ thuộc class. Nên thêm `data-testid="search-summary"`. |
| Panel lỗi | `page.locator("div.bg-red-100").first()` | Fragile vì phụ thuộc class màu. Nên thêm `data-testid="error-panel"`. |

## Kết Luận Review

Page object đã đủ để bắt đầu Step B cho các test case FR-05, nhưng nhiều locator vẫn phụ thuộc class CSS vì frontend hiện chưa có `data-testid` và một số text tiếng Việt trong source đang bị lỗi encoding. Khi viết automation, các assertion nên bám đặc tả trong README. Nếu test fail vì UI hiển thị khác đặc tả, ghi nhận bug sản phẩm thay vì sửa expected theo code.
