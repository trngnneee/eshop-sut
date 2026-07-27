// app.js — Starter kit theo đề bài (Mini Lab Database Testing)
// Mã nguồn CÓ CHỦ ĐÍCH chứa lỗi (đánh dấu bằng comment LỖI).
// KHÔNG sửa trực tiếp — test sẽ phát hiện, fix patch đề xuất trong REPORT.md.
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();

app.use(express.json());
const db = new sqlite3.Database(':memory:');

db.serialize(() => {
  db.run(`CREATE TABLE users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, name TEXT)`);
  db.run(`CREATE TABLE products
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, stock INTEGER)`);
  db.run(`CREATE TABLE coupons
    (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE,
     discount_type TEXT, discount_value REAL, min_order_amount REAL,
     max_uses_per_user INTEGER, expired_at DATETIME, is_active INTEGER)`);

  // LỖI THIẾT KẾ: không khai báo FOREIGN KEY!
  db.run(`CREATE TABLE coupon_usage
    (id INTEGER PRIMARY KEY AUTOINCREMENT, coupon_id INTEGER,
     user_id INTEGER, used_at DATETIME)`);

  db.run(`CREATE TABLE orders
    (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
     total_amount REAL, discount_amount REAL, final_amount REAL, status TEXT)`);
});

// API 1: Lấy thông tin sản phẩm
app.get('/api/products/:id', (req, res) => {
  const id = req.params.id;
  db.get(`SELECT * FROM products WHERE id = ?`, [id], (err, row) => {
    if (err || !row) return res.status(404).json({ error: 'Product not found' });

    // Cố tình ép sai kiểu dữ liệu ở các ID chẵn
    if (row.id % 2 === 0) row.price = row.price.toString();
    res.json(row);
  });
});

// API 2: Áp dụng coupon
app.post('/api/apply-coupon', (req, res) => {
  const { user_id, coupon_code, total_amount } = req.body;

  db.get(`SELECT * FROM coupons WHERE code = ?`, [coupon_code],
    (err, coupon) => {
      if (!coupon) return res.status(400).json({ error: 'Mã không tồn tại' });
      if (!coupon.is_active)
        return res.status(400).json({ error: 'Mã đã bị khóa' });
      if (new Date(coupon.expired_at) < new Date())
        return res.status(400).json({ error: 'Mã đã hết hạn' });
      if (total_amount < coupon.min_order_amount)
        return res.status(400).json({
          error: 'Chưa đạt giá trị đơn hàng tối thiểu'
        });

      db.get(`SELECT COUNT(*) as count FROM coupon_usage
              WHERE coupon_id = ? AND user_id = ?`,
        [coupon.id, user_id], (err, result) => {
          if (result.count >= coupon.max_uses_per_user) {
            return res.status(400).json({ error: 'Bạn đã dùng hết lượt mã này' });
          }

          let discount_amount = 0;
          if (coupon.discount_type === 'percent') {
            // LỖI: công thức phần trăm sai
            discount_amount = total_amount * (1 - coupon.discount_value);
          } else {
            discount_amount = coupon.discount_value;
          }

          const final_amount = Math.max(0, total_amount - discount_amount);
          res.json({ total_amount, discount_amount, final_amount, coupon_code });
        });
    });
});

// API 3: Cập nhật trạng thái đơn hàng (Admin)
app.put('/api/admin/orders/:id/status', (req, res) => {
  const { status } = req.body;
  const { id } = req.params;

  db.get(`SELECT status FROM orders WHERE id = ?`, [id], (err, order) => {
    if (!order) return res.status(404).json({ error: 'Order not found' });

    const currentStatus = order.status;
    let isValidTransition = false;

    if (currentStatus === 'pending' && status === 'confirmed')
      isValidTransition = true;
    if (currentStatus === 'confirmed' && status === 'shipping')
      isValidTransition = true;
    if (currentStatus === 'shipping' && status === 'delivered')
      isValidTransition = true;

    // LỖI: đơn đã hủy lại được phép thành Delivered!
    if (currentStatus === 'canceled' && status === 'delivered')
      isValidTransition = true;

    if (!isValidTransition) {
      return res.status(400).json({
        error: `Không thể chuyển trạng thái từ ${currentStatus} sang ${status}`
      });
    }

    db.run(`UPDATE orders SET status = ? WHERE id = ?`, [status, id],
      function (err) {
        res.json({ message: 'Update status successfully', status });
      });
  });
});

module.exports = { app, db };
