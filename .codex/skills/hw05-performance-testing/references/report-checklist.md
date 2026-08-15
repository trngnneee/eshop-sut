# HW05 Report Checklist

Use this checklist while preparing the main report, appendix, README, and submission zip.

## Scenario Coverage

- Cover exactly one read-heavy endpoint group.
- Cover exactly one auth-heavy endpoint group.
- Cover exactly one transactional endpoint group.
- Pair the three groups with exactly one Load, one Stress, and one Spike scenario.
- Explain why each endpoint group fits its assigned scenario.

## Required Artifacts

- Three test plans named `{StudentID}_{ScenarioType}_{YYYYMMDD}`.
- Three separate CSV input files, one per endpoint group.
- Three raw `.jtl` logs.
- Three HTML report folders.
- Three distinct listener/report views across scenarios.
- Screenshots showing the test tool and backend resource monitor together.
- Hardware evidence screenshot and hardware spec table.
- Endurance/soak threshold with concrete numbers.
- Demo video link, unlisted YouTube, at least 6 minutes total, Vietnamese narration.
- GitHub issue links and screenshots for genuine bugs or performance issues, if found.
- Git commit log in text format.

## Analysis Requirements

- Use raw `.jtl` values as the source of truth.
- Include total metrics and per-sampler/endpoint metrics from the raw `.jtl`.
- Include AI-generated analysis, then a human correction/review.
- For every AI misinterpretation, cite the correct metric from raw logs.
- Include AI-proposed thresholds with the raw metric used as rationale.
- Include AI optimization recommendations with evidence categories.
- Classify each AI optimization recommendation as feasible, plausible but not
  proven, unsupported, or hallucinated.
- Include a human review table:
  `AI claim or recommendation | Raw evidence / correct value | Human decision | Reason`.
- Include a 200-300 word AI critique.

## Continuous Testing Proposal

- Watch commits or pull requests.
- Decide whether performance tests should run based on changed files or risk.
- Compare p95 latency against a baseline.
- Flag regressions and include cost/false-alarm trade-offs.
- Include a flow chart.

## Submission Package

- Zip name: `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`.
- Include main report in Markdown and PDF.
- Include AI Audit Report in Markdown and PDF.
- Include README with self-assessment table and test summary.
- Include public GitHub repository link.
