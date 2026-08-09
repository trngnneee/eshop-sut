# Assertion Patterns — Playwright Testing

## Ba nhóm assertion bắt buộc (HW04)

Mỗi feature script phải dùng **ít nhất 3 pattern khác nhau** từ danh sách dưới.

---

## Nhóm 1: Kiểm tra UI State (Visibility & Existence)

```typescript
// Element có hiển thị không?
await expect(page.getByRole('alert')).toBeVisible();

// Element ẩn / không tồn tại?
await expect(page.locator('.error')).toBeHidden();

// Element tồn tại trong DOM (không nhất thiết visible)?
await expect(page.locator('#success-msg')).toBeAttached();

// Khi nào dùng:
// → Sau khi submit form, kiểm tra success/error notification xuất hiện
// → Sau khi navigate, kiểm tra section mới render
// → Kiểm tra loading spinner biến mất
```

---

## Nhóm 2: Kiểm tra Nội dung (Text & Value)

```typescript
// Chứa text (partial match — hay dùng nhất)
await expect(page.getByRole('heading')).toContainText('Đăng ký thành công');

// Exact text match
await expect(page.locator('.price')).toHaveText('450.000 đ');

// Giá trị input field
await expect(page.getByLabel('Email')).toHaveValue('user@example.com');

// Attribute value
await expect(page.getByRole('button', { name: 'Submit' }))
  .toHaveAttribute('disabled', '');

// Khi nào dùng:
// → Kiểm tra error message đúng nội dung
// → Kiểm tra giá tiền sau khi áp coupon
// → Kiểm tra input được điền đúng data
```

---

## Nhóm 3: Kiểm tra Navigation & Page State

```typescript
// URL sau redirect
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveURL(/\/login|\/home/);

// Page title
await expect(page).toHaveTitle('EShop - Trang chủ');

// Số lượng elements
await expect(page.locator('table tbody tr')).toHaveCount(3);

// Khi nào dùng:
// → Kiểm tra redirect sau đăng nhập thành công
// → Kiểm tra số row trong bảng sau khi import CSV
// → Kiểm tra breadcrumb / page title đúng
```

---

## Nhóm 4: Kiểm tra Interactive State

```typescript
// Button bật/tắt
await expect(page.getByRole('button', { name: 'Submit' })).toBeEnabled();
await expect(page.getByRole('button', { name: 'Submit' })).toBeDisabled();

// Checkbox/Radio checked state
await expect(page.getByRole('checkbox', { name: 'Nhớ mật khẩu' })).toBeChecked();

// Select option
await expect(page.getByRole('combobox')).toHaveValue('active');

// Khi nào dùng:
// → Kiểm tra nút Submit disable khi form chưa điền đủ
// → Kiểm tra trạng thái sau khi user action
```

---

## Mẫu code kết hợp nhiều patterns

```typescript
test('TC05 - Apply coupon and verify price breakdown', async ({ page }, testInfo) => {
  testInfo.annotations.push({ type: 'Run by', description: '23127486' });

  await page.goto('/cart');
  await page.getByPlaceholder('Nhập mã giảm giá').fill('SAVE10');
  await page.getByRole('button', { name: 'Áp dụng' }).click();

  // Pattern 1 (Group 1): Success badge visible
  await expect(page.locator('.coupon-badge')).toBeVisible();

  // Pattern 2 (Group 2): Discount amount correct
  await expect(page.locator('[data-testid="discount-amount"]'))
    .toContainText('50.000 đ');

  // Pattern 3 (Group 2): Final price correct
  await expect(page.locator('[data-testid="total-price"]'))
    .toHaveText('450.000 đ');

  // Pattern 4 (Group 4): Checkout button enabled
  await expect(page.getByRole('button', { name: 'Thanh toán' })).toBeEnabled();
});
```

---

## Assertions cho Negative Cases

```typescript
test('TC03 - Apply expired coupon', async ({ page }, testInfo) => {
  testInfo.annotations.push({ type: 'Run by', description: '23127486' });

  await page.goto('/cart');
  await page.getByPlaceholder('Nhập mã giảm giá').fill('EXPIRED2023');
  await page.getByRole('button', { name: 'Áp dụng' }).click();

  // Kiểm tra error message
  const errorAlert = page.getByRole('alert');
  await expect(errorAlert).toBeVisible();                            // Pattern 1
  await expect(errorAlert).toContainText('Mã giảm giá đã hết hạn'); // Pattern 2

  // Kiểm tra giá KHÔNG thay đổi
  await expect(page.locator('.coupon-badge')).toBeHidden();           // Pattern 3
  await expect(page.locator('[data-testid="discount-amount"]'))
    .toHaveText('0 đ');                                              // Pattern 4
});
```

---

## Soft Assertions (không dừng test khi fail)

```typescript
// Dùng khi muốn check nhiều điều, report tất cả failures
await expect.soft(page.locator('.price')).toHaveText('450.000 đ');
await expect.soft(page.locator('.stock')).toContainText('Còn hàng');
// Test vẫn tiếp tục ngay cả khi assertion trên fail
```

---

## Best Practices

| Nên | Không nên |
|:----|:----------|
| `getByRole('button', { name: '...' })` | `locator('button:nth-child(2)')` |
| `getByLabel('Email')` | `locator('input[type=email]')` |
| `getByTestId('submit-btn')` | `locator('.btn-primary')` |
| `toContainText('...')` cho partial match | `toHaveText('...')` khi text có thể thay đổi |
| `await expect(locator).toBeVisible()` | `await page.waitForTimeout(2000)` |
