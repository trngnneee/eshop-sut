import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { SharedArray } from 'k6/data';

// Load CSV data using SharedArray
const usersData = new SharedArray('users', function () {
  const file = open('../data/khoa_users.csv');
  const lines = file.split('\n').filter(line => line.trim() !== '');
  const header = lines[0].split(',');
  const rows = [];
  
  for (let i = 1; i < lines.length; i++) {
    // Basic CSV line parser with quotes support
    const regex = /(?:^|,)(?:"([^"]*)"|([^,]*))/g;
    let match;
    const values = [];
    while ((match = regex.exec(lines[i])) !== null) {
      if (match.index === regex.lastIndex) regex.lastIndex++;
      values.push(match[1] !== undefined ? match[1] : match[2]);
    }
    if (values.length >= 7) {
      rows.push({
        email: values[0],
        password: values[1],
        product_id: values[2],
        quantity: parseInt(values[3], 10) || 1,
        price: parseInt(values[4], 10) || 100000,
        total_amount: parseInt(values[5], 10) || 100000,
        shipping_address: values[6]
      });
    }
  }
  return rows;
});

export const options = {
  stages: [
    { duration: '60s', target: 50 },
    { duration: '300s', target: 50 },
    { duration: '30s', target: 0 }
  ],
  thresholds: {
    'http_req_duration{scenario:default}': ['p(95)<800'],
    'http_req_failed': ['rate<0.001']
  }
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

function randomBetween(min, max) {
  return min + Math.random() * (max - min);
}

export default function () {
  const user = usersData[__VU % usersData.length];
  let token = '';
  let selectedPid = user.product_id;

  // [1/5] Login
  group('01_Login', function () {
    const loginPayload = JSON.stringify({
      email: user.email,
      password: user.password
    });
    const res = http.post(`${BASE_URL}/api/login`, loginPayload, {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: '01_Login' }
    });
    check(res, {
      'login status 200': (r) => r.status === 200,
      'token exists': (r) => {
        try {
          const body = JSON.parse(r.body);
          if (body.token) {
            token = body.token;
            return true;
          }
        } catch (e) {}
        return false;
      }
    });
  });
  sleep(randomBetween(1.0, 2.0));

  // [2/5] Browse Products
  group('02_BrowseProducts', function () {
    const res = http.get(`${BASE_URL}/api/products`, {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: '02_BrowseProducts' }
    });
    check(res, {
      'browse status 200': (r) => r.status === 200,
      'is array': (r) => {
        try {
          const body = JSON.parse(r.body);
          if (Array.isArray(body) && body.length > 0) {
            const randItem = body[Math.floor(Math.random() * body.length)];
            if (randItem && randItem.id) selectedPid = randItem.id;
            return true;
          }
        } catch (e) {}
        return false;
      }
    });
  });
  sleep(randomBetween(2.0, 4.0));

  // [3/5] Product Detail
  group('03_ProductDetail', function () {
    const res = http.get(`${BASE_URL}/api/products/${selectedPid}`, {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: '03_ProductDetail' }
    });
    check(res, {
      'detail status 200': (r) => r.status === 200,
      'has name and price': (r) => {
        try {
          const body = JSON.parse(r.body);
          return body.name !== undefined && body.price !== undefined;
        } catch (e) {}
        return false;
      }
    });
  });
  sleep(randomBetween(1.0, 2.0));

  // [4/5] Add to Cart
  group('04_AddToCart', function () {
    const cartPayload = JSON.stringify({
      product_id: selectedPid,
      quantity: user.quantity,
      name: `PERF item ${selectedPid}`,
      price: user.price
    });
    const res = http.post(`${BASE_URL}/api/cart`, cartPayload, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      tags: { name: '04_AddToCart' }
    });
    check(res, {
      'cart status 200': (r) => r.status === 200,
      'added message': (r) => r.body && r.body.includes('Added to cart')
    });
  });
  sleep(randomBetween(1.0, 1.5));

  // [5/5] Checkout
  group('05_Checkout', function () {
    const checkoutPayload = JSON.stringify({
      total_amount: user.total_amount,
      shipping_address: user.shipping_address
    });
    const res = http.post(`${BASE_URL}/api/checkout`, checkoutPayload, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      tags: { name: '05_Checkout' }
    });
    check(res, {
      'checkout status 200': (r) => r.status === 200,
      'orderId exists': (r) => {
        try {
          const body = JSON.parse(r.body);
          return body.orderId !== undefined;
        } catch (e) {}
        return false;
      }
    });
  });
}

export function handleSummary(data) {
  return {
    'performance-testing/results/k6/summary.json': JSON.stringify(data, null, 2),
    stdout: `\n=== k6 Load Test Summary ===\nTotal Requests: ${data.metrics.http_reqs ? data.metrics.http_reqs.values.count : 0}\n`
  };
}
