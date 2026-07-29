# Task 2 â€” Usability Evaluation Submission Report

**Student:** Äáº·ng ÄÄƒng Khoa  
**Student ID:** 23127207  
**System under test:** EShop Web Frontend  
**Evaluated flow:** ÄÄƒng kÃ½ â†’ ÄÄƒng nháº­p â†’ Chá»‰nh sá»­a thÃ´ng tin cÃ¡ nhÃ¢n â†’ ÄÄƒng xuáº¥t  
**Report date/timezone:** 2026-07-29 â€” Asia/Bangkok (UTC+7)  
**Evidence status:** `READY_FOR_HUMAN_REVIEW â€” CONFIRMED_MISSING_DATA`

## Submission statement

BÃ¡o cÃ¡o nÃ y tá»•ng há»£p trung thá»±c báº£y recording chÃ­nh thá»©c P01â€“P07. Replacement P06/HÃ¢n Ä‘Ã£ thay source trÃ¹ng cÅ© vÃ  old duplicate khÃ´ng Ä‘Æ°á»£c tÃ­nh. TÃªn tháº­t vÃ  liÃªn há»‡ Ä‘Ã£ che náº±m riÃªng trong `Participant_Roster.md`; cÃ¡c bÃ¡o cÃ¡o phÃ¢n tÃ­ch chá»‰ dÃ¹ng participant ID. KhÃ´ng cÃ³ SUS, pilot, consent/eligibility supplement, post-session probes hoáº·c usable participant speech; nhá»¯ng trÆ°á»ng nÃ y Ä‘Æ°á»£c giá»¯ `NOT_RECORDED`, `NOT_OBSERVABLE` hoáº·c `NOT_CALCULABLE`, khÃ´ng Ä‘Æ°á»£c ná»™i suy.

## Executive result

- 7/7 official recordings lÃ  nguá»“n Ä‘á»™c láº­p sau replacement; 7/7 decode thÃ nh cÃ´ng.
- 0/7 hoÃ n thÃ nh Ä‘á»™c láº­p; 0/7 hoÃ n thÃ nh vá»›i há»— trá»£; 7/7 Ä‘Æ°á»£c phÃ¢n loáº¡i `FAILED_OR_ABANDONED` vÃ¬ khÃ´ng phiÃªn nÃ o Ä‘áº¡t Ä‘á»§ SC1â€“SC5.
- 6/7 cÃ³ captured task time tÃ­nh Ä‘Æ°á»£c: median 80 giÃ¢y, min 50 giÃ¢y, max 136 giÃ¢y.
- Observed lower bound: 17 errors, 1 wrong turn, 2 hesitations tá»« 5 giÃ¢y trá»Ÿ lÃªn vá»›i tá»•ng 10 giÃ¢y.
- Hai software-bug candidates cÃ³ participant evidence: `BUG-PF-02` (3/7, S1) vÃ  `BUG-AUTH-PLAINTEXT-01` (5/7, S2).
- SUS: 0/7 complete response sets; má»i aggregate `NOT_CALCULABLE`.

## Method and success criteria

PhÃ¢n tÃ­ch dÃ¹ng screen recording vÃ  timestamp `HH:MM:SS`. CÃ¡c milestone T0â€“T11 Ä‘Æ°á»£c coding riÃªng cho tá»«ng participant. Technical preflight chá»‰ dÃ¹ng Ä‘á»ƒ hiá»ƒu há»‡ thá»‘ng, khÃ´ng Ä‘Æ°á»£c tÃ­nh lÃ  participant evidence. Má»™t phiÃªn chá»‰ hoÃ n thÃ nh khi Ä‘áº¡t toÃ n bá»™:

1. SC1 â€” táº¡o account thÃ nh cÃ´ng.
2. SC2 â€” Ä‘Äƒng nháº­p thÃ nh cÃ´ng báº±ng account vá»«a táº¡o.
3. SC3 â€” cáº­p nháº­t Ä‘á»§ name, phone vÃ  address.
4. SC4 â€” dá»¯ liá»‡u cáº­p nháº­t cÃ²n tá»“n táº¡i sau reload/revisit.
5. SC5 â€” logout cÃ³ behavioral success.

## Dataset and data quality

