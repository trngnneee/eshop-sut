# Bộ prompt theo giai đoạn

Placeholder `<<...>>` phải điền trước khi gửi. Mỗi prompt = một lần gọi AI = một dòng Audit Report. **Không gộp prompt.**

Ký hiệu chung dùng trong tài liệu này:
- `<<SUT>>` — tên app, ví dụ "EShop, Vietnamese e-commerce demo"
- `<<FE>>` — thư mục frontend trong scope, ví dụ `frontend-web/` (React + Vite + Tailwind), URL `localhost:5173`
- `<<UI-REQ-N>>` — mã mục yêu cầu giao diện trong tài liệu SUT, ví dụ FR-21..FR-24
- `<<OUT>>` — thư mục output, ví dụ `tests/gui_and_usability_testing`

---

## Prompt #1 — UI Inventory (lặp cho từng màn hình)

```md
ROLE: You are helping build a UI element inventory for GUI testing (not generating checklist items yet). You have read access to the <<SUT repo>> repository, already cloned locally.

CONTEXT: <<SUT>>. Screen in scope: "<<tên màn hình>>", corresponding to <<FR-0X>> in the SUT spec. The relevant code lives under <<FE>>.

STEPS:
1. Search <<FE>>/src/ for the file(s) implementing this screen (by route, page/component name, or FR-related keyword). List every file path you used — don't guess without checking.
2. Read the full component tree: the page component + any imported sub-components, shared form/button/toast/dialog components, and every conditional-rendering branch (loading, error, empty, success, disabled states).
3. If you can run shell commands: start the dev server and fetch/render the page to cross-check the static-code inventory against what actually renders — flag anything that only shows up at runtime (computed classes, dynamic labels, API-driven content, backend errors leaking into the UI). If you cannot execute or browse, skip this and say so explicitly instead of guessing.
4. Build an exhaustive UI element inventory for THIS SCREEN ONLY.

OUTPUT: write the result to `<<OUT>>/ui-inventory/<<screen-slug>>.md` as a markdown table:

| # | Element type | Element label/name | Location | Apparent purpose / linked requirement | Source file:line |
|---|---|---|---|---|---|

Include every button, field, label, link, icon, toast/dialog trigger, and any conditionally-rendered element — even ones not visible by default. Shared header/footer elements go in a separate `_shared-layout.md` instead of being repeated per screen.
```

*Dự phòng khi tool AI không đọc được file:* thay STEPS 1–2 bằng `INPUT: <<dán nguyên source .jsx/.tsx của màn hình>>` và bỏ cột `Source file:line` nếu không xác định được số dòng.

---

## Prompt #2a — Aspect 1: General UI standards

```md
ROLE: You are a senior QA engineer creating a requirements-based GUI checklist.

CONTEXT — System Under Test:
- App: <<SUT>>, <<FE>> at <<URL>>.
- UI element inventory for the screens in scope:
<<dán toàn bộ bảng inventory từ GĐ1, tất cả màn hình>>
- Official "General UI Standards" requirement (<<UI-REQ-1>>), verbatim from the SUT spec:
<<dán nguyên văn>>

TASK: Generate GUI checklist items for IA-01 – General UI standards ONLY (visual consistency, layout/alignment, typography, spacing, color usage, iconography, responsive/viewport behavior, page-title correctness).

RULES:
1. Each item = one objective, testable Pass/Fail statement.
2. Each item must reference a specific screen/element from the inventory — no generic filler like "UI should look professional."
3. Include items that verify each rule in <<UI-REQ-1>>, PLUS extra best-practice items beyond it that are still specific to this app.
4. If the same rule applies identically to multiple screens, write ONE item and list all applicable screens.
5. Produce at least 12 items.

OUTPUT — a markdown table:
| ID | Screen(s) | Checklist Item | Expected Result | Traced to (<<UI-REQ-1>> / heuristic) |
|---|---|---|---|---|
Use IDs GUI-IA01-01, GUI-IA01-02, ...
```

## Prompt #2b — Aspect 2: Forms

