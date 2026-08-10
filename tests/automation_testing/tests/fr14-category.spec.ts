import { test, expect } from '@playwright/test';
import { AdminCategoriesPage } from '../pages/AdminCategoriesPage';
import { loginToken, getCategories, deleteCategory } from '../utils/api';
import data from '../data/fr14-category.json';

// FR-14 — Quản lý Danh mục (CRUD) trên Web Admin
// Data-driven: toàn bộ test case đọc từ data/fr14-category.json
//
// Traceability — TC fail-đúng-kỳ-vọng đã được xác nhận là bug của SUT:
//   FR14-TC03 + TC04 → issue #398 (tên rỗng/khoảng trắng vẫn được thêm)
// Mỗi test chụp snapshot danh mục trước khi chạy; afterEach xóa mọi danh mục phát sinh
// để CSDL không bị rác giữa các lần chạy/giữa các browser.

const LONG_255 = 'A'.repeat(255);
const resolveName = (raw: string, runId: string) =>
  raw.replace('{{UNIQUE}}', runId).replace('{{LONG255}}', LONG_255);

test.describe(data.feature, { tag: ['@fr14', '@pool-c', '@admin'] }, () => {
  let adminToken: string;
  let snapshotIds: number[] = [];
  let admin: AdminCategoriesPage;

  test.beforeAll(async ({ request }) => {
    adminToken = await loginToken(request, 'admin@eshop.com', 'Admin123!');
  });

  test.beforeEach(async ({ page, request }) => {
    snapshotIds = (await getCategories(request)).map((c) => c.id);
    // Bơm token qua localStorage để bỏ qua màn hình login admin (đã có test riêng cho FR-12)
    await page.addInitScript((t) => localStorage.setItem('adminToken', t), adminToken);
    admin = new AdminCategoriesPage(page);
    await admin.gotoCategoriesTab();
  });

  test.afterEach(async ({ request }) => {
    // Dọn: xóa mọi danh mục không có trong snapshot đầu test
    for (const c of await getCategories(request)) {
      if (!snapshotIds.includes(c.id)) {
        await deleteCategory(request, adminToken, c.id);
      }
    }
  });

  for (const tc of data.cases) {
    test(`${tc.id} [${tc.type}] ${tc.title}`, async ({ page }, testInfo) => {
      const runId = `${testInfo.project.name}-${Date.now()}`;
      const name = tc.name !== undefined ? resolveName(tc.name, runId) : '';

      switch (tc.action) {
        case 'view': {
          for (const header of tc.expected.headers!) {
            await expect(page.getByRole('columnheader', { name: header })).toBeVisible();
          }
          for (const seeded of tc.expected.contains!) {
            await expect.soft(admin.cellByName(seeded).first()).toBeVisible();
          }
          break;
        }

        case 'create': {
          const rowsBefore = await admin.rows.count();
          await admin.addCategory(name);
          if (tc.expected.accepted) {
            await expect(admin.cellByName(name)).toBeVisible();
            await expect(admin.rows).toHaveCount(rowsBefore + 1);
          } else {
            // Spec: tên bắt buộc → không được thêm dòng mới vào bảng
            await expect(
              admin.rows,
              'tên rỗng/khoảng trắng phải bị từ chối, số dòng giữ nguyên',
            ).toHaveCount(rowsBefore);
          }
          break;
        }

        case 'create-duplicate': {
          await admin.addCategory(name);
          await expect(admin.cellByName(name)).toHaveCount(tc.expected.cellCount!);
          break;
        }

        case 'create-xss': {
          await admin.addCategory(name);
          // Chuỗi thẻ HTML phải hiển thị nguyên văn, không được render thành phần tử
          await expect(admin.table).toContainText(tc.expected.literalText!);
          await expect(admin.table.locator('b')).toHaveCount(0);
          break;
        }

        case 'delete': {
          await admin.addCategory(name);
          const row = admin.rowByText(name);
          await expect(row).toHaveCount(1);
          await row.getByRole('button', { name: 'Xóa' }).click();
          await expect(admin.rowByText(name)).toHaveCount(0);
          break;
        }

        case 'persist': {
          await admin.addCategory(name);
          await expect(admin.cellByName(name)).toBeVisible();
          await page.reload();
          await admin.openCategoriesTab();
          await expect(admin.cellByName(name)).toBeVisible();
          break;
        }

        case 'select-integration': {
          await admin.addCategory(name);
          await expect(admin.cellByName(name)).toBeVisible();
          await admin.openProductsTab();
          await expect(page.locator('select option').filter({ hasText: name })).toHaveCount(1);
          break;
        }

        case 'input-cleared': {
          await admin.addCategory(name);
          await expect(admin.cellByName(name)).toBeVisible();
          await expect(admin.nameInput).toHaveValue('');
          break;
        }
      }
    });
  }
});
