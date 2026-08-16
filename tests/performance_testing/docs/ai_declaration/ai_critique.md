# AI Critique — HW05

- Họ và tên: Đặng Trường Nguyên
- MSSV: 23127438

*(200–300 words, as required by the AI Policy appendix. Material drawn from the human-review findings in Task 1 and the misinterpretation hunt in Task 2.)*

Across this assignment I used Claude Code as an AI collaborator, and a clear pattern emerged in where it fails. AI was strong at mechanical scaffolding — generating four JMeter plans from a script, wiring CSV data-driven inputs, and computing percentiles — but consistently weak whenever a claim had to be checked against the running system rather than inferred from a general pattern.

Three failure modes recurred. **First, trusting documents over reality:** it took the group README's `Laptop` search keyword, which returns an empty result on the seed data, and it followed the spec's lockout rule (≥3 fails, 30 s) instead of the stricter behaviour actually coded (+2 per fail, 180 s). Both were caught only by reading `server.js` and probing the live API. **Second, misreading metrics:** asked to interpret the results, it called p95 the "average", read a single worst-case `max` as systemic degradation, mistook one process at 42 % CPU on a 10-core machine for a saturated breaking point, and reported a think-time-limited baseline as maximum capacity. **Third, transplanting patterns:** it prescribed a B-tree index for a leading-wildcard `LIKE` and a connection pool for an embedded single-file SQLite — optimizations valid for client-server databases but not this SUT.

The common root cause is that AI reasons from statistical priors ("high load ⇒ timeouts", "LIKE ⇒ slow") rather than from the specific code, seed data, and raw `.jtl`. The principle I take away: AI is a fast first-drafter, but every parameter, metric, and recommendation must be re-verified against ground truth — and the human owns that verification.
