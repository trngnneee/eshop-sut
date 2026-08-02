# HW03 Main Report — GUI, Usability and Cross-Platform Testing

**Student:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**System under test:** EShop  
**Report date/timezone:** 2026-08-03 — Asia/Bangkok (UTC+7)  
**Review state:** `HUMAN_REVIEWED`  
**Overall evidence state:** `LOCALLY_VALIDATED_WITH_DISCLOSED_EXTERNAL_LIMITATIONS`

## 1. Executive summary

This report consolidates the three HW03 tasks into one auditable narrative while retaining the original evidence folders. Task 1 provides a 58-item GUI checklist and an item-level Chrome execution. Task 2 analyzes the registration → login → profile update → logout flow for exactly seven participant IDs, P01–P07, including T0–T11 session coding and seven user-provided SUS response sets. Task 3 re-executes the same 58 GUI IDs across four browser environments and produces 232 platform-item results with 160 screenshots.

| Task | Core dataset | Result | Completion boundary |
|---|---|---|---|
| Task 1 — GUI checklist | 58 unique items; 40 Chrome screenshots | 37 Pass / 20 Fail / 1 Blocked | GUI-skill YouTube demo is verified; all 20 failed rows map to 18 verified GitHub issues. Native soft-keyboard evidence remains unavailable. |
| Task 2 — usability | 7 official recordings; 7 session reports; exact T0–T11 coding; 70 SUS responses | 0/7 completed all SC1–SC5; funnel collapses at profile update; calculable task-time median 80 s; SUS mean 76.79 | Core session-count, notes, SUS and analysis deliverables are present. A separate pilot record and post-session probe responses remain unavailable. |
| Task 3 — cross-platform | 58 IDs × 4 environments = 232 rows; 160 screenshots | 37 Pass / 20 Fail / 1 Not Observable per environment | Chrome and Firefox are eligible; WebKit Windows is not Safari and Pixel emulation is not real Android, leaving 2/3 eligible platforms. |

Default/local validators return exit 0 for all three packages. Strict evidence validators return exit 2 only for the disclosed external/fieldwork gaps. No pilot, consent, quote, probe, participant value, platform, issue URL, device run or video URL was synthesized to turn a strict failure into a pass.

### 1.1 Work completed across the three tasks

The submission was produced as one connected testing programme rather than three unrelated documents:

| Phase | Task 1 — GUI | Task 2 — usability | Task 3 — cross-platform |
|---|---|---|---|
| Requirement interpretation | Mapped FR-01, FR-02, FR-12 and FR-14 to five in-scope screens and corrected unsupported test oracles. | Converted the account journey into SC1–SC5 and a T0–T11 observation schema. | Reused the exact corrected 58-ID Task 1 oracle without changing the item set. |
| Test preparation | Built a 58-row checklist with IA coverage, origin, severity, steps and expected results. | Prepared plan, moderator guide, task cards, SUS form, probes, consent template, roster and session structure. | Inventoried installed browsers/tooling, established eligibility rules and built a repeatable browser runner. |
| Execution/data collection | Executed the local Chrome run, including controlled network/loading/empty/write states and Expo Web limitations. | Analyzed seven official recordings, replaced one duplicated source, and kept unavailable observations explicit. | Executed four environments, captured identity/platform overlays and generated 232 platform-item rows. |
| Analysis | Reconciled 58 rows, 40 screenshots, 37 Pass, 20 Fail and 1 Blocked. | Calculated task metrics, exact raw SUS, seven findings and three independent technical reproductions. | Compared all 58 IDs across environments, grouped systemic failures and separated engine differences from product defects. |
| Quality control | Checked evidence paths, PNG signatures, execution modes, GitHub URL shape and requirement corrections. | Validated P01–P07, T0–T11, 70 SUS values, score arithmetic, privacy and bug/usability separation. | Excluded the flawed initial run, corrected three harness defects and validated 160 indexed screenshots. |
| Reporting | Consolidated results into this report and `Bug_Report.md`. | Consolidated participant results, SUS, missing-data declaration and canonical issues #55/#37/#118. | Consolidated platform inventory, result matrix, evidence eligibility and third-platform blocker. |

### 1.2 Submission structure

The grading entry point provides `README.md`, the consolidated Markdown reports, current PDF counterparts and the authentic full-hash Git log. The correctly named ZIP also includes the Task 1 XLSX checklist, test summaries, all three task evidence directories and both submitted Agent Skills. Participant recordings remain in the access-controlled Drive locations indexed as D01–D07; they are not duplicated into the archive because the raw files contain PII and plaintext-password intervals.

### 1.3 Assessment-template reconciliation

The assignment PDF allocates 30 points to Task 1, 40 to Task 2, 20 to Task 3 and 10 to Agent Skills. The completed README self-assessment is **088/100**: 29/30, 36/40, 13/20 and 10/10 respectively. Task 2 is credited for seven official recordings, seven structured notes, a complete SUS dataset, funnel/error diagnostics and severity-ranked findings; it is not given unsupported credit for a missing pilot or probe-response record. This estimate does not override the instructor's judgement.

Submission-format compliance has been restored: the build generates Markdown and PDF reports, includes the XLSX checklist, test summaries, task evidence and both skills, and closes the correctly named `23127207_HW03_AI_GUIUsability_088.zip` only after checking required entries.

## 2. Scope and evidence model

### 2.1 Task 1 scope

Task 1 covers five screens/modules:

| Platform | Screen | Requirement mapping | Item count |
|---|---|---|---:|
| Web frontend | Login `/login` | FR-02 and GUI/accessibility heuristics | 13 |
| Web frontend | Register `/register` | FR-01 | 12 |
| Web admin | Admin Login, unauthenticated `/` | FR-12 | 9 |
| Web admin | Category tab | FR-14 | 13 |
| Mobile UI through Expo Web | Login view | FR-02/mobile UI quality | 11 |
| **Total** |  |  | **58** |

