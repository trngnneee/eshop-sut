# Evidence Index

**Current status:** `READY_FOR_FIELDWORK`
**Naming rule:** Use participant IDs only; never put real names or unmasked contacts in filenames.

## Technical preflight — excluded from participant evidence

| Evidence ID | Type | Path | Integrity / notes |
| :--- | :--- | :--- | :--- |
| PRE-01 | Result JSON | `evidence/technical-preflight/result.json` | Automated/researcher check; never counted as a participant |
| PRE-02 | Screenshots | `evidence/technical-preflight/` | Label all images as technical preflight |

## Pilot — excluded from the seven official sessions

| Evidence ID | Type | Path or refusal reason | Consent / integrity note |
| :--- | :--- | :--- | :--- |
| PILOT-01 | Screen recording | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` |
| PILOT-02 | Audio or refusal reason | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` |
| PILOT-03 | Notes, consent, and instrument | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` |

## Official sessions

| Participant | Screen recording | Audio or refusal reason | Consent evidence | SUS response evidence | Notes / screenshots | Integrity checked |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P01 | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |
| P02 | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |
| P03 | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |
| P04 | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |
| P05 | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |
| P06 | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |
| P07 | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |

## Bug evidence and GitHub traceability

| Bug ID | Screenshot/clip | GitHub issue URL | Participant IDs / session timestamps | Status |
| :--- | :--- | :--- | :--- | :--- |
| `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `<REQUIRED_REAL_DATA>` | `UNVERIFIED` |

## Evidence handling

- Store recordings in `task2-usability/evidence/<participant-id>/` or an access-controlled external location referenced here.
- If evidence is external, provide a durable access-controlled link and access note.
- Preserve original timestamps and do not edit a quote to change meaning.
- Screenshots in a GitHub issue must exclude the participant's name/contact and unrelated personal data.
- Record any missing evidence and the genuine reason; do not silently substitute reconstructed notes.
