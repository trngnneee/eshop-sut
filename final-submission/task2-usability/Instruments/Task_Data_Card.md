# Task and Test-Data Cards

Keep this document out of the participant's view until the named card is required.

## Card A — Give before the task

Use a session-specific alias. This is test data, not participant identity.

| Field | Assigned value |
| :--- | :--- |
| Display name for registration | `Khách hàng Pxx` |
| Unique test email | `ux.pxx.<session-timestamp>@example.com` |
| Test password | Participant creates a non-personal test password after reading the interface and remembers it only for this session |
| Updated display name | `Khách hàng Pxx - Hồ sơ mới` |
| Test phone | `0912345678` |
| Test shipping address | `123 Đường Kiểm Thử, Phường Bến Nghé, Quận 1, TP.HCM` |

Before recording starts, replace `Pxx` and `<session-timestamp>` with the assigned session ID and actual timestamp. Do not capture the test password in notes or analysis.

## Card B — Technical-blocker fallback

Show this only after the intervention threshold in the test plan is met and a valid test phone beginning with `0` prevents profile saving:

> Để tiếp tục phiên sau lỗi kỹ thuật, hãy thử số kiểm thử thay thế: `912345678`.

Showing Card B is a task-directed intervention. Record its timestamp and classify an otherwise completed task as `COMPLETED_WITH_ASSISTANCE`.

## Researcher-only verification

After the participant says they are finished, the researcher may verify account/profile persistence and logout state without asking the participant to change their answer. This verification is not part of the participant's task time.
