# Usability Findings

**Current status:** `COMPLETE_WITH_DISCLOSED_LIMITATIONS — HUMAN_REVIEWED — CONFIRMED_MISSING_DATA`
**Official session mappings:** 7/7 resolved
**Independent official recordings:** 7; old duplicate D06 đã được supersede và loại khỏi official analysis
**Rule applied:** Frequency chỉ tính distinct participant evidence; replacement D06 là nguồn chính thức cho P06.

## Severity model

| Severity | Operational definition |
|---|---|
| S1 | Ngăn task completion; không có independent recovery hợp specification. |
| S2 | Cần moderator help hoặc gây serious confusion/error/privacy exposure. |
| S3 | Gây delay, repeated action hoặc hesitation đáng kể nhưng participant tự recovery. |
| S4 | Friction nhỏ, visual/copy issue hoặc detour ngắn. |

## Severity-ranked summary

| Rank | Finding | Type | Participant frequency | Severity |
|---:|---|---|---:|---:|
| 1 | `BUG-PF-02` — phone validation trái FR-04 | SOFTWARE_BUG | 3/7 | S1 |
| 2 | `UF-PHONE-RECOVERY-01` — phone recovery không dẫn tới format hợp requirement | USABILITY_ISSUE | 3/7 | S1 |
| 3 | `BUG-AUTH-PLAINTEXT-01` — login password plaintext | SOFTWARE_BUG | 5/7 | S2 |
| 4 | `BUG-REG-PASSWORD-POLICY-01` — API bypass special-character policy | SOFTWARE_BUG, technical-only | N/A | S2 provisional |
| 5 | `UF-REG-PASSWORD-RECOVERY-01` — repeated registration recovery | USABILITY_ISSUE | 2/7 | S2 |
| 6 | `UF-LOGIN-IDENTIFIER-01` — `Username` không rõ là email | USABILITY_ISSUE | 1/7 | S3 |
| 7 | `UF-PASSWORD-MANAGER-DETOUR-01` | USABILITY_ISSUE | 1/7 | S4 |

Xếp hạng theo severity trước, sau đó xét task impact, privacy/security exposure và độ mạnh evidence. Finding technical-only không được dùng để tăng participant frequency.

## F-01 / BUG-PF-02 — Phone validation không tuân FR-04

- Finding ID: `BUG-PF-02`.
- Type: `SOFTWARE_BUG`.
- Title: Valid phone 10–11 chữ số bắt đầu bằng 0 bị từ chối; non-leading-zero format có thể được chấp nhận.
- Participant IDs: P01, P02, P04.
- Frequency: 3/7 distinct official participants.
- Evidence:
  - P01/D01 @ 00:00:53–00:01:49 — năm profile submits; các leading-zero phone hợp hình thức FR-04 vẫn bị phone error.
  - P02/D02 @ 00:00:57–00:01:34 — first update có phone 10 chữ số bắt đầu bằng 0 nhưng bị từ chối; ba submits thất bại trước confirmed task end.
  - P04/D04 @ 00:01:43–00:02:09 — leading-zero 10/11-digit attempts bị từ chối; một non-leading-zero value nhận success alert.
- Genuine quote: NOT_RECORDED — không có usable speech.
- Impact: P01 và P02 không hoàn thành SC3 tại task end; P04 chỉ nhận success bằng phone trái FR-04 và vẫn thiếu name/address, nên SC3 fail.
- Recovery behaviour: P01 thử tổng cộng 5 submits nhưng không thành công; P02 thử 3 submits trước task end; P04 thử 4 formats và chỉ nhận success sau khi bỏ số 0 đầu.
- Severity: `S1` — lỗi chặn profile task với input hợp requirement; không có reasonable spec-compliant recovery được quan sát.
- Recommendation: Đồng bộ frontend/backend validation với FR-04; chấp nhận đúng 10–11 digits bắt đầu bằng `0`, từ chối non-leading-zero values, và sửa error copy để phản ánh chính xác rule.
- Measurable retest criterion: Trong automated + 5-user retest, cả 10-digit và 11-digit leading-zero test numbers đều save/persist; non-leading-zero fallback bị từ chối; 5/5 users hoàn thành first valid update không workaround/moderator assistance.
- Related draft: `github-issues/DRAFT-BUG-USABILITY-01.md`; canonical issue #55 và evidence comment đã publish.

## F-02 / BUG-AUTH-PLAINTEXT-01 — Login password hiển thị plaintext

