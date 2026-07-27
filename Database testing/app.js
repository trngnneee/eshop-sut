const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
app.use(express.json());

const db = new sqlite3.Database(':memory:');

const schemaReady = new Promise((resolve, reject) => {
  db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE,
      name TEXT
    );`);

    db.run(`CREATE TABLE IF NOT EXISTS products (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      price REAL,
      stock INTEGER
    );`);

    db.run(`CREATE TABLE IF NOT EXISTS coupons (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      code TEXT UNIQUE,
      discount_type TEXT,
      discount_value REAL,
      min_order_amount REAL,
      max_uses_per_user INTEGER,
      expired_at DATETIME,
      is_active INTEGER
    );`);

    db.run(`CREATE TABLE IF NOT EXISTS coupon_usage (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      coupon_id INTEGER,
      user_id INTEGER,
      used_at DATETIME
    );`);

    db.run(`CREATE TABLE IF NOT EXISTS orders (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      total_amount REAL,
      discount_amount REAL,
      final_amount REAL,
      status TEXT
    );`, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
});

// 5.1. GET /api/products/:id
app.get('/api/products/:id', (req, res) => {
  const productId = req.params.id;
  db.get('SELECT * FROM products WHERE id = ?', [productId], (err, row) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (!row) {
      return res.status(404).json({ error: 'Product not found' });
    }
    // Hidden bug: if product ID is even, convert price to string
    if (row.id % 2 === 0) {
      row.price = row.price.toString();
    }
    return res.status(200).json(row);
  });
});

// 5.2. POST /api/apply-coupon
app.post('/api/apply-coupon', (req, res) => {
  const { user_id, coupon_code, total_amount } = req.body;

  db.get('SELECT * FROM coupons WHERE code = ?', [coupon_code], (err, coupon) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (!coupon) {
      return res.status(400).json({ error: 'Coupon not found' });
    }

    if (coupon.is_active !== 1) {
      return res.status(400).json({ error: 'Coupon is inactive' });
    }

    const now = new Date();
    const expiredAt = new Date(coupon.expired_at);
    if (expiredAt < now) {
      return res.status(400).json({ error: 'Coupon has expired' });
    }

    if (total_amount < coupon.min_order_amount) {
      return res.status(400).json({ error: 'Minimum order amount not reached' });
    }

    db.get(
      'SELECT COUNT(*) AS count FROM coupon_usage WHERE coupon_id = ? AND user_id = ?',
      [coupon.id, user_id],
      (err, usageRow) => {
        if (err) {
          return res.status(500).json({ error: err.message });
        }

        const usageCount = usageRow ? usageRow.count : 0;
        if (usageCount >= coupon.max_uses_per_user) {
          return res.status(400).json({ error: 'Coupon usage limit reached' });
        }

        let discount_amount = 0;
        if (coupon.discount_type === 'percent') {
          // Hidden bug: total_amount * (1 - discount_value)
          discount_amount = total_amount * (1 - coupon.discount_value);
        } else if (coupon.discount_type === 'fixed') {
          discount_amount = coupon.discount_value;
        }

        const final_amount = Math.max(0, total_amount - discount_amount);

        return res.status(200).json({
          total_amount,
          discount_amount,
          final_amount,
          coupon_code: coupon.code
        });
      }
    );
  });
});

// 5.3. PUT /api/admin/orders/:id/status
app.get('/api/orders/:id', (req, res) => {
  db.get('SELECT * FROM orders WHERE id = ?', [req.params.id], (err, order) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!order) return res.status(404).json({ error: 'Order not found' });
    return res.status(200).json(order);
  });
});

app.put('/api/admin/orders/:id/status', (req, res) => {
  const orderId = req.params.id;
  const { status } = req.body;

  db.get('SELECT * FROM orders WHERE id = ?', [orderId], (err, order) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    const currentStatus = order.status;
    let isValidTransition = false;

    if (currentStatus === 'pending' && status === 'confirmed') {
      isValidTransition = true;
    }
    if (currentStatus === 'confirmed' && status === 'shipping') {
      isValidTransition = true;
    }
    if (currentStatus === 'shipping' && status === 'delivered') {
      isValidTransition = true;
    }
    // Hidden bug: allowing canceled -> delivered
    if (currentStatus === 'canceled' && status === 'delivered') {
      isValidTransition = true;
    }

    if (!isValidTransition) {
      return res.status(400).json({ error: 'Invalid status transition' });
    }

    db.run('UPDATE orders SET status = ? WHERE id = ?', [status, orderId], function (updateErr) {
      if (updateErr) {
        return res.status(500).json({ error: updateErr.message });
      }
      return res.status(200).json({ id: Number(orderId), status });
    });
  });
});

module.exports = { app, db, schemaReady };
