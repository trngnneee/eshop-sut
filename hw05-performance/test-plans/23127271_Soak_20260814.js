/**
 * 23127271_Soak_20260814 — constant 15 VU, 30s ramp + 720s hold, Load think 1–3s.
 * Clone of Load (K06). Not a Spike. Graded: --out json=../logs/23127271_Soak_20260814.json
 */
import { searchToBuy } from './_k6_workflow.js';

export const options = {
  stages: [
    { duration: '30s', target: 15 },
    { duration: '720s', target: 15 },
  ],
};

export default function () {
  searchToBuy(1, 2);
}