- Finding ID: `BUG-AUTH-PLAINTEXT-01`.
- Type: `SOFTWARE_BUG`.
- Title: Login password được render như text thường thay vì masked password.
- Participant IDs: P01, P02, P04, P05, P07.
- Frequency: 5/7; P03 và replacement P06 không tới login.
- Evidence:
  - P01/D01 @ 00:00:19–00:00:33.
  - P02/D02 @ 00:00:17–00:00:35.
  - P04/D04 @ 00:01:01–00:01:39.
  - P05/D05 @ 00:00:39–00:00:46.
  - P07/D07 @ 00:00:29–00:00:48.
- Genuine quote: NOT_RECORDED; không kết luận participant lo ngại vì audio không có speech.
- Impact: Credential bị lộ cho người đứng cạnh và trong screen recording. Không quan sát task-blocking impact, nhưng privacy/security exposure là trực tiếp.
- Recovery behaviour: Không có recovery vì UI không che password; participants tiếp tục flow. PII/password values tuyệt đối không được chép lại.
- Severity: `S2` provisional — serious credential exposure; severity cần owner/security review, không dựa trên verbal concern.
- Recommendation: Dùng password input masked mặc định, optional reveal control rõ ràng và reversible; kiểm tra autocomplete/password-manager semantics.
- Measurable retest criterion: Password masked by default ở 100% supported-browser checks; reveal chỉ xảy ra sau explicit action, remasks đúng; screenshot/recording mặc định không lộ characters.
- Related draft: `github-issues/DRAFT-BUG-AUTH-PLAINTEXT-01.md`; canonical issue #37 và evidence comment đã publish.

## F-03 / UF-PHONE-RECOVERY-01 — Error recovery ở profile tạo repeated attempts nhưng không dẫn tới input hợp lệ

- Finding ID: `UF-PHONE-RECOVERY-01`.
- Type: `USABILITY_ISSUE`.
- Title: Feedback phone không giúp participant recovery theo requirement.
- Participant IDs: P01, P02, P04.
- Frequency: 3/7.
- Evidence: Cùng participant timestamps với BUG-PF-02; P01 có 4 repeated submits, P02 có 2, P04 có 3 repeated profile submits.
- Genuine quote: NOT_RECORDED.
- Impact: Repeated actions và task failure; success feedback ở P04 chỉ xuất hiện với format trái specification, làm giảm độ tin cậy của guidance.
- Recovery behaviour: Participants tự thay đổi độ dài/leading digit; không có evidence moderator workaround vì audio silent.
- Severity: `S1` — recovery UI không cung cấp con đường hợp requirement để hoàn thành SC3.
- Recommendation: Sau khi sửa validator, hiển thị accepted example đã mask/generic, field-level message chỉ ra “bắt đầu bằng 0, gồm 10–11 chữ số”, giữ các field khác và focus vào field lỗi.
- Measurable retest criterion: 5/5 retest users sửa phone thành valid leading-zero format sau tối đa một error, không repeated submit và không assistance.
- Related bug: `BUG-PF-02`; draft `github-issues/DRAFT-BUG-USABILITY-01.md`.

## F-04 / UF-REG-PASSWORD-RECOVERY-01 — Password-policy recovery tạo repeated registration attempts

- Finding ID: `UF-REG-PASSWORD-RECOVERY-01`.
- Type: `USABILITY_ISSUE`.
- Title: Password-policy feedback không hỗ trợ recovery ổn định trong registration.
- Participant IDs: P04, P06.
- Frequency: 2/7.
- Evidence:
  - P04/D04 @ 00:00:22–00:01:01 — nhận một weak-password error rồi tự sửa và registration thành công; recovery mất khoảng 39 giây từ first submit đến success.
  - P06/D06 @ 00:00:22–00:00:53 — bốn submits đều nhận cùng weak-password error; ba repeated actions; không có registration success tại confirmed task end.
