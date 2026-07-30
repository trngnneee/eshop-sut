# Overall AI Critique — Task 1 GUI Testing

**Author:** Đặng Đăng Khoa (23127207)  
**Word Count:** 265 words  

During Task 1 GUI checklist generation for EShop, the initial AI output produced a broad baseline of 50 test items. However, a rigorous code-level audit revealed significant structural flaws and cognitive blind spots in the AI's generation capability.

First, the AI exhibited a strong happy-path bias and hallucinated non-existent features. On Admin Category Management (FR-14), the AI generated valid-looking test items for an 'Edit Category Modal' and 'Delete Confirmation Popup'. In reality, inspecting `frontend-admin/src/App.jsx` showed that the SUT completely lacks an Edit Category interface and triggers instant API deletions without any confirmation dialog.

Second, the AI missed critical front-end implementation defects by assuming ideal UI standards. It failed to spot that the Web Login page rendered the heading `<h2>Đăng Ký</h2>` instead of `Đăng Nhập`, used `type="text"` for password masking, hardcoded `tabIndex={1}`, and used standard `<a>` tags causing full page reloads instead of SPA routing. Furthermore, the AI overlooked accessibility standards such as missing `<label>` tags in Admin Login and touch target sizes on Mobile App.

Third, the AI failed to identify client-side logic flaws. On Web Register (FR-01), the code implemented a `flawedStrongPasswordRegex` requiring whitespace (`\s`) while displaying hint text demanding special characters. The AI blindly generated happy-path assertions for standard strong passwords without validating the actual regex pattern.

As a human QA engineer, I systematically audited all 50 AI items, removing 3 hallucinated test cases, revising 19 items to match actual SUT behavior, and adding 11 high-value `HUMAN_ADDED` items covering XSS sanitization, 320px responsive layouts, keyboard navigation, double-submit protection, and soft keyboard scrolling. This collaboration highlights that while AI accelerates initial test scaffolding, human expertise is indispensable for verifying actual codebase implementation and edge cases.
