# K05 — k6 fix log (23127271)

**Gate:** K05 only. Applied accepted K04 fix. No workflow redesign. No Redis. No JMeter XML.

| File | Change |
|------|--------|
| `test-plans/_k6_workflow.js` | CSV index `__ITER % n` → `(__VU - 1 + __ITER) % n` so 100 Stress VUs do not all login as `tram01`. |
| `23127271_Load_20260814.js` | No change (stages 40s+480s, think 1–3s already P01). |
| `23127271_Stress_20260814.js` | No change (100 VU, 25s+300s, think 0–100ms). |
| `23127271_Spike_20260814.js` | No change (`startVUs: 5`, 5→80→5, think 0–200ms). |
| `23127271_Soak_20260814.js` | Already cloned Load at 15 / 30s+720s (K06 file, not a K04 fault). |

Still true: Bearer only on cart/checkout; skip cart if detail check fails; tags `login|search|detail|cart|checkout`; filenames `23127271_{Load|Stress|Spike}_20260814.js`.
