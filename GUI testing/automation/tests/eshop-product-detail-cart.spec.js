import { expect, test } from '@playwright/test';

const PRODUCT = {
  id: 1,
  name: 'Laptop Gaming Alpha',
  price: 25_990_000,
  description: 'Laptop hiệu năng cao dành cho chơi game và công việc.',
  imageUrl: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='640' height='360'%3E%3Crect width='100%25' height='100%25' fill='%23dbeafe'/%3E%3C/svg%3E",
};

async function mockProductDetail(page, { status = 200, waitForRelease } = {}) {
  await page.route('**/api/products/1', async (route) => {
    if (waitForRelease) await waitForRelease;
    await route.fulfill({
      status,
      contentType: 'application/json',
      body: JSON.stringify(status === 200 ? PRODUCT : { error: 'Không tìm thấy sản phẩm' }),
    });
  });
}

async function mockProductList(page) {
  await page.route('**/api/products?*', (route) => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([PRODUCT]),
  }));
}

async function openProduct(page) {
  await mockProductDetail(page);
  await page.goto('/product/1');
  await expect(page.getByRole('heading', { name: PRODUCT.name })).toBeVisible();
}

async function addOneItemFromHome(page) {
  await mockProductList(page);
  await page.goto('/');
  await page.getByRole('button', { name: 'Thêm vào giỏ' }).click();
  await expect(page.getByRole('link', { name: /Giỏ hàng 1/ })).toBeVisible();
}

const noHorizontalOverflow = (page) => page.evaluate(() =>
  document.documentElement.scrollWidth <= document.documentElement.clientWidth,
);

test.describe('GUI — EShop / Chi tiết sản phẩm', () => {
  test('PDP-VIS-01: bố cục desktop hiển thị đủ hai vùng và không tràn ngang', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await openProduct(page);
    await expect(page.locator('main img')).toBeVisible();
    await expect(page.getByRole('heading', { name: PRODUCT.name })).toBeVisible();
    expect(await noHorizontalOverflow(page)).toBe(true);
  });

  test('PDP-VIS-02: tên, giá và mô tả sản phẩm hiển thị đúng', async ({ page }) => {
    await openProduct(page);
    await expect(page.getByRole('heading', { name: PRODUCT.name })).toBeVisible();
    await expect(page.locator('main')).toContainText('25.990.000 ₫');
    await expect(page.locator('main')).toContainText(PRODUCT.description);
  });

  test('PDP-ACC-01: ảnh chi tiết có alt bằng tên sản phẩm', async ({ page }) => {
    await openProduct(page);
    await expect(page.locator('main img')).toHaveAttribute('alt', PRODUCT.name);
  });

  test('PDP-ACC-02: ô số lượng có accessible name rõ nghĩa', async ({ page }) => {
    await openProduct(page);
    await expect(page.locator('main input[type="number"]')).toHaveAccessibleName(/số lượng/i);
  });

  test('PDP-VAL-01: ô số lượng khai báo giá trị nhỏ nhất là 1', async ({ page }) => {
    await openProduct(page);
    await expect(page.locator('main input[type="number"]')).toHaveAttribute('min', '1');
  });

  test('PDP-VAL-02: không cho thêm số lượng bằng 0 vào giỏ', async ({ page }) => {
    await openProduct(page);
    await page.locator('main input[type="number"]').fill('0');
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();
    await expect(page.getByRole('alert')).toContainText(/số lượng phải lớn hơn 0/i);
  });

  test('PDP-NAV-01: truy cập trực tiếp route chi tiết giữ đúng URL', async ({ page }) => {
    await openProduct(page);
    await expect(page).toHaveURL(/\/product\/1$/);
  });

  test('PDP-NAV-02: logo EShop quay về trang danh sách', async ({ page }) => {
    await openProduct(page);
    await mockProductList(page);
    await page.getByRole('link', { name: 'EShop' }).click();
    await expect(page).toHaveURL(/\/$/);
    await expect(page.getByRole('heading', { name: 'Danh sách sản phẩm' })).toBeVisible();
  });

  test('PDP-NAV-03: liên kết Giỏ hàng mở đúng route', async ({ page }) => {
    await openProduct(page);
    await page.getByRole('link', { name: 'Giỏ hàng' }).click();
    await expect(page).toHaveURL(/\/cart$/);
    await expect(page.getByRole('heading', { name: /Giỏ hàng của bạn đang trống/i })).toBeVisible();
  });

  test('PDP-STA-01: hiển thị trạng thái đang tải khi API phản hồi chậm', async ({ page }) => {
    let releaseRequest;
    const waitForRelease = new Promise((resolve) => { releaseRequest = resolve; });
    await mockProductDetail(page, { waitForRelease });
    await page.goto('/product/1');
    try {
      await expect(page.getByText('Đang tải...')).toBeVisible();
    } finally {
      releaseRequest();
    }
  });

  test('PDP-STA-02: API 404 hiển thị thông báo lỗi thân thiện', async ({ page }) => {
    await mockProductDetail(page, { status: 404 });
    await page.goto('/product/1');
    await expect(page.getByRole('alert')).toContainText(/không tìm thấy sản phẩm/i);
  });

  test('PDP-FUN-01: lần nhấn đầu tiên thêm sản phẩm vào giỏ', async ({ page }) => {
    await openProduct(page);
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();
    await expect(page.getByRole('link', { name: /Giỏ hàng 1/ })).toBeVisible();
  });

  test('PDP-FUN-02: sản phẩm được thêm sau khi thao tác thành công', async ({ page }) => {
    await openProduct(page);
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();
    await expect(page.getByRole('link', { name: /Giỏ hàng 1/ })).toBeVisible();
  });

  test('PDP-STA-03: nút hiển thị phản hồi Đã thêm sau khi thêm giỏ', async ({ page }) => {
    await openProduct(page);
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();
    await page.getByRole('button', { name: 'Thêm vào giỏ hàng' }).click();
    await expect(page.getByRole('button', { name: 'Đã thêm' })).toBeVisible();
  });

  test('PDP-RES-01: mobile 390px không có phần tử gây tràn ngang', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await openProduct(page);
    expect(await noHorizontalOverflow(page)).toBe(true);
  });
});

