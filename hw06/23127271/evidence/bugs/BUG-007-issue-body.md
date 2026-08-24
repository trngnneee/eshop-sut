**HW06 API Testing — Student 23127271**

- **Severity:** Medium
- **Found via:** `TC-CART-SEC-SUP-002` (Human (Stage 3))
- **Branch:** `HW6-Tram`

## Screenshot evidence

![BUG-007 evidence](https://github.com/trngnneee/eshop-sut/raw/HW6-Tram/hw06/23127271/evidence/bugs/BUG-007.png)

---

# Bug: POST /api/cart accepts negative quantity

- **Found via test case**: TC-CART-SEC-SUP-002
- **API / Endpoint**: `POST /api/cart`
- **Severity**: Medium
- **Found by**: Human extension (Stage 3)

## Steps to reproduce

1. `POST /api/login` as `test@eshop.com` / `Test1234!`.
2. `POST /api/cart` with body:

```json
{
  "id": 1,
  "name": "iPhone",
  "price": 30000000,
  "quantity": -1
}
```

3. `GET /api/cart` and inspect stored line items.

## Expected result

Oracle (observe): negative quantity is not a valid cart state. SUT should reject the add **or** not persist a line with `quantity < 0`. `GET /api/cart` must not show corrupt cart data.

## Actual result

**HTTP 200 OK** on POST — cart accepts the payload without validation.

Newman log excerpt:

```
□ FR-07 — Cart / Security / TC-CART-SEC-SUP-002
  POST http://localhost:3000/api/cart [200 OK, 294B, 3ms]
  '[TC-CART-SEC-SUP-002] primary status=', 200
```

## Evidence

- Newman: `reports/newman-run.log` (TC-CART-SEC-SUP-002)
- Source: `server.js` — `userCarts[userId].push(req.body)` with no quantity checks

## Notes

**Impact:** Negative quantities can break checkout totals (FR-08) and cart merge logic (FR-07).

**Why AI missed it:** FR-06 documents UI quantity controls only; API-level negative input was not generated until human SUP case.