Product, cart, checkout, coupon, dashboard and order-management behavior is out of scope except when an in-scope control navigates to a destination.

### 2.2 Task 2 scope

The evaluated participant flow is:

> Registration → Login → Update name/phone/address → Verify persistence → Logout

A session is successful only when all five criteria are evidenced:

1. SC1 — account created successfully.
2. SC2 — login succeeds with that account.
3. SC3 — name, phone and address are all updated.
4. SC4 — updated values persist after reload or revisit.
5. SC5 — logout succeeds behaviorally.

Technical reproduction is never counted as participant evidence. Participant analytical artefacts use P01–P07; the separate masked-contact roster is private submission evidence.

### 2.3 Task 3 scope

Task 3 uses the corrected Task 1 checklist ID set without adding or removing rows. Four local environments were executed, but platform eligibility is evaluated separately from whether a run produced useful compatibility evidence.

### 2.4 Out-of-scope and non-claims

- The work does not claim production deployment, load/performance testing, penetration testing or full business-flow coverage.
- A mocked response is used only to make a UI state deterministic; it is never represented as a production backend result.
- Participant video endings are interpreted as task endings only where the user supplied that fieldwork context.
- SUS is analyzed descriptively for the supplied seven response sets and is not used as a completion substitute.
- WebKit on Windows is not Apple Safari, and a Pixel browser descriptor on Windows is not a real Android device.
- Human review confirms interpretation and authorship; it does not create missing evidence.

## 3. Provenance, execution modes and integrity controls

Task 1 contains exactly 48 `AI_INITIAL` and 10 `HUMAN_ADDED` checklist items. Human review was confirmed on 2026-08-02. Each current row includes Expected Result, Actual Result, Notes, status, execution mode, evidence ID, capture timestamp and screenshot path.

Execution modes are explicit:

| Mode | Task 1 rows | Interpretation |
|---|---:|---|
| `LIVE_LOCAL_SUT` | 52 | Runtime action against the local EShop services. |
| `MOCKED_NETWORK_FAILURE` | 1 | Deterministic network-failure state. |
| `MOCKED_WRITE_PREVENTION` | 1 | Empty-category request observed while preventing permanent mutation. |
| `MOCKED_EMPTY_API_STATE` | 1 | Deterministic empty-state response. |
| `MOCKED_SLOW_API` | 1 | Deterministic delayed read for loading-state observation. |
| `MOCKED_SLOW_WRITE` | 1 | Delayed write for double-submit observation. |
| `EXPO_WEB_DESKTOP_BROWSER` | 1 | Honest soft-keyboard non-observation; not a native phone run. |

Task 2 results are derived from the seven official recordings after the replacement P06 source superseded the old duplicate. Missing data is never converted to zero. `NOT_RECORDED`, `NOT_OBSERVABLE` and `NOT_REACHED` are distinct states.

Task 3 screenshots contain the student identity/email overlay, browser or engine version, host/device declaration, current SUT URL, evidence ID, checklist IDs, observation and timestamp. Synthetic accounts, categories and products were used and cleaned after execution. Mocked states retain their execution-mode labels.

## 4. Task 1 — GUI checklist result

### 4.1 Work performed and test-design method

Task 1 was completed in six concrete steps:

1. Inspect the assignment requirements and the local web/admin/mobile entry points.
2. Define the five-screen scope and map every checklist row to a requirement, information-area category and observable expected result.
3. Start from 48 AI-proposed rows, add 10 human rows for keyboard focus, responsive width, edge cases, network/loading/empty states, long input, double submit and touch target coverage, then human-review every oracle.
4. Execute the corrected checklist against the local EShop services. Use live integration for normal flows and explicitly labelled deterministic interception only where timing or a destructive write state must be controlled.
5. Record Actual Result, status, notes, evidence ID, timestamp, mode, screenshot and bug mapping at row level; do not infer a Pass from source code alone.
6. Reconcile the Markdown/XLSX/CSV outputs against one result source, validate screenshots and separate a failed assertion from the eventual root-cause issue.

The four IA dimensions make coverage reviewable rather than a flat list:

| IA | Interpretation used in this package | Examples |
|---|---|---|
| `IA-01` | Visual presentation, accessibility, responsive layout and control appearance | headings, focus order, width 320 px, touch target |
| `IA-02` | Form input, validation, credential semantics and boundary data | `type=email`, password policy, required fields, long names |
| `IA-03` | Navigation and task transition | login/register links, forgot-password, category tab, protected route |
| `IA-04` | Feedback, asynchronous state, error recovery and resilience | lockout, duplicate feedback, loading/empty/network failure, double submit |

Test data used student-specific synthetic identifiers and reversible category/product records. Screenshots contain test credentials only. Category writes were cleaned after execution; the empty-name write was intercepted in `MOCKED_WRITE_PREVENTION` to observe the request without retaining unwanted data.

### 4.2 Coverage

| Dimension | Value | Count |
|---|---|---:|
| Platform | Web Frontend | 25 |
| Platform | Web Admin | 22 |
| Platform | Mobile App | 11 |
| IA | IA-01 | 11 |
| IA | IA-02 | 19 |
| IA | IA-03 | 10 |
| IA | IA-04 | 18 |
| Origin | AI_INITIAL | 48 |
| Origin | HUMAN_ADDED | 10 |

Screen × IA coverage is:

