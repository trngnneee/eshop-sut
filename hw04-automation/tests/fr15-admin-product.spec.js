// @ts-check
const { test, expect } = require('@playwright/test');
const { loadFeatureCases } = require('../helpers/load-test-data');
const {
  registerUser,
  loginUser,
  loginAdmin,
  getAdminCredentials,
} = require('../helpers/auth-api');
const {
  listCategories,
  listProducts,
  createProduct,
  deleteProduct,
  resolveProductName,
  resolveEditedName,
  resolveSiblingName,
  resolveCategoryId,
  findByName,
  findById,
} = require('../helpers/product-api');
const { AdminProductPage } = require('../pages/AdminProductPage');

const { cases } = loadFeatureCases('fr15-admin-product.json', {
  minCases: 12,
  feature: 'FR-15',
});

/**
 * Assertion patterns (HW04 Task 1 — ≥3 distinct):
 * 1. Visibility / hidden
 * 2. Text content (toContainText)
 * 3. Plain API status / field equality / existence
 *
 * Spec oracles are NOT softened for current SUT defects.
 * Matrix evidence (2026-08-10): 6 pass / 8 fail × Chromium, Firefox, WebKit;
 * HTML reports under reports/html/fr15-admin-product/<browser>/ stamped Run by: 23127271.
 * Product fails map to bug-reports/BUG-FR15-001…008 (004,006,008–010,012–014).
 */

/**
 * @param {any} tc
 * @param {any} runtime
 */
function trackId(runtime, id) {
  if (id === undefined || id === null) return;
  const n = Number(id);
  if (!Number.isFinite(n)) return;
  if (!runtime.createdIds.includes(n)) runtime.createdIds.push(n);
}

/**
 * @param {any} tc
 * @param {any} session
 * @param {any} runtime
 */
