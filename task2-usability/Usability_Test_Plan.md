# Usability Test Plan — EShop Account Onboarding and Profile Flow

## 1. Study metadata

| Field | Value |
| :--- | :--- |
| Assignment | HW03 — Task 2: Usability Evaluation |
| Student | Đặng Đăng Khoa |
| Student ID | 23127207 |
| SUT | EShop Web Frontend |
| Study type | Small-sample moderated usability evaluation |
| Flow | Đăng ký → Đăng nhập → Chỉnh sửa thông tin cá nhân → Đăng xuất |
| Official sample | Exactly 7 real participants, P01–P07 |
| Pilot | One separate participant, not included in P01–P07 |
| Scale | System Usability Scale (SUS), 10 items |
| Current status | `READY_FOR_FIELDWORK` |

## 2. Scope and requirements

The flow covers:

- FR-01 — Account registration.
- FR-02 — Login.
- FR-04 — Personal profile management.
- FR-23 — Navigation and the expected “Đăng xuất” action.
- IA-01 — General interface standards.
- IA-02 — Forms.
- IA-03 — Navigation.
- IA-04 — Feedback and state.

The study evaluates the current SUT. The moderator must not silently repair, redesign, or explain the interface during a session.

## 3. Research objectives

1. Determine whether first-time users understand the registration form, including the password rule, without moderator guidance.
2. Identify navigation bottlenecks between successful registration, login, and discovery of personal-profile editing.
3. Assess whether the profile form's labels, validation, feedback, and saved state let users update their name, phone, and shipping address confidently.
4. Measure how efficiently participants complete the whole flow and where errors, wrong turns, or hesitations of at least five seconds occur.
5. Assess whether the logout action is discoverable and whether participants trust that their session and profile data are handled safely.

## 4. Research questions and measures

| Research question | Evidence / measure |
| :--- | :--- |
| Can users create an account without assistance? | Outcome, registration errors, password-rule rereads, interventions |
| Is the transition to login clear? | Wrong turns, hesitation, verbalised expectation, time to first successful login |
| Can users find profile editing? | Navigation path, misclicks, hesitation ≥5 s, intervention |
| Can users update all requested profile fields? | Completion, validation errors, recovery behaviour, persistence check |
| Can users end the session safely? | Logout discoverability, route/state after logout, trust probe |
| What is perceived usability? | Raw Q1–Q10 responses and SUS score per participant |

All results are descriptive. The seven-person sample is not used to claim statistical significance or population-wide prevalence.

## 5. Target participant profile

### Inclusion criteria

- At least 18 years old.
- Uses a Vietnamese-language e-commerce website or app at least once per month.
- Is not currently enrolled in this HW03 class.
- Has not tested or developed this EShop SUT before.
- Can read Vietnamese and use a web browser independently.
- Freely consents to participation and required screen recording.

### Preferred characteristics

- Non-IT and non-software-testing background.
- A mix of shopping frequency, age, and device familiarity.

### Exclusion criteria

- Current HW03 student.
- Member who built or previously tested this SUT.
- Unable or unwilling to consent to screen recording.
- Has already participated in the pilot or another official session in this study.

The pilot participant is recruited separately and is not reused in P01–P07.

## 6. Task scenario

Read the scenario exactly as written:

> Bạn vừa biết đến EShop và muốn chuẩn bị một tài khoản để sử dụng cho lần mua sắm sắp tới. Hãy thiết lập tài khoản thử nghiệm bằng thông tin trên thẻ được cung cấp, bảo đảm hồ sơ có tên hiển thị mới, số điện thoại và địa chỉ giao hàng. Khi bạn tin rằng thông tin đã được lưu, hãy kết thúc phiên sử dụng tài khoản theo cách bạn cho là an toàn. Hãy nói thành tiếng những gì bạn đang nghĩ trong khi thực hiện.

This scenario gives a goal, not click-by-click instructions. Do not name the Registration, Login, Profile, Update, or Logout controls after the task begins.

## 7. Success and outcome definitions

The researcher verifies the following after the participant says they are finished:

1. A new EShop test account was created with the assigned session email.
2. The participant successfully authenticated with that account.
3. The profile contains the assigned updated display name, test phone, and test shipping address.
4. The saved profile can be observed again after a neutral persistence check.
5. The browser no longer holds the EShop authentication token after logout.

Classify one outcome:

- `COMPLETED_INDEPENDENTLY`: all five criteria met with no task-directed help.
- `COMPLETED_WITH_ASSISTANCE`: criteria met after at least one task-directed intervention or fallback data card.
- `FAILED_OR_ABANDONED`: one or more criteria not met when the participant stops or the session limit is reached.

A neutral think-aloud reminder is recorded but is not task-directed assistance.