```md
[Giữ nguyên khối ROLE/CONTEXT của #2a, đổi phần yêu cầu sang <<UI-REQ-2>>:]
- Official "Form Requirements" (<<UI-REQ-2>>), verbatim from the SUT spec:
<<dán nguyên văn>>

TASK: Generate checklist items for IA-02 – Forms ONLY (required-field indicators, input types/masking, validation timing and message placement, multi-step indicators, tab order within forms, confirmation-field matching, format constraints e.g. phone/quantity/CSV).

Pay special attention to any rule in <<UI-REQ-2>> that contradicts common UI conventions (e.g. unusual error-message placement) — do NOT silently "correct" it to the common pattern; check what THIS spec requires.

[Giữ nguyên RULES 1–5 và OUTPUT của #2a, IDs GUI-IA02-xx]
```

## Prompt #2c — Aspect 3: Navigation

```md
[Giữ nguyên khối ROLE/CONTEXT, đổi sang <<UI-REQ-3>>:]
- Official "Navigation Requirements" (<<UI-REQ-3>>), verbatim from the SUT spec:
<<dán nguyên văn>>

TASK: Generate checklist items for IA-03 – Navigation ONLY (active-state highlighting, badges/counters, exact label wording, breadcrumbs on sub-pages, back/continue links, browser back-button behavior, invalid-URL/404 handling, route guards for protected pages, pagination if present).

[Giữ nguyên RULES 1–5 và OUTPUT, IDs GUI-IA03-xx]
```

## Prompt #2d — Aspect 4: Feedback / state

```md
[Giữ nguyên khối ROLE/CONTEXT, đổi sang <<UI-REQ-4>>:]
- Official "Feedback & State Requirements" (<<UI-REQ-4>>), verbatim from the SUT spec:
<<dán nguyên văn>>

TASK: Generate checklist items for IA-04 – Feedback/state ONLY (action feedback e.g. add-to-cart, confirmation dialogs before destructive actions, empty-state visuals, loading indicators, error/success messages, account-lockout messaging, coupon apply/invalid feedback, image alt-text, safe rendering of user-supplied text such as search terms, state consistency after a completed transaction).

[Giữ nguyên RULES 1–5 và OUTPUT, IDs GUI-IA04-xx]
```

---

## Prompt #3 — Gap analysis (AI chỉ chẩn đoán)

```md
Here is my consolidated GUI checklist for <<SUT>> so far (<<X>> items, IA-01 to IA-04):
<<dán checklist từ GĐ2>>

TASK: For EACH of the following 8 dimensions, tell me whether it is already represented, partially represented, or completely absent in my checklist above. Do NOT add new checklist rows — just diagnose gaps, and cite which of my existing item IDs count as evidence.

1. Accessibility (keyboard-only operation beyond simple tab order, screen-reader/ARIA labels, color-contrast ratios, visible focus states)
2. Dark mode / theme switching
3. Right-to-left (RTL) layout support
4. Extreme viewport sizes (narrow mobile widths, 200%+ browser zoom)
5. Network resilience (slow connection, request timeout, offline state)
6. Text-overflow / localization edge cases (very long names, number-formatting edge cases)
7. Print / export-friendly view
8. Browser-native interaction quirks (autofill vs. custom validation, back/forward cache showing stale state)

For each dimension marked "partially represented" or "absent," suggest 1–2 candidate items — but do NOT assume they are correct or complete; I will verify each one against the running app myself.
```

**Sau prompt này là phần người làm, bắt buộc.** Tự thử trên SUT rồi điền Phần B (xem `templates.md`). Danh sách thao tác nên chạy:

- Tab-only qua toàn bộ form của từng màn (có focus ring? thứ tự có nhảy do `tabindex` không?)
- DevTools zoom 200% + viewport 320px/375px trên mọi màn có bảng
- Throttle Slow 3G và Offline giữa một hành động quan trọng
- Dán `<script>` / `<img src=x onerror=...>` vào mọi ô sẽ được render lại (tìm kiếm, địa chỉ, tên)
- F5 giữa luồng, và Back/Forward sau khi state đã đổi
- Lặp cùng một hành động 2 lần (thêm giỏ, submit) xem state có tích luỹ sai
- `grep -rn 'htmlFor\|aria-\|alt=\|lang=' <<FE>>/src <<FE>>/index.html` để bắt lỗi a11y thuần đọc code
- Nhập giá trị cực đoan (tên rất dài, số lượng 9999, số âm, chữ vào ô số)

