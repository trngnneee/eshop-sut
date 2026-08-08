# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr05-listing.spec.js >> FR-05 - Xem danh sách và tìm kiếm sản phẩm >> TC-FR05-06 - Tìm kiếm không có kết quả phù hợp
- Location: tests\fr05-listing.spec.js:124:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText('Không có sản phẩm phù hợp')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByText('Không có sản phẩm phù hợp')

```

```yaml
- banner:
  - link "EShop":
    - /url: /
  - navigation:
    - link "Giỏ hàng":
      - /url: /cart
    - link "Đăng nhập":
      - /url: /login
    - link "Đăng ký":
      - /url: /register
- main:
  - heading "Danh sách sản phẩm" [level=1]
  - textbox "Tìm kiếm...": SanPhamKhongTonTaiFR05
  - button "Tìm"
  - text: "Kết quả tìm kiếm cho: SanPhamKhongTonTaiFR05"
- contentinfo: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  35  |   }) => {
  36  |     const productListingPage = await openProductListing(page);
  37  |     const expectedData = fr05Data.all_products;
  38  | 
  39  |     await expect(productListingPage.productCards).toHaveCount(
  40  |       expectedData.expectedCount,
  41  |     );
  42  | 
  43  |     for (const productName of expectedData.expectedVisibleNames) {
  44  |       await expect(productListingPage.productName(productName)).toBeVisible();
  45  |     }
  46  |   });
  47  | 
  48  |   test("TC-FR05-02 - Thẻ sản phẩm hiển thị đầy đủ thông tin bắt buộc", async ({
  49  |     page,
  50  |   }) => {
  51  |     const productListingPage = await openProductListing(page);
  52  | 
  53  |     for (const product of fr05Data.seedProducts) {
  54  |       const productCard = productListingPage.productCardByName(product.name);
  55  | 
  56  |       await expect(productCard).toBeVisible();
  57  |       await expect(productListingPage.productImage(product.name)).toBeVisible();
  58  |       await expect(productListingPage.productName(product.name)).toBeVisible();
  59  |       await expect(productListingPage.productPrice(product.name)).toBeVisible();
  60  |       await expect(productListingPage.productPrice(product.name)).not.toHaveText("");
  61  |       await expect(productListingPage.productDetailLink(product.name)).toBeVisible();
  62  |       await expect(productListingPage.addToCartButton(product.name)).toBeVisible();
  63  |     }
  64  |   });
  65  | 
  66  |   test("TC-FR05-03 - Giá sản phẩm hiển thị đúng đơn vị và phân cách hàng nghìn", async ({
  67  |     page,
  68  |   }) => {
  69  |     const productListingPage = await openProductListing(page);
  70  |     const expectedData = fr05Data.price_format;
  71  | 
  72  |     for (const priceCheck of expectedData.checks) {
  73  |       await expect(
  74  |         productListingPage.productPrice(priceCheck.productName),
  75  |       ).toHaveText(priceCheck.expectedPriceText);
  76  |     }
  77  |   });
  78  | 
  79  |   test("TC-FR05-04 - Tìm kiếm bằng đúng tên sản phẩm", async ({ page }) => {
  80  |     const productListingPage = await openProductListing(page);
  81  |     const expectedData = fr05Data.exact_match;
  82  |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  83  | 
  84  |     await expect(productListingPage.productCards).toHaveCount(
  85  |       expectedData.expectedCount,
  86  |     );
  87  | 
  88  |     for (const productName of expectedData.expectedVisibleNames) {
  89  |       await expect(productListingPage.productName(productName)).toBeVisible();
  90  |     }
  91  | 
  92  |     for (const productName of expectedData.expectedHiddenNames) {
  93  |       await expect(productListingPage.productName(productName)).toHaveCount(0);
  94  |     }
  95  | 
  96  |     await expect(productListingPage.searchSummary).toContainText(
  97  |       expectedData.expectedSearchSummaryContains,
  98  |     );
  99  |   });
  100 | 
  101 |   test("TC-FR05-05 - Tìm kiếm bằng một phần tên sản phẩm", async ({ page }) => {
  102 |     const productListingPage = await openProductListing(page);
  103 |     const expectedData = fr05Data.partial_match;
  104 | 
  105 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  106 | 
  107 |     await expect(productListingPage.productCards).toHaveCount(
  108 |       expectedData.expectedCount,
  109 |     );
  110 | 
  111 |     for (const productName of expectedData.expectedVisibleNames) {
  112 |       await expect(productListingPage.productName(productName)).toBeVisible();
  113 |     }
  114 | 
  115 |     for (const productName of expectedData.expectedHiddenNames) {
  116 |       await expect(productListingPage.productName(productName)).toHaveCount(0);
  117 |     }
  118 | 
  119 |     await expect(productListingPage.searchSummary).toContainText(
  120 |       expectedData.expectedSearchSummaryContains,
  121 |     );
  122 |   });
  123 | 
  124 |   test("TC-FR05-06 - Tìm kiếm không có kết quả phù hợp", async ({ page }) => {
  125 |     const productListingPage = await openProductListing(page);
  126 |     const expectedData = fr05Data.no_result;
  127 | 
  128 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  129 | 
  130 |     await expect(productListingPage.productCards).toHaveCount(
  131 |       expectedData.expectedCount,
  132 |     );
  133 |     await expect(
  134 |       productListingPage.emptyStateMessage(expectedData.expectedEmptyStateText),
> 135 |     ).toBeVisible();
      |       ^ Error: expect(locator).toBeVisible() failed
  136 | 
  137 |     for (const productName of expectedData.expectedHiddenNames) {
  138 |       await expect(productListingPage.productName(productName)).toHaveCount(0);
  139 |     }
  140 |   });
  141 | 
  142 |   test("TC-FR05-07 - Tìm kiếm với từ khóa rỗng", async ({ page }) => {
  143 |     const productListingPage = await openProductListing(page);
  144 |     const expectedData = fr05Data.empty_keyword;
  145 | 
  146 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  147 | 
  148 |     await expect(productListingPage.productCards).toHaveCount(
  149 |       expectedData.expectedCount,
  150 |     );
  151 | 
  152 |     for (const productName of expectedData.expectedVisibleNames) {
  153 |       await expect(productListingPage.productName(productName)).toBeVisible();
  154 |     }
  155 |   });
  156 | 
  157 |   test("TC-FR05-08 - Tìm kiếm với từ khóa có khoảng trắng đầu/cuối", async ({page,}) => {
  158 |     const productListingPage = await openProductListing(page);
  159 |     const expectedData = fr05Data.padded_keyword;
  160 |     const expectedResult = expectedData.expectedIfTrimmed;
  161 | 
  162 |     await searchAndWaitForProducts(
  163 |       page,
  164 |       productListingPage,
  165 |       expectedData.keyword,
  166 |     );
  167 | 
  168 |     await expect(productListingPage.errorPanel).toHaveCount(0);
  169 | 
  170 |     await expect(productListingPage.productCards).toHaveCount(
  171 |       expectedResult.expectedCount,
  172 |     );
  173 | 
  174 |     for (const productName of expectedResult.expectedVisibleNames) {
  175 |       await expect(
  176 |         productListingPage.productName(productName),
  177 |       ).toBeVisible();
  178 |     }
  179 |   });
  180 | });
  181 | 
```