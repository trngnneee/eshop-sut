'use strict';

/**
 * Generate a standalone HTML report from an Artillery JSON output file.
 * Usage: node generate-report.js <input.json> <output.html> [title]
 */

const fs = require('fs');
const path = require('path');

const inputPath = process.argv[2] || 'reports/baseline-report.json';
const outputPath = process.argv[3] || 'reports/baseline-report.html';
const title = process.argv[4] || 'EShop Artillery — Baseline Load Test';

const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const agg = data.aggregate || {};
const counters = agg.counters || {};
const summaries = agg.summaries || {};
const rates = agg.rates || {};
const intermediate = data.intermediate || [];

function num(v, digits = 1) {
  if (v == null || Number.isNaN(Number(v))) return '—';
  return Number(v).toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: 0,
  });
}

const rt = summaries['http.response_time'] || {};
const requests = counters['http.requests'] || 0;
const ok200 = counters['http.codes.200'] || 0;
const failed = counters['vusers.failed'] || 0;
const created = counters['vusers.created'] || 0;
const completed = counters['vusers.completed'] || 0;
const skipped = counters['vusers.skipped'] || 0;
const errorRate =
  requests > 0 ? (((requests - ok200) / requests) * 100).toFixed(2) : '0.00';

const scenarios = [
  {
    name: 'Browse/Search Products',
    count: counters['vusers.created_by_name.Browse/Search Products'] || 0,
    target: 60,
  },
  {
    name: 'View Product Details',
    count: counters['vusers.created_by_name.View Product Details'] || 0,
    target: 25,
  },
  {
    name: 'Add to Cart',
    count: counters['vusers.created_by_name.Add to Cart'] || 0,
    target: 10,
  },
  {
    name: 'Checkout Flow',
    count: counters['vusers.created_by_name.Checkout Flow'] || 0,
    target: 5,
  },
].map((s) => ({
  ...s,
  pct: created > 0 ? ((s.count / created) * 100).toFixed(1) : '0.0',
}));

const timeline = intermediate
  .filter((p) => p.summaries && p.summaries['http.response_time'])
  .map((p, i) => {
    const s = p.summaries['http.response_time'];
    const r = (p.rates && p.rates['http.request_rate']) || p['http.request_rate'] || 0;
    return {
      i: i + 1,
      period: p.period,
      rps: Number(r) || 0,
      mean: s.mean ?? 0,
      p95: s.p95 ?? 0,
      p99: s.p99 ?? 0,
      requests: (p.counters && p.counters['http.requests']) || 0,
    };
  });

const endpointRows = Object.keys(summaries)
  .filter((k) => k.startsWith('plugins.metrics-by-endpoint.response_time.'))
  .map((k) => {
    const label = k.replace('plugins.metrics-by-endpoint.response_time.', '');
    const s = summaries[k];
    return {
      label,
      mean: s.mean,
      median: s.median,
      p95: s.p95,
      p99: s.p99,
      max: s.max,
    };
  })
  .sort((a, b) => (b.p95 || 0) - (a.p95 || 0));

const generatedAt = new Date().toLocaleString('en-GB', { timeZone: 'Asia/Ho_Chi_Minh' });
const durationMs =
  agg.lastMetricAt && agg.firstMetricAt
    ? agg.lastMetricAt - agg.firstMetricAt
    : null;
