import http from "k6/http";
import { check, group, sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://localhost:3000";
const USER_EMAIL = __ENV.ESHOP_USER_EMAIL || "test@eshop.com";
const USER_PASSWORD = __ENV.ESHOP_USER_PASSWORD || "Test1234!";
const PROFILE = __ENV.K6_PROFILE || "custom";

const browseDuration = new Trend("browse_search_response_time", true);
const detailDuration = new Trend("product_detail_response_time", true);
const cartDuration = new Trend("add_to_cart_response_time", true);
const checkoutDuration = new Trend("checkout_response_time", true);
const browseActions = new Counter("browse_search_actions");
const detailActions = new Counter("view_detail_actions");
const cartActions = new Counter("add_to_cart_actions");
const checkoutActions = new Counter("checkout_actions");
const apiErrors = new Counter("api_errors");
const businessSuccessRate = new Rate("business_success_rate");

export const options = {
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
  stages: buildStages(),
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<1000"],
    checks: ["rate>0.95"],
    business_success_rate: ["rate>0.95"],
  },
};

export function setup() {
  const productsRes = http.get(`${BASE_URL}/api/products`, {
    tags: { endpoint: "setup_products" },
  });
  const products = productsRes.status === 200 ? productsRes.json() : [];

  const loginRes = http.post(
    `${BASE_URL}/api/login`,
    JSON.stringify({
      email: USER_EMAIL,
      password: USER_PASSWORD,
    }),
    {
      headers: { "Content-Type": "application/json" },
      tags: { endpoint: "login_setup" },
    },
  );

  const loginOk = check(loginRes, {
    "setup login returns 200": (res) => res.status === 200,
    "setup login returns token": (res) => Boolean(res.json("token")),
  });

  if (!loginOk) {
    apiErrors.add(1);
    return { token: "", userId: 1 };
  }

  return {
    token: loginRes.json("token"),
    userId: loginRes.json("user.id") || 1,
    products: Array.isArray(products) ? products : [],
  };
}

export default function (data) {
  const headers = { "Content-Type": "application/json" };
  const authHeaders = {
    ...headers,
    Authorization: `Bearer ${data.token}`,
  };
  const product = pickProduct(data.products);
  const action = pickWeightedAction();

  if (action === "browse") {
    browseActions.add(1);
    group("browse/search products - 60%", () => {
      const searchTerm = pickOne(["", "iPhone", "Samsung", "MacBook", "AirPods"]);
      const url = searchTerm
        ? `${BASE_URL}/api/products?search=${encodeURIComponent(searchTerm)}`
        : `${BASE_URL}/api/products`;

      const res = http.get(url, {
        tags: { endpoint: searchTerm ? "product_search" : "products" },
      });
      browseDuration.add(res.timings.duration);
      recordCheck(
        check(res, {
          "browse/search returns 200": (response) => response.status === 200,
          "browse/search returns product array": (response) => Array.isArray(response.json()),
        }),
      );
    });
  } else if (action === "detail") {
    detailActions.add(1);
    group("view product detail - 25%", () => {
      const res = http.get(`${BASE_URL}/api/products/${product.id}`, {
        tags: { endpoint: "product_detail" },
      });
      detailDuration.add(res.timings.duration);
      recordCheck(
        check(res, {
          "product detail returns 200": (response) => response.status === 200,
          "product detail has id": (response) => response.json("id") === product.id,
        }),
      );
    });
  } else if (action === "cart") {
    cartActions.add(1);
    group("add to cart - 10%", () => {
      const res = http.post(
        `${BASE_URL}/api/cart`,
        JSON.stringify({
          id: product.id,
          name: product.name,
          price: product.price,
          quantity: 1,
        }),
        { headers: authHeaders, tags: { endpoint: "add_to_cart" } },
      );
      cartDuration.add(res.timings.duration);
      recordCheck(
        check(res, {
          "POST /api/cart returns 200": (response) => response.status === 200,
          "POST /api/cart confirms add": (response) => response.json("message") === "Added to cart",
        }),
      );
    });
  } else {
    checkoutActions.add(1);
    group("checkout flow - 5%", () => {
      const res = http.post(
        `${BASE_URL}/api/checkout`,
        JSON.stringify({
          total_amount: product.price,
          shipping_address: "123 Le Loi, Quan 1, TP.HCM",
        }),
        { headers: authHeaders, tags: { endpoint: "checkout" } },
      );
      checkoutDuration.add(res.timings.duration);
      recordCheck(
        check(res, {
          "POST /api/checkout returns 200": (response) => response.status === 200,
          "POST /api/checkout returns order id": (response) => response.json("orderId") !== undefined,
        }),
      );
    });
  }

  sleep(Number(__ENV.K6_THINK_TIME || 1));
}

function buildStages() {
  if (PROFILE === "baseline") {
    const vus = Number(__ENV.K6_BASELINE_VUS || 50);
    return [
      { duration: __ENV.K6_BASELINE_RAMP_UP || "1m", target: vus },
      { duration: __ENV.K6_BASELINE_STEADY || "3m", target: vus },
      { duration: __ENV.K6_BASELINE_RAMP_DOWN || "1m", target: 0 },
    ];
  }

  if (PROFILE === "spike") {
    const startVus = Number(__ENV.K6_SPIKE_START_VUS || 50);
    const peakVus = Number(__ENV.K6_SPIKE_PEAK_VUS || 500);
    return [
      { duration: __ENV.K6_SPIKE_PREP || "1s", target: startVus },
      { duration: __ENV.K6_SPIKE_RAMP_UP || "30s", target: peakVus },
      { duration: __ENV.K6_SPIKE_STEADY || "1m", target: peakVus },
      { duration: __ENV.K6_SPIKE_RAMP_DOWN || "30s", target: 0 },
    ];
  }

  const targetVus = Number(__ENV.K6_VUS || 10);
  return [
    { duration: __ENV.K6_RAMP_UP || "15s", target: targetVus },
    { duration: __ENV.K6_STEADY || "45s", target: targetVus },
    { duration: __ENV.K6_RAMP_DOWN || "15s", target: 0 },
  ];
}

