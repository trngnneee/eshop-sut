# Evidence Index

**Current status:** `COMPLETE_WITH_DISCLOSED_LIMITATIONS — HUMAN_REVIEWED — CONFIRMED_MISSING_DATA`
**Naming/privacy rule:** Chỉ dùng participant IDs P01–P07 và file aliases D01–D07. Không đưa tên thật, số điện thoại filename, email, address hoặc password vào filename/report.
**Drive mode:** Read-only

## Independent technical reproduction — không tính là participant evidence

| Evidence ID | Type | Path | Integrity/notes |
|---|---|---|---|
| TECH-01 | Result JSON | `evidence/github-issue-reproduction/result.json` | Automated/synthetic checks; không tính vào frequency P01–P07. |
| TECH-02 | Safe screenshots | `evidence/github-issue-reproduction/BUG-*-safe-reproduction.png` | Chỉ synthetic data; không dùng thay participant evidence. |

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
| BUG-PF-02 | D01 @ 00:00:53–00:01:49; D02 @ 00:00:57–00:01:34; D04 @ 00:01:43–00:02:09 | 3/7 | `evidence/github-issue-reproduction/BUG-PF-02-safe-reproduction.png` — synthetic data | `github-issues/DRAFT-BUG-USABILITY-01.md` | https://github.com/trngnneee/eshop-sut/issues/55#issuecomment-5149476574 | Participant-evidenced; independently reproduced; evidence comment published |
| BUG-AUTH-PLAINTEXT-01 | D01 @ 00:00:19–00:00:33; D02 @ 00:00:17–00:00:35; D04 @ 00:01:01–00:01:39; D05 @ 00:00:39–00:00:46; D07 @ 00:00:29–00:00:48 | 5/7 | `evidence/github-issue-reproduction/BUG-AUTH-PLAINTEXT-01-safe-reproduction.png` — synthetic data | `github-issues/DRAFT-BUG-AUTH-PLAINTEXT-01.md` | https://github.com/trngnneee/eshop-sut/issues/37#issuecomment-5149476796 | Participant-evidenced; independently reproduced; evidence comment published |

P06 không được cộng vào frequency của plaintext-password bug vì replacement recording không tới login.

## Supplemental technical-only bug traceability

| Bug ID | Technical evidence | Participant IDs/frequency | Safe screenshot | Draft | Canonical GitHub URL | Status |
|---|---|---|---|---|---|---|
| BUG-REG-PASSWORD-POLICY-01 | Isolated API run 2026-08-02: missing-special password registration 200; subsequent login 200; frontend EP/BVA control matrix 13/13 PASS | NONE / N/A | `evidence/github-issue-reproduction/BUG-REG-PASSWORD-POLICY-01-safe-reproduction.png`; SHA-256 `5c1e6d718f39f20dff7c5263c505a3789d96f6ddf196fae6167e8ce4f85d0537` | `github-issues/DRAFT-BUG-REG-PASSWORD-POLICY-01.md` | https://github.com/trngnneee/eshop-sut/issues/118 | Independently reproduced; duplicate reused; fresh Task 2 evidence comment NOT_PUBLISHED |

SUS Q1–Q10 không xuất hiện trong recording P01–P07. Ngày 2026-07-31, người dùng cung cấp riêng 7 bộ responses; ngày 2026-08-02, người dùng xác nhận các bộ này dùng participant ID P01–P07 và đã human-review provenance/coding. Arithmetic đã được kiểm tra. Probes, consent supplement và pilot vẫn giữ `NOT_RECORDED`/`PILOT EVIDENCE MISSING`.

## Integrity and evidence handling

- Bản video local chỉ dùng cho phân tích và nằm trong `analysis_assets/`, đã ignore khỏi Git; không phải deliverable để chia sẻ.
- Old D06 duplicate đã được supersede và loại khỏi official analysis nhưng vẫn giữ nguyên trên Drive. Replacement D06 có SHA-256 `544EDA05B62A17088F8967433C20AF72056A080179ECB38ACE90F18CA8E31E1A`, khác D01 `EA10D38B2EF8DA138F00989337C9476BEEA06BF9EC646D47957FC052A4B2248D`; bộ chính thức hiện có 7 unique recordings.
- Không có screenshot/clip participant nào được đưa vào evidence folder; ba ảnh fresh reproduction chỉ dùng synthetic data.
- Trước khi xuất evidence: che name, email, phone, address và toàn bộ plaintext password; giữ nguyên timestamp; không chỉnh quote vì không có genuine quote.
- Fresh technical reproduction không được dùng để tăng participant frequency hoặc thay thế participant evidence.
- Duplicate search hoàn tất: BUG-PF-02 dùng existing issue #55; BUG-AUTH-PLAINTEXT-01 dùng existing issue #37; BUG-REG-PASSWORD-POLICY-01 dùng existing issue #118. Safe-reproduction evidence comments cho #55/#37 được publish ngày 2026-08-01; fresh #118 Task 2 comment chưa publish.
- Publication screenshots: `evidence/github-issue-reproduction/GITHUB-ISSUE-55-comment-5149476574.png` (SHA-256 `f17c297a6c83bac41792b51893b7c3230eb682060e8200f2af83c70b1fa5c9a1`) và `evidence/github-issue-reproduction/GITHUB-ISSUE-37-comment-5149476796.png` (SHA-256 `ef7291d311a1a67dcde814955f3ef894b9c0a71242c145ea4204bdc3b2ce75a0`).