| Screen | IA-01 | IA-02 | IA-03 | IA-04 | Total |
|---|---:|---:|---:|---:|---:|
| Web Login | 4 | 5 | 2 | 2 | 13 |
| Web Register | 2 | 6 | 1 | 3 | 12 |
| Admin Login | 1 | 2 | 3 | 3 | 9 |
| Admin Category | 1 | 3 | 1 | 8 | 13 |
| Mobile Login | 3 | 3 | 3 | 2 | 11 |
| **Total** | **11** | **19** | **10** | **18** | **58** |

### 4.3 Result metrics

| Metric | Value |
|---|---:|
| Total unique checklist IDs | 58 |
| Pass | 37 |
| Fail | 20 |
| Blocked | 1 |
| Unique Chrome screenshots | 40 |
| Unique verified GitHub issues | 18 |
| Fail rows with verified GitHub URLs | 20 |
| Fail rows pending verified GitHub URLs | 0 |

The prior 36/22 checklist, conflicting 40/18 summary and five packed screenshots are superseded. The current machine-readable source is [`../task1-gui/results/Task1_Execution_Chrome.csv`](../task1-gui/results/Task1_Execution_Chrome.csv).

### 4.4 Human-review corrections

Three material expectation problems were corrected before final classification:

1. `GUI-WEB-LOGIN-010` now checks the written FR-02 boundary: three failed attempts and a 30-second lockout requirement.
2. `GUI-WEB-LOGIN-013` no longer invents automatic whitespace trimming; safe rejection with generic feedback satisfies the corrected expectation.
3. `GUI-ADMIN-CATEGORY-005` checks real navigation to the Category tab instead of treating absent Edit Category functionality as an FR-14 defect.
4. `GUI-ADMIN-CATEGORY-011` observes deterministic Add/View behavior for a repeated name; FR-14 does not state that category names must be unique.

The last three observations were reclassified to Pass from the retained runtime evidence. Screenshots and capture timestamps were not changed.

### 4.5 Evidence and defect handling

Forty screenshots cover the 58 rows because one screenshot may legitimately support several assertions from the same state. Reuse is traceable through a stable Evidence ID; it is not presented as 58 independent captures. Every screenshot path is checked for existence, minimum size and PNG signature. Each failed row receives a local Bug ID and a verified GitHub issue URL. Seven publication-safe technical screenshots are also isolated on the public `hw3-public-evidence-khoa` branch for issues #291–#298.

The Task 1 output retained for grading is intentionally compact:

- [`GUI_Checklist_HW3.md`](../task1-gui/GUI_Checklist_HW3.md) and [`GUI_Checklist_HW3.xlsx`](../task1-gui/GUI_Checklist_HW3.xlsx) for the complete row-level checklist;
- [`Task1_Execution_Chrome.csv`](../task1-gui/results/Task1_Execution_Chrome.csv) as the machine-readable execution source;
- [`Evidence_Index.csv`](../task1-gui/results/Evidence_Index.csv) and the [40 screenshots](../task1-gui/evidence/executed-chrome/) for evidence traceability;
- `Bug_Report.md` for the single consolidated defect narrative; and
- the Task 1 validator for semantic/evidence checks.

### 4.6 Main GUI risks

The highest-risk Task 1 observations are plaintext password display, incorrect login semantics, generic lockout feedback, duplicate email acceptance, unsafe in-use category deletion, absent confirmation/loading/empty/double-submit states, positive tabindex, missing admin labels, inconsistent mobile localization and a 39 px mobile submit target below the 44 px threshold. Detailed severity and issue traceability are consolidated in `Bug_Report.md`.

### 4.7 Task 1 completion decision

The Task 1 package is structurally ready. Strict completion is now blocked only by a real Expo Go/physical/cloud phone run for `GUI-MOBILE-LOGIN-011` soft-keyboard behavior.

