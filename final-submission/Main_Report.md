# HW03 Main Report — GUI, Usability and Cross-Platform Testing

**Student:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**System under test:** EShop  
**Report date/timezone:** 2026-08-02 — Asia/Bangkok (UTC+7)  
**Review state:** `HUMAN_REVIEWED`  
**Overall evidence state:** `LOCALLY_VALIDATED_WITH_DISCLOSED_EXTERNAL_LIMITATIONS`

## 1. Executive summary

This report consolidates the three HW03 tasks into one auditable narrative while retaining the original evidence folders. Task 1 provides a 58-item GUI checklist and an item-level Chrome execution. Task 2 analyzes the registration → login → profile update → logout flow for exactly seven participant IDs, P01–P07, including T0–T11 session coding and seven user-provided SUS response sets. Task 3 re-executes the same 58 GUI IDs across four browser environments and produces 232 platform-item results with 160 screenshots.

| Task | Core dataset | Result | Completion boundary |
|---|---|---|---|
| Task 1 — GUI checklist | 58 unique items; 40 Chrome screenshots | 37 Pass / 20 Fail / 1 Blocked | Twelve failed rows still need verified GitHub mappings; a GUI-skill YouTube URL and native soft-keyboard evidence are unavailable. |
| Task 2 — usability | 7 sessions; P01–P07; exact T0–T11 coding; 70 SUS responses | 0/7 completed all SC1–SC5; calculable task-time median 80 s; SUS mean 76.79 | Pilot, consent, probes, usable speech and some environment/timing evidence were not collected and remain explicitly missing. |
| Task 3 — cross-platform | 58 IDs × 4 environments = 232 rows; 160 screenshots | 37 Pass / 20 Fail / 1 Not Observable per environment | Chrome and Firefox are eligible; WebKit Windows is not Safari and Pixel emulation is not real Android, leaving 2/3 eligible platforms. |

Default/local validators return exit 0 for all three packages. Strict evidence validators return exit 2 only for the disclosed external/fieldwork gaps. No pilot, consent, quote, probe, participant value, platform, issue URL, device run or video URL was synthesized to turn a strict failure into a pass.

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

### 4.1 Coverage

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

### 4.2 Result metrics

| Metric | Value |
|---|---:|
| Total unique checklist IDs | 58 |
| Pass | 37 |
| Fail | 20 |
| Blocked | 1 |
| Unique Chrome screenshots | 40 |
| Fail rows mapped to verified existing issues | 8 |
| Fail rows pending verified GitHub URLs | 12 |

The prior 36/22 checklist, conflicting 40/18 summary and five packed screenshots are superseded. The current machine-readable source is [`../task1-gui/results/Task1_Execution_Chrome.csv`](../task1-gui/results/Task1_Execution_Chrome.csv).

### 4.3 Human-review corrections

Three material expectation problems were corrected before final classification:

1. `GUI-WEB-LOGIN-010` now checks the written FR-02 boundary: three failed attempts and a 30-second lockout requirement.
2. `GUI-WEB-LOGIN-013` no longer invents automatic whitespace trimming; safe rejection with generic feedback satisfies the corrected expectation.
3. `GUI-ADMIN-CATEGORY-005` checks real navigation to the Category tab instead of treating absent Edit Category functionality as an FR-14 defect.
4. `GUI-ADMIN-CATEGORY-011` observes deterministic Add/View behavior for a repeated name; FR-14 does not state that category names must be unique.

The last three observations were reclassified to Pass from the retained runtime evidence. Screenshots and capture timestamps were not changed.

### 4.4 Main GUI risks

The highest-risk Task 1 observations are plaintext password display, incorrect login semantics, generic lockout feedback, duplicate email acceptance, unsafe in-use category deletion, absent confirmation/loading/empty/double-submit states, positive tabindex, missing admin labels, inconsistent mobile localization and a 39 px mobile submit target below the 44 px threshold. Detailed severity and issue traceability are consolidated in `Bug_Report.md`.

### 4.5 Task 1 completion decision

The Task 1 package is structurally ready. Strict completion remains blocked by:

- 12 failed assertion rows that still require verified duplicate/new GitHub URLs;
- a real public YouTube URL demonstrating the GUI-testing skill end to end; and
- a real Expo Go/physical/cloud phone run for `GUI-MOBILE-LOGIN-011` soft-keyboard behavior.

## 5. Task 2 — Usability evaluation

### 5.1 Participant and session integrity

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

### 5.2 Observed metrics

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

### 5.3 Raw SUS and calculation

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

SUS is a 0–100 scale, not a percentage. These values are descriptive for the supplied sample; no population-level or statistical-significance claim is made. The apparent contrast between a relatively positive SUS mean and 0/7 full task completion is retained rather than “resolved” by changing either dataset. It may reflect separate collection context, expectations or the difference between perceived usability and the strict SC1–SC5 completion definition.

### 5.4 Severity-ranked usability findings

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

### 5.5 GitHub traceability for Task 2 bugs

