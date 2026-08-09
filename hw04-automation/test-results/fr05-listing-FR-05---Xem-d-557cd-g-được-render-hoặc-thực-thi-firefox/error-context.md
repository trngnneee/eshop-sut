# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr05-listing.spec.js >> FR-05 - Xem danh sách và tìm kiếm sản phẩm >> TC-FR05-15 - Payload image onerror không được render hoặc thực thi
- Location: tests\fr05-listing.spec.js:284:3

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('div.mb-4.text-gray-600').first()
Expected substring: "<image src=1 href=1 onerror=\"javascript:alert(1)\"></image>"
Received string:    "Kết quả tìm kiếm cho: "
Timeout: 5000ms

Call log:
  - Expect "toContainText" with timeout 5000ms
  - waiting for locator('div.mb-4.text-gray-600').first()
    14 × locator resolved to <div class="mb-4 text-gray-600">…</div>
       - unexpected value "Kết quả tìm kiếm cho: "

```

```yaml
- text: "Kết quả tìm kiếm cho:"
- img
```

# Test source

```ts
  198 | 
  199 |     let dialogText = null;
  200 | 
  201 |     page.on("dialog", async (dialog) => {
  202 |       dialogText = dialog.message();
  203 |       await dialog.dismiss();
  204 |     });
  205 | 
  206 |     await searchAndWaitForProducts(
  207 |       page,
  208 |       productListingPage,
  209 |       expectedData.keyword,
  210 |     );
  211 | 
  212 |     await expect(
  213 |       productListingPage.searchSummary.locator("script"),
  214 |     ).toHaveCount(0);
  215 | 
  216 |     expect(dialogText).not.toBe(expectedData.forbiddenDialogText);
  217 |   });
  218 | 
  219 |   test("TC-FR05-11 - Payload kiểu SQL injection không được trả về dữ liệu ngoài phạm vi tìm kiếm", async ({
  220 |     page,
  221 |   }) => {
  222 |     const productListingPage = await openProductListing(page);
  223 |     const expectedData = fr05Data.sql_payload;
  224 | 
  225 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  226 | 
  227 |     await expect(productListingPage.errorPanel).toHaveCount(0);
  228 |     await expect(productListingPage.errorPanel).not.toContainText(
  229 |       expectedData.forbiddenErrorText,
  230 |     );
  231 |     await expect(productListingPage.productCards).toHaveCount(
  232 |       expectedData.expectedSafeCount,
  233 |     );
  234 |     await expect(productListingPage.productCards).not.toHaveCount(
  235 |       expectedData.forbiddenAllProductCount,
  236 |     );
  237 |   });
  238 | 
  239 |   test("TC-FR05-12 - Ảnh sản phẩm có alt text mô tả", async ({ page }) => {
  240 |     const productListingPage = await openProductListing(page);
  241 | 
  242 |     for (const product of fr05Data.seedProducts) {
  243 |       await expect(productListingPage.productImage(product.name)).toHaveAttribute(
  244 |         "alt",
  245 |         product.expectedImageAlt,
  246 |       );
  247 |     }
  248 |   });
  249 | 
  250 |   test("TC-FR05-13 - Trang chủ chỉ có đúng một thẻ h1", async ({ page }) => {
  251 |     const productListingPage = await openProductListing(page);
  252 |     const expectedData = fr05Data.h1_rule;
  253 | 
  254 |     await expect(productListingPage.allHeadingsLevel1).toHaveCount(
  255 |       expectedData.expectedH1Count,
  256 |     );
  257 |     await expect(productListingPage.mainHeading).toContainText(
  258 |       expectedData.expectedMainHeadingText,
  259 |     );
  260 |   });
  261 | 
  262 |   test("TC-FR05-14 - Hiển thị loading khi đang tải dữ liệu sản phẩm", async ({
  263 |     page,
  264 |   }) => {
  265 |     const expectedData = fr05Data.delayed_api;
  266 |     const productListingPage = new ProductListingPage(page);
  267 | 
  268 |     await page.route(expectedData.routePattern, async (route) => {
  269 |       await new Promise((resolve) => setTimeout(resolve, expectedData.delayMs));
  270 |       await route.continue();
  271 |     });
  272 | 
  273 |     await productListingPage.goto();
  274 | 
  275 |     await expect(
  276 |       productListingPage.loadingIndicator(expectedData.expectedLoadingText),
  277 |     ).toBeVisible();
  278 | 
  279 |     await expect(productListingPage.productCards).toHaveCount(
  280 |       expectedData.expectedFinalCount,
  281 |     );
  282 |   });
  283 | 
  284 |   test("TC-FR05-15 - Payload image onerror không được render hoặc thực thi", async ({
  285 |     page,
  286 |   }) => {
  287 |     const productListingPage = await openProductListing(page);
  288 |     const expectedData = fr05Data.image_onerror_payload;
  289 |     const dialogMessages = [];
  290 | 
  291 |     page.on("dialog", async (dialog) => {
  292 |       dialogMessages.push(dialog.message());
  293 |       await dialog.dismiss();
  294 |     });
  295 | 
  296 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  297 | 
> 298 |     await expect(productListingPage.searchSummary).toContainText(
      |                                                    ^ Error: expect(locator).toContainText(expected) failed
  299 |       expectedData.expectedDisplayedText,
  300 |     );
  301 | 
  302 |     for (const forbiddenSelector of expectedData.forbiddenSelectors) {
  303 |       await expect(
  304 |         productListingPage.searchSummary.locator(forbiddenSelector),
  305 |       ).toHaveCount(0);
  306 |     }
  307 | 
  308 |     expect(dialogMessages).not.toContain(expectedData.forbiddenDialogText);
  309 |     await expect(productListingPage.productCards).toHaveCount(
  310 |       expectedData.expectedSafeCount,
  311 |     );
  312 |   });
  313 | 
  314 |   test("TC-FR05-16 - Tìm kiếm bằng từ khóa rất dài", async ({ page }) => {
  315 |     const productListingPage = await openProductListing(page);
  316 |     const expectedData = fr05Data.long_keyword;
  317 | 
  318 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  319 | 
  320 |     await expect(productListingPage.errorPanel).toHaveCount(0);
  321 |     await expect(productListingPage.searchSummary).toContainText(
  322 |       expectedData.expectedSummaryContains,
  323 |     );
  324 |     await expect(productListingPage.productCards).toHaveCount(
  325 |       expectedData.expectedCount,
  326 |     );
  327 |   });
  328 | 
  329 |   test("TC-FR05-17 - Tìm kiếm bằng từ khóa Unicode/emoji", async ({ page }) => {
  330 |     const productListingPage = await openProductListing(page);
  331 |     const expectedData = fr05Data.unicode_keyword;
  332 | 
  333 |     await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);
  334 | 
  335 |     await expect(productListingPage.errorPanel).toHaveCount(0);
  336 |     await expect(productListingPage.searchSummary).toContainText(
  337 |       expectedData.expectedSummaryContains,
  338 |     );
  339 |     await expect(productListingPage.productCards).toHaveCount(
  340 |       expectedData.expectedCount,
  341 |     );
  342 |   });
  343 | });
  344 | 
```