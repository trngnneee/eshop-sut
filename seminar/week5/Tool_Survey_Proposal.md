# Tool Survey Proposal - T05 Performance Testing

## 1. Topic
- **Topic Code**: T05
- **Topic Name**: Performance Testing

## 2. Candidate Tools
- **k6**: Modern, developer-centric, JavaScript-scripted tool by Grafana.
- **JMeter**: Industry-standard, Java-based GUI load testing tool by Apache.
- **Artillery**: Node.js-based tool focused on YAML configurations and DevOps pipelines.

## 3. Comparison Matrix

| Criteria | k6 | JMeter | Artillery |
| :--- | :--- | :--- | :--- |
| **Cost/License** | Open Source (AGPL-3.0) / Free local run | Open Source (Apache-2.0) / Free local run | Open Source (MPL-2.0) / Free local run |
| **Learning Curve** | Low-Medium (JavaScript-based scripting, developer-friendly) | Medium-High (GUI-based, XML configuration, complex UI) | Low-Medium (YAML/JSON config, JS for custom extension) |
| **EShop Fit** | High (Integrates easily via HTTP API, simple custom scenarios) | High (Supports complex cookies, session states via GUI controllers) | Medium-High (Good for HTTP, but scripting complex state flows is verbose) |
| **AI Ability** | High (Highly readable JS is easily generated and audited by LLMs) | Low (XML JMX files are difficult for LLMs to generate reliably) | Medium (YAML configs are easy to generate, but custom logic is disjointed) |
| **Community** | Large, active modern developer community | Massive, long-term legacy support & extensive plugins | Good, focused on Node.js/DevOps ecosystems |

## 4. Recommended Pick
- **Main Tool**: **k6** (for primary scripting and performance evaluation).
- **Comparison Tools**: **JMeter** (traditional baseline comparison) and **Artillery** (configuration-driven testing).
- **AI-Augmented Direction**: **ChatGPT/Claude-assisted k6 scenario generation** from workload specifications, followed by manual audit and refactoring.

## 5. Rationale
* **Script-Based Performance Testing**: k6 uses standard JavaScript, making test scenarios highly readable, modular, and maintainable.
* **Automation & CI/CD Fit**: k6 operates entirely via CLI with lightweight resource requirements, integrating naturally into developer workflows.
* **LLM Friendliness**: LLMs perform exceptionally well at outputting valid JavaScript code, facilitating rapid generation of baseline scripts that the team can audit, correct, and execute.

## 6. AI Disclosure
* **AI Tool Use**: AI tools (ChatGPT/Claude) were used to research baseline tool parameters, organize comparisons, and suggest scenario skeletons.
* **Verification**: All tool details, licenses, and command parameters were cross-checked with the official documentations of k6, JMeter, and Artillery.
* **Data Integrity**: AI was **not** used to fabricate testing logs, benchmark outcomes, screenshots, or team task metrics. Any empirical measurements included later in this project will be collected from manual execution on the SUT (EShop).

## Scope Note

This proposal focuses on tool evaluation and demonstration planning. Actual benchmark results, screenshots, and execution logs will be collected during Stage S3 after running the selected scenarios on the EShop system.

---
**Evidence / Project Management References**:
- Shared Evidence Folder: `[Link evidence here]`
- Tool Survey Jira Tasks: `[Insert Jira task screenshot here]`