## 8. Session design

Each official session is individual and moderated.

| Segment | Planned duration |
| :--- | :--- |
| Welcome, eligibility confirmation, consent | 3–4 minutes |
| Scenario and moderated think-aloud task | 8–12 minutes |
| SUS Q1–Q10 | 3 minutes |
| Four required probes and follow-ups | 5–7 minutes |
| Total | Approximately 20–25 minutes |

Use the same SUT build and baseline browser state for all seven sessions. Record deviations.

## 9. Moderator intervention policy

1. Observe neutrally and do not explain controls.
2. If the participant is silent for about 20 seconds, say only: “Bạn đang nghĩ gì lúc này?”
3. If the participant asks what to click, reply once: “Bạn hãy làm theo cách bạn cho là hợp lý.”
4. A participant is considered completely stuck when they explicitly request help, repeat the same failed action three times, or make no progress for 120 seconds.
5. At that threshold, record the timestamp and the participant's last action before giving the smallest possible intervention.
6. If a valid Vietnamese test phone beginning with `0` blocks profile saving, show **Fallback Card B** from `Instruments/Task_Data_Card.md`. Record this as task-directed assistance and classify the outcome accordingly.
7. Record every intervention verbatim in the session file.

## 10. Data captured per session

- Date/time, location, device, OS, browser/version, viewport.
- Participation, screen-recording, and audio-consent choices.
- Start/end time and task duration.
- Outcome and success criteria.
- Wrong turns, errors, hesitations ≥5 seconds, and interventions.
- Timestamped observation notes and only genuine verbatim quotes.
- Raw SUS responses Q1–Q10 before any score calculation.
- Responses to Clarity, Error Recovery, Speed, and Trust probes.
- Evidence paths or an explicit refusal/not-applicable reason.

## 11. SUS scoring

- Odd-numbered item contribution: `response - 1`.
- Even-numbered item contribution: `5 - response`.
- Participant SUS score: sum of ten contributions × `2.5`.
- Report mean, median, minimum, and maximum for exactly seven official participants.
- Keep raw responses and contribution calculations in the submission.
- Do not describe the result as statistically significant.

## 12. Qualitative analysis

1. Review timestamped notes and recordings.
2. Create an atomic observation for each friction point.
3. Separate software failures from usability issues.
4. Group similar observations without erasing minority or contradictory experiences.
5. Link every finding to participant IDs, timestamps, and evidence paths.
6. Assign frequency and impact before severity.
7. Rank:
   - S1 — prevents task completion.
   - S2 — requires help or causes serious confusion.
   - S3 — causes meaningful delay or hesitation.
   - S4 — minor friction or visual complaint.
8. Give each finding a recommendation and a measurable retest criterion.

Technical-preflight or pilot-only findings remain `PROVISIONAL` until official participant evidence exists.

## 13. Bug handling

A software bug is a reproducible deviation from the specification; a usability issue is an observed barrier that may occur even when the implementation matches the specification. For every confirmed software bug:

1. Reproduce it independently after the session.
2. Add it to `Usability_Bug_Report.md`.
3. Save a screenshot or short clip with the participant's identity excluded.
4. Search existing Task 1 issues to avoid duplicates.
5. Create or update a GitHub Issue with steps, actual/expected result, environment, severity, and evidence.
6. Add the GitHub URL to the bug report, finding, summary, and evidence index.

## 14. Ethics, privacy, and retention

- Test the product, not the participant.
- Participation is voluntary and can stop at any time without penalty.
- Do not collect a participant's real password, personal shipping address, or personal phone in the SUT.
- Keep unmasked contact details outside this repository; commit only the version with the middle four characters/digits masked.
- Screen recording is required for an official session; audio is optional and separately consented.
- Exclude notifications, unrelated tabs, and personal accounts from the recording.
- Use participant IDs in filenames and analysis.

## 15. Stop conditions

Stop a session if the participant withdraws, personal data is accidentally exposed, the SUT cannot run, or the moderator can no longer remain neutral. Preserve only evidence for which consent remains valid. A stopped or ineligible session does not silently count toward the required seven.

## 16. Readiness checklist

- [ ] Flow uniqueness confirmed with group.
- [x] One end-to-end flow selected.
- [x] Objectives and measures defined.
- [x] Goal-oriented scenario written.
- [x] SUS and four probes prepared.
- [x] Consent and moderator protocol prepared.
- [x] P01–P07 templates prepared as `UNVERIFIED`.
- [ ] Separate pilot completed and refinement recorded.
- [ ] Seven eligible real participants recruited.
- [ ] Seven official sessions completed.
- [ ] SUS aggregate generated.
- [ ] Findings and GitHub issues completed.
- [ ] Completion validator passes.