test.describe('GUI — EShop / Giỏ hàng', () => {
  test('CART-STA-01: giỏ rỗng hiển thị empty state rõ ràng', async ({ page }) => {
    await page.goto('/cart');
    await expect(page.getByRole('heading', { name: /Giỏ hàng của bạn đang trống/i })).toBeVisible();
  });

  test('CART-NAV-01: liên kết Tiếp tục mua sắm quay về trang chủ', async ({ page }) => {
    await mockProductList(page);
    await page.goto('/cart');
    await page.getByRole('link', { name: 'Tiếp tục mua sắm' }).click();
    await expect(page).toHaveURL(/\/$/);
  });

  test('CART-FUN-01: thêm từ danh sách cập nhật badge số lượng', async ({ page }) => {
    await addOneItemFromHome(page);
    await expect(page.getByRole('link', { name: /Giỏ hàng 1/ })).toBeVisible();
  });

  test('CART-NAV-02: click badge Giỏ hàng mở đúng route', async ({ page }) => {
    await addOneItemFromHome(page);
    await page.getByRole('link', { name: /Giỏ hàng 1/ }).click();
    await expect(page).toHaveURL(/\/cart$/);
    await expect(page.getByRole('heading', { name: 'Giỏ Hàng' })).toBeVisible();
  });

  test('CART-VIS-01: bảng giỏ có đủ năm tiêu đề cột', async ({ page }) => {
    await addOneItemFromHome(page);
    await page.goto('/cart');
    for (const heading of ['Sản phẩm', 'Giá', 'Số lượng', 'Thành tiền', 'Thao tác']) {
      await expect(page.getByRole('columnheader', { name: heading })).toBeVisible();
    }
  });

  test('CART-FUN-02: dòng sản phẩm và tổng tạm tính chính xác', async ({ page }) => {
    await addOneItemFromHome(page);
    await page.goto('/cart');
    await expect(page.getByRole('cell', { name: PRODUCT.name })).toBeVisible();
    await expect(page.locator('main')).toContainText('Tổng tạm tính: 25.990.000 ₫');
  });

  test('CART-FUN-03: xóa sản phẩm đưa giỏ về empty state', async ({ page }) => {
    await addOneItemFromHome(page);
    await page.goto('/cart');
    await page.getByRole('button', { name: 'Xóa' }).click();
    await expect(page.getByRole('heading', { name: /Giỏ hàng của bạn đang trống/i })).toBeVisible();
  });

  test('CART-NAV-03: khách chưa đăng nhập được chuyển tới Login khi checkout', async ({ page }) => {
    await addOneItemFromHome(page);
    await page.goto('/cart');
    page.once('dialog', (dialog) => dialog.accept());
    await page.getByRole('button', { name: 'Tiến hành thanh toán' }).click();
    await expect(page).toHaveURL(/\/login$/);
  });

  test('CART-ACC-01: bảng giỏ có accessible name hoặc caption', async ({ page }) => {
    await addOneItemFromHome(page);
    await page.goto('/cart');
    await expect(page.getByRole('table')).toHaveAccessibleName(/giỏ hàng/i);
  });

  test('CART-RES-01: mobile 390px không tràn ngang', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await addOneItemFromHome(page);
    await page.goto('/cart');
    expect(await noHorizontalOverflow(page)).toBe(true);
  });
});