- `BUG-PF-02` reuses canonical [issue #55](https://github.com/trngnneee/eshop-sut/issues/55); fresh synthetic evidence was published in the recorded issue comment.
- `BUG-AUTH-PLAINTEXT-01` reuses canonical [issue #37](https://github.com/trngnneee/eshop-sut/issues/37); fresh synthetic evidence was published in the recorded issue comment.
- `BUG-REG-PASSWORD-POLICY-01` reuses canonical [issue #118](https://github.com/trngnneee/eshop-sut/issues/118). Duplicate search prevented a new issue. Its reviewed reproduction remains local; no new #118 comment is claimed.

### 5.6 Task 2 missing-data declaration

The following were not collected or cannot be verified from the supplied evidence:

- pilot session and protocol refinement;
- consent supplement or recorded consent evidence;
- post-session clarity, recovery, speed, trust and requested-change probes;
- usable participant speech and genuine quotes;
- exact moderator wording, think-aloud reminders and task-directed intervention counts;
- some session environment, device and full timing fields;
- complete seven-person distributions for metrics where P03 or another session is not observable.

These omissions are the reason strict evidence validation returns exit 2. The default package-closure validator returns exit 0 because the missing fields are disclosed instead of populated with invented data.

### 5.7 Task 2 demo and private package

The verified public Task 2 skill-demo link is [https://youtu.be/QAh6W9AJXiU](https://youtu.be/QAh6W9AJXiU). Submission mode is YouTube-link-only; no local MP4 is required. A private ZIP exists at `submission/23127207_Task2_Usability_Submission.zip`, excludes raw/local recordings and was checked after creation. The participant roster must remain in the private grading channel.

## 6. Task 3 — Cross-platform execution

### 6.1 Platform inventory and eligibility

| Platform | Browser/engine | Device/host | Eligible? | Rows | Screenshots |
|---|---|---|---|---:|---:|
| `chrome-windows` | Google Chrome 150.0.7871.187 | Windows 10.0.26200; 1440×900 | Yes | 58 | 40 |
| `firefox-windows` | Firefox 153.0 | Windows 10.0.26200; 1440×900 | Yes | 58 | 40 |
| `webkit-windows` | Playwright WebKit 26.5 | Windows 10.0.26200; 1440×900 | No — not Safari | 58 | 40 |
| `android-chrome-emulation` | Chromium 151.0.7922.34 with Pixel 7 descriptor | Windows host; emulated viewport/touch/UA | No — not real/cloud Android | 58 | 40 |

The rubric requires at least three eligible real/cloud/physical platforms covering Chrome, Firefox and Safari or Android Chrome. Current eligibility is 2/3. WebKit Windows and device emulation are useful supplemental compatibility runs but cannot be renamed to satisfy the third-platform requirement.

### 6.2 Cross-platform metrics

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

### 6.3 Cross-platform findings

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

### 6.4 Harness corrections and evidence integrity

An initial Chrome run with 55/58 rows was excluded after two ambiguous navigation locators and a remaining XSS-dialog listener produced three scenario errors. Mobile login was rerun on all environments after the route proxy was corrected to await `Content-Type`. Keyboard checks were rerun from a truly unfocused document after a preparatory click was found to alter the focus start. Only corrected final evidence is indexed.

Three unsupported inherited expectations were later reconciled under human review. The reconciliation script updates status and Actual Result interpretations while preserving the original screenshots and capture timestamps. Per-platform JSON contains the reconciliation note.

### 6.5 Task 3 completion decision

The local execution, evidence matrix and reports are structurally complete. Strict completion remains `BLOCKED_THIRD_REQUIRED_PLATFORM`. One complete 58-item run is still required from Safari on macOS, real/cloud Android Chrome or Expo Go on a real phone. A real-phone run could also close the Task 1 soft-keyboard blocker.

## 7. Combined defect and usability interpretation

Task 1 and Task 3 measure requirement/UI mismatches; a failed checklist assertion is not automatically an independent root-cause defect. `Bug_Report.md` therefore retains per-assertion IDs for traceability while grouping related root causes for prioritization. Task 2 additionally separates observed user difficulty from the underlying software fault: for example, phone validation is a software bug, while repeated unsupported attempts are a usability recovery issue.

The most important combined risks are credential exposure, data-integrity loss on category deletion, inconsistent authentication/localization semantics, weak validation and feedback, inaccessible form labelling/focus behavior, and insufficient asynchronous/error recovery states.

## 8. Validator and completion record

| Command/gate | Exit | Meaning |
|---|---:|---|
| Task 1 default validator | 0 | File/data/evidence structure and semantics pass. |
| Task 1 `-RequireComplete` | 2 | Pending GitHub mappings, GUI demo URL and native phone evidence. |
| Task 2 SUS analyzer | 0 | Exactly seven structurally valid P01–P07 response sets and exact SUS arithmetic. |
| Task 2 default validator | 0 | `COMPLETE_WITH_DISCLOSED_LIMITATIONS`. |
| Task 2 `-RequireCompleteEvidence` | 2 | Missing pilot, consent, probes, environment/timing provenance. |
| Task 2 submission validator | 0 | Required package artefacts, exact T0–T11, SUS, bug/usability separation, PDFs, demo and privacy checks pass. |
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
| Task 2 finding register | [`../task2-usability/Analysis/Findings_Register.csv`](../task2-usability/Analysis/Findings_Register.csv) |
| Task 2 technical reproduction | [`../task2-usability/evidence/github-issue-reproduction/`](../task2-usability/evidence/github-issue-reproduction/) |
| Task 3 result CSV | [`../task3-cross-platform/results/Task3_Cross_Platform_Results.csv`](../task3-cross-platform/results/Task3_Cross_Platform_Results.csv) |
| Task 3 matrix | [`../task3-cross-platform/Cross_Platform_Matrix.md`](../task3-cross-platform/Cross_Platform_Matrix.md) |
| Task 3 evidence index | [`../task3-cross-platform/Evidence_Index.md`](../task3-cross-platform/Evidence_Index.md) |
| Task 3 screenshots | [`../task3-cross-platform/evidence/`](../task3-cross-platform/evidence/) |

## 10. Final declaration

The consolidated report is human-reviewed and consistent with the current machine-readable evidence. It does not claim a guaranteed rubric score or full external completion. Task 1 GitHub publication and GUI demo, Task 1 native soft-keyboard behavior, Task 2 missing fieldwork records, and Task 3 third-platform execution remain explicit. Local package validation is complete; unavailable evidence has not been reconstructed.
