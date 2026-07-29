# Evidence Index

**Current status:** `READY_FOR_HUMAN_REVIEW — CONFIRMED_MISSING_DATA`
**Naming/privacy rule:** Chỉ dùng participant IDs P01–P07 và file aliases D01–D07. Không đưa tên thật, số điện thoại filename, email, address hoặc password vào filename/report.
**Drive mode:** Read-only

## Technical preflight — không tính là participant evidence

| Evidence ID | Type | Path | Integrity/notes |
|---|---|---|---|
| PRE-01 | Result JSON | `evidence/technical-preflight/result.json` | Researcher/automated check; không tính vào frequency P01–P07. |
| PRE-02 | Screenshots | `evidence/technical-preflight/` | Label technical preflight; không dùng thay participant evidence. |

## Pilot — loại khỏi bảy phiên chính thức

| Evidence ID | Type | Path/refusal reason | Status |
|---|---|---|---|
| PILOT-01 | Screen/audio/notes | Không có file pilot riêng; người dùng xác nhận pilot không được thu thập | **PILOT EVIDENCE MISSING — CONFIRMED_NOT_COLLECTED** |

## Official sessions

| Participant | Source | Screen evidence | Audio/quotes | Consent | SUS | Session report | Integrity/status |
|---|---|---|---|---|---|---|---|
| P01 | D01 | 00:00:00–00:01:52 | Audio stream silent; quotes NOT_RECORDED | NOT_RECORDED | Q1–Q10 NOT_RECORDED | `Sessions/Session_P01.md` | Full-decode PASS; complete-looking |
| P02 | D02 | 00:00:00–00:01:34 | Audio stream silent; quotes NOT_RECORDED | NOT_RECORDED | Q1–Q10 NOT_RECORDED | `Sessions/Session_P02.md` | Full-decode PASS; complete session confirmed; task ends on validation alert |
| P03 | D03 | 00:00:00–00:00:04 | Audio stream silent; quotes NOT_RECORDED | NOT_RECORDED | Q1–Q10 NOT_RECORDED | `Sessions/Session_P03.md` | Full-decode PASS with DTS warning; entire 4-second session confirmed |
| P04 | D04 | 00:00:00–00:02:16 | Không có usable speech; quotes NOT_RECORDED | NOT_RECORDED | Q1–Q10 NOT_RECORDED | `Sessions/Session_P04.md` | Full-decode PASS; complete-looking |
| P05 | D05 | 00:00:00–00:00:51 | Audio stream silent; quotes NOT_RECORDED | NOT_RECORDED | Q1–Q10 NOT_RECORDED | `Sessions/Session_P05.md` | Full-decode PASS; complete session confirmed; task ends at login |
| P06 | D06 | 00:00:00–00:00:53 | Low-level audio; VAD xác nhận 0 speech segments; quotes NOT_RECORDED | NOT_RECORDED | Q1–Q10 NOT_RECORDED | `Sessions/Session_P06.md` | Replacement full-decode PASS với DTS warnings; distinct hash; complete session confirmed; task ends on registration error |
| P07 | D07 | 00:00:00–00:01:06 | Audio stream silent; quotes NOT_RECORDED | NOT_RECORDED | Q1–Q10 NOT_RECORDED | `Sessions/Session_P07.md` | Full-decode PASS with DTS warning; complete-looking |

## Participant-evidenced bug traceability

| Bug ID | Participant evidence | Frequency | Redacted screenshot/clip | Draft | Published GitHub URL | Status |
|---|---|---:|---|---|---|---|
| BUG-PF-02 | D01 @ 00:00:53–00:01:49; D02 @ 00:00:57–00:01:34; D04 @ 00:01:43–00:02:09 | 3/7 | NOT_CREATED — originals contain PII; redaction required | `github-issues/DRAFT-BUG-USABILITY-01.md` | NOT_CREATED | Participant-evidenced; independent reproduction/search/review pending |
| BUG-AUTH-PLAINTEXT-01 | D01 @ 00:00:19–00:00:33; D02 @ 00:00:17–00:00:35; D04 @ 00:01:01–00:01:39; D05 @ 00:00:39–00:00:46; D07 @ 00:00:29–00:00:48 | 5/7 | NOT_CREATED — password/PII redaction required | `github-issues/DRAFT-BUG-AUTH-PLAINTEXT-01.md` | NOT_CREATED | Participant-evidenced; independent reproduction/search/review pending |

P06 không được cộng vào frequency của plaintext-password bug vì replacement recording không tới login.

Người dùng xác nhận SUS, probes, consent/eligibility supplement và pilot không được thu thập; các trường này giữ `NOT_RECORDED`/`PILOT EVIDENCE MISSING` và không còn là pending upload request.

## Integrity and evidence handling

- Bản video local chỉ dùng cho phân tích và nằm trong `analysis_assets/`, đã ignore khỏi Git; không phải deliverable để chia sẻ.
- Old D06 duplicate đã được supersede và loại khỏi official analysis nhưng vẫn giữ nguyên trên Drive. Replacement D06 có SHA-256 `544EDA05B62A17088F8967433C20AF72056A080179ECB38ACE90F18CA8E31E1A`, khác D01 `EA10D38B2EF8DA138F00989337C9476BEEA06BF9EC646D47957FC052A4B2248D`; bộ chính thức hiện có 7 unique recordings.
- Không có screenshot/clip participant nào được đưa vào evidence folder vì chưa redaction.
- Trước khi xuất evidence: che name, email, phone, address và toàn bộ plaintext password; giữ nguyên timestamp; không chỉnh quote vì không có genuine quote.
- Technical preflight không được dùng để tăng participant frequency hoặc thay thế participant evidence.
- Published GitHub issue URL giữ `NOT_CREATED`; chỉ có local drafts cho review, không issue nào đã được đăng.
