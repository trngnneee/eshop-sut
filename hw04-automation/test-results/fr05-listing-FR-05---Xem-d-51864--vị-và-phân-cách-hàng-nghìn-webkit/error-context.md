# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr05-listing.spec.js >> FR-05 - Xem danh sách và tìm kiếm sản phẩm >> TC-FR05-03 - Giá sản phẩm hiển thị đúng đơn vị và phân cách hàng nghìn
- Location: tests\fr05-listing.spec.js:54:3

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator:  locator('div.border.rounded.shadow-sm.p-4.flex.flex-col.bg-white').filter({ has: getByRole('heading', { name: 'iPhone 15 Pro Max', level: 2 }) }).locator('p.text-red-500').first()
Expected: "30.000.000 ₫"
Received: "30,000,000 VND"
Timeout:  5000ms

Call log:
  - Expect "toHaveText" with timeout 5000ms
  - waiting for locator('div.border.rounded.shadow-sm.p-4.flex.flex-col.bg-white').filter({ has: getByRole('heading', { name: 'iPhone 15 Pro Max', level: 2 }) }).locator('p.text-red-500').first()
    13 × locator resolved to <p class="text-red-500 font-bold mb-2">30,000,000 VND</p>
       - unexpected value "30,000,000 VND"

```

```yaml
- paragraph: 30,000,000 VND
```

# Test source

```ts
  1  | const { test, expect } = require("@playwright/test");
  2  | const { ProductListingPage } = require("./pages/ProductListingPage");
  3  | const fr05Data = require("../data/fr05.json");
  4  | 
  5  | async function openProductListing(page) {
  6  |   const productListingPage = new ProductListingPage(page);
  7  |   const productsResponse = page.waitForResponse(
  8  |     (response) =>
  9  |       response.url().includes(fr05Data.api.products) &&
  10 |       response.request().method() === "GET",
  11 |   );
  12 | 
  13 |   await productListingPage.goto();
  14 |   await productsResponse;
  15 |   await expect(productListingPage.productGrid).toBeVisible();
  16 | 
  17 |   return productListingPage;
  18 | }
  19 | 
  20 | test.describe("FR-05 - Xem danh sách và tìm kiếm sản phẩm", () => {
  21 |   test("TC-FR05-01 - Hiển thị tất cả sản phẩm trên trang chủ", async ({
  22 |     page,
  23 |   }) => {
  24 |     const productListingPage = await openProductListing(page);
  25 |     const expectedData = fr05Data.all_products;
  26 | 
  27 |     await expect(productListingPage.productCards).toHaveCount(
  28 |       expectedData.expectedCount,
  29 |     );
  30 | 
  31 |     for (const productName of expectedData.expectedVisibleNames) {
  32 |       await expect(productListingPage.productName(productName)).toBeVisible();
  33 |     }
  34 |   });
  35 | 
  36 |   test("TC-FR05-02 - Thẻ sản phẩm hiển thị đầy đủ thông tin bắt buộc", async ({
  37 |     page,
  38 |   }) => {
  39 |     const productListingPage = await openProductListing(page);
  40 | 
  41 |     for (const product of fr05Data.seedProducts) {
  42 |       const productCard = productListingPage.productCardByName(product.name);
  43 | 
  44 |       await expect(productCard).toBeVisible();
  45 |       await expect(productListingPage.productImage(product.name)).toBeVisible();
  46 |       await expect(productListingPage.productName(product.name)).toBeVisible();
  47 |       await expect(productListingPage.productPrice(product.name)).toBeVisible();
  48 |       await expect(productListingPage.productPrice(product.name)).not.toHaveText("");
  49 |       await expect(productListingPage.productDetailLink(product.name)).toBeVisible();
  50 |       await expect(productListingPage.addToCartButton(product.name)).toBeVisible();
  51 |     }
  52 |   });
  53 | 
  54 |   test("TC-FR05-03 - Giá sản phẩm hiển thị đúng đơn vị và phân cách hàng nghìn", async ({
  55 |     page,
  56 |   }) => {
  57 |     const productListingPage = await openProductListing(page);
  58 |     const expectedData = fr05Data.price_format;
  59 | 
  60 |     for (const priceCheck of expectedData.checks) {
  61 |       await expect(
  62 |         productListingPage.productPrice(priceCheck.productName),
> 63 |       ).toHaveText(priceCheck.expectedPriceText);
     |         ^ Error: expect(locator).toHaveText(expected) failed
  64 |     }
  65 |   });
  66 | 
  67 |   test("TC-FR05-04 - Tìm kiếm bằng đúng tên sản phẩm", async ({ page }) => {
  68 |     const productListingPage = await openProductListing(page);
  69 |     const expectedData = fr05Data.exact_match;
  70 |     const searchResponse = page.waitForResponse(
  71 |       (response) =>
  72 |         response.url().includes(fr05Data.api.products) &&
  73 |         response.url().includes(`search=${encodeURIComponent(expectedData.keyword)}`) &&
  74 |         response.request().method() === "GET",
  75 |     );
  76 | 
  77 |     await productListingPage.search(expectedData.keyword);
  78 |     await searchResponse;
  79 | 
  80 |     await expect(productListingPage.productCards).toHaveCount(
  81 |       expectedData.expectedCount,
  82 |     );
  83 | 
  84 |     for (const productName of expectedData.expectedVisibleNames) {
  85 |       await expect(productListingPage.productName(productName)).toBeVisible();
  86 |     }
  87 | 
  88 |     for (const productName of expectedData.expectedHiddenNames) {
  89 |       await expect(productListingPage.productName(productName)).toHaveCount(0);
  90 |     }
  91 | 
  92 |     await expect(productListingPage.searchSummary).toContainText(
  93 |       expectedData.expectedSearchSummaryContains,
  94 |     );
  95 |   });
  96 | });
  97 | 
```