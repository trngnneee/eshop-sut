# Task 2 Flow Funnel and SUS Diagnostics

**Status:** `HUMAN_REVIEWED — DERIVED_FROM_OFFICIAL_P01–P07_DATA`  
**Scope:** Descriptive analysis of exactly seven official sessions; no population-level inference.  
**Sources:** `Sessions/Session_P01.md`–`Session_P07.md`, `Observation_Metrics.csv`, `SUS_Raw_Responses.csv`, and `Findings_Register.csv`.

## 1. Submission evidence coverage

This table separates deliverables that are present from method limitations that are disclosed elsewhere. A recording is counted once only; the superseded D06 file is excluded.

| Evidence component | Coverage | Audit location |
|---|---:|---|
| Official screen recordings | 7/7 | `Stage_0_Drive_Inventory.md`, links D01–D07 |
| Structured session reports | 7/7 | `Sessions/Session_P01.md`–`Session_P07.md` |
| Exact T0–T11 milestone schema | 7/7 | One row per code in every session report |
| Masked verifiable contacts | 7/7 | `Participant_Roster.md` — private grading artefact |
| Raw SUS response sets | 7/7 (70/70 items) | `SUS_Raw_Responses.csv` |
| Calculated SUS scores | 7/7 | `SUS_Scores.csv`, arithmetic revalidated by script |
| Severity-ranked findings | 7 findings | `Findings_Register.csv` — 3 software bugs and 4 usability issues |
| Pilot record | 0/1 | Disclosed method limitation; no source artefact exists |
| Post-session probe response sets | 0/7 | Instrument exists; responses are not recorded in available sources |
| Usable think-aloud speech | 0/7 | All official videos were checked; no genuine quote was manufactured |

## 2. Success-criterion funnel

`Pass` requires visible evidence by the confirmed task end. `Not reached` remains distinct from `Fail` in the session reports; the funnel below reports only evidenced passes over the fixed denominator of seven.

| Flow checkpoint | Participants with evidenced pass | Pass rate | Main loss point |
|---|---|---:|---|
| SC1 — account created | P01, P02, P04, P05, P07 | 5/7 (71.4%) | P06 remained blocked by password recovery; P03 performed no observable task action. |
| SC2 — authenticated | P01, P02, P04, P07 | 4/7 (57.1%) | P05 stopped at login; earlier SC1 losses carry forward. |
| SC3 — requested profile data saved | None | 0/7 (0.0%) | Leading-zero phone validation blocked P01/P02/P04; P07 left without submitting; others never reached the step. |
| SC4 — saved data persisted | None | 0/7 (0.0%) | No participant produced a requirement-conforming SC3 save to verify. |
| SC5 — behavioral logout | P01, P04, P07 | 3/7 (42.9%) | Counted as visible guest-state transition only; token deletion is not inferred. |
| Full SC1–SC5 completion | None | 0/7 (0.0%) | The profile-update checkpoint is the dominant system-level blocker. |

The most useful design conclusion is not merely “0/7 completed.” Five participants passed account creation and four passed login, but the funnel collapsed at profile update. Remediation should therefore prioritize the phone-format contract and recovery feedback before optimizing lower-severity navigation details.

## 3. Error concentration and recovery burden

Seventeen visible interaction-error events form an observed lower bound because P03 and some early session segments are not observable. Their distribution is:

| Stage | Visible error events | Share of 17-event lower bound | Evidence |
|---|---:|---:|---|
| Registration/password recovery | 5 | 29.4% | P04: 1; P06: 4 |
| Login/identifier recovery | 1 | 5.9% | P07: 1 |
| Profile/phone recovery | 11 | 64.7% | P01: 5; P02: 3; P04: 3 |

The recordings also show one wrong turn and two hesitations of at least five seconds. Intervention counts remain `NOT_OBSERVABLE`, so the analysis does not convert unavailable moderator audio into zeros. The concentration of 11/17 visible errors at profile update triangulates with both S1 findings: `BUG-PF-02` and `UF-PHONE-RECOVERY-01`.

## 4. SUS item-level diagnostics

The supplied SUS scale is internally complete. Positive odd items should trend high and negative even items should trend low. Mean item responses and normalized contributions are:

| Item | Mean response | Mean contribution (0–4) | Diagnostic reading |
|---|---:|---:|---|
| Q1 | 4.00 | 3.00 | Generally positive willingness to use. |
| Q2 | 2.14 | 2.86 | Some perceived complexity remains. |
| Q3 | 4.29 | 3.29 | Strong perceived ease-of-use signal. |
| Q4 | 1.71 | 3.29 | Low stated need for technical support. |
| Q5 | 4.14 | 3.14 | Functions perceived as reasonably integrated. |
| Q6 | 2.14 | 2.86 | Some perceived inconsistency remains. |
| Q7 | 4.29 | 3.29 | Strong learnability signal. |
| Q8 | 2.14 | 2.86 | Some perceived cumbersomeness remains. |
| Q9 | 4.00 | 3.00 | Generally positive confidence signal. |
| Q10 | 1.86 | 3.14 | Low perceived learning burden. |

Aggregate SUS is mean 76.79, median 75, minimum 62.5, maximum 100, sample standard deviation 13.97, and interquartile range 65–87.5. SUS is a 0–100 score, not a percentage.

The favorable perceived-usability scores and the failed strict task outcomes are not treated as contradictory data to “fix.” They measure different things: SUS captures the supplied post-use perception responses, while SC1–SC5 requires every predefined behavioral checkpoint. The gap is itself actionable: participants could perceive the interface as learnable while a narrow validation contract still blocks the required profile outcome.

## 5. Evidence-backed remediation order

1. Fix the leading-zero phone contract and field-linked recovery copy (`BUG-PF-02`, `UF-PHONE-RECOVERY-01`). Retest criterion: 5/5 users save a valid leading-zero phone on the first attempt.
2. Add a live password-policy checklist (`UF-REG-PASSWORD-RECOVERY-01`). Retest criterion: 5/5 users register with at most one password validation error.
3. Mask the login password by default (`BUG-AUTH-PLAINTEXT-01`). Retest across every supported browser.
4. Rename the login identifier to `Email` and use flow-specific Vietnamese copy (`UF-LOGIN-IDENTIFIER-01`). Retest criterion: 5/5 first-attempt identifier selections succeed.
5. Recheck autocomplete semantics to prevent the password-manager detour (`UF-PASSWORD-MANAGER-DETOUR-01`).

This order combines reach (frequency), impact (flow drop-off), severity, and whether a reproducible product defect is already linked to a canonical GitHub issue.
