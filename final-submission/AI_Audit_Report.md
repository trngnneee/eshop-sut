# HW03 Consolidated AI Audit Report

**Student:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**System under test:** EShop  
**Audit date/timezone:** 2026-08-02 — Asia/Bangkok (UTC+7)  
**Audit state:** `HUMAN_REVIEWED — LOCALLY_VALIDATED_WITH_DISCLOSED_LIMITATIONS`

## 1. Declaration and audit boundary

**I use AI tools for the following tasks:** inspect the repository and rubric, structure the test packages, build and correct automation, calculate metrics, reconcile traceability, draft reports, check Git history and run validators. AI was not treated as the source of participant identity, consent, session behavior, SUS responses, quotes, probes, pilot results or human-review decisions.

The AI tool for every material interaction in §2 is **OpenAI Codex**. The Codex interface did not export exact UI times for several conversation messages. Known dates are retained, and unknown times are written as `TIME_NOT_EXPORTED`; no timestamp was invented. The “User direction” column preserves or concisely paraphrases the prompt, and the “AI use/output” column records the material output. This audit consolidates the retained Task 1, Task 2 and Task 3 audit records; it does not claim a verbatim transcript of every tool call.

## 2. Material interaction record

| Date/time | User direction or decision | AI use/output | Human/source control |
|---|---|---|---|
| 2026-07-29, `TIME_NOT_EXPORTED` | Begin Task 2 and use the repository usability-testing skill for registration → login → profile update → logout. | Read the assignment/skill, inspected the SUT, and prepared the seven-participant plan, instruments, session templates, SUS calculation and anti-fabrication validation. | The selected flow and fieldwork scope came from the user; AI did not recruit participants or run missing sessions. |
| 2026-07-29, `TIME_NOT_EXPORTED` | Analyze seven real recordings and explain which fields still required human input. | Inventoried sources, assigned P01–P07 aliases, decoded video/audio, created T0–T11 session coding, metrics, findings, evidence index and missing-data report. | Missing values remained `NOT_RECORDED`, `NOT_OBSERVABLE` or `NOT_CALCULABLE`. Source filenames containing contact data were treated as PII. |
| 2026-07-29, `TIME_NOT_EXPORTED` | Supply participant order and replace a duplicated D06 clip. | Recorded the user-provided order without face/voice inference; verified replacement metadata/hash, decoded the 52.525-second replacement, and excluded the superseded duplicate from all frequencies. | Participant mapping came from the user’s recruitment records, not AI inference. The old duplicate did not become an eighth participant. |
| 2026-07-29, `TIME_NOT_EXPORTED` | Confirm that P06 stopped at the password error and that three other short clips were complete sessions; confirm missing instruments. | Reclassified those recording ends as confirmed task ends, recalculated times/outcomes and retained absent SUS-at-that-stage, pilot, consent and probes as missing. | AI did not interpret absent instruments as zero or reconstruct responses. Later SUS data was included only when supplied as seven P01–P07 sets. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Audit the Task 2 package, enforce IDs P01–P07/T0–T11/SUS correctness, separate usability issues from bugs, and run validators without fabrication. | Reconciled session coding, metrics, findings and SUS arithmetic; separated software defects from observed recovery behavior; reported strict failures honestly. | No pilot, consent, quote, probe or missing participant datum was created. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Clean obsolete Task 1/2 artefacts and add the registration special-character defect. | Applied boundary/domain checks, reproduced the direct-API server bypass using synthetic data, distinguished frontend policy behavior from backend enforcement, and mapped the result to the existing issue #118 after duplicate search. | The technical bug has participant IDs `NONE` and frequency `N/A`; masked P04/P06 inputs were not used to fabricate attribution. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Keep only a YouTube demo link; confirm all human-review sections were reviewed. | Recorded the explicit review state, used the verified Task 2 YouTube URL, regenerated affected reports and reran validation. | Human review does not convert missing pilot/consent/probes/speech into evidence. No local MP4 is required under the user-confirmed rule. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Treat the Task 2 strict gate’s missing-evidence failure as the expected honest refusal. | Split local package closure from strict evidence completeness: default closure can pass with disclosures while the optional strict audit continues to fail. | The wording `COMPLETE_WITH_DISCLOSED_LIMITATIONS` means the package is internally closed, not that uncollected fieldwork occurred. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Execute Task 3 and capture complete evidence. | Built/corrected a 58-item multi-environment runner, produced 232 result rows and 160 screenshots, generated matrices/findings/reports and validated the package. | Only Chrome Windows and Firefox Windows qualify. WebKit Windows was not renamed Safari; Pixel emulation was not renamed real Android. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Repair all three tasks toward maximum rubric coverage; user confirmed human review. | Reconciled Task 1 to the corrected Chrome run, updated Task 2 closure and issue traceability, reconciled Task 3 expectations, and maintained real Git history. | External gaps stayed blocked: pending issue URLs, Task 1 GUI video, native soft keyboard and the third eligible platform. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Reduce the submission entry point to exactly six consolidated files for all three tasks. | Created one README, Main Report, Bug Report, AI Critique, AI Audit Report and authentic Git commit-log snapshot in `final-submission`. | Original task/evidence folders were preserved because the six reports link to their machine-readable evidence; no evidence was deleted merely to reach six files. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Confirm that no ZIP is needed; rewrite the Main Report with detailed work for all three tasks and remove unused material before submission. | Removed the ZIP/checksum and packaging script; expanded the Main Report with design, execution, metric, participant, reproduction and platform pipelines; rewired validators to the six consolidated files; deleted duplicate task-specific reports/PDFs/Git logs/drafts/render intermediates while retaining all depended-on evidence. | Deletion followed an explicit dependency map. Checklist/XLSX/CSV/JSON, 200 screenshots, P01–P07 sessions, SUS, instruments, safe reproductions and validators were retained; authentic historical commit subjects were not rewritten to hide the former ZIP step. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Supply `https://youtu.be/tMar6OyMG80` as the Task 1 GUI-skill demo. | Verified the public URL through YouTube oEmbed, which returned title `GUI-testing-skill demo`, author `Đặng Đăng Khoa` and provider `YouTube`; updated the consolidated README/Main/Audit and Task 1 validator. | The URL came directly from the user and was externally verified. No local MP4 was downloaded or claimed. |
| 2026-08-02, `TIME_NOT_EXPORTED` | Automatically update whatever remains missing across all three tasks. | Queried all 262 public GitHub issues and inspected ambiguous issue bodies; mapped three Admin Login rows to exact existing issues #45/#46; rejected cross-implementation near matches; checked `gh`, GitHub credentials, `adb`, Android emulator and cloud-device credential names. | Nine Task 1 issue publications, real-phone soft-keyboard evidence, missing Task 2 fieldwork records and the Task 3 third eligible platform remain unavailable. No issue URL, participant record or device run was fabricated. |
| 2026-08-02T23:28:57+07:00 | Recheck the authoritative rubric and make the work reach 100% if it is not already complete. | Read all nine pages of the assignment PDF; compared the 30/40/20/10 criteria and submission rules against retained evidence; searched authenticated Drive for overlooked pilot/consent/SUS/usability artefacts; tested GitHub branch/issue creation; added the mandatory README self-assessment and complete test-summary fields. | Drive contained no missing HW03 pilot/consent/probe artefact. GitHub writes returned HTTP 403. The evidence-backed self-assessment is 078/100; unsupported 100/100 was rejected. |
| 2026-08-02T23:55:03+07:00 | Grant GitHub issue write access or create the eight prepared issues, upload seven screenshots, run Expo Go/real Android, and supply real Task 2 pilot/consent/probe records if they exist. | Used user-authorized Git Credential Manager device authentication; pushed a seven-PNG evidence-only branch; created issues #291–#298 after exact-title duplicate checks; verified all image endpoints and issue bodies. Traced D01–D07 to their common Drive folder and inspected both that folder and its HW3 parent. Started Expo Metro on LAN and checked for connected devices. | GitHub publication completed without Task 2 data. The recording folder contained eight MP4 files only and the HW3 parent contained participant folders/allocation files only—no pilot, consent, probe or SUS artefact. Metro served `exp://192.168.50.111:8081`, but no physical/cloud device connected, so no device result or screenshot was claimed. |

