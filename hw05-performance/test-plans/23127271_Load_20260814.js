/**
 * 23127271_Load_20260814 — Search-to-buy LOAD (k6 / K01+K05).
 * Parity: JMeter 20 threads, 40s ramp, duration 520 (40+480), Uniform 1000–3000ms per sampler.
 * Graded: k6 run --out json=../logs/23127271_Load_20260814.json
 * Tree-equivalent: short k6 run --http-debug=full -e K6_VUS=1 (not the 520s run).
 */
import { searchToBuy } from './_k6_workflow.js';

export const options = {
  stages: [
    { duration: '40s', target: 20 },
    { duration: '480s', target: 20 },
  ],
};

export default function () {
  searchToBuy(1, 2);
}
