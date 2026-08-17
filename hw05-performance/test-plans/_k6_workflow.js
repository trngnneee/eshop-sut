/**
 * Shared Search-to-buy VU (23127271). Used by Load/Stress/Spike/Soak k6 scripts.
 * Graded numbers: k6 run --out json=../logs/23127271_<Scenario>_20260814.json
 * --http-debug is Tree-equivalent for a SHORT peek only (not the 520s Load).
 */
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

const BASE = 'http://localhost:3000';
const TIMEOUT = '10s';

export const users = new SharedArray('tram-users', function () {
  const text = open('./23127271_users.csv');
  const parsed = papaparse.parse(text, {
    header: true,
    skipEmptyLines: true,
  });
  const rows = parsed.data.filter((r) => r.email && r.email.indexOf('tram') === 0);
  if (rows.length < 1) {
    throw new Error('CSV produced no tramNN rows');
  }
  return rows;
});

function rowForVu() {
  // JMeter CSV shareMode.all: distinct row per concurrent thread.
  // __ITER % n alone → every VU's first loop is tram01 (K04 hunt 5).
  return users[(__VU - 1 + __ITER) % users.length];
}

function think(minS, rangeS) {
  sleep(minS + Math.random() * rangeS);
}

function jsonBody(res) {
  try {
    return res.json();
  } catch (e) {
    return null;
  }
}

/**
 * @param {number} thinkMin seconds
 * @param {number} thinkRange seconds (uniform add-on)
 */
export function searchToBuy(thinkMin, thinkRange) {
  const u = rowForVu();
  const jsonH = { 'Content-Type': 'application/json' };

  const login = http.post(
    `${BASE}/api/login`,
    JSON.stringify({ email: u.email, password: u.password }),
    { headers: jsonH, timeout: TIMEOUT, tags: { name: 'login' } },
  );
  const loginBody = jsonBody(login);
  const loginOk = check(login, {
    'login status 200': (r) => r.status === 200,
    'login has token': () => !!(loginBody && loginBody.token),
  });
  if (!loginOk) {
    if (login.status === 401 || login.status === 403) {
      console.log(`login ${login.status} email=${u.email} body=${login.body}`);
    }
    think(thinkMin, thinkRange);
    return;
  }
  think(thinkMin, thinkRange);

  const token = loginBody.token;
  const bearer = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };

  const search = http.get(
    `${BASE}/api/products?search=${encodeURIComponent(u.search)}`,
    { timeout: TIMEOUT, tags: { name: 'search' } },
  );
  const searchBody = jsonBody(search);
  const searchOk = check(search, {
    'search status 200': (r) => r.status === 200,
    'search $[0].id': () =>
      Array.isArray(searchBody) && searchBody.length > 0 && searchBody[0].id != null,
  });
  if (!searchOk) {
    think(thinkMin, thinkRange);
    return;
  }
  think(thinkMin, thinkRange);

  const detail = http.get(`${BASE}/api/products/${u.product_id}`, {
    timeout: TIMEOUT,
    tags: { name: 'detail' },
  });
  const detailBody = jsonBody(detail);
  const detailOk = check(detail, {
    'detail status 200': (r) => r.status === 200,
    'detail has name': () => !!(detailBody && detailBody.name),
    'detail has id': () => !!(detailBody && detailBody.id != null),
  });
  if (!detailOk) {
    think(thinkMin, thinkRange);
    return;
  }
  think(thinkMin, thinkRange);

  const cart = http.post(
    `${BASE}/api/cart`,
    JSON.stringify({
      product_id: Number(u.product_id),
      quantity: Number(u.quantity),
      name: detailBody.name,
      price: Number(u.price),
    }),
    { headers: bearer, timeout: TIMEOUT, tags: { name: 'cart' } },
  );
  const cartBody = jsonBody(cart);
  const cartOk = check(cart, {
    'cart status 200': (r) => r.status === 200,
    'cart Added to cart': () => cartBody && cartBody.message === 'Added to cart',
  });
  if (!cartOk) {
    think(thinkMin, thinkRange);
    return;
  }
  think(thinkMin, thinkRange);

  const checkout = http.post(
    `${BASE}/api/checkout`,
    JSON.stringify({
      total_amount: Number(u.total_amount),
      shipping_address: u.shipping_address,
    }),
    { headers: bearer, timeout: TIMEOUT, tags: { name: 'checkout' } },
  );
  const checkoutBody = jsonBody(checkout);
  check(checkout, {
    'checkout status 200': (r) => r.status === 200,
    'checkout has orderId': () => !!(checkoutBody && checkoutBody.orderId != null),
  });
  think(thinkMin, thinkRange);
}
