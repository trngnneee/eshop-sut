# G9.5 — AI-Driven API Test Generator Design

**Student:** 23127271 · **Homework:** HW06 API Testing · **Bloom-AI level:** G9.5 Create

## Deliverables

| File | Purpose |
|------|---------|
| [`test-generator-diagram.mmd`](test-generator-diagram.mmd) | Flowchart (Mermaid source — self-authored) |
| [`test-generator-pseudocode.md`](test-generator-pseudocode.md) | Pseudocode aligned with each diagram node |
| `test-generator-diagram.png` | Export for Moodle zip *(generate from `.mmd` — see below)* |

## Export diagram to PNG

1. Open [Mermaid Live Editor](https://mermaid.live) or VS Code Mermaid preview.
2. Paste contents of `test-generator-diagram.mmd`.
3. Export PNG → save as `docs/test-generator-diagram.png`.

> **Anti-cheat (§11):** Diagram structure is student-designed. Do not use AI image generators for the PNG.

## How this relates to HW06

The generator design is **implemented** as:

- **Agent Skill:** `.cursor/skills/api-testing/SKILL.md` (orchestrates Stages 1–6)
- **Scripts:** `scripts/generate_*.py`, `apply_stage2_audit*.py`, `append_stage3_*`, `build_execution_artifacts.py`
- **Evidence:** 280 test cases, Postman collection, Newman report, 8 bugs, `ai_audit_log.md`

## Legend (diagram colours)

| Colour | Meaning |
|--------|---------|
| Green | Input / Output |
| Blue | Human-only steps |
| Yellow | AI-assisted generation |
| Grey | Data artifacts |
| Pink | Decision (loop over 3 APIs) |

## Oral defense — one sentence

*"Given `api_specification.md` and an endpoint, we route four category-specific prompts through an LLM, block on human audit and extend, then build Postman/Newman artifacts and manually triage because observe-only scripts cannot replace spec oracles."*
