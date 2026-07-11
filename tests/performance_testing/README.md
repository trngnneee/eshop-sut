# Performance Testing - EShop

## Scope

Student: `23127438 - Đặng Trường Nguyên`

This folder contains reusable `k6` performance test scripts for the EShop backend API.

Target system:

- Backend base URL: `http://localhost:3000`
- Default user: `test@eshop.com` / `Test1234!`
- Main workload: browse/search, view product detail, add to cart, and checkout

## 1. Install Tools

`k6` is installed globally on the machine.

Check the installed version:

```bash
k6 version
```

## 2. Workload Model

Each iteration chooses one user action using this weighted distribution:

| User action | Target mix | Endpoint behavior |
| --- | ---: | --- |
| Browse/Search Products | 60% | `GET /api/products` or `GET /api/products?search=...` |
| View Product Details | 25% | `GET /api/products/:id` |
| Add to Cart | 10% | `POST /api/cart` with JWT |
| Checkout Flow | 5% | `POST /api/checkout` with JWT |

The script records action counters in the k6 summary:

- `browse_search_actions`
- `view_detail_actions`
- `add_to_cart_actions`
- `checkout_actions`

## 3. Start Backend

From the repository root:

```bash
cd backend
npm start
```

The backend resets and seeds `database.sqlite` every time `server.js` starts.

## 4. Run k6

From `tests/performance_testing`:

```bash
npm run k6:smoke
npm run k6:baseline
npm run k6:spike
```

`npm run k6:load` is an alias for the baseline profile.

### Baseline Profile

```bash
npm run k6:baseline
```

- Target VUs: 50
- Ramp-up: 1 minute
- Steady state: 3 minutes
- Ramp-down: 1 minute

### Spike Profile

```bash
npm run k6:spike
```

- Starts at 50 VUs
- Spikes to 500 VUs in 30 seconds
- Holds 500 VUs for 1 minute
- Ramps down in 30 seconds

Optional custom smoke/load overrides:

```bash
BASE_URL=http://localhost:3000 K6_VUS=20 K6_STEADY=1m npm run k6:smoke
```

k6 writes summary files to:

- `reports/k6-summary.json`
- `reports/k6-summary.html`

## 5. Analyze

Use `report/performance-report.md` to record:

- Response time: average, median, p95, p99
- Throughput: requests per second
- Latency: p95/p99 request duration under load
- Error rate: failed HTTP requests / total HTTP requests
- Observed workload action distribution
