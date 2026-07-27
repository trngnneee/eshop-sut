import { expect, test } from '@playwright/test';

const PRODUCTS = [
  {
    id: 1,
    name: 'Laptop Gaming Alpha',
    price: 25_990_000,
    imageUrl:
      "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='640' height='360'%3E%3Crect width='100%25' height='100%25' fill='%23dbeafe'/%3E%3C/svg%3E",
  },
  {
    id: 2,
    name: 'Chuột không dây Beta',
    price: 690_000,
    imageUrl:
      "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='360' height='640'%3E%3Crect width='100%25' height='100%25' fill='%23dcfce7'/%3E%3C/svg%3E",
  },
  {
    id: 3,
    name: 'Bàn phím cơ Gamma phiên bản tên rất dài',
    price: 1_590_000,
    imageUrl:
      "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='500'%3E%3Crect width='100%25' height='100%25' fill='%23fef3c7'/%3E%3C/svg%3E",
  },
];

const ui = (page) => ({
  main: page.locator('main'),
  heading: page.locator('main h1').first(),
  searchForm: page.locator('main form'),
  searchInput: page.locator('main form input[type="text"]'),
  searchButton: page.locator('main form button[type="submit"]'),
  grid: page.locator('main .grid'),
  cards: page.locator('main .grid > div'),
  productCount: page.locator('main .grid + h1'),
});

async function mockProductApi(page, options = {}) {
  const {
    products = PRODUCTS,
    status = 200,
    body,
    waitForRelease,
  } = options;

  await page.route('**/api/products?*', async (route) => {
    if (waitForRelease) {
      await waitForRelease;
    }

    if (status !== 200) {
      await route.fulfill({
        status,
        contentType: 'application/json',
        body: body ?? JSON.stringify({ message: 'Không thể tải sản phẩm' }),
      });
      return;
    }

    const requestUrl = new URL(route.request().url());
    const query = (requestUrl.searchParams.get('search') ?? '').toLowerCase();
    const result = products.filter((product) =>
      product.name.toLowerCase().includes(query),
    );

    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(result),
    });
  });
}

async function openWithProducts(page, products = PRODUCTS) {
  await mockProductApi(page, { products });
  await page.goto('/');
  await expect(ui(page).cards).toHaveCount(products.length);
}

async function columnCount(locator) {
  return locator.evaluate((grid) => {
    const firstTop = grid.firstElementChild?.getBoundingClientRect().top;
    if (firstTop === undefined) return 0;
    return [...grid.children].filter(
      (child) => Math.abs(child.getBoundingClientRect().top - firstTop) < 2,
    ).length;
  });
}

