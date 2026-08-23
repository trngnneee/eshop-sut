# HW06 API Testing — Student 23127271

**APIs:** FR-04 Profile · FR-07 Cart · FR-19 Admin Users  
**SUT:** EShop backend (`http://localhost:3000`)

## Layout

| Path | Contents |
|------|----------|
| `tests/test-cases/` | Per-TC markdown (domain, state, security, schema) |
| `sheets/` | CSV test-case sheets |
| `postman/` | Newman/Postman collection + environment |
| `reports/` | Newman CLI log + HTML report |
| `bugs/` | Markdown bug reports |
| `docs/` | Stage reports, audit, execution summary |
| `scripts/` | Generators, audit helpers, Newman analysis |
| `git-commit-log.txt` | Full git log for submission |

## Newman

```bash
cd hw06/23127271
newman run postman/eshop-hw06.postman_collection.json -r cli,htmlextra \
  --reporter-htmlextra-export reports/newman-report.html
```

Do **not** pass `-e postman/eshop-hw06.postman_environment.json` when empty env tokens would override Setup tokens.

Student header `X-Student-Id: 23127271` is injected via collection pre-request script.
