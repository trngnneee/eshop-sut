# EShop Artillery Performance Tests

Artillery scripts implementing the EShop workload model (browse / view / cart / checkout).

## Prerequisites

1. Backend running at `http://localhost:3000`
2. Seeded test user: `test@eshop.com` / `Test1234!`
3. Node.js 18+ (Artillery 2.x prefers Node 22+)

```bash
cd Repo/eshop-sut/backend
npm start
```

## Install

```bash
cd Repo/eshop-sut/performance-tests/Artillery
npm install
```

## Workload distribution

| Scenario                 | Weight | Main APIs                                      |
| ------------------------ | ------ | ---------------------------------------------- |
| Browse/Search Products   | 60%    | `GET /api/products`, `/categories`, `?search=` |
| View Product Details     | 25%    | `GET /api/products`, `GET /api/products/:id`   |
| Add to Cart              | 10%    | login → products → `POST/GET /api/cart`        |
| Checkout Flow            | 5%     | login → cart → `POST /api/checkout`            |

## Test profiles

### A. Baseline (load test)

- **File:** `baseline.yml`
- **VUs:** 50 concurrent (`maxVusers: 50`)
- **Phases:** ramp-up 1m → steady 3m → ramp-down 1m

```bash
npm run test:baseline
# run + export HTML report (~5 min):
npm run test:baseline:report
# or regenerate HTML from an existing JSON:
npm run report:baseline
```

Open `reports/baseline-report.html` in a browser for screenshots.

### B. Spike test

- **File:** `spike.yml`
- **VUs:** 50 → 500
- **Phases:** pre-spike 30s @ 50 → ramp 30s → peak 1m @ 500 → ramp-down 30s

```bash
npm run test:spike
npm run test:spike:report
# or: npm run report:spike
```

## Metrics to record

After each run, capture from the Artillery summary:

- Response time: mean, p50, p95, p99
- Throughput (req/s)
- Error rate (HTTP 4xx/5xx, timeouts)
- Stability notes (crashes, DB locks) during spike

## Files

| File                  | Role                                      |
| --------------------- | ----------------------------------------- |
| `baseline.yml`        | Baseline load profile + scenarios         |
| `spike.yml`           | Spike profile + same scenario mix         |
| `helpers.js`          | Random product/keyword + checkout payload |
| `generate-report.js`  | Build HTML report from Artillery JSON     |
| `package.json`        | Local Artillery dependency + npm scripts  |
| `reports/*.html`      | Exported HTML reports (after a run)       |