test.describe('GUI — EShop / Danh sách sản phẩm', () => {
  test('PLP-VIS-01: tiêu đề hiển thị đúng nội dung và không chồng form', async ({
    page,
  }) => {
    await openWithProducts(page);
    const { heading, searchForm } = ui(page);

    await expect(heading).toHaveText('Danh sách sản phẩm');
    await expect(heading).toBeVisible();

    const headingBox = await heading.boundingBox();
    const formBox = await searchForm.boundingBox();
    expect(headingBox).not.toBeNull();
    expect(formBox).not.toBeNull();
    expect(headingBox.x + headingBox.width).toBeLessThanOrEqual(formBox.x);
  });

  test('PLP-VIS-02: input và nút Tìm thẳng hàng, không bị cắt', async ({
    page,
  }) => {
    await openWithProducts(page);
    const { searchInput, searchButton } = ui(page);
    const inputBox = await searchInput.boundingBox();
    const buttonBox = await searchButton.boundingBox();

    expect(inputBox).not.toBeNull();
    expect(buttonBox).not.toBeNull();
    expect(Math.abs(inputBox.y - buttonBox.y)).toBeLessThanOrEqual(2);
    expect(Math.abs(inputBox.height - buttonBox.height)).toBeLessThanOrEqual(2);
    await expect(searchButton).toHaveText('Tìm');
  });

  test('PLP-VIS-03: product card có kích thước và khoảng cách đồng nhất', async ({
    page,
  }) => {
    await openWithProducts(page);
    const boxes = await ui(page).cards.evaluateAll((cards) =>
      cards.map((card) => {
        const box = card.getBoundingClientRect();
        return { width: box.width, top: box.top };
      }),
    );

    expect(boxes).toHaveLength(3);
    expect(new Set(boxes.map((box) => Math.round(box.width))).size).toBe(1);
    expect(new Set(boxes.map((box) => Math.round(box.top))).size).toBe(1);
  });

  test('PLP-VIS-04: ảnh, tên, giá và action nằm gọn trong product card', async ({
    page,
  }) => {
    await openWithProducts(page);

    for (const card of await ui(page).cards.all()) {
      await expect(card.locator('img')).toBeVisible();
      await expect(card.locator('h2')).toBeVisible();
      await expect(card.locator('p')).toContainText('VND');
      await expect(card.locator('a')).toBeVisible();
      await expect(card.locator('button')).toBeVisible();

      const fitsInside = await card.evaluate((element) => {
        const parent = element.getBoundingClientRect();
        return [...element.querySelectorAll('img, h2, p, a, button')].every(
          (child) => {
            const box = child.getBoundingClientRect();
            return box.left >= parent.left && box.right <= parent.right;
          },
        );
      });
      expect(fitsInside).toBe(true);
    }
  });

  test('PLP-FUN-01: route / tải được danh sách sản phẩm', async ({ page }) => {
    await openWithProducts(page);
    await expect(page).toHaveURL(/\/$/);
    await expect(ui(page).searchForm).toBeVisible();
    await expect(ui(page).cards).toHaveCount(3);
  });

  test('PLP-FUN-02: tìm kiếm bằng tên đầy đủ', async ({ page }) => {
    await openWithProducts(page);
    const { searchInput, searchButton, cards } = ui(page);

    await searchInput.fill(PRODUCTS[0].name);
    await searchButton.click();

    await expect(cards).toHaveCount(1);
    await expect(cards.first().locator('h2')).toHaveText(PRODUCTS[0].name);
  });

  test('PLP-FUN-03: tìm kiếm một phần tên bằng phím Enter', async ({ page }) => {
    await openWithProducts(page);
    const { searchInput, cards } = ui(page);

    await searchInput.fill('Gamma');
    await searchInput.press('Enter');

    await expect(cards).toHaveCount(1);
    await expect(cards.first().locator('h2')).toContainText('Gamma');
  });

  test('PLP-FUN-04: xóa từ khóa sẽ tải lại danh sách đầy đủ', async ({ page }) => {
    await openWithProducts(page);
    const { searchInput, cards } = ui(page);

    await searchInput.fill('Laptop Gaming Alpha');
    await searchInput.press('Enter');
    await expect(cards).toHaveCount(1);

    await searchInput.fill('');
    await searchInput.press('Enter');
    await expect(cards).toHaveCount(PRODUCTS.length);
  });

  test('PLP-FUN-05: từ khóa không tồn tại hiển thị empty message', async ({
    page,
  }) => {
    await openWithProducts(page);
    const { searchInput, cards, main } = ui(page);

    await searchInput.fill('san-pham-khong-ton-tai-987654');
    await searchInput.press('Enter');

    await expect(cards).toHaveCount(0);
    await expect(main.getByText(/không tìm thấy sản phẩm/i)).toBeVisible();
  });

  test('PLP-FUN-06: bộ đếm khớp số product card', async ({ page }) => {
    await openWithProducts(page);
    await expect(ui(page).productCount).toHaveText(
      `Hiển thị ${PRODUCTS.length} sản phẩm`,
    );
  });

  test('PLP-STA-01: hiển thị loading state khi API phản hồi chậm', async ({
    page,
  }) => {
    let releaseRequest;
    const waitForRelease = new Promise((resolve) => {
      releaseRequest = resolve;
    });
    await mockProductApi(page, { waitForRelease });
    await page.goto('/');

    try {
      await expect(
        page.getByRole('status').filter({ hasText: /đang tải/i }),
      ).toBeVisible();
    } finally {
      releaseRequest();
    }
  });

  test('PLP-STA-02: API trả mảng rỗng hiển thị empty state', async ({ page }) => {
    await openWithProducts(page, []);
    await expect(ui(page).main.getByText(/chưa có sản phẩm/i)).toBeVisible();
    await expect(ui(page).productCount).toHaveCount(0);
  });

  test('PLP-STA-03: API lỗi hiển thị thông báo thân thiện', async ({ page }) => {
    await mockProductApi(page, { status: 500 });
    await page.goto('/');

    await expect(page.getByRole('alert')).toContainText(
      /không thể tải sản phẩm/i,
    );
  });

  test('PLP-VAL-01: từ khóa chỉ có khoảng trắng được trim', async ({ page }) => {
    let submittedQuery;
    await page.route('**/api/products?*', async (route) => {
      const requestUrl = new URL(route.request().url());
      submittedQuery = requestUrl.searchParams.get('search');
      await route.fulfill({ json: PRODUCTS });
    });
    await page.goto('/');
    const { searchInput } = ui(page);

    await searchInput.fill('   ');
    await searchInput.press('Enter');

    expect(submittedQuery).toBe('');
    await expect(ui(page).cards).toHaveCount(PRODUCTS.length);
  });

  test('PLP-VAL-02: chuỗi HTML trong tìm kiếm không được thực thi', async ({
    page,
  }) => {
    await page.addInitScript(() => {
      window.__xssTriggered = false;
      window.alert = () => {
        window.__xssTriggered = true;
      };
    });
    await openWithProducts(page);
    const payload = '<img src=x onerror=alert(1)>';

    await ui(page).searchInput.fill(payload);
    await ui(page).searchInput.press('Enter');
    await page.waitForTimeout(100);

    expect(await page.evaluate(() => window.__xssTriggered)).toBe(false);
    await expect(ui(page).main.locator('img[src="x"]')).toHaveCount(0);
    await expect(ui(page).main).toContainText(payload);
  });

  test('PLP-RES-01: desktop 1440px hiển thị 3 cột, không tràn ngang', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await openWithProducts(page);

    expect(await columnCount(ui(page).grid)).toBe(3);
    expect(
      await page.evaluate(
        () =>
          document.documentElement.scrollWidth <=
          document.documentElement.clientWidth,
      ),
    ).toBe(true);
  });

  test('PLP-RES-02: tablet 768px hiển thị 2 cột, không tràn ngang', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await openWithProducts(page);

    expect(await columnCount(ui(page).grid)).toBe(2);
    expect(
      await page.evaluate(
        () =>
          document.documentElement.scrollWidth <=
          document.documentElement.clientWidth,
      ),
    ).toBe(true);
  });

  test('PLP-RES-03: mobile 390px hiển thị 1 cột, không tràn ngang', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await openWithProducts(page);

    expect(await columnCount(ui(page).grid)).toBe(1);
    expect(
      await page.evaluate(
        () =>
          document.documentElement.scrollWidth <=
          document.documentElement.clientWidth,
      ),
    ).toBe(true);
  });

  test('PLP-ACC-01: thành phần tương tác có thể nhận focus bằng Tab', async ({
    page,
  }) => {
    await openWithProducts(page);
    const { searchInput, searchButton } = ui(page);

    await searchInput.focus();
    await expect(searchInput).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(searchButton).toBeFocused();

    const outlineStyle = await searchButton.evaluate((element) => {
      const style = getComputedStyle(element);
      return {
        outlineStyle: style.outlineStyle,
        outlineWidth: style.outlineWidth,
      };
    });
    expect(outlineStyle.outlineStyle).not.toBe('none');
    expect(outlineStyle.outlineWidth).not.toBe('0px');
  });

  test('PLP-ACC-02: input có accessible name và ảnh có alt mô tả', async ({
    page,
  }) => {
    await openWithProducts(page);
    await expect(ui(page).searchInput).toHaveAccessibleName(
      /tìm kiếm sản phẩm/i,
    );

    const altTexts = await ui(page).cards.locator('img').evaluateAll((images) =>
      images.map((image) => image.getAttribute('alt')),
    );
    expect(altTexts).toEqual(PRODUCTS.map((product) => product.name));
  });
});