| Participant | Source alias | Completeness | Main limitation |
|---|---|---|---|
| P01 | D01 | Complete-looking | Audio silence; thiáº¿u SUS/probes/intervention/persistence |
| P02 | D02 | Complete; task end Ä‘Ã£ xÃ¡c nháº­n | Ends on phone-validation alert |
| P03 | D03 | Entire session Ä‘Ã£ xÃ¡c nháº­n | Chá»‰ 4,369 giÃ¢y; T0 vÃ  pháº§n lá»›n metrics khÃ´ng quan sÃ¡t Ä‘Æ°á»£c |
| P04 | D04 | Complete-looking | KhÃ´ng usable speech; thiáº¿u SUS/probes/persistence |
| P05 | D05 | Complete; task end Ä‘Ã£ xÃ¡c nháº­n | Ends at login before submit/result |
| P06 | D06 replacement | Complete; task end Ä‘Ã£ xÃ¡c nháº­n | Ends on repeated weak-password error |
| P07 | D07 | Complete-looking | KhÃ´ng profile update; audio silence |

ThÃ´ng tin xÃ¡c minh submission-only, gá»“m tÃªn Ä‘Æ°á»£c cung cáº¥p vÃ  contact Ä‘Ã£ mask bá»‘n chá»¯ sá»‘ giá»¯a, náº±m trong `Participant_Roster.md`. Äiá»u kiá»‡n â€œoutside HW03 classâ€ vÃ  evidence consent khÃ´ng Ä‘Æ°á»£c ghi nháº­n trong artefacts hiá»‡n cÃ³.

## Success criteria by participant

| Participant | SC1 account | SC2 login | SC3 update all fields | SC4 persistence | SC5 logout | Outcome |
|---|---|---|---|---|---|---|
| P01 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |
| P02 | PASS | PASS | FAIL | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P03 | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P04 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |
| P05 | PASS | FAIL | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P06 | FAIL | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P07 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |

Behavioral logout PASS khÃ´ng chá»©ng minh token/storage deletion; auth storage state váº«n `NOT_OBSERVABLE`.

## Observed metrics

| Participant | Outcome | Task time | Wrong turns | Errors | Hesitations â‰¥5 s | SUS |
|---|---|---:|---:|---:|---:|---|
| P01 | FAILED_OR_ABANDONED | 111 s | 0 | 5 | 0 | NOT_RECORDED |
| P02 | FAILED_OR_ABANDONED | 94 s | NOT_OBSERVABLE | 3 | 1 | NOT_RECORDED |
| P03 | FAILED_OR_ABANDONED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |
| P04 | FAILED_OR_ABANDONED | 136 s | 1 | 4 | 0 | NOT_RECORDED |
| P05 | FAILED_OR_ABANDONED | 50 s | NOT_OBSERVABLE | 0 | 0 | NOT_RECORDED |
| P06 | FAILED_OR_ABANDONED | 52 s | 0 | 4 | 0 | NOT_RECORDED |
| P07 | FAILED_OR_ABANDONED | 66 s | 0 | 1 | 1 | NOT_RECORDED |

KhÃ´ng bÃ¡o cÃ¡o seven-person median cho metric bá»‹ thiáº¿u. Card B, moderator interventions vÃ  think-aloud reminders lÃ  `NOT_OBSERVABLE`, khÃ´ng Ä‘Æ°á»£c máº·c Ä‘á»‹nh báº±ng 0.

## Prioritized findings

| Rank | Finding | Frequency | Severity | Recommendation |
|---:|---|---:|---:|---|
| 1 | `BUG-PF-02` â€” phone validation trÃ¡i FR-04 | 3/7 | S1 | Cho phÃ©p 10â€“11 chá»¯ sá»‘ báº¯t Ä‘áº§u báº±ng 0; Ä‘á»“ng bá»™ validator vÃ  error copy; retest persistence |
| 2 | `BUG-AUTH-PLAINTEXT-01` â€” login password hiá»ƒn thá»‹ plaintext | 5/7 | S2 | Mask máº·c Ä‘á»‹nh; reveal pháº£i explicit vÃ  reversible; kiá»ƒm tra browser matrix |
| 3 | `UF-PHONE-RECOVERY-01` â€” feedback dáº«n tá»›i repeated attempts | 3/7 | S1 | Feedback theo field vÃ  nÃªu Ä‘Ãºng accepted format |
| 4 | `UF-REG-PASSWORD-RECOVERY-01` â€” password-policy recovery láº·p láº¡i | 2/7 | S2 | Live policy checklist vÃ  state-specific feedback |
| 5 | `UF-LOGIN-IDENTIFIER-01` â€” â€œUsernameâ€ khÃ´ng nÃ³i rÃµ cáº§n full email | 1/7 | S3 | DÃ¹ng nhÃ£n Email vÃ  copy Ä‘Äƒng nháº­p tiáº¿ng Viá»‡t |
| 6 | `UF-PASSWORD-MANAGER-DETOUR-01` | 1/7 | S4 | RÃ  soÃ¡t autocomplete semantics vÃ  password-manager integration |

