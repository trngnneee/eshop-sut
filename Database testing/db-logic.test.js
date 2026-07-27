const request = require('supertest');
const { app, db, schemaReady } = require('./app');
const { setupTestDB, teardownTestDB, run, get, all } = require('./generate-data');

beforeAll(async () => {
  await schemaReady;
});

beforeEach(async () => {
  await setupTestDB(db);
});

afterAll(async () => {
  await teardownTestDB(db);
});

describe('Database Integrity Testing', () => {
  // TC-DB-001: Referential Integrity – orphan record
  test('TC-DB-001: Referential Integrity – orphan record', async () => {
    // Confirm child record exists before deletion
    const beforeRows = await all(db, 'SELECT * FROM coupon_usage WHERE user_id = 1');
    expect(beforeRows.length).toBeGreaterThan(0);

    // Delete parent user
    await run(db, 'DELETE FROM users WHERE id = 1');

    // Query orphan records
    const afterRows = await all(db, 'SELECT * FROM coupon_usage WHERE user_id = 1');

    // Expected according to proper DB design: no orphan records (length === 0)
    // Expected Result for test suite: FAIL (due to missing FK & cascade deletion design defect)
    expect(afterRows.length).toBe(0);
  });

  // TC-DB-002: Unique Constraint
  test('TC-DB-002: Unique Constraint', async () => {
    const countBefore = (await get(db, 'SELECT COUNT(*) as count FROM coupons')).count;
    let err = null;

    try {
      await run(
        db,
        "INSERT INTO coupons (code, discount_type, discount_value, min_order_amount, max_uses_per_user, expired_at, is_active) VALUES ('CP_FIXED', 'fixed', 10, 0, 1, '2030-01-01', 1)"
      );
    } catch (e) {
      err = e;
    }

    const countAfter = (await get(db, 'SELECT COUNT(*) as count FROM coupons')).count;

    expect(err).not.toBeNull();
    expect(err.code || err.message).toMatch(/SQLITE_CONSTRAINT/);
    expect(countAfter).toBe(countBefore);
  });

  // TC-DB-003: Data Type Consistency
  test('TC-DB-003: Data Type Consistency – price field must be number across all products', async () => {
    const results = [];

    for (let id = 1; id <= 5; id++) {
      const res = await request(app).get(`/api/products/${id}`);

      results.push({
        id,
        statusCode: res.statusCode,
        price: res.body.price,
        priceType: typeof res.body.price
      });
    }

    // Verify all products return HTTP 200
    expect(results.map(({ id, statusCode }) => ({ id, statusCode }))).toEqual([
      { id: 1, statusCode: 200 },
      { id: 2, statusCode: 200 },
      { id: 3, statusCode: 200 },
      { id: 4, statusCode: 200 },
      { id: 5, statusCode: 200 }
    ]);

    // Filter invalid price data types (expected: empty array, actual: contains IDs 2 and 4)
    const invalidProducts = results.filter((result) => result.priceType !== 'number');

    // Expected Result for test suite: FAIL (due to even ID string cast bug)
    expect(invalidProducts).toEqual([]);
  });
});

describe('Integration Testing – Apply Coupon', () => {
  // TC-COUPON-001: Valid percent coupon apply
  test('TC-COUPON-001: Coupon percent hợp lệ – tính toán discount_amount và final_amount chính xác', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1,
      coupon_code: 'CP_PERCENT',
      total_amount: 200
    });

    expect(res.statusCode).toBe(200);

    // Expected formula: discount = 200 * 0.10 = 20, final = 200 - 20 = 180
    // Expected Result for test suite: FAIL (due to bug formula discount = 200 * (1 - 0.10) = 180)
    expect(res.body).toMatchObject({
      total_amount: 200,
      discount_amount: 20,
      final_amount: 180,
      coupon_code: 'CP_PERCENT'
    });
  });

  // TC-COUPON-002: Total amount below minimum requirement
  test('TC-COUPON-002: Tổng đơn dưới min_order_amount – hệ thống từ chối', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1,
      coupon_code: 'CP_PERCENT',
      total_amount: 50
    });

    expect(res.statusCode).toBe(400);
    expect(res.body.error).toBeDefined();
  });

  // TC-COUPON-003: Expired coupon
  test('TC-COUPON-003: Coupon hết hạn – hệ thống từ chối', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1,
      coupon_code: 'CP_EXPIRED',
      total_amount: 100
    });

    expect(res.statusCode).toBe(400);
    expect(res.body.error).toBeDefined();
  });

  // TC-COUPON-004: Max uses reached
  test('TC-COUPON-004: Đã dùng hết lượt – hệ thống từ chối', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1,
      coupon_code: 'CP_MAX_REACHED',
      total_amount: 100
    });

    expect(res.statusCode).toBe(400);
    expect(res.body.error).toBeDefined();
  });

  // TC-COUPON-005: Inactive coupon
  test('TC-COUPON-005: Coupon inactive – hệ thống từ chối', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1,
      coupon_code: 'CP_INACTIVE',
      total_amount: 100
    });

    expect(res.statusCode).toBe(400);
    expect(res.body.error).toBeDefined();
  });

  // TC-COUPON-006: Valid fixed coupon apply
  test('TC-COUPON-006: Coupon fixed hợp lệ – tính toán discount_amount và final_amount chính xác', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1,
      coupon_code: 'CP_FIXED',
      total_amount: 100
    });

    expect(res.statusCode).toBe(200);
    expect(res.body.discount_amount).toBe(15);
    expect(res.body.final_amount).toBe(85);
  });
});

describe('Integration Testing – Order State Machine', () => {
  // TC-ORDER-001: Valid status transition chain
  test('TC-ORDER-001: Valid transition chain – pending -> confirmed -> shipping -> delivered', async () => {
    // 1. pending -> confirmed
    const res1 = await request(app)
      .put('/api/admin/orders/1/status')
      .send({ status: 'confirmed' });
    expect(res1.statusCode).toBe(200);
    expect(res1.body.status).toBe('confirmed');

    // 2. confirmed -> shipping
    const res2 = await request(app)
      .put('/api/admin/orders/1/status')
      .send({ status: 'shipping' });
    expect(res2.statusCode).toBe(200);
    expect(res2.body.status).toBe('shipping');

    // 3. shipping -> delivered
    const res3 = await request(app)
      .put('/api/admin/orders/1/status')
      .send({ status: 'delivered' });
    expect(res3.statusCode).toBe(200);
    expect(res3.body.status).toBe('delivered');

    // Direct database state verification
    const order = await get(db, 'SELECT status FROM orders WHERE id = ?', [1]);
    expect(order.status).toBe('delivered');
  });

  // TC-ORDER-002: Invalid canceled -> delivered transition
  test('TC-ORDER-002: Invalid canceled -> delivered status transition – hệ thống phải từ chối', async () => {
    const res = await request(app)
      .put('/api/admin/orders/2/status')
      .send({ status: 'delivered' });

    // Query database state directly
    const order = await get(db, 'SELECT status FROM orders WHERE id = ?', [2]);

    // Expected: HTTP 400 and database status remains 'canceled'
    // Expected Result for test suite: FAIL (due to bug allowing canceled -> delivered transition)
    expect({
      statusCode: res.statusCode,
      databaseStatus: order.status
    }).toEqual({
      statusCode: 400,
      databaseStatus: 'canceled'
    });
  });
});