- Genuine quote: NOT_RECORDED — không có usable speech.
- Impact: P04 bị delay trước khi recovery; P06 không hoàn thành SC1 tại task end.
- Recovery behaviour: P04 tự recovery sau một lỗi; P06 liên tục xóa/sửa masked password nhưng cùng lỗi lặp lại qua bốn submits.
- Severity: `S2` — repeated error và task failure ở P06 là nghiêm trọng; P04 cho thấy recovery vẫn có thể xảy ra. Masked input không cho phép xác định validator có sai hay participant nhập chưa đúng policy.
- Recommendation: Cần hiển thị checklist policy động trong lúc nhập, đánh dấu từng tiêu chí đã/chưa đạt và cung cấp state-specific feedback; tiếp tục mask password và không hiển thị giá trị.
- Measurable retest criterion: 5/5 retest users tạo password hợp policy và đăng ký thành công với tối đa một validation error, không cần moderator assistance.
- Related bug/GitHub issue: Session evidence không chứng minh một validator defect cụ thể. Supplemental direct-API test tìm thấy `BUG-REG-PASSWORD-POLICY-01`/issue #118, nhưng finding usability này vẫn độc lập và chỉ dùng P04/P06 behavior.

## F-05 / UF-LOGIN-IDENTIFIER-01 — `Username` không truyền đạt rằng cần full email

- Finding ID: `UF-LOGIN-IDENTIFIER-01`.
- Type: `USABILITY_ISSUE`.
- Title: Login label/copy dẫn tới lựa chọn sai identifier ở một participant.
- Participant IDs: P07.
- Frequency: 1/7.
- Evidence: P07/D07 @ 00:00:34–00:00:48 — first submit dùng full name, nhận login failure; khoảng 5 giây hesitation; sau đó sửa qua local part tới full email và login thành công.
- Genuine quote: NOT_RECORDED.
- Impact: Một failed login, một repeated submit và khoảng 5 giây hesitation.
- Recovery behaviour: Participant tự recovery bằng full email, không có intervention evidence.
- Severity: `S3` — delay/error đáng kể nhưng independent recovery thành công.
- Recommendation: Đổi heading thành `Đăng nhập`, label thành `Email`, button thành tiếng Việt; error message xác định identifier format mà không tiết lộ account existence.
- Measurable retest criterion: 5/5 retest users nhập full email và login thành công ở first attempt; không identifier-related hesitation ≥5 giây.
- Related bug/GitHub issue: Không tạo bug draft; cần design/copy review.
- Contradictory evidence: P01, P02 và P04 login thành công mà không có observable identifier wrong attempt; P05 nhập email nhưng task kết thúc trước login submit. Không gọi finding này “phổ biến”.

## F-06 / UF-PASSWORD-MANAGER-DETOUR-01 — Browser password-manager detour

- Finding ID: `UF-PASSWORD-MANAGER-DETOUR-01`.
- Type: `USABILITY_ISSUE`.
- Title: Password-manager workflow làm gián đoạn login ngắn ở P04.
- Participant IDs: P04.
- Frequency: 1/7.
- Evidence: P04/D04 @ 00:01:22–00:01:24 — Microsoft Edge Password Manager mở rồi participant quay lại SUT.
- Genuine quote: NOT_RECORDED.
- Impact: Wrong turn khoảng 2 giây; participant tự recovery.
- Recovery behaviour: Quay lại login không cần observable assistance.
- Severity: `S4`.
- Recommendation: Review form autocomplete attributes và supported-browser password-manager integration; không coi system prompt ở P05 là cùng issue vì trigger/intent NOT_OBSERVABLE.
- Measurable retest criterion: 5/5 Edge retests hoàn thành login mà không rời SUT ngoài explicit participant intent.
- Related bug/GitHub issue: Không tạo; isolated observation.

## F-07 / BUG-REG-PASSWORD-POLICY-01 — Backend không enforce ký tự đặc biệt của FR-01

- Finding ID: `BUG-REG-PASSWORD-POLICY-01`.
- Type: `SOFTWARE_BUG` — supplemental technical reproduction.
- Title: Direct registration API chấp nhận password không có ký tự nào trong allowed-special set và account đó login được.
- Participant IDs: `NONE`.
- Frequency: `N/A`; không cộng vào sample P01–P07.
- Evidence: Isolated API run ngày 2026-08-02; registration `200`, login `200`; `evidence/github-issue-reproduction/result.json` và `BUG-REG-PASSWORD-POLICY-01-safe-reproduction.png`.
- Frontend controls: 13/13 EP/BVA regex cases đúng FR-01, gồm length 7/8/9, đủ bảy allowed characters và unsupported-only `#`. Defect nằm ở server-side enforcement, không phải frontend allowed set.
- Genuine quote: `NOT_APPLICABLE`; đây không phải participant observation.
- Impact: Client validation có thể bị bypass; weak account được tạo và sử dụng. Không suy ra participant trust hoặc participant exposure.
- Severity: `S2` provisional; canonical existing issue #118 dùng Critical/P0 và cần owner/security adjudication.
- Recommendation: Validate cùng FR-01 policy tại backend trước insert, trả 4xx cụ thể, dùng shared policy definition và thêm direct-API EP/BVA regression tests.
- Measurable retest criterion: Missing-class và length-7 cases đều 4xx/no account; valid length-8 và từng `@ $ ! % * ? &` được accept; rejected credentials không login được.
- Related draft/canonical issue: `github-issues/DRAFT-BUG-REG-PASSWORD-POLICY-01.md`; https://github.com/trngnneee/eshop-sut/issues/118. Không tạo duplicate; Task 2 evidence comment chưa publish.

