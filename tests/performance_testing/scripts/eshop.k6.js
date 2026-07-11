import http from "k6/http";
import { check, group, sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://localhost:3000";
const USER_EMAIL = __ENV.ESHOP_USER_EMAIL || "test@eshop.com";
const USER_PASSWORD = __ENV.ESHOP_USER_PASSWORD || "Test1234!";
const TARGET_VUS = Number(__ENV.K6_VUS || 10);

const productDuration = new Trend("product_response_time", true);
const loginDuration = new Trend("login_response_time", true);
const couponDuration = new Trend("coupon_response_time", true);
const apiErrors = new Counter("api_errors");
const businessSuccessRate = new Rate("business_success_rate");

export const options = {
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
  stages: [
    { duration: __ENV.K6_RAMP_UP || "15s", target: TARGET_VUS },
    { duration: __ENV.K6_STEADY || "45s", target: TARGET_VUS },
    { duration: __ENV.K6_RAMP_DOWN || "15s", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<1000"],
    checks: ["rate>0.95"],
    business_success_rate: ["rate>0.95"],
  },
};

export function setup() {
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
  };
}

export default function (data) {
  const headers = { "Content-Type": "application/json" };
  const authHeaders = {
    ...headers,
    Authorization: `Bearer ${data.token}`,
  };

  group("public product browsing", () => {
    const productsRes = http.get(`${BASE_URL}/api/products`, {
      tags: { endpoint: "products" },
    });
    productDuration.add(productsRes.timings.duration);
    recordCheck(
      check(productsRes, {
        "GET /api/products is 200": (res) => res.status === 200,
        "GET /api/products returns an array": (res) => Array.isArray(res.json()),
      }),
    );

    const searchRes = http.get(`${BASE_URL}/api/products?search=iPhone`, {
      tags: { endpoint: "product_search" },
    });
    productDuration.add(searchRes.timings.duration);
    recordCheck(
      check(searchRes, {
        "GET /api/products?search is 200": (res) => res.status === 200,
      }),
    );

    const detailRes = http.get(`${BASE_URL}/api/products/1`, {
      tags: { endpoint: "product_detail" },
    });
    productDuration.add(detailRes.timings.duration);
    recordCheck(
      check(detailRes, {
        "GET /api/products/1 is 200": (res) => res.status === 200,
        "GET /api/products/1 has id": (res) => res.json("id") === 1,
      }),
    );
  });

  group("authenticated user flow", () => {
    const loginRes = http.post(
      `${BASE_URL}/api/login`,
      JSON.stringify({
        email: USER_EMAIL,
        password: USER_PASSWORD,
      }),
      { headers, tags: { endpoint: "login" } },
    );
    loginDuration.add(loginRes.timings.duration);
    recordCheck(
      check(loginRes, {
        "POST /api/login is 200": (res) => res.status === 200,
        "POST /api/login returns token": (res) => Boolean(res.json("token")),
      }),
    );

    const token = loginRes.json("token") || data.token;
    const profileRes = http.get(`${BASE_URL}/api/users/me`, {
      headers: { ...headers, Authorization: `Bearer ${token}` },
      tags: { endpoint: "profile" },
    });
    recordCheck(
      check(profileRes, {
        "GET /api/users/me is 200": (res) => res.status === 200,
        "GET /api/users/me returns user email": (res) => res.json("email") === USER_EMAIL,
      }),
    );
  });

  group("coupon calculation", () => {
    const couponRes = http.post(
      `${BASE_URL}/api/apply-coupon`,
      JSON.stringify({
        code: "SAVE10",
        total_amount: 500000,
        user_id: data.userId || 1,
      }),
      { headers: authHeaders, tags: { endpoint: "apply_coupon" } },
    );
    couponDuration.add(couponRes.timings.duration);
    recordCheck(
      check(couponRes, {
        "POST /api/apply-coupon returns success": (res) => res.status === 200,
        "POST /api/apply-coupon has final_amount": (res) => res.json("final_amount") !== undefined,
      }),
    );
  });

  sleep(1);
}

function recordCheck(ok) {
  businessSuccessRate.add(ok);
  if (!ok) {
    apiErrors.add(1);
  }
}

export function handleSummary(data) {
  return {
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

  return [
    "",
    "EShop k6 performance summary",
    `- Total requests: ${requests.values.count}`,
    `- Throughput: ${requests.values.rate.toFixed(2)} req/s`,
    `- Response time avg: ${formatMs(duration.values.avg)}`,
    `- Response time p95: ${formatMs(duration.values["p(95)"])}`,
    `- Response time p99: ${formatMs(duration.values["p(99)"])}`,
    `- Error rate: ${formatPercent(failed.values.rate)}`,
    `- Check pass rate: ${formatPercent(checksMetric.values.rate)}`,
    "",
  ].join("\n");
}

function htmlReport(data) {
  const duration = data.metrics.http_req_duration.values;
  const failed = data.metrics.http_req_failed.values;
  const requests = data.metrics.http_reqs.values;
  const checksMetric = data.metrics.checks.values;

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
    <tr><td>Total requests</td><td>${requests.count}</td></tr>
    <tr><td>Throughput</td><td>${formatRate(requests.rate)}</td></tr>
    <tr><td>Average response time</td><td>${formatMs(duration.avg)}</td></tr>
    <tr><td>Median response time</td><td>${formatMs(duration.med)}</td></tr>
    <tr><td>p95 latency</td><td>${formatMs(duration["p(95)"])}</td></tr>
    <tr><td>p99 latency</td><td>${formatMs(duration["p(99)"])}</td></tr>
    <tr><td>Error rate</td><td>${formatPercent(failed.rate)}</td></tr>
    <tr><td>Check pass rate</td><td>${formatPercent(checksMetric.rate)}</td></tr>
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
