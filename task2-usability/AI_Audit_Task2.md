# AI Audit Report — Task 2

**Declaration:** I use AI tools for the following tasks.
**Audit recorded at:** 2026-07-29 22:32:07 +07:00
**Last updated:** 2026-08-02 following explicit student review confirmation
**Timezone:** Asia/Bangkok (UTC+7)
**Final audit status:** `HUMAN_REVIEWED`

The exact UI timestamps of several chat messages were not exported by the Codex interface. Their date is known to be 2026-07-29; the audit uses `TIME_NOT_EXPORTED` rather than inventing a time.

## Interaction log

### Interaction 1 — Create the fieldwork package

| Field | Value |
|---|---|
| AI tool | OpenAI Codex, GPT-5-based coding agent |
| Date/time | 2026-07-29 14:12:29 +07:00 |
| User prompt | `thực hiện task 2 đi` |
| AI output/use | Inspected the HW03 specification and identified Task 2 as a seven-participant moderated usability evaluation. Prepared a non-fabricated fieldwork package. |
| Human/source control | No participant evidence was created in this interaction. |

### Interaction 2 — Select the usability flow and skill

| Field | Value |
|---|---|
| AI tool | OpenAI Codex, GPT-5-based coding agent |
| Date/time | 2026-07-29 14:12:29 +07:00 |
| User prompt | `sử dụng usability-testing-skill để thực hiện task 2, flown đăng ký, đăng nhập, chỉnh sửa thông tin cá nhân và sau đó đăng xuất` |
| AI output/use | Applied the repository usability skill, selected the account flow, inspected the SUT, prepared plan/instruments/session templates, and added SUS and anti-fabrication validation scripts. |
| Human/source control | Technical preflight remained separate from participant evidence. |

### Interaction 3 — Detailed Drive-analysis request

| Field | Value |
|---|---|
| AI tool | OpenAI Codex with Google Drive read-only connector, FFmpeg/FFprobe and local analysis tools |
| Date/time | 2026-07-29, `TIME_NOT_EXPORTED` |
| User prompt | Attached detailed Vietnamese instruction beginning: `Bạn là một Senior Usability Researcher và Software Test Analyst...`, requesting read-only analysis of seven real EShop usability recordings. |
| AI output/use | Inventoried Drive sources, applied P01–P07 aliases, decoded recordings, created timestamped session reports, metrics, findings, bug drafts, evidence index, video-quality report, missing-data report and final summary. |
| Human/source control | Names/contact values were not inferred from video. Quotes/SUS/probes were not generated. Silent or unreliable ASR output was rejected. |

### Interaction 4 — Identify the files requiring input

| Field | Value |
|---|---|
| AI tool | OpenAI Codex |
| Date/time | 2026-07-29, `TIME_NOT_EXPORTED` |
| User prompt | `là bây giờ tui cần điền những file nào` |
| AI output/use | Identified genuinely missing fields and distinguished source data from report fields. |
| Human/source control | Missing values remained `NOT_RECORDED`, `NOT_OBSERVABLE` or `NOT_CALCULABLE`. |

### Interaction 5 — Explain Drive filenames

| Field | Value |
|---|---|
| AI tool | OpenAI Codex |
| Date/time | 2026-07-29, `TIME_NOT_EXPORTED` |
| User prompt | `số điện thoại là tên file trên drive đó` |
| AI output/use | Treated source filenames as contact PII and used only D01–D07 aliases in analytical reports. |
| Human/source control | Full phone numbers were not copied into reports. The submission roster later masks exactly four middle digits. |

### Interaction 6 — Confirm participant order

| Field | Value |
|---|---|
| AI tool | OpenAI Codex |
| Date/time | 2026-07-29, `TIME_NOT_EXPORTED` |
| User prompt | `Thịnh, Bách, Phương, Hiển, Ngọc, Nguyên, Trâm này là tên từ D01 đến D07` |
| AI output/use | Recorded the user-provided D01–D07 order without using face/voice inference. |
| Human/source control | Analytical session reports continued to use P01–P07 only. |

