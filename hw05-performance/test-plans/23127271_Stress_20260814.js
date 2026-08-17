/**
 * 23127271_Stress_20260814 — Search-to-buy STRESS (k6 / K02+K05).
 * Parity: JMeter 100 threads, 25s ramp, duration 325 (25+300), Uniform 0–100ms per sampler.
 * Graded view: console summary + --out json=../logs/23127271_Stress_20260814.json
 */
import { searchToBuy } from './_k6_workflow.js';

export const options = {
  stages: [
    { duration: '25s', target: 100 },
    { duration: '300s', target: 100 },
  ],
};

export default function () {
  searchToBuy(0, 0.1);
}