async function prepareRuntime(tc, session, runtime) {
  const stamp = `${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
  runtime.stamp = stamp;

  const categories = await listCategories();
  if (
    (tc.setup.ensureCategory ||
      tc.setup.seedProduct ||
      tc.inputs?.categoryMode === 'existingFirst') &&
    categories.length === 0
  ) {
    throw new Error(`${tc.id}: no categories seeded — cannot run FR-15`);
  }
  runtime.categories = categories;
  runtime.categoryId = resolveCategoryId(tc.inputs || {}, categories);

  runtime.productName = resolveProductName(tc.inputs || {}, stamp);
  runtime.editedName = resolveEditedName(tc.inputs || {}, stamp);
  runtime.siblingName = resolveSiblingName(tc.inputs || {}, stamp);
  runtime.originalName = runtime.productName;
  runtime.editedPrice =
    tc.inputs?.editPrice !== undefined ? Number(tc.inputs.editPrice) : undefined;
  runtime.siblingPrice =
    tc.inputs?.siblingPrice !== undefined
      ? Number(tc.inputs.siblingPrice)
      : undefined;
  runtime.price =
    tc.inputs?.price !== undefined ? Number(tc.inputs.price) : undefined;

  if (tc.setup.authMode === 'admin') {
    const admin = await loginAdmin();
    expect(admin.status, 'admin login must succeed for setup').toBe(200);
    expect(admin.token, 'admin token required').toBeTruthy();
    session.token = admin.token;
    session.role = 'admin';
  } else if (tc.setup.authMode === 'user') {
    const email = `${tc.id.toLowerCase()}.${stamp}@hw4-fr15.local`;
    const password = 'UserPass1!';
    await registerUser({ name: `HW4 ${tc.id}`, email, password });
    const login = await loginUser({ email, password });
    expect(login.status).toBe(200);
    expect(login.body?.user?.role).not.toBe('admin');
    session.token = login.body.token;
    session.role = 'user';
    session.email = email;
    session.password = password;
  } else {
    session.token = null;
    session.role = 'none';
  }

  // Seed via API for deterministic UI journeys (auth not required by current API).
  if (tc.setup.seedProduct) {
    const seeded = await createProduct(
      {
        name: runtime.productName,
        price: runtime.price,
        description: tc.inputs?.description || '',
        imageUrl: tc.inputs?.imageUrl || '',
        category_id: runtime.categoryId,
      },
      session.token || undefined,
    );
    expect(seeded.status).toBeLessThan(400);
    runtime.productId = seeded.body?.id;
    trackId(runtime, runtime.productId);
  }

  if (tc.setup.seedSibling) {
    const sibling = await createProduct(
      {
        name: runtime.siblingName,
        price: runtime.siblingPrice,
        description: 'sibling',
        imageUrl: '',
        category_id: runtime.categoryId,
      },
      session.token || undefined,
    );
    expect(sibling.status).toBeLessThan(400);
    runtime.siblingId = sibling.body?.id;
    trackId(runtime, runtime.siblingId);
    runtime.siblingBefore = {
      name: runtime.siblingName,
      price: runtime.siblingPrice,
    };
  }
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {any} tc
 * @param {any} session
 * @param {any} runtime
 */
async function ensureAdminUi(page, tc, session, runtime) {
  const admin = new AdminProductPage(page);
  if (tc.setup.authMode !== 'admin' || !session.token) {
    throw new Error(`${tc.id}: UI journey requires admin authMode + token`);
  }
  try {
    await admin.injectAdminToken(session.token);
  } catch {
    await admin.loginWithForm(getAdminCredentials());
  }
  await admin.openProducts();
  return admin;
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {any} tc
 * @param {any} session
 * @param {any} runtime
 */
async function runJourney(page, tc, session, runtime) {
  if (tc.journey === 'apiCreate') {
    const token =
      tc.setup.authMode === 'none' ? undefined : session.token || undefined;
    const result = await createProduct(
      {
        name: runtime.productName,
        price: runtime.price,
        description: tc.inputs?.description || '',
        imageUrl: tc.inputs?.imageUrl || '',
        category_id: runtime.categoryId,
      },
      token,
    );
    runtime.createResponse = result.status;
    if (result.body?.id) {
      runtime.productId = result.body.id;
      trackId(runtime, result.body.id);
    }
    return;
  }

  const admin = await ensureAdminUi(page, tc, session, runtime);

  if (tc.journey === 'uiCreate') {
    await admin.fillProductForm({
      name: runtime.productName,
      price: runtime.price,
      description: tc.inputs?.description || '',
      imageUrl: tc.inputs?.imageUrl || '',
      categoryId: runtime.categoryId,
    });
    const status = await admin.saveProduct();
    runtime.createResponse = status;
    // Discover created id by unique name for cleanup.
    const products = await listProducts();
    const found = findByName(products, runtime.productName);
    if (found?.id) {
      runtime.productId = found.id;
      trackId(runtime, found.id);
    }
    return;
  }

  if (tc.journey === 'uiView') {
    await expect(admin.productRow(runtime.productName)).toBeVisible({
      timeout: 15_000,
    });
    return;
  }

  if (tc.journey === 'uiEdit') {
    await expect(admin.productRow(runtime.productName)).toBeVisible({
      timeout: 15_000,
    });
    await admin.startEdit(runtime.productName);
    await admin.fillProductForm({
      name: runtime.editedName,
      price: runtime.editedPrice,
      categoryId: runtime.categoryId,
    });
    await admin.saveProduct();
    runtime.productName = runtime.editedName;
    return;
  }

  if (tc.journey === 'uiEditIsolation') {
    await expect(admin.productRow(runtime.originalName)).toBeVisible({
      timeout: 15_000,
    });
    await expect(admin.productRow(runtime.siblingName)).toBeVisible({
      timeout: 15_000,
    });
    runtime.siblingBefore = {
      name: runtime.siblingName,
      price: runtime.siblingPrice,
    };
    await admin.startEdit(runtime.originalName);
    await admin.fillProductForm({
      name: runtime.editedName,
      price: runtime.editedPrice,
      categoryId: runtime.categoryId,
    });
    await admin.saveProduct();
    runtime.productName = runtime.editedName;
    return;
  }

  if (tc.journey === 'uiDelete') {
    await expect(admin.productRow(runtime.productName)).toBeVisible({
      timeout: 15_000,
    });
    await admin.deleteProduct(runtime.productName);
    return;
  }

  throw new Error(`${tc.id}: unsupported journey ${tc.journey}`);
}

/**
 * @param {string} match
 * @param {any} runtime
 */
function lookupName(match, runtime) {
  switch (match) {
    case 'nameExact':
    case 'productName':
    case 'namePrice':
    case 'namePriceCategory':
      return runtime.productName;
    case 'originalName':
      return runtime.originalName;
    case 'emptyName':
      return '';
    default:
      return runtime.productName;
  }
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {any} tc
 * @param {any} session
 * @param {any} runtime
 */
async function applyAssertions(page, tc, session, runtime) {
  const admin = new AdminProductPage(page);
  const ctx = {
    productName: runtime.productName,
    siblingName: runtime.siblingName,
  };

  for (const assertion of tc.expected.assertions) {
    switch (assertion.type) {
      case 'visible':
        await expect(admin.target(assertion.target, ctx)).toBeVisible();
        break;
      case 'hidden':
        await expect(admin.target(assertion.target, ctx)).toBeHidden();
        break;
      case 'containText': {
        const text =
          assertion.valueFrom != null
            ? runtime[assertion.valueFrom]
            : assertion.value;
        await expect(admin.target(assertion.target, ctx)).toContainText(
          String(text),
        );
        break;
      }
      case 'apiStatus': {
        const key = assertion.on || 'createResponse';
        const status = runtime[key];
        expect(
          status,
          `${tc.id}: missing runtime.${key} for apiStatus`,
        ).toEqual(expect.any(Number));
        expect(status).toBeGreaterThanOrEqual(assertion.min);
        expect(status).toBeLessThanOrEqual(assertion.max);
        break;
      }
      case 'apiProductExists': {
        const products = await listProducts();
        const name = lookupName(assertion.match, runtime);
        const found = findByName(products, name);
        expect(found, `${tc.id}: expected product "${name}" to exist`).toBeTruthy();
        if (assertion.match === 'namePrice' || assertion.match === 'namePriceCategory') {
          expect(Number(found.price)).toBe(Number(runtime.price));
        }
        if (assertion.match === 'namePriceCategory') {
          expect(Number(found.category_id)).toBe(Number(runtime.categoryId));
        }
        if (found?.id) trackId(runtime, found.id);
        break;
      }
      case 'apiProductAbsent': {
        const products = await listProducts();
        if (assertion.match === 'originalName') {
          // Target product A must no longer have the pre-edit name.
          const stillOriginal = findByName(products, runtime.originalName);
          expect(
            stillOriginal,
            `${tc.id}: original name must not remain on a product after edit`,
          ).toBeFalsy();
          break;
        }
        if (assertion.match === 'emptyName') {
          // Avoid flaking on unrelated empty-name rows; only this attempt's id.
          if (runtime.productId) {
            expect(
              findById(products, runtime.productId),
              `${tc.id}: empty-name create must not persist id ${runtime.productId}`,
            ).toBeFalsy();
          }
          break;
        }
        if (runtime.productId) {
          const byId = findById(products, runtime.productId);
          expect(
            byId,
            `${tc.id}: product id ${runtime.productId} must be absent`,
          ).toBeFalsy();
        }
        const name = lookupName(assertion.match, runtime);
        const found = findByName(products, name);
        expect(
          found,
          `${tc.id}: product name "${name}" must be absent`,
        ).toBeFalsy();
        break;
      }
      case 'apiProductFieldEquals': {
        const products = await listProducts();
        const product =
          (runtime.productId && findById(products, runtime.productId)) ||
          findByName(products, runtime.productName) ||
          findByName(products, runtime.editedName);
        expect(product, `${tc.id}: product for field check`).toBeTruthy();
        const expected =
          assertion.valueFrom != null
            ? runtime[assertion.valueFrom]
            : assertion.value;
        const actual = product[assertion.field];
        if (assertion.field === 'price') {
          expect(Number(actual)).toBe(Number(expected));
        } else {
          expect(actual).toBe(expected);
        }
        break;
      }
      case 'apiSiblingUnchanged': {
        const products = await listProducts();
        const sibling =
          (runtime.siblingId && findById(products, runtime.siblingId)) ||
          findByName(products, runtime.siblingBefore?.name);
        expect(sibling, `${tc.id}: sibling must still exist`).toBeTruthy();
        for (const field of assertion.fields || ['name', 'price']) {
          if (field === 'price') {
            expect(Number(sibling.price)).toBe(
              Number(runtime.siblingBefore.price),
            );
          } else {
            expect(sibling[field]).toBe(runtime.siblingBefore[field]);
          }
        }
        break;
      }
      case 'uiSiblingNameUnchanged': {
        // Spec FR-15: sibling row must still show original name on screen.
        await expect(
          admin.target(assertion.target || 'siblingRow', {
            ...ctx,
            siblingName: runtime.siblingBefore?.name,
          }),
        ).toContainText(String(runtime.siblingBefore?.name));
        break;
      }
      default:
        throw new Error(`${tc.id}: unsupported assertion ${assertion.type}`);
    }
  }
}

/**
 * @param {any} runtime
 * @param {any} session
 * @param {any} tc
 */
async function cleanup(runtime, session, tc) {
  if (tc.setup.cleanupProduct === false) {
    // Delete journey: still remove if delete failed and id remains.
    const products = await listProducts();
    for (const id of runtime.createdIds || []) {
      if (findById(products, id)) {
        await deleteProduct(id, session.token || undefined);
      }
    }
    return;
  }
  for (const id of runtime.createdIds || []) {
    await deleteProduct(id, session.token || undefined);
  }
}

for (const tc of cases) {
  test.describe(`FR-15 Admin Product CRUD — ${tc.id}`, () => {
    /** @type {{ token: string | null, role: string, email?: string, password?: string }} */
    let session;
    /** @type {any} */
    let runtime;

    test.beforeEach(async () => {
      session = { token: null, role: 'none' };
      runtime = { createdIds: [] };
      await prepareRuntime(tc, session, runtime);
    });

    test.afterEach(async () => {
      await cleanup(runtime, session, tc);
    });

    test(`${tc.id}: ${tc.purpose}`, async ({ page }) => {
      await runJourney(page, tc, session, runtime);
      await applyAssertions(page, tc, session, runtime);
    });
  });
}
