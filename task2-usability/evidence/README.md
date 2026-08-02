# Evidence Folder

This folder is reserved for controlled evidence artefacts. It must not contain raw participant recordings or unredacted participant frames.

Recommended layout:

```text
evidence/
├── github-issue-reproduction/   # synthetic, technical-only evidence
├── pilot/
├── P01/
├── P02/
├── P03/
├── P04/
├── P05/
├── P06/
└── P07/
```

`github-issue-reproduction/` contains the machine-readable reproduction result and privacy-safe synthetic screenshots for `BUG-PF-02`, `BUG-AUTH-PLAINTEXT-01` and `BUG-REG-PASSWORD-POLICY-01`. These artefacts are not participant evidence and do not affect P01–P07 frequencies. Intermediate navigation screenshots and runtime stdout/stderr logs are not deliverables.

Use participant IDs only. Never store unmasked contact details, real passwords, personal addresses, or unrelated notifications in this folder.
