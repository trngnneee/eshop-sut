# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr05-listing.spec.js >> FR-05 - Xem danh sách và tìm kiếm sản phẩm >> TC-FR05-14 - Hiển thị loading khi đang tải dữ liệu sản phẩm
- Location: tests\fr05-listing.spec.js:258:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText('Đang tải')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByText('Đang tải')

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
  - textbox "Tìm kiếm..."
  - button "Tìm"
  - heading "iPhone 15 Pro Max" [level=2]
  - paragraph: 30,000,000 VND
  - link "Xem chi tiết":
    - /url: /product/1
  - button "Thêm vào giỏ"
  - heading "Samsung Galaxy S24 Ultra" [level=2]
  - paragraph: 28,000,000 VND
  - link "Xem chi tiết":
    - /url: /product/2
  - button "Thêm vào giỏ"
  - heading "MacBook Pro M3" [level=2]
  - paragraph: 45,000,000 VND
  - link "Xem chi tiết":
    - /url: /product/3
  - button "Thêm vào giỏ"
  - heading "Tai nghe AirPods Pro 2" [level=2]
  - paragraph: 6,000,000 VND
  - link "Xem chi tiết":
    - /url: /product/4
  - button "Thêm vào giỏ"
  - heading "Bàn phím cơ Keychron Q1" [level=2]
  - paragraph: 4,000,000 VND
  - link "Xem chi tiết":
    - /url: /product/5
  - button "Thêm vào giỏ"
  - heading "Hiển thị 5 sản phẩm" [level=1]
- contentinfo: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  173 | 
  174 |     for (const productName of expectedResult.expectedVisibleNames) {
  175 |       await expect(
  176 |         productListingPage.productName(productName),
  177 |       ).toBeVisible();
  178 |     }
  179 |   });
  180 | 
  181 |   test("TC-FR05-09 - Từ khóa chứa HTML phải được hiển thị an toàn", async ({
  182 |     page,
  183 |   }) => {
  184 |     const productListingPage = await openProductListing(page);
  185 |     const expectedData = fr05Data.html_payload;
  186 | 
  187 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  188 | 
  189 |     await expect(productListingPage.searchSummary).toContainText(
  190 |       expectedData.expectedDisplayedText,
  191 |     );
  192 |     await expect(page.locator(expectedData.forbiddenSelector)).toHaveCount(0);
  193 |   });
  194 | 
  195 |   test("TC-FR05-10 - Từ khóa chứa script không được thực thi", async ({
  196 |     page,
  197 |   }) => {
  198 |     const productListingPage = await openProductListing(page);
  199 |     const expectedData = fr05Data.script_payload;
  200 |     let dialogText = null;
  201 | 
  202 |     page.on("dialog", async (dialog) => {
  203 |       dialogText = dialog.message();
  204 |       await dialog.dismiss();
  205 |     });
  206 | 
  207 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  208 | 
  209 |     await expect(productListingPage.searchSummary).toContainText(
  210 |       expectedData.expectedDisplayedText,
  211 |     );
  212 |     expect(dialogText).not.toBe(expectedData.forbiddenDialogText);
  213 |   });
  214 | 
  215 |   test("TC-FR05-11 - Payload kiểu SQL injection không được trả về dữ liệu ngoài phạm vi tìm kiếm", async ({
  216 |     page,
  217 |   }) => {
  218 |     const productListingPage = await openProductListing(page);
  219 |     const expectedData = fr05Data.sql_payload;
  220 | 
  221 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  222 | 
  223 |     await expect(productListingPage.errorPanel).toHaveCount(0);
  224 |     await expect(productListingPage.errorPanel).not.toContainText(
  225 |       expectedData.forbiddenErrorText,
  226 |     );
  227 |     await expect(productListingPage.productCards).toHaveCount(
  228 |       expectedData.expectedSafeCount,
  229 |     );
  230 |     await expect(productListingPage.productCards).not.toHaveCount(
  231 |       expectedData.forbiddenAllProductCount,
  232 |     );
  233 |   });
  234 | 
  235 |   test("TC-FR05-12 - Ảnh sản phẩm có alt text mô tả", async ({ page }) => {
  236 |     const productListingPage = await openProductListing(page);
  237 | 
  238 |     for (const product of fr05Data.seedProducts) {
  239 |       await expect(productListingPage.productImage(product.name)).toHaveAttribute(
  240 |         "alt",
  241 |         product.expectedImageAlt,
  242 |       );
  243 |     }
  244 |   });
  245 | 
  246 |   test("TC-FR05-13 - Trang chủ chỉ có đúng một thẻ h1", async ({ page }) => {
  247 |     const productListingPage = await openProductListing(page);
  248 |     const expectedData = fr05Data.h1_rule;
  249 | 
  250 |     await expect(productListingPage.allHeadingsLevel1).toHaveCount(
  251 |       expectedData.expectedH1Count,
  252 |     );
  253 |     await expect(productListingPage.mainHeading).toContainText(
  254 |       expectedData.expectedMainHeadingText,
  255 |     );
  256 |   });
  257 | 
  258 |   test("TC-FR05-14 - Hiển thị loading khi đang tải dữ liệu sản phẩm", async ({
  259 |     page,
  260 |   }) => {
  261 |     const expectedData = fr05Data.delayed_api;
  262 |     const productListingPage = new ProductListingPage(page);
  263 | 
  264 |     await page.route(expectedData.routePattern, async (route) => {
  265 |       await new Promise((resolve) => setTimeout(resolve, expectedData.delayMs));
  266 |       await route.continue();
  267 |     });
  268 | 
  269 |     await productListingPage.goto();
  270 | 
  271 |     await expect(
  272 |       productListingPage.loadingIndicator(expectedData.expectedLoadingText),
> 273 |     ).toBeVisible();
      |       ^ Error: expect(locator).toBeVisible() failed
  274 | 
  275 |     await expect(productListingPage.productCards).toHaveCount(
  276 |       expectedData.expectedFinalCount,
  277 |     );
  278 |   });
  279 | });
  280 | 
```