function pickWeightedAction() {
  const value = Math.random();
  if (value < 0.6) return "browse";
  if (value < 0.85) return "detail";
  if (value < 0.95) return "cart";
  return "checkout";
}

function pickProduct(products) {
  if (products && products.length > 0) {
    return pickOne(products);
  }

  return {
    id: 1,
    name: "iPhone 15 Pro Max",
    price: 30000000,
  };
}

function pickOne(values) {
  return values[Math.floor(Math.random() * values.length)];
}

function recordCheck(ok) {
  businessSuccessRate.add(ok);
  if (!ok) {
    apiErrors.add(1);
  }
}

export function handleSummary(data) {
  const summaryBase = `reports/k6-${PROFILE}-summary`;
  return {
    [`${summaryBase}.json`]: JSON.stringify(data, null, 2),
    [`${summaryBase}.html`]: htmlReport(data),
    "reports/k6-summary.json": JSON.stringify(data, null, 2),
    "reports/k6-summary.html": htmlReport(data),
    stdout: textSummary(data),
  };
}

function textSummary(data) {
  const duration = data.metrics.http_req_duration;
  const failed = data.metrics.http_req_failed;
  const requests = data.metrics.http_reqs;
  const checksMetric = data.metrics.checks;
  const iterations = data.metrics.iterations;

  return [
    "",
    "EShop k6 performance summary",
    `- Profile: ${PROFILE}`,
    `- Total requests: ${requests.values.count}`,
    `- Completed iterations: ${iterations.values.count}`,
    `- Throughput: ${requests.values.rate.toFixed(2)} req/s`,
    `- Response time avg: ${formatMs(duration.values.avg)}`,
    `- Response time p95: ${formatMs(duration.values["p(95)"])}`,
    `- Response time p99: ${formatMs(duration.values["p(99)"])}`,
    `- Error rate: ${formatPercent(failed.values.rate)}`,
    `- Check pass rate: ${formatPercent(checksMetric.values.rate)}`,
    `- Browse/Search actions: ${metricCount(data, "browse_search_actions")}`,
    `- View Detail actions: ${metricCount(data, "view_detail_actions")}`,
    `- Add to Cart actions: ${metricCount(data, "add_to_cart_actions")}`,
    `- Checkout actions: ${metricCount(data, "checkout_actions")}`,
    "",
  ].join("\n");
}

function htmlReport(data) {
  const duration = data.metrics.http_req_duration.values;
  const failed = data.metrics.http_req_failed.values;
  const requests = data.metrics.http_reqs.values;
  const checksMetric = data.metrics.checks.values;
  const iterations = data.metrics.iterations.values;

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>EShop k6 Performance Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 32px; color: #1f2937; }
    table { border-collapse: collapse; width: 100%; max-width: 840px; }
    th, td { border: 1px solid #d1d5db; padding: 10px 12px; text-align: left; }
    th { background: #f3f4f6; }
  </style>
</head>
<body>
  <h1>EShop k6 Performance Report</h1>
  <table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>Profile</td><td>${PROFILE}</td></tr>
    <tr><td>Total requests</td><td>${requests.count}</td></tr>
    <tr><td>Completed iterations</td><td>${iterations.count}</td></tr>
    <tr><td>Throughput</td><td>${formatRate(requests.rate)}</td></tr>
    <tr><td>Average response time</td><td>${formatMs(duration.avg)}</td></tr>
    <tr><td>Median response time</td><td>${formatMs(duration.med)}</td></tr>
    <tr><td>p95 latency</td><td>${formatMs(duration["p(95)"])}</td></tr>
    <tr><td>p99 latency</td><td>${formatMs(duration["p(99)"])}</td></tr>
    <tr><td>Error rate</td><td>${formatPercent(failed.rate)}</td></tr>
    <tr><td>Check pass rate</td><td>${formatPercent(checksMetric.rate)}</td></tr>
  </table>
  <h2>Workload Action Distribution</h2>
  <table>
    <tr><th>Action</th><th>Target Mix</th><th>Observed Count</th></tr>
    <tr><td>Browse/Search Products</td><td>60%</td><td>${metricCount(data, "browse_search_actions")}</td></tr>
    <tr><td>View Product Details</td><td>25%</td><td>${metricCount(data, "view_detail_actions")}</td></tr>
    <tr><td>Add to Cart</td><td>10%</td><td>${metricCount(data, "add_to_cart_actions")}</td></tr>
    <tr><td>Checkout Flow</td><td>5%</td><td>${metricCount(data, "checkout_actions")}</td></tr>
  </table>
</body>
</html>`;
}

function formatMs(value) {
  return value === undefined ? "n/a" : `${value.toFixed(2)} ms`;
}

function formatRate(value) {
  return value === undefined ? "n/a" : `${value.toFixed(2)} req/s`;
}

function formatPercent(value) {
  return value === undefined ? "n/a" : `${(value * 100).toFixed(2)}%`;
}

function metricCount(data, metricName) {
  return data.metrics[metricName]?.values?.count || 0;
}