---

## Prompt #4 — Hợp nhất & chuẩn hoá

```md
I ran 4 separate checklist-generation passes (IA-01 to IA-04) plus manual additions from my own gap review. Combined raw list below:
<<dán output #2a+#2b+#2c+#2d + các item GUI-GAP từ GĐ3>>

TASK:
1. Remove exact or near-duplicate items (if two items test the same underlying rule on different screens, merge into one row and list all applicable screens). Keep a dedup log at the end: which IDs merged into which, and why.
2. Renumber sequentially within each Interface Aspect (GUI-IA01-01, ...). Keep manually-added items prefixed GUI-GAP-xx — do NOT renumber them into the IA sequence, so it stays traceable which items were AI-generated vs. manually added.
3. Verify each item is an objective, testable Pass/Fail statement — rewrite any vague/subjective one.
4. Output the final table:
| ID | Interface Aspect | Screen(s) | Checklist Item | Expected Result | Kết quả | Ghi chú (lý do Fail) |
leaving the last two columns empty for manual execution. The separator row MUST have exactly as many cells as the header.
5. At the end, report total item count and per-aspect breakdown, and confirm the total is above 40.
```

---

## Prompt #5 — Chuốt ghi chú thi hành (tuỳ chọn, KHÔNG dùng để quyết Pass/Fail)

```md
Below are my raw, quickly-written execution notes for FAILED checklist items (may be messy):
<<mỗi dòng: ID – ghi chú thô>>

TASK: Rewrite each into one clear, professional sentence describing WHY the item failed, suitable for a formal test report. Keep every concrete value I recorded (strings, coordinates, computed styles, file:line).

STRICT RULE: Do not invent details, root causes, or severity judgments I did not state. If a note is too vague to rewrite confidently, flag it back to me instead of guessing.
```

---

## Prompt #6 — Bug report / GitHub issue (lặp theo từng bug)

```md
I found a UI bug while executing GUI checklist item(s) <<ID(s)>> on <<SUT>>.

Raw details (all provided by me — do not add anything I have not stated):
- Screen: <<...>>
- Steps I performed: <<...>>
- Expected result (per checklist / <<UI-REQ-N>>): <<...>>
- Actual result observed: <<...>>
- Environment: <<browser/OS/device>>

TASK: Draft a GitHub issue using exactly this structure:

## Title
[concise, descriptive, prefixed with [Blocker]/[Major]/[Minor]/[Cosmetic]]

## Description
[1–2 sentences]

## Steps to Reproduce
1. ...

## Expected Result
...

## Actual Result
...

## Environment
...

## Related checklist item(s)
<<ID(s)>>

## Requirement
<<UI-REQ-N>>

## Severity
[Suggest one of: Blocker / Major / Minor / Cosmetic, with 1-sentence justification]

## Screenshot
`<<ID>>.png`

Do not invent, assume, or embellish any detail beyond what I gave you above.
```

Giữ token ảnh đúng dạng `` `<<ID>>.png` `` — `scripts/upload_screenshots.py` tìm đúng pattern này để thay bằng URL đã upload.

---

## Prompt #7 — Sinh dòng Audit Report (tuỳ chọn, dùng cuối cùng)

```md
Below is the log of the AI interactions from this GUI-checklist run: for each step, the tool + version, timestamp, verbatim prompt, and what the AI produced.
<<dán log>>

TASK: Format these into the AI Audit Report table with columns:
| (1) Prompt + Tool | (2) AI Output | (3) Verdict | (4) Reasoning (ISTQB) | (5) Student Fix |

RULES:
- One row per AI call. Never merge rows.
- Column 1 must contain the prompt VERBATIM (escape pipes as &#124;), not a paraphrase.
- Column 3: VALID / INVALID / INCOMPLETE.
- Column 4 must cite a concrete ISTQB concept or course slide, not a generic sentence.
- Column 5: leave a clearly-marked TODO placeholder for me to fill — do NOT invent what I fixed.
```
