#!/usr/bin/env node
/**
 * P02 helper — generate 23127271_users.csv and optionally POST /api/register.
 *
 * BEFORE ANY JMETER RUN: register once per seed (SUT must be up):
 *   node generate-tram-users.js --register
 * Fresh seed only has admin@ / test@ — tram01–tram100 will 401 until this runs.
 *
 * Usage:
 *   node generate-tram-users.js              # write CSV only
 *   node generate-tram-users.js --register   # write CSV + register (SUT must be up)
 *
 * Seed product names (database.js), NOT category "Laptop":
 *   iPhone, Samsung, MacBook, AirPods, Keychron
 */
const fs = require("fs");
const path = require("path");

const BASE = process.env.ESHOP_BASE || "http://localhost:3000";
const COUNT = 100;
const PASSWORD = "Test1234!";
const OUT = path.join(__dirname, "23127271_users.csv");

// Fresh seed AUTOINCREMENT ids 1–5. Re-verify after re-seed:
//   SELECT id, name, price FROM products;
const PRODUCTS = [
  { search: "iPhone", product_id: 1, price: 30000000 },
  { search: "Samsung", product_id: 2, price: 28000000 },
  { search: "MacBook", product_id: 3, price: 45000000 },
  { search: "AirPods", product_id: 4, price: 6000000 },
  { search: "Keychron", product_id: 5, price: 4000000 },
];

const ADDRESSES = [
  "123 Nguyen Hue, Q1",
  "45 Le Loi, Q3",
  "12 Tran Hung Dao, Q5",
  "88 Hai Ba Trung, Q1",
  "7 Nguyen Trai, Q5",
];

function pad(n) {
  return String(n).padStart(2, "0");
}

function csvEscape(value) {
  const s = String(value);
  if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
}

function rows() {
  const header =
    "email,password,search,product_id,quantity,price,total_amount,shipping_address";
  const lines = [header];
  const data = [];
  for (let i = 1; i <= COUNT; i++) {
    const p = PRODUCTS[(i - 1) % PRODUCTS.length];
    const quantity = 1;
    const row = {
      email: `tram${pad(i)}@eshop.com`,
      password: PASSWORD,
      search: p.search,
      product_id: p.product_id,
      quantity,
      price: p.price,
      total_amount: p.price * quantity,
      shipping_address: ADDRESSES[(i - 1) % ADDRESSES.length],
    };
    data.push(row);
    lines.push(
      [
        row.email,
        row.password,
        row.search,
        row.product_id,
        row.quantity,
        row.price,
        row.total_amount,
        csvEscape(row.shipping_address),
      ].join(","),
    );
  }
  return { text: lines.join("\n") + "\n", data };
}

async function registerAll(data) {
  let ok = 0;
  let skip = 0;
  let fail = 0;
  for (const row of data) {
    const login = await fetch(`${BASE}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: row.email, password: row.password }),
    });
    if (login.ok) {
      skip++;
      console.log(`SKIP ${row.email}  already registered`);
      continue;
    }
    const name = row.email.split("@")[0];
    const res = await fetch(`${BASE}/api/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email: row.email, password: row.password }),
    });
    const body = await res.text();
    if (res.ok) {
      ok++;
      console.log(`OK  ${row.email}  ${body}`);
    } else {
      fail++;
      console.error(`FAIL ${row.email}  HTTP ${res.status}  ${body}`);
    }
  }
  console.log(`Registered OK=${ok} SKIP=${skip} FAIL=${fail} (email is NOT UNIQUE — skip existing logins, do not duplicate).`);
}

async function main() {
  const { text, data } = rows();
  fs.writeFileSync(OUT, text, "utf8");
  console.log(`Wrote ${COUNT} rows → ${OUT}`);

  if (process.argv.includes("--register")) {
    await registerAll(data);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
