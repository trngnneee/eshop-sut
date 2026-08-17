# K04 — k6 vs JMeter parity review (23127271)

**Gate:** K04 only. Scripts: `_k6_workflow.js` + Load/Stress/Spike `.js`. JMeter freeze: P08 / P01 locked 20 / 100 / 5→80→5.

Checked all nine hunt items. One real fix for K05; the rest MATCH.

| # | Hunt | Verdict | What / why / fix |
|---|------|---------|------------------|
| 1 | VU/stages vs P01 | **MATCH** after Spike `startVUs: 5` | Load `40s→20 + 480s hold` = JMeter 520. Stress `25s→100 + 300s` = 325. Spike stages match Ultimate TG. A naive `{duration:'30s', target:5}` would ramp 0→5 during “baseline” — **already avoided** with `startVUs: 5` (see `23127271_Spike_20260814-k6-notes.md`). |
| 2 | Think-time per request | **MATCH** | `searchToBuy` sleeps after **each** of the five HTTP calls. Bands 1–3s / 0–100ms / 0–200ms. Not one sleep per iteration. |
| 3 | Checks 200 + body | **MATCH** | token; search `[0].id`; detail name+id (empty `{}` fails); cart `Added to cart`; checkout `orderId`. No price-type check. |
| 4 | Bearer / Content-Type | **MATCH** | JSON Content-Type on POSTs only. `Authorization` only on cart + checkout. GETs have neither. |
| 5 | CSV | **FIX** | SharedArray + papaparse + quoted fields + `tram*` filter (no `test@eshop.com`) MATCH. **Bug:** `users[__ITER % n]` makes **every VU’s first iteration `tram01`**. JMeter `shareMode.all` hands out distinct rows. Under Stress 100 that is 100 parallel logins on one account. **Why:** generic k6 CSV snippet uses `__ITER` only. **K05:** `users[(__VU - 1 + __ITER) % n]`. |
| 6 | Failed-login / lockout | **MATCH** | No failed-login request. Reset stays K06 SQL (Node up), same as P09. |
| 7 | Spike flat 80 / soak in Spike | **MATCH** | ramping-vus 5→80→5 + 90s recover. Soak is a **separate** `23127271_Soak_20260814.js` (15 / 30s+720s). |
| 8 | `name` tags | **MATCH** | `login`, `search`, `detail`, `cart`, `checkout`. |
| 9 | Workflow drift | **MATCH** | Five Search-to-buy paths only. |

**K05 must apply:** CSV index `__VU - 1 + __ITER`. Do not ship `__ITER % n` alone.
