# HW06 — API Testing (23127271)

**Student:** 23127271  
**Scope:** FR-04 `PUT /api/users/me` · FR-07 `POST /api/cart` · FR-19 `DELETE /api/admin/users/:id`  
**SUT:** `Repo/eshop-sut` · **280 test cases** · **8 bugs**

## G9.5 — AI test generator (Agent Skills)

| Path | What |
|------|------|
| `docs/test-generator-design.md` | Index + export instructions |
| `docs/test-generator-diagram.mmd` | Flowchart (Mermaid — self-authored) |
| `docs/test-generator-pseudocode.md` | Pseudocode mapped to diagram nodes |
| `.cursor/skills/api-testing/SKILL.md` | Agent Skill implementation |

Export `test-generator-diagram.mmd` → PNG for Moodle zip (see `test-generator-design.md`).

## Pipeline artifacts

| Path | What |
|------|------|
| `sheets/all-test-cases.csv` / `.xlsx` | Combined 280 TC + Summary |
| `postman/eshop-hw06.postman_collection.json` | Postman collection |
| `reports/newman-report.html` | Newman HTML report |
| `bugs/BUG-*.md` | 8 product bug reports |
| `ai_audit_log.md` | AI Audit Report appendix |
| `git-commit-log.txt` | Git commit log per stage |

## Stage docs

| Path | What |
|------|------|
| `docs/domain-testing-report.md` | Domain partitions (Skill-01) |
| `docs/stage2-audit*.md` | Audit per category |
| `docs/stage3-extend*.md` | Human SUP cases + why AI missed |
| `docs/execution-artifacts.md` | Postman features + run instructions |
| `docs/cicd-report.md` | GitHub Actions CI/CD + pass/fail run evidence |
| `docs/data-driven-runner.md` | CSV Collection Runner (folder 99) |
| `docs/newman-execution-summary.md` | Manual triage outcome |

## CI/CD

GitHub Actions workflow: `.github/workflows/hw06-api-tests.yml` (in `Repo/eshop-sut` root).

Runs Newman folder **`CI — HW06 pipeline demo`** on push to `main`. See `docs/cicd-report.md`.

Do not re-run Stage 1 generators after audit; they would overwrite corrected oracles.
