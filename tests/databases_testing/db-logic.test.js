// db-logic.test.js — Database Integrity & Integration Testing (Jest + Supertest)
//
// LƯU Ý: Các assertion mô tả HÀNH VI ĐÚNG theo đặc tả. Vì app.js (starter kit)
// chứa bug có chủ đích, một số test sẽ FAIL — đó là bằng chứng chứng minh bug
// tồn tại (xem REPORT.md). Các test FAIL dự kiến được đánh dấu [EXPECTED FAIL].
const request = require('supertest');
const { app, db } = require('./app');
const { setupTestDB, teardownTestDB } = require('./generate-data');

// Helper promisify: đưa assertion ra NGOÀI callback native của sqlite3.
// (Throw bên trong callback native làm hỏng statement queue của sqlite3.)
const dbRun = (sql, params = []) =>
  new Promise((resolve) => db.run(sql, params, (err) => resolve(err)));
const dbAll = (sql, params = []) =>
  new Promise((resolve, reject) =>
    db.all(sql, params, (err, rows) => (err ? reject(err) : resolve(rows))));

beforeEach(() => setupTestDB(db));
afterAll(() => teardownTestDB(db));

// ===========================================================================
// PHẦN 2 — DATABASE INTEGRITY TESTING
// ===========================================================================
describe('Phần 2.1 — Referential Integrity', () => {
  // [EXPECTED FAIL] Chứng minh BUG-03: coupon_usage thiếu FOREIGN KEY.
  test('Referential Integrity: orphan record sau khi xóa user', async () => {
    const delErr = await dbRun(`DELETE FROM users WHERE id = 1`);
    if (delErr) {
      // Hợp lệ nếu DB chặn lệnh xóa vì còn bản ghi con (FK RESTRICT).
      expect(delErr.code).toBe('SQLITE_CONSTRAINT');
      return;
    }
    const rows = await dbAll(`SELECT * FROM coupon_usage WHERE user_id = 1`);
    // Nếu FK + ON DELETE CASCADE đúng, rows phải rỗng.
    expect(rows.length).toBe(0); // Dự kiến FAIL: chứng minh lỗ hổng.
  });

  // [EXPECTED FAIL] Orphan record tương tự khi xóa coupon cha.
  test('Referential Integrity: orphan record sau khi xóa coupon', async () => {
    const delErr = await dbRun(`DELETE FROM coupons WHERE id = 5`);
    if (delErr) {
      expect(delErr.code).toBe('SQLITE_CONSTRAINT');
      return;
    }
    const rows = await dbAll(`SELECT * FROM coupon_usage WHERE coupon_id = 5`);
    expect(rows.length).toBe(0); // Dự kiến FAIL: chứng minh lỗ hổng.
  });
});

describe('Phần 2.2 — Constraints & Data Anomaly', () => {
  // PASS: schema có UNIQUE trên coupons.code.
  test('Unique Constraint: không cho phép trùng code coupon', async () => {
    const err = await dbRun(`INSERT INTO coupons
      (code, discount_type, discount_value, expired_at)
      VALUES ('CP_FIXED', 'fixed', 5, '2030-01-01')`);
    expect(err).not.toBeNull();
    expect(err.code).toBe('SQLITE_CONSTRAINT');
  });

  // PASS: schema có UNIQUE trên users.email.
  test('Unique Constraint: không cho phép trùng email user', async () => {
    const err = await dbRun(`INSERT INTO users (email, name)
      VALUES ('test@example.com', 'Another User')`);
    expect(err).not.toBeNull();
    expect(err.code).toBe('SQLITE_CONSTRAINT');
  });

  // [EXPECTED FAIL] Chứng minh BUG-04: API ép price thành string với ID chẵn.
  test('Data Type Consistency: price luôn phải là number', async () => {
    for (let id = 1; id <= 5; id++) {
      const res = await request(app).get(`/api/products/${id}`);
      if (res.statusCode === 200) {
        expect(typeof res.body.price).toBe('number'); // Dự kiến FAIL ở id chẵn.
      }
    }
  });
});