### Interaction 7 — Replace duplicate D06

| Field | Value |
|---|---|
| AI tool | OpenAI Codex with Google Drive read-only connector, FFmpeg/FFprobe and Faster-Whisper VAD |
| Date/time | 2026-07-29, `TIME_NOT_EXPORTED` |
| User prompt | Drive file link followed by: `thay thế clip bị trùng bằng clip này với participant tên hân` |
| AI output/use | Replaced the official P06 evidence source in the analysis, verified a distinct SHA-256, decoded the 52.525-second recording, coded four weak-password errors and three repeated actions, and excluded the superseded duplicate from frequencies. |
| Human/source control | Drive files were not modified or deleted. Non-VAD canned ASR hallucinations were discarded; no quote was created. |

### Interaction 8 — Confirm session endings and missing instruments

| Field | Value |
|---|---|
| AI tool | OpenAI Codex |
| Date/time | 2026-07-29, `TIME_NOT_EXPORTED` |
| User prompt | `1. PA6 đúng là dừng ở khúc lỗi password` / `2. 3 clip đó tới đó là hết rồi` / `3. không có` / `4. không có` / `5. không có` |
| AI output/use | Treated D02, D03, D05 and D06 recording ends as confirmed task ends; recalculated task times and aggregate metrics. Recorded SUS, consent supplement, probes and pilot as confirmed not collected. |
| Human/source control | The AI did not convert absent instruments into zero scores or completed responses. |

### Interaction 9 — Task 2 completion status

| Field | Value |
|---|---|
| AI tool | OpenAI Codex |
| Date/time | 2026-07-29, `TIME_NOT_EXPORTED` |
| User prompt | `vậy task 2 đã làm xong chưa` |
| AI output/use | Explained that analysis deliverables were ready for human review but the study could not honestly claim complete SUS/pilot/consent data. |
| Human/source control | Completion limitations were disclosed instead of hidden. |

### Interaction 10 — Prepare the submission package

| Field | Value |
|---|---|
| AI tool | OpenAI Codex with local shell, Google Drive metadata and document-rendering tools |
| Date/time | 2026-07-29 22:32:07 +07:00 (audit logging time) |
| User prompt | `hãy làm hết để có thể nộp bài được tasks 2 đi` |
| AI output/use | Audited the official PDF rubric, prepared the masked participant-verification roster, consolidated report, PDF artefacts, submission checklist, real commit-log export and demo-video materials while preserving anti-fabrication constraints. |
| Human/source control | Public GitHub issue publication, participant consent proof, human critique approval and a public demo-video upload are not claimed without real external action. |

### Interaction 11 — Clean obsolete artefacts and add the registration password-policy bug

| Field | Value |
|---|---|
| AI tool | OpenAI Codex with local shell, repository domain/boundary testing skill, Playwright/API checks and public GitHub Search API |
| Date/time | 2026-08-02, `TIME_NOT_EXPORTED` |
| User prompt | `xóa những gì không cần sử dụng nữa trong task 2 và task 1. Ngoài ra task 2 update thêm bug khi đăng ký mật khẩu thì ký tự đặc biệt đang bị sai nữa` |
| AI output/use | Classified mandatory versus generated/obsolete files; removed the stale Task 1 deliverable generator and superseded Task 2 preflight report/runner; tested FR-01 EP/BVA controls; reproduced the backend API bypass with synthetic data; separated the technical software bug from P04/P06 usability recovery; linked canonical issue #118 instead of creating a duplicate; updated findings, reports, test case and traceability. |
| Human/source control | No participant input, quote, consent, pilot, probe or missing session data was created. The API test used an isolated synthetic account. The fresh #118 evidence comment was not published or claimed as published. Safety controls refused bulk deletion of referenced evidence/support directories, so those remaining cleanup candidates were disclosed rather than deleted indirectly. |

### Interaction 12 — Confirm YouTube-only demo and complete human review

