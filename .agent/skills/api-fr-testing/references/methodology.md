# Methodology — conventions & per-phase detail

## Core conventions (learned the hard way)

1. **Contract = spec, not implementation.** Expected = what the FR says. If the SUT returns
   something else, the test FAILS on purpose and maps to a bug. Never edit an expected value
   to match observed behavior "so it passes".
2. **Probe safely.** Many toy SUTs re-seed the DB on boot and have no transactions. Always
   `cp db.sqlite db.bak` before probing and restore after, and run **read-only cases before
   destructive ones** (a stray DELETE/PUT poisons later reads).
3. **Decide ambiguity once, write it down (a DEC record).** When the spec is ambiguous
   (e.g. is `"1.0"` / `" 1"` / `"01"` a valid integer id?), pick strict or lenient, apply it
   to *all* sibling cases, and record the decision + rationale in the OpenAPI/spec so the two
   readings never mix. Default to **strict** (`type: integer, minimum: 1` rejects
   non-canonical forms) — it's consistent and matches standard validators.
4. **Expected-FAIL is a first-class outcome.** Mark bug-revealing cases clearly; count them
   separately from expected-PASS. A run with many reds is correct when reds = bugs.
5. **Anti-cheat / attribution.** If the assignment requires a header like `X-Student-Id`,
   inject it once via a collection-level pre-request script (not per request) and screenshot
   the Postman Console proving it. Keep the SUT host on `localhost` / `127.0.0.1`.
6. **Security realism.** If a secret is hard-coded in the source, a *forged* JWT signed with
   it has a valid signature → the server accepts it. An **empty** token (`Bearer ` with
   nothing after) is different from a **missing** header — trace the exact auth code
   (`token == null` vs `jwt.verify("")`) to predict 401 vs 403 correctly.

## Phase 1 — probe reality

```bash
SUT=eshop-sut/backend
cp "$SUT/database.sqlite" /tmp/db.bak            # 1. back up
(cd "$SUT" && node server.js &) ; sleep 3        # 2. start SUT
# 3. probe each branch — record status + body + content-type
curl -s -w "\n[%{http_code} | %{content_type}]\n" localhost:3000/api/<endpoint>
# ...valid / boundary / invalid / missing-auth / wrong-type...
pkill -f "node server.js"                         # 4. stop
cp /tmp/db.bak "$SUT/database.sqlite"             # 5. restore
```

**Spec-table template** (`api_specification.md`), two behavior columns per case:

| Case | Spec (FR) = Expected | Actual (SUT) | Bug? |
|------|----------------------|--------------|------|
| id not found | `404 {error}` | `200 {}` | BUG-xx |

## Test-case format

One Markdown table, paste-ready into Excel. Columns:

`TC-ID | API | FR/SEC | Technique | Precondition | Method+URL | Headers | Body | Expected status | Expected body/schema | Priority`

- **TC-ID naming:** one stable prefix per API, zero-padded: e.g. `TC-P1-001` (product read),
  `TC-O2-001` (order cancel), `TC-P3-001` (product manage). Keep numbers monotonic across
  all files of that API so extends append cleanly.
- **Priority:** security > state > boundary > partition, times "is this a required param?".
  P0 = bug-revealing or security-critical.
- **Expected** always from contract; annotate bug-revealing rows with `⇒ BUG-xx`.

## Phase 3 audit checklist

Tag each case VALID / INVALID / INCOMPLETE. Recurring AI mistakes to hunt:

| Signal | Verdict | Why |
|--------|---------|-----|
| Expected `201 Created` for a `POST` the SUT answers `200` | INVALID | Expected must follow spec; don't invent REST conventions the SUT doesn't use. |
| `404` for not-found softened to `200` to avoid red | INVALID (keep 404) | That red *is* the bug. |
| "verify SQLi blocked" with no payload/assertion | INCOMPLETE | Add concrete payload + measurable assertion. |
| State case with no fixture chain to reach the state | INCOMPLETE | Add checkout→admin-status steps. |
| Hard-coded id after a create/delete case ran | INVALID | Use a chained variable; order destructive last. |
| Expired-token test using a real (never-expiring) token | INVALID | Self-sign a token with a past `exp`. |
| Two cases, same partition, different wording | INVALID (merge) | Don't pad the count. |
| Ambiguous expected (`200/400`, "hoặc") where spec *does* constrain | INCOMPLETE | Pin it; if spec truly doesn't constrain, set the real value + observation. |
| Missing required submission header | INCOMPLETE | Add it. |

Record per-API counts (VALID/INVALID/INCOMPLETE) and how many VALID are expected-FAIL.
State the **counting unit** (per-case vs per-artifact) whenever you quote a number, so two
different tallies don't look contradictory.

## Phase 4 — extend, with "why AI missed it"

Categories to tag each extend case:
- **[Prompt]** — you didn't feed the source / didn't ask for flow or state testing.
- **[Model]** — AI reasoned from ideal REST / tested only sequentially / skipped odd types
  (boolean, array) or concurrency.
- **[API]** — the bug is hidden in code: a parity branch, hard-coded secret, missing FK /
  UNIQUE / middleware, unchecked `this.changes`, silent no-op. Impossible from the black box.

The most valuable extends are the ones with **no trace in the spec at all** — e.g. an
adjacent endpoint missing auth (IDOR), a silent DELETE of a non-existent row, a race on a
read-check-write. Verify every extend live with cURL before writing its Expected.
