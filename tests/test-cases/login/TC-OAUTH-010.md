# TC-OAUTH-010: Kiểm tra chặn Redirect URI không hợp lệ trong yêu cầu OAuth

## Requirement ID
SEC-02

## Module / Test type / Technique
OAuth / Security Testing

## Preconditions
- Gửi request đăng nhập OAuth.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| redirect_uri | http://malicious-site.com |

## Test steps
1. Yêu cầu đăng nhập OAuth tới Google nhưng thay đổi tham số `redirect_uri` thành trang web độc hại.

## Expected result
- Google OAuth API hoặc backend EShop từ chối xử lý yêu cầu (Redirect URI mismatch).

## Status / Related bugs
Failed / #45