## 3. Tools, purpose and data controls

| Tool/capability | Permitted purpose in this work | Control applied |
|---|---|---|
| OpenAI Codex | Planning, repository inspection, calculations, drafting, consistency checks and automation repair | Every material verdict remains traceable to a requirement, recorded observation or machine-readable result. |
| Repository usability-testing skill | Fieldwork structure, evidence taxonomy, metrics, severity and anti-fabrication rules | Skill templates did not authorize inventing pilot, consent, probes, quotes or participant data. |
| PowerShell and repository scripts | Run validators, analyze SUS, inspect files/hashes and generate deterministic package checks | Validator exit codes were reported as observed; strict failures were not suppressed. |
| Playwright, Node.js and browsers | Execute GUI scenarios, observe dialog/network/focus state, capture required overlays and generate result matrices | Synthetic test entities only; execution mode recorded; harness defects corrected before final classification. |
| FFmpeg/FFprobe and speech analysis | Inspect recording metadata, decode streams and assess usable audio | Hallucinated non-VAD transcript was rejected; no quote was retained because usable speech was absent. |
| Git/GitHub duplicate search and authenticated publication | Verify existing issue mappings, publish only new root causes and preserve authentic change history | All 262 pre-publication issues were searched; #45/#46 were reused for three exact Admin Login rows; no duplicate #118 was created. GitHub App writes first returned HTTP 403; user-authorized Git Credential Manager access then published the isolated evidence branch and issues #291–#298. |
| Google Drive connector | Check whether missing pilot, consent, probes or SUS collection artefacts had been overlooked | Read-only searches found the assignment and unrelated documents, but no missing HW03 fieldwork artefact; unrelated course files were not imported. |
| Document/report tooling | Produce readable Markdown/XLSX artefacts in the retained six-file/evidence structure | Consolidated claims were checked against CSV/JSON sources rather than inferred from document presence. |

