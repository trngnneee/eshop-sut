# AI Audit Report — Task 2

**Declaration:** I use AI tools for the following tasks.
**Audit recorded at:** 2026-07-29 22:32:07 +07:00
**Timezone:** Asia/Bangkok (UTC+7)
**Final audit status:** `READY_FOR_STUDENT_REVIEW`

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
| AI output/use | Treated D02, D03, D05 and D06 recording ends as confirmed task ends; recalculated task times and aggregate metrics. Recorded SUS, consent/eligibility supplement, probes and pilot as confirmed not collected. |
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
| Human/source control | Public GitHub issue publication, participant eligibility proof, human critique approval and a public demo-video upload are not claimed without real external action. |

## Tools and purposes

| Tool | Purpose | Data handling |
|---|---|---|
| OpenAI Codex | Planning, repository inspection, consistency checks, report drafting and calculations | Participant evidence referenced by P IDs; no passwords reproduced |
| Google Drive connector | Read-only folder/file metadata and source access | No rename, delete, move, permission change or share operation |
| FFmpeg/FFprobe | Media metadata, decode validation, frame extraction and audio-level checks | Raw media kept in ignored local analysis storage |
| Faster-Whisper with VAD | Check for usable speech | Zero reliable P06 segments; hallucinated non-VAD text discarded |
| PowerShell/Git | CSV checks, report validation, PDF/package preparation and real history export | No fake commits or backdating |

## Human review and decisions still required

| Decision | Evidence/status |
|---|---|
| Confirm all seven participants were outside the current HW03 class | `NOT_RECORDED`; must not be claimed without participant verification |
| Confirm screen-recording consent | `NOT_RECORDED`; no consent artefact exists |
| Approve the 200–300 word AI critique in the student's own voice | `STUDENT_REVIEW_REQUIRED` |
| Review participant-evidence timestamps and redactions before publication | `STUDENT_REVIEW_REQUIRED` |
| Confirm no participant evidence was generated by AI | Evidence provenance in session reports supports this; student must sign the declaration |
| Publish or link GitHub Issues | Drafts exist; publication requires student review and external GitHub action |
| Upload the demo video and verify access | Local demo package can be prepared; public URL requires student upload |

## Student declaration block

I confirm that I reviewed this audit, that the participant names/contact sources came from my real recruitment records, and that no participant, response, quote, SUS score, consent record or observation was fabricated by AI.

- Student name: Đặng Đăng Khoa
- Student ID: 23127207
- Review date: ____________________
- Signature/confirmation: ____________________
- Final audit status after signature: `HUMAN_REVIEWED`
