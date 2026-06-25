# TC-OAUTH-009: Kiểm tra chống tấn công CSRF qua tham số State trong OAuth

## Requirement ID
SEC-02

## Module / Test type / Technique
OAuth / Security Testing

## Preconditions
- Gửi request callback OAuth.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Code | valid_code |
| State | mismatch_or_empty_state |

## Test steps
1. Gửi yêu cầu tới callback OAuth kèm tham số state không trùng khớp với state được sinh ra ở session ban đầu.

## Expected result
- Backend phát hiện state mismatch, từ chối đăng nhập để ngăn chặn tấn công CSRF.

## Status / Related bugs
Failed / #45