Chi tiáº¿t evidence timestamps, impact, contradictory evidence vÃ  acceptance criteria náº±m trong `Usability_Findings.md`, `Usability_Bug_Report.md` vÃ  `Analysis/Findings_Register.csv`.

## Bugs and publication status

Hai draft Ä‘Ã£ Ä‘Æ°á»£c soáº¡n trong `github-issues/`. ChÆ°a issue nÃ o Ä‘Æ°á»£c Ä‘Äƒng; fresh independent reproduction, duplicate search, privacy review vÃ  screenshot/clip redaction cÃ²n báº¯t buá»™c trÆ°á»›c publication. Participant recordings hiá»ƒn thá»‹ PII vÃ  má»™t sá»‘ plaintext password nÃªn khÃ´ng cÃ³ raw screenshot Ä‘Æ°á»£c Ä‘Æ°a vÃ o gÃ³i ná»™p.

## SUS and qualitative probes

P01â€“P07 Ä‘á»u thiáº¿u Q1â€“Q10; mean, median, minimum vÃ  maximum Ä‘á»u `NOT_CALCULABLE`. Clarity, error recovery, speed, trust vÃ  final requested change Ä‘á»u `NOT_RECORDED`. Behavioral observations khÃ´ng Ä‘Æ°á»£c trÃ¬nh bÃ y nhÆ° participant quotes hoáº·c self-report.

## Limitations and integrity

- Pilot khÃ´ng Ä‘Æ°á»£c thu tháº­p; khÃ´ng thá»ƒ chá»©ng minh protocol Ä‘Ã£ pilot/refine.
- Consent, eligibility supplement vÃ  Ä‘iá»u kiá»‡n outside-class khÃ´ng cÃ³ evidence.
- 0/7 cÃ³ usable speech; exact moderator words, quotes vÃ  interventions khÃ´ng thá»ƒ xÃ¡c minh.
- P03 chá»‰ dÃ i 4,369 giÃ¢y; distribution Ä‘á»§ báº£y ngÆ°á»i khÃ´ng tÃ­nh Ä‘Æ°á»£c.
- D02, D03, D05 vÃ  D06 káº¿t thÃºc sá»›m nhÆ°ng ngÆ°á»i dÃ¹ng xÃ¡c nháº­n Ä‘Ã³ lÃ  toÃ n bá»™ session.
- Sample nhá», khÃ´ng ngáº«u nhiÃªn; khÃ´ng cÃ³ claim vá» statistical significance hoáº·c generalizability.
- KhÃ´ng táº¡o dá»¯ liá»‡u cÃ²n thiáº¿u há»“i cá»©u vÃ  khÃ´ng suy ra SUS tá»« behavior.

## Deliverable traceability

- Verification appendix: `Participant_Roster.md`
- Plan/protocol: `Usability_Test_Plan.md`, `Instruments/`
- Session coding: `Sessions/Session_P01.md`â€“`Session_P07.md`
- Evidence: `Stage_0_Drive_Inventory.md`, `Evidence_Index.md`, `Video_Data_Quality_Report.md`
- Metrics: `Analysis/Observation_Metrics.csv`
- SUS: `Analysis/SUS_Raw_Responses.csv`, `Analysis/SUS_Scores.csv`, `Analysis/SUS_Results.md`
- Findings and bugs: `Usability_Findings.md`, `Usability_Bug_Report.md`, `Analysis/Findings_Register.csv`, `github-issues/`
- Missing data: `Missing_Data_and_Followup.md`
- AI transparency: `AI_Audit_Task2.md`, `AI_Critique_Task2.md`
- Demo: `demo/Task2_Usability_Skill_Demo.mp4`, `Demo_Video_Link.md`
- Submission control: `README.md`, `SUBMISSION_CHECKLIST.md`, `git-commit-log.txt`

## Final declaration

Local analytical artefacts are complete to the limit of the evidence supplied and remain `READY_FOR_HUMAN_REVIEW`. Missing pilot, SUS, consent, eligibility and probes are disclosed rather than reconstructed. External publication and human-only declarations are intentionally not represented as complete.