## Cross-participant synthesis

| Participant | Outcome | Task time | Wrong turns | Errors | Hesitations | Interventions | Card B | SUS |
|---|---|---:|---:|---:|---:|---|---|---|
| P01 | FAILED_OR_ABANDONED | 111 s | 0 | 5 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | 82.5 |
| P02 | FAILED_OR_ABANDONED | 94 s | NOT_OBSERVABLE | 3 | 1 | NOT_OBSERVABLE | NOT_OBSERVABLE | 75 |
| P03 | FAILED_OR_ABANDONED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | 100 |
| P04 | FAILED_OR_ABANDONED | 136 s | 1 | 4 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | 65 |
| P05 | FAILED_OR_ABANDONED | 50 s | NOT_OBSERVABLE | 0 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | 62.5 |
| P06 | FAILED_OR_ABANDONED | 52 s | 0 | 4 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | 65 |
| P07 | FAILED_OR_ABANDONED | 66 s | 0 | 1 | 1 | NOT_OBSERVABLE | NOT_OBSERVABLE | 87.5 |

- Completed independently: 0/7.
- Completed with assistance: 0/7.
- Failed/abandoned: 7/7 theo taxonomy; task end của P02, P03, P05 và P06 đã được người dùng xác nhận.
- Task time: 6/7 calculable (trừ P03); các giá trị 50, 52, 66, 94, 111 và 136 giây có median 80 giây, min 50, max 136. Seven-person median/range vẫn NOT_CALCULABLE.
- Wrong turns: observed lower bound 1; numeric data ở P01/P04/P06/P07 có median 0. P05 NOT_OBSERVABLE; P02/P03 NOT_OBSERVABLE, nên seven-person total/median NOT_CALCULABLE.
- Errors: observed lower bound 17; sáu numeric counts P01/P02/P04/P05/P06/P07 có median 3,5. P03 NOT_OBSERVABLE, nên seven-person total/median NOT_CALCULABLE.
- Hesitations: 2 confirmed (P02 và P07), tổng 10 giây; sáu numeric counts có median 0. P03 NOT_OBSERVABLE, nên seven-person total/median NOT_CALCULABLE.
- Card B/interventions: 0 không thể khẳng định; cả 7 là NOT_OBSERVABLE do không có speech. Không có Card B visible trên screen.
- SUS dataset P01–P07: 7/7 valid user-provided response sets; mean 76.79, median 75, min 62.5, max 100.

## Contradictory and non-findings

- Login copy/heading không nhất quán xuất hiện trên nhiều screen, nhưng observable identifier impact chỉ có P07. P01/P02/P04 login trực tiếp; không nâng copy issue thành higher-frequency impact finding.
- Behavioral logout thành công và không có wrong turn ở P01, P04, P07. Trust vẫn NOT_OBSERVABLE vì không có speech/probe và token state không hiện trên screen.
- P05 system password prompt là NOT_OBSERVABLE; không cộng vào P04 password-manager finding.
- Old D06 duplicate đã bị supersede và không được tính. Replacement D06 đóng góp independent P06 evidence cho password-recovery finding; P06 không đóng góp plaintext-password frequency vì recording không tới login.

## Limitations

- Mẫu 7 nhỏ, không random; không tuyên bố statistical significance hoặc generalize ngoài sample.
- 0/7 recording có usable speech hoặc probes; không có genuine quote hay self-reported impact. SUS chỉ có trong dataset P01–P07 do người dùng cung cấp riêng.
- D02/D03/D05/D06 được xác nhận là toàn bộ session nhưng kết thúc sớm trong flow; đây là failed/abandoned outcomes, không phải upload/file-cut artefacts.
- Device/browser khác nhau và version phần lớn không quan sát được.
- Researcher preflight chỉ là watchpoint/reproduction context, không tính vào participant frequency.