## 4. Material AI errors and corrections

### 4.1 Task 1 corrections

| Problem | Why it was unsafe | Correction retained in the final package |
|---|---|---|
| Initial checklist treated source inspection and five static images as runtime execution. | Dynamic behavior such as loading, lockout and double submit was not proven. | Task 1 now uses 58 item-level Chrome execution rows with 40 indexed screenshots and an explicit execution mode per row. |
| Conflicting totals appeared as 36/22 and 40/18. | Artefacts were internally inconsistent. | One source of truth now reports 37 Pass, 20 Fail and 1 Blocked. |
| AI expanded FR-14 to full category CRUD and invented duplicate-name/automatic-trim expectations. | A test oracle cannot exceed the requirement without labelling the added heuristic. | Unsupported expectations were corrected before final classification and the same retained observations were reconciled. |
| Lockout expectation used the wrong threshold/duration. | It could misclassify the product against FR-02. | Expected result now uses three failed attempts and 30 seconds. |
| Desktop Expo Web was insufficient for soft-keyboard behavior. | Emulation cannot prove native keyboard resize/overlap. | `GUI-MOBILE-LOGIN-011` remains Blocked/Not Observable pending a real device. |

### 4.2 Task 2 corrections

| Problem | Why it was unsafe | Correction retained in the final package |
|---|---|---|
| A non-VAD speech attempt produced unrelated text from near-silent recordings. | Accepting it would fabricate participant quotes. | Transcript was rejected; quotes and probes remain `NOT_RECORDED`. |
| Short sessions were initially interpreted as cut files. | File duration alone cannot establish participant task end. | Outcomes/times were changed only after the user confirmed the recordings ended there. |
| The original D06 source duplicated another clip. | It could falsely count one person twice. | Replacement D06 was verified; the superseded duplicate is excluded; official IDs remain exactly P01–P07. |
| Completeness templates expected pilot/consent/probes even though they had not been collected. | Filling them for validator success would invent fieldwork. | Default closure is `COMPLETE_WITH_DISCLOSED_LIMITATIONS`; strict evidence validation remains exit 2. |
| P04/P06 registration errors could be conflated with the server special-character defect. | Their entered password values were masked and cannot establish the missing character class. | `UF-REG-PASSWORD-RECOVERY-01` retains only observable behavior; `BUG-REG-PASSWORD-POLICY-01` is technical-only, `NONE`/`N/A`, reproduced separately and mapped to #118. |

### 4.3 Task 3 harness corrections

| Problem | Detection | Resolution and evidence effect |
|---|---|---|
| Navigation locators matched both header and form links; an unused dialog listener survived. | Initial Chrome run produced 55/58 rows and three scenario errors. | Links were scoped and listener removed; the initial run was excluded and Chrome rerun to 58/58 with zero scenario errors. |
| Expo Web proxy passed an unresolved Promise as `Content-Type`. | Mobile successful login returned backend 500 and console behavior contradicted the intended live test. | Header value was awaited; seven mobile screenshots per environment were recaptured; no false Mobile Login product bug remained. |
| Keyboard scenario clicked the page before pressing Tab. | WebKit result differed while source still showed positive `tabIndex=1`. | Rerun started from an unfocused document and captured eight targets; final status consistently fails while preserving engine-specific sequences. |
| Three inherited unsupported expectations remained in the runner. | Human comparison against FR-02/FR-14 identified oracle drift. | Expectations and future runner were corrected; final per-environment totals changed from 34/23/1 to 37/20/1 without changing original capture timestamps. |

## 5. Data reconciliation controls

### Task 1

- Exactly 58 unique checklist IDs are represented.
- Final Chrome outcome is 37 Pass, 20 Fail and 1 Blocked.
- Evidence index contains 40 screenshots; execution modes distinguish live, controlled mocked state and Expo Web browser context.
- The Task 1 bug register has 20 failed assertions. All 20 rows have verified URLs across 18 unique issues; no Task 1 issue publication remains pending.

### Task 2