// ===========================================================================
// PHẦN 3 — DATABASE UNIT / INTEGRATION TESTING
// ===========================================================================
describe('Phần 3.1 — POST /api/apply-coupon (FR09)', () => {
  // [EXPECTED FAIL] Chứng minh BUG-01: công thức phần trăm sai.
  // Đơn 200, giảm 10% -> discount đúng = 20, final = 180.
  // Code hiện tại: 200 * (1 - 0.10) = 180 (discount), final = 20 -> SAI.
  test('Case 1 (Valid): CP_PERCENT giảm đúng 10% cho đơn 200', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1, coupon_code: 'CP_PERCENT', total_amount: 200,
    });
    expect(res.statusCode).toBe(200);
    expect(res.body.discount_amount).toBe(20);  // Dự kiến FAIL: nhận 180.
    expect(res.body.final_amount).toBe(180);    // Dự kiến FAIL: nhận 20.
  });

  // PASS: ràng buộc min_order_amount hoạt động đúng.
  test('Case 2 (Below Min): đơn hàng chưa đạt min_order_amount', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1, coupon_code: 'CP_PERCENT', total_amount: 50,
    });
    expect(res.statusCode).toBe(400);
  });

  // PASS: boundary theo thời gian — coupon hết hạn bị từ chối.
  test('Case 3 (Expired): coupon đã hết hạn', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1, coupon_code: 'CP_EXPIRED', total_amount: 100,
    });
    expect(res.statusCode).toBe(400);
  });

  // PASS: coupon bị khóa (is_active = 0) bị từ chối dù còn hạn.
  test('Case 3b (Inactive): coupon bị khóa vẫn phải bị từ chối', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1, coupon_code: 'CP_INACTIVE', total_amount: 100,
    });
    expect(res.statusCode).toBe(400);
  });

  // PASS: giới hạn lượt dùng theo user.
  test('Case 4 (Max Usage): user đã dùng hết lượt', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1, coupon_code: 'CP_MAX_REACHED', total_amount: 100,
    });
    expect(res.statusCode).toBe(400);
  });

  // PASS: kiểm chứng công thức giảm cố định (nhánh else không có bug).
  test('Case 5 (Fixed): CP_FIXED giảm đúng 15 cho đơn 100', async () => {
    const res = await request(app).post('/api/apply-coupon').send({
      user_id: 1, coupon_code: 'CP_FIXED', total_amount: 100,
    });
    expect(res.statusCode).toBe(200);
    expect(res.body.discount_amount).toBe(15);
    expect(res.body.final_amount).toBe(85);
  });
});

describe('Phần 3.2 — PUT /api/admin/orders/:id/status (FR10 & FR18)', () => {
  // PASS: chuỗi chuyển trạng thái hợp lệ của state machine.
  test('Valid: pending -> confirmed -> shipping -> delivered', async () => {
    let res = await request(app)
      .put('/api/admin/orders/1/status').send({ status: 'confirmed' });
    expect(res.statusCode).toBe(200);

    res = await request(app)
      .put('/api/admin/orders/1/status').send({ status: 'shipping' });
    expect(res.statusCode).toBe(200);

    res = await request(app)
      .put('/api/admin/orders/1/status').send({ status: 'delivered' });
    expect(res.statusCode).toBe(200);
  });

  // PASS: không được nhảy cóc pending -> delivered.
  test('Invalid: pending -> delivered (nhảy cóc) phải bị chặn', async () => {
    const res = await request(app)
      .put('/api/admin/orders/1/status').send({ status: 'delivered' });
    expect(res.statusCode).toBe(400);
  });

  // [EXPECTED FAIL] Chứng minh BUG-02: canceled là terminal state
  // nhưng code cho phép canceled -> delivered.
  test('Invalid: canceled -> delivered phải bị chặn', async () => {
    // Order #2 được setup sẵn ở trạng thái canceled (generate-data.js).
    const res = await request(app)
      .put('/api/admin/orders/2/status').send({ status: 'delivered' });
    expect(res.statusCode).toBe(400); // Dự kiến FAIL: nhận 200.
  });

  test('404 khi order không tồn tại', async () => {
    const res = await request(app)
      .put('/api/admin/orders/999/status').send({ status: 'confirmed' });
    expect(res.statusCode).toBe(404);
  });
});