The GitHub App first available to this audit could read repository branches and issues, but its write calls returned HTTP 403 `Resource not accessible by integration`. The user then authorized Git Credential Manager device authentication. A sanitized evidence-only branch was pushed, all seven PNG URLs returned HTTP 200 `image/png`, and eight deduplicated issues [#291](https://github.com/trngnneee/eshop-sut/issues/291)–[#298](https://github.com/trngnneee/eshop-sut/issues/298) were created and read back successfully. Those eight issues close the nine previously pending row mappings because #297 covers the shared mobile-localization root cause for two checklist rows.

The Task 1 GUI-skill demo is [https://youtu.be/tMar6OyMG80](https://youtu.be/tMar6OyMG80). Status is `PUBLIC_LINK_VERIFIED`: YouTube oEmbed returned title `GUI-testing-skill demo`, author `Đặng Đăng Khoa` and provider `YouTube`. The submission stores only this public link; no local MP4 is required.

## 5. Task 2 — Usability evaluation

### 5.1 Study preparation and analysis workflow

Task 2 was prepared as a moderated usability evaluation of one continuous account journey. The retained method assets include the usability test plan, moderator guide, two task cards, SUS form, post-session probes and consent template. Their presence documents the intended method; it does not claim that every instrument was actually administered.

The analysis workflow was:

1. Inventory the supplied recording sources in read-only mode and treat source filenames/contact values as private data.
2. Assign analytical aliases D01–D07 and participant IDs P01–P07 from the user-provided recruitment mapping, without using face or voice inference.
3. Detect that the first D06 source duplicated another recording, replace it with the user-supplied official D06, verify that its SHA-256/media metadata differ from D01, and exclude the superseded file from every frequency.
4. Decode each official video, inspect screen milestones and assess whether audio contains usable speech. A non-VAD transcript attempt produced unrelated text and was rejected; no quote was retained.
5. Code each session using the same T0–T11 schema, record observable errors/wrong turns/hesitations, and classify SC1–SC5 at confirmed task end.
6. Use the user’s confirmation to interpret the early ends of P02, P03, P05 and P06 as complete session ends rather than inventing missing continuation.
7. Import the separately supplied P01–P07 SUS response sets with `COMPLETED_USER_PROVIDED` provenance, calculate scores independently and cross-check the result tables.
8. Aggregate participant behavior into findings, reproduce product defects using synthetic data, search GitHub for duplicates and keep technical-only evidence outside participant frequencies.

### 5.2 Participant and session integrity

Exactly seven official IDs are used: P01, P02, P03, P04, P05, P06 and P07. There are seven official session files and no identifier outside that exact set or extra participant row. Every session report contains exactly one row for each code T0 through T11.

The same coding schema is used in all seven session reports:

| Code | Session milestone |
|---|---|
| `T0` | First observable task action after recording begins. |
| `T1` | Registration page/form opens. |
| `T2` | First registration submit. |
| `T3` | Registration success/transition to login. |
| `T4` | First login submit. |
| `T5` | Login success/authenticated state appears. |
| `T6` | Profile page opens. |
| `T7` | First profile-update submit. |
| `T8` | Successful profile save is observed. |
| `T9` | Persistence/trust confirmation is observed or elicited. |
| `T10` | Logout action. |
| `T11` | Confirmed task/session end. |

When a milestone is absent, the row retains `NOT_REACHED`, `NOT_OBSERVABLE` or the applicable disclosed status rather than substituting a timestamp.

The participant recordings produced these success-criterion outcomes:

| Participant | SC1 account | SC2 login | SC3 update all fields | SC4 persistence | SC5 logout | Outcome |
|---|---|---|---|---|---|---|
| P01 | Pass | Pass | Fail | Not reached | Behavioral pass | Failed or abandoned |
| P02 | Pass | Pass | Fail | Not reached | Not reached | Failed or abandoned |
| P03 | Not reached | Not reached | Not reached | Not reached | Not reached | Failed or abandoned |
| P04 | Pass | Pass | Fail | Not reached | Behavioral pass | Failed or abandoned |
| P05 | Pass | Fail | Not reached | Not reached | Not reached | Failed or abandoned |
| P06 | Fail | Not reached | Not reached | Not reached | Not reached | Failed or abandoned |
| P07 | Pass | Pass | Fail | Not reached | Behavioral pass | Failed or abandoned |

Behavioral logout does not independently prove token/storage deletion; storage state remains not observable from participant evidence.

### 5.3 Metric definitions and observed metrics

Metrics follow these rules:

| Metric | Operational definition |
|---|---|
| Completion | Pass only if SC1–SC5 are all evidenced by confirmed task end. Partial progress is not converted into completion. |
| Task time | `T11 − T0` only when both endpoints are observable/confirmed. P03 remains not calculable because T0 is not observable. |
| Error | Visible failed submit, validation rejection or incorrect credential/format action attributable to the observed interaction. |
| Wrong turn | Observable departure from the intended SUT flow, such as opening browser password-manager settings. |
| Hesitation | Observable inactivity of at least five seconds associated with the task state. |
| Intervention/Card B | Count only when moderator speech/action is observable; otherwise retain `NOT_OBSERVABLE`, not zero. |
| Behavioral logout | Visible transition out of the authenticated state; storage/token deletion requires separate technical evidence and is not inferred. |

| Participant | Outcome | Task time | Wrong turns | Errors | Hesitations ≥5 s | SUS |
|---|---|---:|---:|---:|---:|---:|
| P01 | Failed or abandoned | 111 s | 0 | 5 | 0 | 82.5 |
| P02 | Failed or abandoned | 94 s | Not observable | 3 | 1 | 75 |
| P03 | Failed or abandoned | Not observable | Not observable | Not observable | Not observable | 100 |
| P04 | Failed or abandoned | 136 s | 1 | 4 | 0 | 65 |
| P05 | Failed or abandoned | 50 s | Not observable | 0 | 0 | 62.5 |
| P06 | Failed or abandoned | 52 s | 0 | 4 | 0 | 65 |
| P07 | Failed or abandoned | 66 s | 0 | 1 | 1 | 87.5 |

Summary:

- Independent completion: 0/7.
- Completion with assistance: 0/7.
- Failed or abandoned: 7/7.
- Calculable task times: 6/7; median 80 s, minimum 50 s, maximum 136 s.
- Observed lower bound: 17 errors, one wrong turn, two hesitations of at least five seconds, totaling ten seconds.
- Intervention, think-aloud-reminder and Card B counts remain `NOT_OBSERVABLE`; they are not reported as zero.

#### Flow funnel and error concentration

| Flow checkpoint | Evidenced passes | Rate |
|---|---|---:|
| SC1 — account created | P01, P02, P04, P05, P07 | 5/7 (71.4%) |
| SC2 — authenticated | P01, P02, P04, P07 | 4/7 (57.1%) |
| SC3 — requested profile data saved | None | 0/7 (0.0%) |
| SC4 — saved data persisted | None | 0/7 (0.0%) |
| SC5 — behavioral logout | P01, P04, P07 | 3/7 (42.9%) |

Five participants passed account creation and four passed login, but no participant produced a requirement-conforming profile save. Of the 17 visible error events, 5 occurred during registration/password recovery, 1 during login/identifier recovery and 11 during profile/phone recovery. The profile stage therefore contains 64.7% of the visible error lower bound and is the dominant remediation target. This triangulates the behavioral funnel with both S1 findings, `BUG-PF-02` and `UF-PHONE-RECOVERY-01`.

### 5.4 Session-by-session analysis

| Participant | What was observed | Why the final outcome is not complete |
|---|---|---|
| P01 | Registered and logged in; made five profile submits with leading-zero phone formats; then logged out. | No successful SC3 save or SC4 persistence; task time 111 s and five observed errors. |
| P02 | Registered and logged in; made three failed profile submits before the confirmed end at the validation alert. | SC3–SC5 not achieved; captured task time 94 s, three errors and one hesitation. |
| P03 | Four-second recording with no observable first task action; the user confirmed this is the complete session. | SC1–SC5 not reached; T0 and most behavior metrics remain not observable even though SUS was supplied separately. |
| P04 | Recovered from one registration-password error, briefly opened Edge Password Manager, logged in and tried multiple phone formats; a non-leading-zero phone produced success feedback; then logged out. | The accepted phone contradicted FR-04 and name/address remained incomplete, so SC3/SC4 fail; 136 s, one wrong turn and four errors. |
| P05 | Registered, reached login and entered credentials, but no login submit occurred before the confirmed session end. | SC2–SC5 not achieved; 50 s captured time and zero visible system-error events, with other unavailable measures not forced to zero. |
| P06 | Replacement recording shows four registration submits receiving the same weak-password error and three repeated recovery actions. | SC1 was not achieved before the confirmed end; 52 s and four observed errors. |
| P07 | Registered; initially used the wrong identifier under the `Username` label, hesitated, self-corrected to full email, logged in, opened profile and later logged out. | No profile update or persistence occurred, so SC3/SC4 fail; 66 s, one error and one hesitation. |

These narratives use only visible behavior and the user-confirmed task-end context. They do not infer participant intent, satisfaction, trust or moderator assistance from silent audio.

### 5.5 Raw SUS and calculation

Seven complete user-provided response sets are identified as P01–P07. All 70 responses are integers from 1 to 5. Collection is not visible in the recordings, so provenance remains `COMPLETED_USER_PROVIDED` rather than inferred from participant behavior.

For odd questions, contribution = response − 1. For even questions, contribution = 5 − response. SUS score = contribution sum × 2.5.

| Participant | Raw Q1–Q10 | Contributions Q1–Q10 | Sum | SUS |
|---|---|---|---:|---:|
| P01 | 4;2;5;1;4;2;5;2;4;2 | 3;3;4;4;3;3;4;3;3;3 | 33 | 82.5 |
| P02 | 4;2;4;2;4;2;4;2;4;2 | 3;3;3;3;3;3;3;3;3;3 | 30 | 75 |
| P03 | 5;1;5;1;5;1;5;1;5;1 | 4;4;4;4;4;4;4;4;4;4 | 40 | 100 |
| P04 | 3;3;4;2;4;3;4;3;4;2 | 2;2;3;3;3;2;3;2;3;3 | 26 | 65 |
| P05 | 4;3;4;2;3;3;4;2;3;3 | 3;2;3;3;2;2;3;3;2;2 | 25 | 62.5 |
| P06 | 3;2;4;3;4;2;4;3;3;2 | 2;3;3;2;3;3;3;2;2;3 | 26 | 65 |
| P07 | 5;2;4;1;5;2;4;2;5;1 | 4;3;3;4;4;3;3;3;4;4 | 35 | 87.5 |

| Statistic | Value |
|---|---:|
| Mean | 76.79 |
| Median | 75 |
| Minimum | 62.5 |
| Maximum | 100 |
| Sample standard deviation | 13.97 |
| Interquartile range | 65–87.5 |

The item-level means are Q1 4.00, Q2 2.14, Q3 4.29, Q4 1.71, Q5 4.14, Q6 2.14, Q7 4.29, Q8 2.14, Q9 4.00 and Q10 1.86. After direction normalization, Q2, Q6 and Q8 have the lowest mean contributions (2.86/4), making perceived complexity, inconsistency and cumbersomeness the most useful SUS-level follow-up signals.

SUS is a 0–100 scale, not a percentage. These values are descriptive for the supplied sample; no population-level or statistical-significance claim is made. The contrast between a relatively positive SUS mean and 0/7 strict task completion is retained because the measures answer different questions: SUS captures the supplied perceptions, while SC1–SC5 requires every predefined behavioral checkpoint. The detailed derivation is retained in `Analysis/Flow_Funnel_and_SUS_Diagnostics.md`.

### 5.6 Severity-ranked usability findings

| Rank | Finding | Type | Frequency | Severity |
|---:|---|---|---:|---|
| 1 | `BUG-PF-02` — required leading-zero phone format is rejected | Software bug | 3/7 | S1 |
| 2 | `UF-PHONE-RECOVERY-01` — error recovery causes repeated unsupported phone attempts | Usability issue | 3/7 | S1 |
| 3 | `BUG-AUTH-PLAINTEXT-01` — login password is displayed as plaintext | Software bug | 5/7 | S2 |
| 4 | `BUG-REG-PASSWORD-POLICY-01` — registration API accepts a password missing the required special-character class | Technical-only software bug | N/A | S2 provisional |
| 5 | `UF-REG-PASSWORD-RECOVERY-01` — password-policy recovery repeats | Usability issue | 2/7 | S2 |
| 6 | `UF-LOGIN-IDENTIFIER-01` — Username copy does not communicate that full email is required | Usability issue | 1/7 | S3 |
| 7 | `UF-PASSWORD-MANAGER-DETOUR-01` — browser password-manager detour | Usability issue | 1/7 | S4 |

Software bugs and usability issues remain separate. The technical password-policy defect is not attributed to P04 or P06 because their typed passwords are masked in the recordings. Its participant frequency is therefore N/A.

### 5.7 Independent reproduction and GitHub traceability

Three isolated reproductions used synthetic names, accounts, phone values and passwords. They were executed to verify product behavior after the participant analysis, not to replace participant observations:

| Bug | Reproduction result | Relationship to participant data |
|---|---|---|
| `BUG-PF-02` | Requirement-conforming leading-zero phone input follows the invalid path; reproduction supports issue #55. | Corroborates P01/P02/P04 and keeps frequency 3/7. |
| `BUG-AUTH-PLAINTEXT-01` | Login credential control renders as ordinary text rather than a masked password control; reproduction supports issue #37. | Corroborates P01/P02/P04/P05/P07 and keeps frequency 5/7. |
| `BUG-REG-PASSWORD-POLICY-01` | Direct API registration without an allowed special character returns 200 and the account logs in with 200; 13/13 frontend EP/BVA controls still pass. | Technical-only `NONE`/`N/A`; no participant attribution. |

Duplicate search was completed before issue handling:

- `BUG-PF-02` reuses canonical [issue #55](https://github.com/trngnneee/eshop-sut/issues/55); fresh synthetic evidence was published in the recorded issue comment.
- `BUG-AUTH-PLAINTEXT-01` reuses canonical [issue #37](https://github.com/trngnneee/eshop-sut/issues/37); fresh synthetic evidence was published in the recorded issue comment.
- `BUG-REG-PASSWORD-POLICY-01` reuses canonical [issue #118](https://github.com/trngnneee/eshop-sut/issues/118). Duplicate search prevented a new issue. Its reviewed reproduction remains local; no new #118 comment is claimed.

### 5.8 Task 2 method limitations and missing-data declaration

The following were not collected or cannot be verified from the supplied evidence:

- pilot session and protocol refinement;
- consent supplement or recorded consent evidence;
- post-session clarity, recovery, speed, trust and requested-change probes;
- usable participant speech and genuine quotes;
- exact moderator wording, think-aloud reminders and task-directed intervention counts;
- some session environment, device and full timing fields;
- complete seven-person distributions for metrics where P03 or another session is not observable.

These limitations do not mean that additional official session recordings are being requested: D01–D07 are the complete official recording set, all seven are linked, decoded and represented by structured session reports. Optional audio is not treated as a reason to reject the seven sessions. The unavailable items are kept separate so the grader can distinguish complete core deliverables from method evidence that cannot be recreated retrospectively.

An authenticated Drive recheck on 2026-08-02 traced D01–D07 to one common `Khoa` folder. Its direct listing contained eight MP4 files and no documents, forms, spreadsheets or subfolders. The parent `HW3` folder contained participant folders and two allocation files, but no pilot, consent, probe or SUS collection artefact. Broader authenticated searches using the corresponding HW03 and generic keywords also found no relevant EShop fieldwork record. This is an evidence-availability finding, not an inference that consent did or did not occur.

These omissions are the reason strict evidence validation returns exit 2. The default package-closure validator returns exit 0 because the missing fields are disclosed instead of populated with invented data.

### 5.9 Retained Task 2 evidence and submission mode

The verified public Task 2 skill-demo link is [https://youtu.be/QAh6W9AJXiU](https://youtu.be/QAh6W9AJXiU). The skill demo is submitted by public YouTube link. The seven participant recordings are separate, access-controlled Drive evidence linked from `Stage_0_Drive_Inventory.md`. The private participant roster is included in the Moodle ZIP for TA verification and must not be published to GitHub.

The retained Task 2 archive contains the study plan/instruments, seven session reports, masked private roster, seven-link recording manifest, missing-data and video-quality records, six analysis files, verified YouTube metadata, synthetic reproduction evidence and three validation scripts. The package build verifies 7/7 session reports, 7/7 official Drive links and 7/7 SUS response rows before closing the ZIP.

## 6. Task 3 — Cross-platform execution

### 6.1 Work performed and automation pipeline

Task 3 converted the corrected Task 1 oracle into a repeatable platform runner. The runner does not decide that all engines are equivalent; it performs the same observable assertion and records the engine-specific Actual Result.

Execution proceeded as follows:

1. Inventory locally available Chrome, Firefox, Playwright WebKit, Chromium device descriptors, Expo Web, cloud credentials and Android tooling.
2. Mark platform eligibility before result interpretation: only real Chrome/Firefox and a genuine Safari-or-Android category can satisfy the required three-platform gate.
3. Start the local frontend, admin, API and Expo Web paths, create student-specific synthetic fixtures, and route the Expo Web API request to the disclosed local backend.
4. Execute all 58 IDs in each environment using the same corrected expected results. Preserve five controlled mocked-state rows and one Expo-Web soft-keyboard limitation per environment.
5. Capture the visible state with an overlay containing student name, ID/email, platform/browser version, host/device declaration, localhost URL, evidence/checklist IDs, observation and ISO timestamp.
6. Record dialogs, HTTP outcomes, route changes, focus sequences, element dimensions, validation state and cleanup results in platform JSON; generate a normalized CSV row per platform-item.
7. Aggregate 232 rows into a 58-row comparison matrix and 160-row screenshot index, then detect status inconsistencies, missing IDs, duplicate IDs and scenario errors.
8. Investigate every abnormal difference as one of three sources—SUT, browser/engine or harness—before retaining a product finding.

Across the four environments, execution-mode totals are 208 `LIVE_LOCAL_SUT`, 20 explicitly labelled `MOCKED_*` rows and four `EXPO_WEB_DESKTOP_BROWSER` rows. These labels prevent a deterministic UI-state test or desktop emulation from being mistaken for unavailable device evidence.

### 6.2 Platform inventory and eligibility

| Platform | Browser/engine | Device/host | Eligible? | Rows | Screenshots |
|---|---|---|---|---:|---:|
| `chrome-windows` | Google Chrome 150.0.7871.187 | Windows 10.0.26200; 1440×900 | Yes | 58 | 40 |
| `firefox-windows` | Firefox 153.0 | Windows 10.0.26200; 1440×900 | Yes | 58 | 40 |
| `webkit-windows` | Playwright WebKit 26.5 | Windows 10.0.26200; 1440×900 | No — not Safari | 58 | 40 |
| `android-chrome-emulation` | Chromium 151.0.7922.34 with Pixel 7 descriptor | Windows host; emulated viewport/touch/UA | No — not real/cloud Android | 58 | 40 |

The rubric requires at least three eligible real/cloud/physical platforms covering Chrome, Firefox and Safari or Android Chrome. Current eligibility is 2/3. WebKit Windows and device emulation are useful supplemental compatibility runs but cannot be renamed to satisfy the third-platform requirement.

### 6.3 Cross-platform metrics

| Metric | Value |
|---|---:|
| Executed environments | 4 |
| Eligible environments | 2 |
| Checklist IDs | 58 |
| Total platform-item rows | 232 |
| Evidence screenshots | 160 |
| Status-consistent IDs | 58/58 |
| Harness scenario errors in final JSON | 0 |

Every environment has the same high-level status distribution:

| Platform | Pass | Fail | Not Observable |
|---|---:|---:|---:|
| Chrome / Windows | 37 | 20 | 1 |
| Firefox / Windows | 37 | 20 | 1 |
| WebKit / Windows | 37 | 20 | 1 |
| Pixel 7 Chromium emulation | 37 | 20 | 1 |

The eligible Chrome + Firefox subtotal is 116 rows: 74 Pass, 40 Fail and two Not Observable. Status consistency does not prove Safari or Android compatibility, and it does not imply identical engine behavior. For example, keyboard sequences vary in detail while still failing the natural focus-order assertion.

### 6.4 Evidence capture and comparison method

One platform has 58 result rows but only 40 screenshots because a baseline or common state may prove multiple checklist assertions. The relationship is not implicit: every result row carries an Evidence ID and path, while the index stores the platform, route, capture time, covered IDs and file location. The validator verifies all 160 files, PNG signatures and the exact 40-per-platform distribution.

Comparison is performed by checklist ID:

- **Same status, same root cause:** group as a systemic product finding rather than four browser bugs.
- **Same status, different engine detail:** retain platform-specific Actual Results, such as focus sequence order, while keeping the shared failed assertion.
- **Different status:** investigate runner logs, DOM state, network/dialog evidence and source before classifying an engine-specific compatibility problem.
- **Not Observable:** retain the limitation when the environment cannot produce the required phenomenon, as with a native soft keyboard in desktop Expo Web.

No final ID has a cross-environment status inconsistency, and no browser-exclusive failure was established. That conclusion applies only to the four executed environments.

### 6.5 Cross-platform findings

The failures are systemic in the four executed environments rather than browser-exclusive:

1. Login password plaintext and incorrect login semantics — Critical, 4/4.
2. Category deletion without confirmation and deletion while referenced — High, 4/4.
3. Generic lockout feedback despite HTTP `401/401/403` — High, 4/4.
4. Duplicate email accepted with HTTP 200 — High, 4/4.
5. Missing Admin Login labels and native-alert feedback — Medium, 4/4.
6. Missing category empty-name prevention, empty/loading state and double-submit protection — Medium, 4/4.
7. Positive `tabIndex=1` moves Sign In before form fields — Medium, 4/4.
8. Expo Web uses Username/Sign In and renders a 39 px submit target below the 44 px threshold — Medium, 4/4 Expo Web runs.
9. Forgot-password performs full document navigation and loses the SPA marker — Low, 4/4.

### 6.6 Harness corrections and evidence integrity

An initial Chrome run with 55/58 rows was excluded after two ambiguous navigation locators and a remaining XSS-dialog listener produced three scenario errors. Mobile login was rerun on all environments after the route proxy was corrected to await `Content-Type`. Keyboard checks were rerun from a truly unfocused document after a preparatory click was found to alter the focus start. Only corrected final evidence is indexed.

Three unsupported inherited expectations were later reconciled under human review. The reconciliation script updates status and Actual Result interpretations while preserving the original screenshots and capture timestamps. Per-platform JSON contains the reconciliation note.

### 6.7 Retained Task 3 evidence and completion decision

The local execution, evidence matrix and reports are structurally complete. Strict completion remains `BLOCKED_THIRD_REQUIRED_PLATFORM`. One complete 58-item run is still required from Safari on macOS, real/cloud Android Chrome or Expo Go on a real phone. A real-phone run could also close the Task 1 soft-keyboard blocker.

The retained archive consists of the four platform JSON files, normalized result/evidence CSVs, run and derived summaries, the 58-row Markdown matrix, the 160-row evidence index, 160 screenshots, the runner/summarizer and the validator. Task-specific Main/Findings/AI reports, PDFs, local Git export and one-off reconciliation/export scripts are removed because the consolidated reports and final Git log replace them.

## 7. Combined defect and usability interpretation

Task 1 and Task 3 measure requirement/UI mismatches; a failed checklist assertion is not automatically an independent root-cause defect. `Bug_Report.md` therefore retains per-assertion IDs for traceability while grouping related root causes for prioritization. Task 2 additionally separates observed user difficulty from the underlying software fault: for example, phone validation is a software bug, while repeated unsupported attempts are a usability recovery issue.

The most important combined risks are credential exposure, data-integrity loss on category deletion, inconsistent authentication/localization semantics, weak validation and feedback, inaccessible form labelling/focus behavior, and insufficient asynchronous/error recovery states.

## 8. Validator and completion record

| Command/gate | Exit | Meaning |
|---|---:|---|
| Task 1 default validator | 0 | File/data/evidence structure and semantics pass. |
| Task 1 `-RequireComplete` | 2 | GUI demo and all GitHub mappings pass; native-phone soft-keyboard evidence remains. |
| Task 2 SUS analyzer | 0 | Exactly seven structurally valid P01–P07 response sets and exact SUS arithmetic. |
| Task 2 default validator | 0 | `COMPLETE_WITH_DISCLOSED_LIMITATIONS`. |
| Task 2 `-RequireCompleteEvidence` | 2 | Optional strict method audit retains the separate pilot, probe and source-provenance limitations. |
| Task 2 submission validator | 0 | Structural, exact T0–T11, SUS, finding separation, demo, privacy and core-deliverable checks pass. |
| HW03 package build | 0 | Created a portable 277-entry ZIP after verifying Markdown/PDF/XLSX/test-summary/skill/evidence entries, seven sessions, seven recording links, seven SUS sets and 160 Task 3 screenshots. |
| Task 3 default validator | 0 | Local 232-row/160-screenshot package passes. |
| Task 3 `-RequireComplete` | 2 | Only 2/3 eligible platforms. |

## 9. Evidence traceability

| Evidence area | Source |
|---|---|
| Task 1 execution rows | [`../task1-gui/results/Task1_Execution_Chrome.csv`](../task1-gui/results/Task1_Execution_Chrome.csv) |
| Task 1 evidence index | [`../task1-gui/results/Evidence_Index.csv`](../task1-gui/results/Evidence_Index.csv) |
| Task 1 Chrome screenshots | [`../task1-gui/evidence/executed-chrome/`](../task1-gui/evidence/executed-chrome/) |
| Task 2 session reports | [`../task2-usability/Sessions/`](../task2-usability/Sessions/) |
| Task 2 observation metrics | [`../task2-usability/Analysis/Observation_Metrics.csv`](../task2-usability/Analysis/Observation_Metrics.csv) |
| Task 2 raw SUS | [`../task2-usability/Analysis/SUS_Raw_Responses.csv`](../task2-usability/Analysis/SUS_Raw_Responses.csv) |
| Task 2 SUS scores | [`../task2-usability/Analysis/SUS_Scores.csv`](../task2-usability/Analysis/SUS_Scores.csv) |
| Task 2 funnel and SUS diagnostics | [`../task2-usability/Analysis/Flow_Funnel_and_SUS_Diagnostics.md`](../task2-usability/Analysis/Flow_Funnel_and_SUS_Diagnostics.md) |
| Task 2 recording links/integrity | [`../task2-usability/Stage_0_Drive_Inventory.md`](../task2-usability/Stage_0_Drive_Inventory.md) |
| Task 2 finding register | [`../task2-usability/Analysis/Findings_Register.csv`](../task2-usability/Analysis/Findings_Register.csv) |
| Task 2 technical reproduction | [`../task2-usability/evidence/github-issue-reproduction/`](../task2-usability/evidence/github-issue-reproduction/) |
| Task 3 result CSV | [`../task3-cross-platform/results/Task3_Cross_Platform_Results.csv`](../task3-cross-platform/results/Task3_Cross_Platform_Results.csv) |
| Task 3 matrix | [`../task3-cross-platform/Cross_Platform_Matrix.md`](../task3-cross-platform/Cross_Platform_Matrix.md) |
| Task 3 evidence index | [`../task3-cross-platform/Evidence_Index.md`](../task3-cross-platform/Evidence_Index.md) |
| Task 3 screenshots | [`../task3-cross-platform/evidence/`](../task3-cross-platform/evidence/) |

## 10. Submission cleanup and retained dependency boundary

Cleanup is evidence-aware. A file is retained if it is directly linked by a consolidated report, consumed by a validator, required to recompute a metric, required to reproduce a technical observation, or is the original screenshot/session record behind a claim.

| Area | Retained | Removed as obsolete/redundant |
|---|---|---|
| Task 1 | Final 58-row checklist in Markdown/XLSX, execution/evidence CSVs, 40 screenshots and consolidated validator. | Task-specific Main/Bug/Summary/AI reports and PDFs, old audits, AI draft output, duplicate issue drafts, local Git export and one-off generators. |
| Task 2 | Plan/instruments, P01–P07 sessions, private masked roster, seven-link recording manifest, missing/video-quality evidence, SUS/metrics/findings/funnel analysis, YouTube metadata, safe reproduction evidence and validators. | Raw participant MP4 copies, PII-bearing frames and duplicate/superseded D06 are excluded from the ZIP. |
| Task 3 | Platform JSON/CSV summaries, 58-row matrix, 160-row evidence index, 160 screenshots, runner, summarizer and validator. | Task-specific Main/Findings/AI reports and PDFs, duplicate platform narrative, local Git export and one-off reconciliation/export scripts. |
| Submission root | Markdown and PDF reports, authentic Git log, manifest, three evidence directories, test summary and two Agent Skills inside the correctly named ZIP. | Temporary HTML render files and raw participant MP4s. |

Historical commit subjects remain unchanged because rewriting authentic history to hide earlier packaging decisions would be inaccurate. The current build supersedes the earlier six-file/no-ZIP decision and follows the authoritative assignment PDF.

## 11. Final declaration

The consolidated report is human-reviewed and consistent with the current machine-readable evidence. Task 2 uses all seven official recordings and no additional session video is requested. The submission now includes required PDF counterparts, XLSX/test-summary evidence and both Agent Skills in the correctly named ZIP. It does not claim a guaranteed score: Task 1 native soft-keyboard behavior, Task 2 pilot/probe method evidence and Task 3 third-platform execution remain explicit, and none has been reconstructed.
