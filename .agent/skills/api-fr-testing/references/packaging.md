# Phase 5 — Postman collection + Newman

## Collection structure

```
<Collection name>
  00-Setup            login(s) → set {{adminToken}}/{{userToken}}; seed product/order → set ids
  01-<API1>           Positive-Boundary / Negative / Security / Schema
  02-<API2>           Fixtures / State-Transitions / Auth-IDOR / Schema     (if stateful)
  03-<API3>           Create-Validation / Update-Validation / Auth-Escalation / Schema
  04-DataDriven-CSV   one request per CSV (matrix runs via Collection Runner -d)
  05-Mock-Spec        (optional) spec-correct example responses for a Postman Mock, to contrast vs SUT
  99-Teardown         delete test-created rows; run LAST
```

## Non-negotiables

- **Collection-level pre-request script** injects the attribution header once and logs it
  (screenshot the Console as anti-cheat evidence):
  ```js
  pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  console.log('[HW06] X-Student-Id =', pm.environment.get('studentId'), '->', pm.request.url.toString());
  ```
- **Environment** holds: `baseUrl` (full origin, e.g. `http://localhost:3000`), `studentId`,
  tokens, ids, and any forged tokens. **Variables are case-sensitive** — the collection must
  use exactly `{{baseUrl}}` (not `{{baseurl}}`), and requests use `{{baseUrl}}/api/...`
  (no hard-coded `http://` prefix, or you get a double-protocol URL).
- **Expected = contract** in every `pm.test`; bug cases stay red.
- **Collection variables** hold the reusable JSON schemas so
  `pm.response.to.have.jsonSchema(pm.collectionVariables.get('productSchema'))` works.
- Forged JWTs can't be signed inside Postman (no jwt lib) → generate with node and paste the
  token strings into the environment:
  ```bash
  node -e "console.log(require('jsonwebtoken').sign({id:<victimId>,role:'admin'},'<leaked-secret>'))"
  ```
  A run where the forged vars are empty sends `Bearer ` (empty) → server rejects → the
  escalation assert passes green and hides the bug. Paste real forged tokens, then re-run.

## Postman features to list in the report

Workspace · nested folders · Environment · Collection variables · collection-level
pre-request script · `pm.test`/`pm.expect` · `pm.response.to.have.jsonSchema` · request
chaining / dynamic variables (`{{$randomProductName}}`, `{{$timestamp}}`, `{{$guid}}`) ·
Collection Runner + CSV data files · Bearer auth inherited from folder · `pm.sendRequest` ·
Mock server · Monitor · saved examples · Newman + htmlextra reporter.

## Newman commands

```bash
npm i -g newman newman-reporter-htmlextra

# terminal 1: SUT (re-seeds on boot)
cd <sut>/backend && node server.js

# terminal 2: main run (functional folders only; keeps report clean)
cd <collection dir> && newman run <collection>.json \
  -e <environment>.json \
  --folder "00-Setup" --folder "01-<API1>" --folder "02-<API2>" --folder "03-<API3>" \
  -r cli,htmlextra \
  --reporter-htmlextra-export newman/report.html \
  --reporter-htmlextra-title "<title>"

# data-driven (one CSV per request name)
newman run <collection>.json -e <environment>.json \
  -d data/<file>.csv --folder '<exact DD request name>' \
  -r cli,htmlextra --reporter-htmlextra-export newman/report-dd1.html
```

Notes:
- Skip the `json` reporter unless you need it — its export can be tens of MB (full req/resp
  bodies) and bloats the submission zip.
- Restart the SUT before each fresh full run (destructive DELETE cases mutate the seed).
- Reds are expected: write `"<N> failures = <N> bugs, mapped in the Bug Report"` in the report.

## Evidence screenshots (typical rubric)

`console-x-student-id.png` (mandatory) · `newman-terminal-localhost.png` (mandatory, hostname
localhost/127.0.0.1) · `newman-htmlextra-summary.png` · CI `all-pass` + `one-fail` runs ·
one screenshot per bug on the issue tracker.
