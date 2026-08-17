# Gate map — HW05 Search-to-buy (23127271)

One gate per prompt. Full prompt text lives in [`prompt-plan.md`](./prompt-plan.md). Scope is locked in [`frozen-scope.md`](./frozen-scope.md).

| Gate | Task | Bloom | AI may produce | Human must do before next gate |
|------|------|-------|----------------|--------------------------------|
| **P00** | Scope lock | G9.2 | Endpoint map + coverage sentences | Confirm paths against `server.js` |
| **P01** | Parameters | G9.2 | Load/Stress/Spike table + justification | Reject generic 50/100/200 if not tied to this SUT/hardware |
| **P02** | CSV + lockout | G9.2 | CSV schema, row count, recycle policy, reset steps | Unique users ≥ max threads; Load = happy login only |
| **P03** | Listeners | G9.2 | One distinct listener per plan | No repeated listener type |
| **P04** | Human review of design | G9.3 | Critique of P00–P03 (no `.jmx` yet) | Write “what AI missed and why” |
| **P05** | Generate Load `.jmx` | G9.2 | One JMeter plan | Filename + assertions + CSV path |
| **P06** | Generate Stress `.jmx` | G9.2 | One JMeter plan | Same workflow; different profile + Summary Report |
| **P07** | Generate Spike `.jmx` | G9.2 | One JMeter plan | Sudden jump + Aggregate Report |
| **P08** | Fix plans | G9.4 | Patched `.jmx` / CSV only where P04 found faults | You are responsible for the final plans |
| **P09** | Runbook | G9.2 | CLI commands, evidence checklist, soak plan | **You** run tests; AI does not fabricate logs |
| **P10** | `.jtl` analysis | G9.3 | Metrics + proposed thresholds | Feed **raw** logs, not a pre-summary |
| **P11** | Misinterpretation hunt | G9.3 / G9.4 | Candidate mistakes (optional) | Cite correct values from raw `.jtl` yourself |
| **P12** | Judge optimizations | G9.3 | Feasible vs hallucinated vs this stack | Check `server.js` / SQLite / in-memory cart |
| **P13** | Continuous testing | G9.6 | Flow chart + trade-offs | Concrete p95 margin, not “add CI” |
| **P14** | AI Critique | G9.4 | 200–300 word draft | Rewrite from *this* run’s mistakes |
| **P15** | Report assembly | G9.2 | Markdown sections from real numbers | Fill templates; no invented evidence |
| **P16** | Skill demo script | G9.6 | Narration outline for the **second** video | Separate from the ≥6 min JMeter demo |

k6 bonus (only if you run both tools) — full prompts in [`k6-prompt-plan.md`](./k6-prompt-plan.md):

| Gate | Task | Bloom | AI may produce | Human must do before next gate |
|------|------|-------|----------------|--------------------------------|
| **K01** | Load `.js` | G9.2 | One k6 Load script | Stages 20 VU; per-request sleep 1–3s; CSV SharedArray |
| **K02** | Stress `.js` | G9.2 | One k6 Stress script | 100 VU; sleep 0–100 ms; same five paths |
| **K03** | Spike `.js` | G9.2 | One k6 Spike script | `stages` 5→80→5 + recover; not a flat 80 |
| **K04** | Review vs JMeter | G9.3 | Parity issue list | Genuine corrections before `k6 run` |
| **K05** | Fix scripts | G9.4 | Patched `.js` only | Filenames `23127271_*_20260814.js` |
| **K06** | k6 runbook | G9.2 | CLI + evidence + soak clone | **You** run; AI does not fabricate JSON |
| **K07** | JSON analysis | G9.3 | Metrics from `--out json` | Do not copy P10 `.jtl` numbers |
| **K08** | k6 hunt | G9.3 / G9.4 | Claim → correct value | Recompute from JSON yourself |
| **K09** | JMeter vs k6 | G9.3 | Comparison table + footprint | UNKNOWN if not measured |
