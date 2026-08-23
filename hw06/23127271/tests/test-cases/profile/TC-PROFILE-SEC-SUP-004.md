# TC-PROFILE-SEC-SUP-004: Content-Type text/plain with JSON body

## Requirement ID
FR-04 / SEC-02

## Module / Test type / Technique
profile / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-02

## Threat / probe
Content-Type text/plain with JSON body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Snapshot GET /api/users/me.

## Test data
```json
{
  "headers": {
    "Authorization": "Bearer <valid_user_token>",
    "Content-Type": "text/plain"
  },
  "body_raw": "{\"name\":\"Hacked Via Plain\",\"phone\":\"0912345678\",\"shipping_address\":\"X\"}"
}
```

## Test steps
1. PUT /api/users/me with valid JWT and Content-Type: text/plain; body is JSON string.
2. GET /api/users/me with valid token.

## Expected result
SEC-02: profile must not change if body is ignored or parsed unsafely. GET matches snapshot unless plain-text updates allowed (they are not). HTTP status is not specified — record actual without inventing codes.

## Type
Header / parser confusion

## Why the AI missed this
Prompt quality — SEC-02 cases targeted missing/invalid Authorization only; Content-Type confusion (valid JWT + wrong media type) is a common bypass class not in the SEC checklist prompt.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** SEC-02 Content-Type confusion with valid JWT.

## Status / Related bugs
Not Run / None
