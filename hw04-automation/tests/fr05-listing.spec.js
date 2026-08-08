const { test, expect } = require("@playwright/test");
const { ProductListingPage } = require("./pages/ProductListingPage");
const fr05Data = require("../data/fr05.json");

async function openProductListing(page) {
  const productListingPage = new ProductListingPage(page);
  const productsResponse = page.waitForResponse(
    (response) =>
      response.url().includes(fr05Data.api.products) &&
      response.request().method() === "GET",
  );

  await productListingPage.goto();
  await productsResponse;
  await expect(productListingPage.productGrid).toBeVisible();

  return productListingPage;
}

async function searchAndWaitForProducts(page, productListingPage, keyword) {
  const productsResponse = page.waitForResponse(
    (response) =>
      response.url().includes(fr05Data.api.products) &&
      response.url().includes("search=") &&
      response.request().method() === "GET",
  );

  await productListingPage.search(keyword);
  await productsResponse;
}

test.describe("FR-05 - Xem danh sách và tìm kiếm sản phẩm", () => {
  test("TC-FR05-01 - Hiển thị tất cả sản phẩm trên trang chủ", async ({
    page,
  }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.all_products;

    await expect(productListingPage.productCards).toHaveCount(
      expectedData.expectedCount,
    );

    for (const productName of expectedData.expectedVisibleNames) {
      await expect(productListingPage.productName(productName)).toBeVisible();
    }
  });

  test("TC-FR05-02 - Thẻ sản phẩm hiển thị đầy đủ thông tin bắt buộc", async ({
    page,
  }) => {
    const productListingPage = await openProductListing(page);

    for (const product of fr05Data.seedProducts) {
      const productCard = productListingPage.productCardByName(product.name);

      await expect(productCard).toBeVisible();
      await expect(productListingPage.productImage(product.name)).toBeVisible();
      await expect(productListingPage.productName(product.name)).toBeVisible();
      await expect(productListingPage.productPrice(product.name)).toBeVisible();
      await expect(productListingPage.productPrice(product.name)).not.toHaveText("");
      await expect(productListingPage.productDetailLink(product.name)).toBeVisible();
      await expect(productListingPage.addToCartButton(product.name)).toBeVisible();
    }
  });

  test("TC-FR05-03 - Giá sản phẩm hiển thị đúng đơn vị và phân cách hàng nghìn", async ({
    page,
  }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.price_format;

    for (const priceCheck of expectedData.checks) {
      await expect(
        productListingPage.productPrice(priceCheck.productName),
      ).toHaveText(priceCheck.expectedPriceText);
    }
  });

  test("TC-FR05-04 - Tìm kiếm bằng đúng tên sản phẩm", async ({ page }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.exact_match;
    await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);

    await expect(productListingPage.productCards).toHaveCount(
      expectedData.expectedCount,
    );

    for (const productName of expectedData.expectedVisibleNames) {
      await expect(productListingPage.productName(productName)).toBeVisible();
    }

    for (const productName of expectedData.expectedHiddenNames) {
      await expect(productListingPage.productName(productName)).toHaveCount(0);
    }

    await expect(productListingPage.searchSummary).toContainText(
      expectedData.expectedSearchSummaryContains,
    );
  });

  test("TC-FR05-05 - Tìm kiếm bằng một phần tên sản phẩm", async ({ page }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.partial_match;

    await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);

    await expect(productListingPage.productCards).toHaveCount(
      expectedData.expectedCount,
    );

    for (const productName of expectedData.expectedVisibleNames) {
      await expect(productListingPage.productName(productName)).toBeVisible();
    }

    for (const productName of expectedData.expectedHiddenNames) {
      await expect(productListingPage.productName(productName)).toHaveCount(0);
    }

    await expect(productListingPage.searchSummary).toContainText(
      expectedData.expectedSearchSummaryContains,
    );
  });

  test("TC-FR05-06 - Tìm kiếm không có kết quả phù hợp", async ({ page }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.no_result;

    await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);

    await expect(productListingPage.productCards).toHaveCount(
      expectedData.expectedCount,
    );
    await expect(
      productListingPage.emptyStateMessage(expectedData.expectedEmptyStateText),
    ).toBeVisible();

    for (const productName of expectedData.expectedHiddenNames) {
      await expect(productListingPage.productName(productName)).toHaveCount(0);
    }
  });

  test("TC-FR05-07 - Tìm kiếm với từ khóa rỗng", async ({ page }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.empty_keyword;

    await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);

    await expect(productListingPage.productCards).toHaveCount(
      expectedData.expectedCount,
    );

    for (const productName of expectedData.expectedVisibleNames) {
      await expect(productListingPage.productName(productName)).toBeVisible();
    }
  });

  test("TC-FR05-08 - Tìm kiếm với từ khóa có khoảng trắng đầu/cuối", async ({page,}) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.padded_keyword;
    const expectedResult = expectedData.expectedIfTrimmed;

    await searchAndWaitForProducts(
      page,
      productListingPage,
      expectedData.keyword,
    );

    await expect(productListingPage.errorPanel).toHaveCount(0);

    await expect(productListingPage.productCards).toHaveCount(
      expectedResult.expectedCount,
    );

    for (const productName of expectedResult.expectedVisibleNames) {
      await expect(
        productListingPage.productName(productName),
      ).toBeVisible();
    }
  });

  test("TC-FR05-09 - Từ khóa chứa HTML phải được hiển thị an toàn", async ({
    page,
  }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.html_payload;

    await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);

    await expect(productListingPage.searchSummary).toContainText(
      expectedData.expectedDisplayedText,
    );
    await expect(page.locator(expectedData.forbiddenSelector)).toHaveCount(0);
  });

  test("TC-FR05-10 - Từ khóa chứa script không được thực thi", async ({
    page,
  }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.script_payload;
    let dialogText = null;

    page.on("dialog", async (dialog) => {
      dialogText = dialog.message();
      await dialog.dismiss();
    });

    await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);

    await expect(productListingPage.searchSummary).toContainText(
      expectedData.expectedDisplayedText,
    );
    expect(dialogText).not.toBe(expectedData.forbiddenDialogText);
  });

  test("TC-FR05-11 - Payload kiểu SQL injection không được trả về dữ liệu ngoài phạm vi tìm kiếm", async ({
    page,
  }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.sql_payload;

    await searchAndWaitForProducts(page, productListingPage, expectedData.keyword);

    await expect(productListingPage.errorPanel).toHaveCount(0);
    await expect(productListingPage.errorPanel).not.toContainText(
      expectedData.forbiddenErrorText,
    );
    await expect(productListingPage.productCards).toHaveCount(
      expectedData.expectedSafeCount,
    );
    await expect(productListingPage.productCards).not.toHaveCount(
      expectedData.forbiddenAllProductCount,
    );
  });

  test("TC-FR05-12 - Ảnh sản phẩm có alt text mô tả", async ({ page }) => {
    const productListingPage = await openProductListing(page);

    for (const product of fr05Data.seedProducts) {
      await expect(productListingPage.productImage(product.name)).toHaveAttribute(
        "alt",
        product.expectedImageAlt,
      );
    }
  });

  test("TC-FR05-13 - Trang chủ chỉ có đúng một thẻ h1", async ({ page }) => {
    const productListingPage = await openProductListing(page);
    const expectedData = fr05Data.h1_rule;

    await expect(productListingPage.allHeadingsLevel1).toHaveCount(
      expectedData.expectedH1Count,
    );
    await expect(productListingPage.mainHeading).toContainText(
      expectedData.expectedMainHeadingText,
    );
  });

  test("TC-FR05-14 - Hiển thị loading khi đang tải dữ liệu sản phẩm", async ({
    page,
  }) => {
    const expectedData = fr05Data.delayed_api;
    const productListingPage = new ProductListingPage(page);

    await page.route(expectedData.routePattern, async (route) => {
      await new Promise((resolve) => setTimeout(resolve, expectedData.delayMs));
      await route.continue();
    });

    await productListingPage.goto();

    await expect(
      productListingPage.loadingIndicator(expectedData.expectedLoadingText),
    ).toBeVisible();

    await expect(productListingPage.productCards).toHaveCount(
      expectedData.expectedFinalCount,
    );
  });
});
