// generate-data.js — Test Data Generation & Management
// Sinh dữ liệu biên (boundary data) + quản lý vòng đời test (setup/teardown).
const { faker } = require('@faker-js/faker');

// ---------------------------------------------------------------------------
// Bộ dữ liệu coupon biên theo yêu cầu Phần 3.1.1
//   CP_EXPIRED     : hết hạn (expired_at < ngày hiện tại) -> phải bị từ chối
//   CP_INACTIVE    : còn hạn nhưng is_active = 0          -> phải bị từ chối
//   CP_PERCENT     : giảm 10% (0.10), min_order = 100     -> kiểm tra công thức
//   CP_FIXED       : giảm cố định 15, không phụ thuộc tổng đơn
//   CP_MAX_REACHED : user 1 đã đạt max lượt dùng (chèn sẵn coupon_usage)
// ---------------------------------------------------------------------------
const BOUNDARY_COUPONS = [
  { id: 1, code: 'CP_EXPIRED',     type: 'fixed',   value: 10,   min: 0,   maxUses: 1, expired: '2020-01-01', active: 1 },
  { id: 2, code: 'CP_INACTIVE',    type: 'fixed',   value: 10,   min: 0,   maxUses: 1, expired: '2030-01-01', active: 0 },
  { id: 3, code: 'CP_PERCENT',     type: 'percent', value: 0.10, min: 100, maxUses: 5, expired: '2030-01-01', active: 1 },
  { id: 4, code: 'CP_FIXED',       type: 'fixed',   value: 15,   min: 0,   maxUses: 5, expired: '2030-01-01', active: 1 },
  { id: 5, code: 'CP_MAX_REACHED', type: 'fixed',   value: 10,   min: 0,   maxUses: 1, expired: '2030-01-01', active: 1 },
];

// Sinh sản phẩm bằng faker: id 1..n cố định để test lặp lại được,
// price LUÔN là number (phục vụ test Data Type Consistency).
function generateProducts(count = 5) {
  const products = [];
  for (let id = 1; id <= count; id++) {
    products.push({
      id,
      name: faker.commerce.productName(),
      price: Number(faker.commerce.price({ min: 10, max: 500, dec: 2 })),
      stock: faker.number.int({ min: 0, max: 100 }),
    });
  }
  return products;
}

// Sinh thêm user phụ bằng faker (user 1 luôn cố định để test ổn định).
function generateUsers(count = 3) {
  const users = [{ id: 1, email: 'test@example.com', name: 'Test User' }];
  for (let id = 2; id <= count; id++) {
    users.push({ id, email: `user${id}_${faker.internet.email()}`, name: faker.person.fullName() });
  }
  return users;
}

// Đơn hàng phục vụ test state machine:
//   Order 1: pending  -> test chuỗi chuyển trạng thái hợp lệ
//   Order 2: canceled -> test terminal state (canceled -> delivered phải bị chặn)
const SEED_ORDERS = [
  { id: 1, user_id: 1, total: 200, discount: 0, final: 200, status: 'pending' },
  { id: 2, user_id: 1, total: 150, discount: 0, final: 150, status: 'canceled' },
];

// setupTestDB(): làm sạch toàn bộ bảng rồi insert bộ dữ liệu chuẩn.
// Gọi trong beforeEach để bảo đảm Test Isolation — mỗi test chạy trên
// cùng một trạng thái DB, không phụ thuộc dữ liệu test trước để lại.
function setupTestDB(db) {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run(`DELETE FROM coupon_usage`);
      db.run(`DELETE FROM coupons`);
      db.run(`DELETE FROM orders`);
      db.run(`DELETE FROM products`);
      db.run(`DELETE FROM users`);

      for (const u of generateUsers()) {
        db.run(`INSERT INTO users (id, email, name) VALUES (?, ?, ?)`,
          [u.id, u.email, u.name]);
      }

      for (const p of generateProducts()) {
        db.run(`INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)`,
          [p.id, p.name, p.price, p.stock]);
      }

      for (const c of BOUNDARY_COUPONS) {
        db.run(`INSERT INTO coupons
                (id, code, discount_type, discount_value, min_order_amount,
                 max_uses_per_user, expired_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
          [c.id, c.code, c.type, c.value, c.min, c.maxUses, c.expired, c.active]);
      }

      for (const o of SEED_ORDERS) {
        db.run(`INSERT INTO orders
                (id, user_id, total_amount, discount_amount, final_amount, status)
                VALUES (?, ?, ?, ?, ?, ?)`,
          [o.id, o.user_id, o.total, o.discount, o.final, o.status]);
      }

      // User 1 đã dùng hết lượt CP_MAX_REACHED (max_uses_per_user = 1)
      db.run(`INSERT INTO coupon_usage (coupon_id, user_id, used_at)
              VALUES (5, 1, CURRENT_TIMESTAMP)`,
        (err) => (err ? reject(err) : resolve()));
    });
  });
}

// teardownTestDB(): đóng kết nối, dọn tài nguyên sau khi suite kết thúc.
function teardownTestDB(db) {
  return new Promise((resolve, reject) => {
    db.close((err) => (err ? reject(err) : resolve()));
  });
}

module.exports = {
  setupTestDB,
  teardownTestDB,
  generateProducts,
  generateUsers,
  BOUNDARY_COUPONS,
  SEED_ORDERS,
};
