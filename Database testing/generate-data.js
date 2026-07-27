const { faker } = require('@faker-js/faker');

function run(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function (err) {
      if (err) reject(err);
      else resolve(this);
    });
  });
}

function get(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
}

function all(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
}

async function setupTestDB(db) {
  // Reset faker seed on every setup call for deterministic generation
  faker.seed(23127207);

  // Clear tables in reverse dependency order
  await run(db, 'DELETE FROM coupon_usage');
  await run(db, 'DELETE FROM orders');
  await run(db, 'DELETE FROM coupons');
  await run(db, 'DELETE FROM products');
  await run(db, 'DELETE FROM users');
  await run(db, 'DELETE FROM sqlite_sequence');

  // Insert standard user (User 1) + optional faker user
  await run(
    db,
    'INSERT INTO users (id, email, name) VALUES (?, ?, ?)',
    [1, 'test@example.com', 'Test User']
  );
  
  const fakerUserEmail = faker.internet.email();
  const fakerUserName = faker.person.fullName();
  await run(
    db,
    'INSERT INTO users (id, email, name) VALUES (?, ?, ?)',
    [2, fakerUserEmail, fakerUserName]
  );

  // Insert 5 products with fixed IDs (1-5) and prices, using Faker for product names and stock
  const productPrices = [100, 200, 300, 400, 500];
  for (let i = 1; i <= 5; i++) {
    const productName = `Product ${i} - ${faker.commerce.productName()}`;
    const stock = faker.number.int({ min: 10, max: 100 });
    await run(
      db,
      'INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)',
      [i, productName, productPrices[i - 1], stock]
    );
  }

  // Dynamic relative timestamps
  const pastDateStr = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
  const futureDateStr = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString();

  // Insert coupons
  // 1. CP_EXPIRED
  await run(
    db,
    `INSERT INTO coupons (id, code, discount_type, discount_value, min_order_amount, max_uses_per_user, expired_at, is_active)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    [1, 'CP_EXPIRED', 'fixed', 10, 0, 1, pastDateStr, 1]
  );

  // 2. CP_INACTIVE
  await run(
    db,
    `INSERT INTO coupons (id, code, discount_type, discount_value, min_order_amount, max_uses_per_user, expired_at, is_active)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    [2, 'CP_INACTIVE', 'fixed', 10, 0, 1, futureDateStr, 0]
  );

  // 3. CP_PERCENT (10% stored as 0.10)
  await run(
    db,
    `INSERT INTO coupons (id, code, discount_type, discount_value, min_order_amount, max_uses_per_user, expired_at, is_active)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    [3, 'CP_PERCENT', 'percent', 0.10, 100, 5, futureDateStr, 1]
  );

  // 4. CP_FIXED
  await run(
    db,
    `INSERT INTO coupons (id, code, discount_type, discount_value, min_order_amount, max_uses_per_user, expired_at, is_active)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    [4, 'CP_FIXED', 'fixed', 15, 0, 5, futureDateStr, 1]
  );

  // 5. CP_MAX_REACHED
  await run(
    db,
    `INSERT INTO coupons (id, code, discount_type, discount_value, min_order_amount, max_uses_per_user, expired_at, is_active)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    [5, 'CP_MAX_REACHED', 'fixed', 10, 0, 1, futureDateStr, 1]
  );

  // Insert 1 usage record for User 1 with CP_MAX_REACHED (coupon_id = 5)
  await run(
    db,
    'INSERT INTO coupon_usage (id, coupon_id, user_id, used_at) VALUES (?, ?, ?, ?)',
    [1, 5, 1, pastDateStr]
  );

  // Insert 2 orders
  // Order 1: pending
  await run(
    db,
    'INSERT INTO orders (id, user_id, total_amount, discount_amount, final_amount, status) VALUES (?, ?, ?, ?, ?, ?)',
    [1, 1, 500, 0, 500, 'pending']
  );

  // Order 2: canceled
  await run(
    db,
    'INSERT INTO orders (id, user_id, total_amount, discount_amount, final_amount, status) VALUES (?, ?, ?, ?, ?, ?)',
    [2, 1, 200, 0, 200, 'canceled']
  );
}

function teardownTestDB(db) {
  return new Promise((resolve, reject) => {
    db.close((err) => {
      if (err) reject(err);
      else resolve();
    });
  });
}

module.exports = {
  setupTestDB,
  teardownTestDB,
  run,
  get,
  all
};
