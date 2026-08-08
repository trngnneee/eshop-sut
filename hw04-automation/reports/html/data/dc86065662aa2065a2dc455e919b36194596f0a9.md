# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr05-listing.spec.js >> FR-05 - Xem danh sách và tìm kiếm sản phẩm >> TC-FR05-12 - Ảnh sản phẩm có alt text mô tả
- Location: tests\fr05-listing.spec.js:235:3

# Error details

```
Error: expect(locator).toHaveAttribute(expected) failed

Locator:  locator('div.border.rounded.shadow-sm.p-4.flex.flex-col.bg-white').filter({ has: getByRole('heading', { name: 'iPhone 15 Pro Max', level: 2 }) }).locator('img').first()
Expected: "iPhone 15 Pro Max"
Received: ""
Timeout:  5000ms

Call log:
  - Expect "toHaveAttribute" with timeout 5000ms
  - waiting for locator('div.border.rounded.shadow-sm.p-4.flex.flex-col.bg-white').filter({ has: getByRole('heading', { name: 'iPhone 15 Pro Max', level: 2 }) }).locator('img').first()
    13 × locator resolved to <img alt="" class="w-full h-48 object-cover mb-4 rounded" src="https://placehold.co/300x300/png?text=iPhone+15"/>
       - unexpected value ""

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - link "EShop" [ref=e5]:
      - /url: /
    - navigation [ref=e6]:
      - link "Giỏ hàng" [ref=e7]:
        - /url: /cart
      - link "Đăng nhập" [ref=e8]:
        - /url: /login
      - link "Đăng ký" [ref=e9]:
        - /url: /register
  - main [ref=e10]:
    - generic [ref=e11]:
      - generic [ref=e12]:
        - heading "Danh sách sản phẩm" [level=1] [ref=e13]
        - generic [ref=e14]:
          - textbox "Tìm kiếm..." [ref=e15]
          - button "Tìm" [ref=e16] [cursor=pointer]
      - generic [ref=e17]:
        - generic [ref=e18]:
          - heading "iPhone 15 Pro Max" [level=2] [ref=e19]
          - paragraph [ref=e20]: 30,000,000 VND
          - generic [ref=e21]:
            - link "Xem chi tiết" [ref=e22]:
              - /url: /product/1
            - button "Thêm vào giỏ" [ref=e23] [cursor=pointer]
        - generic [ref=e24]:
          - heading "Samsung Galaxy S24 Ultra" [level=2] [ref=e25]
          - paragraph [ref=e26]: 28,000,000 VND
          - generic [ref=e27]:
            - link "Xem chi tiết" [ref=e28]:
              - /url: /product/2
            - button "Thêm vào giỏ" [ref=e29] [cursor=pointer]
        - generic [ref=e30]:
          - heading "MacBook Pro M3" [level=2] [ref=e31]
          - paragraph [ref=e32]: 45,000,000 VND
          - generic [ref=e33]:
            - link "Xem chi tiết" [ref=e34]:
              - /url: /product/3
            - button "Thêm vào giỏ" [ref=e35] [cursor=pointer]
        - generic [ref=e36]:
          - heading "Tai nghe AirPods Pro 2" [level=2] [ref=e37]
          - paragraph [ref=e38]: 6,000,000 VND
          - generic [ref=e39]:
            - link "Xem chi tiết" [ref=e40]:
              - /url: /product/4
            - button "Thêm vào giỏ" [ref=e41] [cursor=pointer]
        - generic [ref=e42]:
          - heading "Bàn phím cơ Keychron Q1" [level=2] [ref=e43]
          - paragraph [ref=e44]: 4,000,000 VND
          - generic [ref=e45]:
            - link "Xem chi tiết" [ref=e46]:
              - /url: /product/5
            - button "Thêm vào giỏ" [ref=e47] [cursor=pointer]
      - heading "Hiển thị 5 sản phẩm" [level=1] [ref=e48]
  - contentinfo [ref=e49]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
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
> 239 |       await expect(productListingPage.productImage(product.name)).toHaveAttribute(
      |                                                                   ^ Error: expect(locator).toHaveAttribute(expected) failed
  240 |         "alt",
  241 |         product.expectedImageAlt,
  242 |       );
  243 |     }
  244 |   });
  245 | });
  246 | 
```