- Official participant set is exactly P01, P02, P03, P04, P05, P06 and P07, with no identifier outside that exact set.
- Session coding uses the exact T0–T11 schema.
- SUS contains exactly 70 integer responses, Q1–Q10 for each P01–P07. Odd-item contribution is response minus 1; even-item contribution is 5 minus response; sum is multiplied by 2.5.
- Validated SUS scores are 82.5, 75, 100, 65, 62.5, 65 and 87.5; mean 76.79, median 75, minimum 62.5 and maximum 100.
- Participant observations contain three software bugs and four usability issues. The technical password-policy bug is not added to participant frequency.
- 0/7 completed all SC1–SC5. Six calculable task times have median 80 seconds and range 50–136 seconds; missing P03 time prevents a claimed seven-person timing distribution.

### Task 3

- Exactly 58 IDs × 4 environments produce 232 result rows.
- Every environment has 37 Pass, 20 Fail and 1 Not Observable.
- Evidence archive contains 160 screenshots.
- Only 2/3 required platform categories are currently eligible; supplemental WebKit/Pixel-emulation evidence remains honestly labelled.

## 6. Validator record

These are the observed local outcomes retained at consolidation time. Exit 2 denotes a disclosed external/fieldwork blocker, not a validator crash.

| Gate | Exit | Audited interpretation |
|---|---:|---|
| Task 1 default validator | 0 | File, row, semantic and evidence structure pass. |
| Task 1 strict `-RequireComplete` | 2 | GUI demo and all GitHub mappings are verified; native-phone soft-keyboard evidence remains external. |
| Task 2 SUS analyzer | 0 | P01–P07 raw responses and score arithmetic pass. |
| Task 2 default validator | 0 | Package closes as `COMPLETE_WITH_DISCLOSED_LIMITATIONS`. |
| Task 2 strict `-RequireCompleteEvidence` | 2 | Pilot, consent, probes and some environment/timing provenance remain missing. |
| Task 2 submission validator | 0 | Structural, T0–T11, SUS, finding-type separation, six-file, demo-link and privacy checks pass while disclosed missing fieldwork evidence remains explicit. |
| Task 3 default validator | 0 | The local 232-row/160-screenshot evidence package passes. |
| Task 3 strict `-RequireComplete` | 2 | A third eligible Safari-or-real-Android category is absent. |

## 7. Anti-fabrication and privacy register

| Evidence category | Final handling |
|---|---|
| Pilot | Not collected; retained as missing. |
| Consent/screen-recording consent | No artefact available; retained as `NOT_RECORDED`. |
| Moderator probes and Card B | Not observable/recorded; no zero value substituted. |
| Participant speech/quotes | No usable speech; no quote synthesized from failed transcription. |
| Participant identity | Reports use P01–P07; private recruitment/contact sources are not copied into the six-file package. |
| SUS | Included only as the seven user-provided P01–P07 response sets; collection is not claimed visible in recordings. |
| Technical reproduction | Uses synthetic data and is excluded from participant frequencies. |
| GitHub | Only URLs returned and read back from GitHub are linked. Issues #291–#298 and seven PNGs are verified; no duplicate #118 or unpublished comment is claimed. |
| Video | Task 1 uses verified GUI-skill URL `https://youtu.be/tMar6OyMG80`; Task 2 uses verified usability URL `https://youtu.be/QAh6W9AJXiU`. Both are YouTube-link-only; no local MP4 is claimed necessary. |
| Platform/device | WebKit Windows is not called Safari; Pixel/Expo Web emulation is not called a physical Android/Expo Go run. |
| Evidence modes | `LIVE_LOCAL_SUT`, `MOCKED_*` and browser/emulation contexts remain distinguishable. |
| Git history | `git-commit-log.txt` is generated from real repository commits and full hashes, not a manually invented timeline. |
| Submission packaging | No ZIP or local MP4 is retained. The Task 2 deliverable uses the verified YouTube link and the six-file consolidated entry point. |

## 8. Human review and authorship

The student explicitly confirmed on 2026-08-02 that the human-review sections had been reviewed. That confirmation covers the final session interpretation, metrics, finding classification, reports, critiques, audits and evidence eligibility decisions. It does not waive rubric requirements or reclassify missing evidence as collected.

The student remains responsible for:

- confirming the participant mapping and task-end decisions supplied from real fieldwork context;
- protecting the private participant roster and reviewing any frames before public sharing;
- accepting the corrected test oracle and severity prioritization;
- maintaining or closing the published GitHub issues and deciding whether any future comments are appropriate;
- collecting a real-device soft-keyboard/third-platform run if required by grading;
- reviewing and submitting the final six-file package with its linked evidence archive.

The original task-specific audit drafts were reconciled into this document and removed from the submission archive to avoid three stale copies of the same disclosure. Provenance is retained through the real Git history, machine-readable results and evidence links in this consolidated audit.
