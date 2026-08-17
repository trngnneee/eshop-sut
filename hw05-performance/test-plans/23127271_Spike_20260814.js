/**
 * 23127271_Spike_20260814 — Search-to-buy SPIKE (k6 / K03+K05).
 * Parity: JMeter Ultimate TG 5→80→5. Peak 80 (below Stress 100). Think 0–200ms per request.
 * startVUs: 5 so the first 30s is AT 5, not a 0→5 ramp (K04 hunt 1 / K05).
 * Jump vs recover is NOT in whole-run http_req_duration p95 — split JSON by time in K07.
 * Graded: k6 run --out json=../logs/23127271_Spike_20260814.json
 */
import { searchToBuy } from './_k6_workflow.js';

export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-vus',
      startVUs: 5,
      stages: [
        { duration: '30s', target: 5 },
        { duration: '2s', target: 80 },
        { duration: '60s', target: 80 },
        { duration: '5s', target: 5 },
        { duration: '90s', target: 5 },
      ],
      gracefulRampDown: '5s',
    },
  },
};

export default function () {
  searchToBuy(0, 0.2);
}