| Field | Value |
|---|---|
| AI tool | OpenAI Codex with local validators and document-rendering tools |
| Date/time | 2026-08-02, `TIME_NOT_EXPORTED` |
| User prompt | `video thì chỉ cần link ytb, những chỗ cần human review thì tui đã review xong rồi` |
| AI output/use | Recorded the student's explicit human-review confirmation across sessions, roster, metrics, findings, reports, critique and audit; changed structural validation to require only the verified YouTube link; regenerated the affected PDFs and reran validators. |
| Human/source control | `HUMAN_REVIEWED` represents the student's explicit confirmation in this chat. It does not convert missing pilot, consent, probes, speech or unobserved states into collected evidence. No local MP4 is required under the student's confirmed submission rule. |

### Interaction 13 — Close the package through acknowledged missing evidence

| Field | Value |
|---|---|
| AI tool | OpenAI Codex with local validation and report-consistency checks |
| Date/time | 2026-08-02, `TIME_NOT_EXPORTED` |
| User prompt | `Task 2 completion gate FAIL — 54 issues Pilot/consent/probes/device-time/status COMPLETED không có thật; đây là expected honest refusal để phần này complete luôn` |
| AI output/use | Split package closure from strict fieldwork-evidence completeness. The default validator now succeeds as `COMPLETE_WITH_DISCLOSED_LIMITATIONS` only when confirmed missing items remain disclosed; optional `-RequireCompleteEvidence` still returns `INCOMPLETE_EVIDENCE`. Updated the plan, reports, checklist and validator messages to use the same closure semantics. |
| Human/source control | The student's instruction accepts honest refusal as final closure. Pilot, consent, probes, exact environment/time values and unavailable participant observations remain missing; SUS retains `COMPLETED_USER_PROVIDED` provenance. No source value was changed to `COMPLETED` and no absent evidence was created. |

## Tools and purposes

| Tool | Purpose | Data handling |
|---|---|---|
| OpenAI Codex | Planning, repository inspection, consistency checks, report drafting and calculations | Participant evidence referenced by P IDs; no passwords reproduced |
| Google Drive connector | Read-only folder/file metadata and source access | No rename, delete, move, permission change or share operation |
| FFmpeg/FFprobe | Media metadata, decode validation, frame extraction and audio-level checks | Raw media kept in ignored local analysis storage |
| Faster-Whisper with VAD | Check for usable speech | Zero reliable P06 segments; hallucinated non-VAD text discarded |
| PowerShell/Git | CSV checks, report validation, PDF/package preparation and real history export | No fake commits or backdating |

## Human review confirmation and retained limitations

| Decision | Evidence/status |
|---|---|
| Confirm participant consent evidence | Human-reviewed; remains `NOT_RECORDED` and is not claimed |
| Confirm screen-recording consent | Human-reviewed; remains `NOT_RECORDED` because no consent artefact exists |
| Approve the 200–300 word AI critique in the student's own voice | `HUMAN_REVIEWED` — student confirmation 2026-08-02 |
| Review participant-evidence timestamps and redaction requirements | `HUMAN_REVIEWED` — student confirmation 2026-08-02; participant frames still require redaction before public sharing |
| Confirm no participant evidence was generated by AI | Confirmed by the student in chat on 2026-08-02; missing evidence was not reconstructed |
| Publish or link GitHub Issues | Canonical #55/#37/#118 are linked; #55/#37 evidence comments are published; reviewed disposition for fresh #118 evidence is local-only unless a later publication action is requested |
| Verify/retain the demo video | Public YouTube metadata was verified through oEmbed on 2026-08-02; the student confirmed that only the YouTube link is required and no repository-local MP4 is needed |

## Student declaration block

I confirm that I reviewed this audit, that the participant names/contact sources came from my real recruitment records, and that no participant, response, quote, SUS score, consent record or observation was fabricated by AI.

- Student name: Đặng Đăng Khoa
- Student ID: 23127207
- Review date: 2026-08-02
- Signature/confirmation: Confirmed by the student via chat on 2026-08-02
- Final audit status: `HUMAN_REVIEWED — COMPLETE_WITH_DISCLOSED_LIMITATIONS`