const durationMin = durationMs != null ? (durationMs / 60000).toFixed(1) : '—';

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${title}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg: #0f1419;
      --panel: #1a222c;
      --border: #2a3544;
      --text: #e7eef7;
      --muted: #8b9bb0;
      --accent: #3d9cf0;
      --good: #3ecf8e;
      --warn: #f0b429;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
    }
    header {
      padding: 28px 32px 20px;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, #16202b, var(--bg));
    }
    header h1 { margin: 0 0 6px; font-size: 1.55rem; font-weight: 650; }
    header p { margin: 0; color: var(--muted); font-size: 0.92rem; }
    main { padding: 24px 32px 48px; max-width: 1200px; margin: 0 auto; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }
    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px 18px;
    }
    .card .label { color: var(--muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; }
    .card .value { font-size: 1.55rem; font-weight: 700; margin-top: 4px; }
    .card .unit { color: var(--muted); font-size: 0.85rem; font-weight: 500; }
    .good { color: var(--good); }
    h2 { font-size: 1.1rem; margin: 28px 0 12px; }
    table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); }
    th { color: var(--muted); font-weight: 600; font-size: 0.78rem; text-transform: uppercase; }
    .charts { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    @media (max-width: 860px) { .charts { grid-template-columns: 1fr; } }
    .chart-wrap { height: 280px; }
    footer { margin-top: 28px; color: var(--muted); font-size: 0.82rem; }
    code { background: #243040; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }
  </style>
</head>
<body>
  <header>
    <h1>${title}</h1>
    <p>Generated ${generatedAt} · Source <code>${path.basename(inputPath)}</code> · Duration ~${durationMin} min</p>
  </header>
  <main>
    <section class="grid">
      <div class="card"><div class="label">Requests</div><div class="value">${num(requests, 0)}</div></div>
      <div class="card"><div class="label">HTTP 200</div><div class="value good">${num(ok200, 0)}</div></div>
      <div class="card"><div class="label">Error rate</div><div class="value good">${errorRate}<span class="unit"> %</span></div></div>
      <div class="card"><div class="label">Avg RPS (full run)</div><div class="value">${num(rates['http.request_rate'] || 0, 0)}<span class="unit"> /s</span></div></div>
      <div class="card"><div class="label">Mean latency</div><div class="value">${num(rt.mean)}<span class="unit"> ms</span></div></div>
      <div class="card"><div class="label">p50</div><div class="value">${num(rt.median)}<span class="unit"> ms</span></div></div>
      <div class="card"><div class="label">p95</div><div class="value">${num(rt.p95)}<span class="unit"> ms</span></div></div>
      <div class="card"><div class="label">p99</div><div class="value">${num(rt.p99)}<span class="unit"> ms</span></div></div>
      <div class="card"><div class="label">Max latency</div><div class="value">${num(rt.max)}<span class="unit"> ms</span></div></div>
      <div class="card"><div class="label">VUs completed</div><div class="value">${num(completed, 0)}</div></div>
      <div class="card"><div class="label">VUs failed</div><div class="value good">${num(failed, 0)}</div></div>
      <div class="card"><div class="label">VUs skipped</div><div class="value">${num(skipped, 0)}</div></div>
    </section>

    <h2>Latency &amp; throughput over time</h2>
    <div class="charts">
      <div class="card chart-wrap"><canvas id="latencyChart"></canvas></div>
      <div class="card chart-wrap"><canvas id="rpsChart"></canvas></div>
    </div>

    <h2>Workload mix</h2>
    <div class="card" style="padding:0; overflow:auto;">
      <table>
        <thead>
          <tr><th>Scenario</th><th>Sessions</th><th>Actual %</th><th>Target %</th></tr>
        </thead>
        <tbody>
          ${scenarios
            .map(
              (s) =>
                `<tr><td>${s.name}</td><td>${num(s.count, 0)}</td><td>${s.pct}%</td><td>${s.target}%</td></tr>`
            )
            .join('')}
        </tbody>
      </table>
    </div>

    <h2>Latency by endpoint</h2>
    <div class="card" style="padding:0; overflow:auto;">
      <table>
        <thead>
          <tr><th>Endpoint</th><th>Mean</th><th>Median</th><th>p95</th><th>p99</th><th>Max</th></tr>
        </thead>
        <tbody>
          ${endpointRows
            .map(
              (e) =>
                `<tr><td>${e.label}</td><td>${num(e.mean)} ms</td><td>${num(e.median)} ms</td><td>${num(e.p95)} ms</td><td>${num(e.p99)} ms</td><td>${num(e.max)} ms</td></tr>`
            )
            .join('')}
        </tbody>
      </table>
    </div>

    <footer>
      Profile: 50 concurrent VUs · ramp-up 1m · steady 3m · ramp-down 1m · Target http://localhost:3000
    </footer>
  </main>
  <script>
    const timeline = ${JSON.stringify(timeline)};
    const labels = timeline.map((t) => t.i);
    const common = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#c5d0dc' } } },
      scales: {
        x: { ticks: { color: '#8b9bb0' }, grid: { color: '#2a3544' } },
        y: { ticks: { color: '#8b9bb0' }, grid: { color: '#2a3544' } },
      },
    };
    new Chart(document.getElementById('latencyChart'), {
      type: 'line',
      data: {
        labels,
        datasets: [
          { label: 'Mean (ms)', data: timeline.map((t) => t.mean), borderColor: '#3d9cf0', tension: 0.25, pointRadius: 0 },
          { label: 'p95 (ms)', data: timeline.map((t) => t.p95), borderColor: '#f0b429', tension: 0.25, pointRadius: 0 },
          { label: 'p99 (ms)', data: timeline.map((t) => t.p99), borderColor: '#ff6b6b', tension: 0.25, pointRadius: 0 },
        ],
      },
      options: { ...common, plugins: { ...common.plugins, title: { display: true, text: 'Response time', color: '#e7eef7' } } },
    });
    new Chart(document.getElementById('rpsChart'), {
      type: 'bar',
      data: {
        labels,
        datasets: [
          { label: 'Request rate (/s)', data: timeline.map((t) => t.rps), backgroundColor: 'rgba(62, 207, 142, 0.65)' },
        ],
      },
      options: { ...common, plugins: { ...common.plugins, title: { display: true, text: 'Throughput', color: '#e7eef7' } } },
    });
  </script>
</body>
</html>
`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, html, 'utf8');
console.log(`HTML report written: ${path.resolve(outputPath)}`);
