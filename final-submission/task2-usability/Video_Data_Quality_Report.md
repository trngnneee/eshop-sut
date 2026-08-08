# Video Data Quality Report

**Verification status:** `COMPLETE_WITH_DISCLOSED_LIMITATIONS — HUMAN_REVIEWED — CONFIRMED_MISSING_DATA`
**Nguồn:** Google Drive sources do người dùng cung cấp; truy cập chỉ đọc
**Mapping:** D01–D07→P01–P07 đã được người dùng xác nhận; D06 sử dụng replacement source
**Chi tiết inventory:** `Stage_0_Drive_Inventory.md`

## Tóm tắt

| Hạng mục | Kết quả |
|---|---|
| Official source files | 7 MP4 sau khi thay D06 |
| Recording contents độc lập | 7; old duplicate D06 đã bị loại khỏi analysis |
| Screen stream | 7/7 |
| Audio stream | 7/7 |
| Usable speech | 0/7 |
| Full-decode | 7/7 thành công |
| Complete recordings | 7/7 — D02/D03/D05/D06 completeness confirmed externally |
| Cut/upload-incomplete | NONE after user confirmation |
| Superseded artefact | Old D06 = D01 byte-for-byte; không còn dùng làm P06 evidence |
| Timestamp warnings | D03, D07, replacement D06 có non-monotonic DTS |
| Pilot | **PILOT EVIDENCE MISSING — confirmed not collected** |

## Chất lượng theo phiên

| Participant | File | Duration | Video | Audio/speech | Completeness | Ảnh hưởng phân tích |
|---|---|---:|---|---|---|---|
| P01 | D01 | 111,851 s | H.264 1920×1032; decode PASS | AAC; digital silence | Complete-looking | Visual milestones/metrics dùng được; quote, intervention, SUS, probes không có. |
| P02 | D02 | 93,931 s | H.264 2558×1350; decode PASS | AAC; digital silence | Complete; task ends on validation alert | T11 = 00:01:34; captured-task time 94 s; persistence/logout NOT_REACHED. |
| P03 | D03 | 4,369 s | H.264 1376×736; decode PASS với DTS warning | AAC; digital silence | Complete but only 4.369 s | T11 = 00:00:04; T0 và phần lớn metric vẫn NOT_OBSERVABLE. |
| P04 | D04 | 135,659 s | H.264 2556×1470; decode PASS | AAC; chỉ ~0,2 s non-silent, không có usable speech | Complete-looking | Visual flow dùng được; không có speech/SUS/probes/persistence. |
| P05 | D05 | 50,740 s | HEVC portrait 1242×2688; decode PASS | AAC; digital silence | Complete; task ends at login | T11 = 00:00:51; task time 50 s; login submit/result và downstream milestones NOT_REACHED. |
| P06 | D06 replacement | 52,525 s | HEVC portrait 1126×2436; decode PASS với DTS warnings | AAC; low-level signal, VAD 0 speech segments | Complete; task ends at register error | T11 = 00:00:53; task time 52 s; bốn registration errors; T3–T10 NOT_REACHED/NOT_OBSERVABLE. |
| P07 | D07 | 66,197 s | H.264 1920×1008; decode PASS với DTS warning | AAC; digital silence | Complete-looking | Visual flow tới logout dùng được; không có profile update, speech/SUS/probes. |

## Audio và transcript

- D01, D02, D03, D05 và D07 là digital silence trong toàn file.
- D04 chỉ có khoảng 0,2 giây non-silent signal, quá ngắn để xác nhận speech.
- Replacement D06 có mean volume khoảng -74,3 dB và max khoảng -39,3 dB. Faster-Whisper với VAD trả về 0 speech segments. Khi bỏ VAD, model sinh các canned phrases không liên quan; toàn bộ bị đánh dấu hallucination và loại bỏ.
- Kết quả: genuine quotes, exact moderator words, think-aloud reminders, neutral prompts, task-directed interventions, Card B, SUS và probes đều không thể suy ra từ audio.

## Completeness và timing

- P01, P02, P04, P05, P06 và P07 có T0/T11 đủ để tính captured task time; P02/P03/P05/P06 task-end timestamps dựa thêm trên user confirmation.
- P02, P05 và P06 kết thúc sớm giữa flow nhưng không phải file cut; recording end được dùng làm T11 sau user confirmation.
- P03 là entire session nhưng chỉ dài 4,369 giây và không có observable T0; task time và phần lớn metrics giữ NOT_OBSERVABLE.
- Replacement P06 kết thúc ở weak-password error sau bốn registration submits; T11 = 00:00:53 và total task time = 52 giây.
- DTS warnings ở P03/P06/P07 được giữ như limitation; milestones được làm tròn tới HH:MM:SS và các transitions liệt kê trong session reports đã được human-review ngày 2026-08-02.

## Privacy và redaction

| File/participant | Khoảng bắt buộc rà soát | Lý do |
|---|---|---|
| D01/P01 | 00:00:19–00:00:33 và register/profile | Plaintext password; name/email/phone/address |
| D02/P02 | 00:00:17–00:00:35 và register/profile | Plaintext password; name/email/phone/address |
| D03/P03 | Register segment | PII nếu dùng ảnh; không có login password evidence |
| D04/P04 | 00:01:01–00:01:39 và register/profile | Plaintext password; name/email/phone/address |
| D05/P05 | 00:00:39–00:00:46 và register/login | Plaintext password; name/email |
| D06/P06 | 00:00:02–00:00:53 register | Name/email; password được masked nhưng frame vẫn cần privacy review |
| D07/P07 | 00:00:29–00:00:48 và register/profile | Plaintext password; name/email/phone/address |

Không chép giá trị password, số điện thoại, email, địa chỉ hoặc tên thật vào báo cáo. Chưa xuất screenshot/clip participant evidence vì chưa có bản redacted.

## Integrity

- Replacement D06 tải đủ 43.102.934 bytes, full-decode PASS.
- Replacement D06 SHA-256: `544EDA05B62A17088F8967433C20AF72056A080179ECB38ACE90F18CA8E31E1A`.
- D01 SHA-256: `EA10D38B2EF8DA138F00989337C9476BEEA06BF9EC646D47957FC052A4B2248D`; hai source khác nhau.
- Old D06 duplicate vẫn có thể tồn tại trên Drive nhưng bị supersede và không tham gia official analysis.
- Không phát hiện official source file không phát được hoặc decode failure.
