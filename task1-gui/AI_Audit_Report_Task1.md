# AI Audit Report — Task 1 (HW03)

**Tool Name:** Gemini 3.6 Flash (High) / Antigravity AI Assistant  
**Date:** 2026-07-28  
**Student:** Đặng Đăng Khoa (23127207)  

---  

## 1. Initial AI Generation Summary
- **Prompt Used:** Prompt yêu cầu sinh bộ GUI checklist ban đầu cho 5 phạm vi của Khoa (Web Login, Web Register, Admin Login, Admin Category, Mobile Login).
- **Raw AI Output Location:** `ai-output/AI_INITIAL_GUI_Checklist.md` (50 items verbatim).

## 2. Human Audit & Corrections Applied
1. **Category Edit Hallucination:** AI generated items for Category Edit modal. *Student Fix:* Reframed item as missing CRUD feature bug (BUG-GUI-04).
2. **Delete Confirmation Hallucination:** AI expected confirmation popup. *Student Fix:* Marked as bug for immediate deletion without prompt.
3. **Login Password Type Defect:** AI expected `type='password'`. *Student Fix:* Updated actual result to observe `type='text'` plaintext bug.
4. **Register Password Regex Flaw:** AI assumed standard regex. *Student Fix:* Verified regex code requiring space `\s` and logged BUG-GUI-02.
5. **Human Added Items:** Added 11 items for Accessibility, Responsive 320px, XSS, Keyboard Navigation, and Double Submit.
