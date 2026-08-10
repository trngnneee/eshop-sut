Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)

CS423 / CSC13003 – Software Testing (AI-augmented · 2026)

AI POLICY · TEMPLATES — 2026 v1.0

# AI Critique — HW04: Automation Testing

Mandatory section (200–300 words). Address: Where did the AI get something wrong, biased, or incomplete? Why did it fail to catch the issue? What principle have you learned about collaborating with AI during this assignment?

## 1. Student Information

| Field | Value |
| --- | --- |
| Student name (printed): | DANG TRUONG NGUYEN |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Assignment ID: | HW04 — Automation Testing |
| Date: | 10/08/2026 |
| AI tool(s) used: | Claude Code (Claude Fable 5) |

## 2. AI Critique (200–300 words)

When I look back at what the AI actually got wrong in this assignment, none of it was where I expected. The generated Playwright code looked professional: clean Page Objects, web-first assertions, a tidy data-driven loop. The real defects were buried in assumptions. The AI reached for `getByLabel()` on a login form whose labels are not associated with any input, so those locators could never resolve. It treated the three browser projects as independent, while in reality they share one SQLite backend — its original lockout scenarios would have locked the shared test account for every run that followed. Even its batch script for filing GitHub issues paired each issue title with the body of the previous bug, because zsh arrays are 1-indexed while the AI silently assumed bash.

The common thread is that the AI was not wrong about testing; it was wrong about this system. It writes from the statistics of typical projects — associated labels, stateless environments, bash semantics — and nothing in its output signals when those priors stop holding. Code carrying a silent assumption looks exactly as confident as code that carries none. It also never volunteered to verify its own claims: the "Run by: StudentID" requirement was only proven after I decoded the HTML report payload myself. The principle I take away is that collaborating with AI means designing the verification, not just the prompt. I now feed it the real artifacts — source code, the SRS, the seeded database — and gate every generated artifact behind an execution check, because reviewing AI output by reading alone is not reviewing at all.

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 10/08/2026 |
| Signature: | ![signature](./signature.png) |
