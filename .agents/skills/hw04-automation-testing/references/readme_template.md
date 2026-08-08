# HW04 — Automation Testing — {{StudentID}}

## Test Summary Report
- Number of features automated: 3 (Pool A / B / C — list FR IDs)
- Number of test cases: automated {{n}}, executed {{n}}, passed {{n}}, failed {{n}}
- Number of browser runs: {{n}} (minimum 9 = 3 features × 3 browsers)
- Number of bugs filed: {{n}}
- Demo video (unlisted YouTube): {{link}}

## Self-Assessment

| No. | Criteria | Grade | Self-Assessed Grade |
|---|---|---|---|
| 1 | Task 1 - Feature A | 25 | {{n}} |
| 1 | Task 1 - Feature B | 25 | {{n}} |
| 1 | Task 1 - Feature C | 25 | {{n}} |
| 2 | Task 2 — Demo video | 15 | {{n}} |
| 3 | Agent Skills | 10 | {{n}} |
|   | **Total** | **100** | {{n}} |

## Repository Structure
```
hw04-automation/
├── playwright.config.js
├── package.json
├── data/
├── tests/
├── reports/
└── docs/
    ├── report.md
    ├── ai-audit-report.md
    ├── ai-critique.md
    ├── bug-report.md
    └── commit-log.txt
```

## How to run
```bash
npm install
npx playwright install
npx playwright test --reporter=html
npx playwright show-report reports/
```