# Boundary Value Analysis (BVA) — Points Reference

## The 4-Point Model

BVA focuses on values **at and around** the boundary of a partition, where
off-by-one errors most frequently occur. For any boundary, four points exist:

| Point | Symbol | Location | Purpose |
|-------|--------|----------|---------|
| **ON** | ●—— | Exactly on the boundary | Confirm the boundary itself is accepted/rejected correctly |
| **OFF** | ——● | One step outside the boundary | Confirm the system rejects (or accepts) just past the line |
| **IN** | ——●—— | Comfortably inside the valid domain | Baseline "normal" case, should always pass |
| **OUT** | ●————● | Far outside the domain | Extreme invalid value; tests robustness |

> **Key insight**: ON and OFF are the most valuable. IN confirms the happy
> path. OUT checks for catastrophic failures on extreme input.

---

## Boundary Direction

Every boundary has **two sides**: the lower boundary and the upper boundary.
Apply the 4-point model to each side independently.

For a valid range **[min, max]**:

```
OUT    OFF   ON          IN         ON   OFF    OUT
 ●      ●    ●───────────●───────────●    ●      ●
       min-1  min                  max  max+1
```

---

## BVA by Data Type

### 1. String Length  (e.g., password length 8–32 chars)

| Point | Lower boundary (min=8) | Upper boundary (max=32) |
|-------|----------------------|------------------------|
| ON    | 8 chars              | 32 chars               |
| OFF   | 7 chars              | 33 chars               |
| IN    | 20 chars (midpoint)  | 20 chars               |
| OUT   | 0 chars (empty)      | 100 chars              |

**Unit**: 1 character

**Example values**:
```
ON-low:  "Abcdef1!"              (exactly 8)
OFF-low: "Abcde1!"               (exactly 7)
IN:      "Abcdefghij1234!ABCDE"  (20)
ON-high: "Abcdefghij1234!ABCDE12" (32 — count carefully!)
OFF-high: <33-char string>
OUT:     "" (empty) / <100-char string>
```

---

### 2. Integer Range  (e.g., quantity 1–99)

| Point | Lower (min=1) | Upper (max=99) |
|-------|--------------|----------------|
| ON    | 1            | 99             |
| OFF   | 0            | 100            |
| IN    | 50           | 50             |
| OUT   | -100         | 999            |

**Unit**: 1

---

### 3. Floating-Point Range  (e.g., discount 0.0–100.0%)

| Point | Lower (min=0.0) | Upper (max=100.0) |
|-------|----------------|------------------|
| ON    | 0.0            | 100.0            |
| OFF   | -0.01          | 100.01           |
| IN    | 50.0           | 50.0             |
| OUT   | -999.99        | 999.99           |

**Unit**: smallest increment meaningful to the system (usually 0.01)

---

### 4. Date Range  (e.g., coupon valid 2025-01-01 to 2025-12-31)

| Point | Lower | Upper |
|-------|-------|-------|
| ON    | 2025-01-01 | 2025-12-31 |
| OFF   | 2024-12-31 | 2026-01-01 |
| IN    | 2025-06-15 | 2025-06-15 |
| OUT   | 2020-01-01 | 2030-12-31 |

**Unit**: 1 day

---

### 5. Enumerated Set  (e.g., role ∈ {admin, user, moderator})

For sets, ON/OFF are membership-based:

| Point | Value | Meaning |
|-------|-------|---------|
| ON    | `admin` (or any valid member) | Should be accepted |
| OFF   | `superadmin` (adjacent but not in set) | Should be rejected |
| IN    | `user` | Typical accepted value |
| OUT   | `""` or `null` | Extreme invalid |

---

### 6. File Size  (e.g., CSV import ≤ 5 MB)

| Point | Value |
|-------|-------|
| ON    | exactly 5 MB (5 × 1024 × 1024 bytes) |
| OFF   | 5 MB + 1 byte |
| IN    | 2.5 MB |
| OUT   | 50 MB |

---

## BVA Test Case Table Template

```markdown
## BVA Test Cases — <Variable Name> (range: <min>–<max>)

| TC ID | Point | Value | Expected Result | Actual | Status |
|-------|-------|-------|-----------------|--------|--------|
| TC-FRxx-BVA-001 | ON (lower) | <min> | Accepted | | |
| TC-FRxx-BVA-002 | OFF (lower) | <min-1> | Rejected: "<error msg>" | | |
| TC-FRxx-BVA-003 | IN | <midpoint> | Accepted | | |
| TC-FRxx-BVA-004 | ON (upper) | <max> | Accepted | | |
| TC-FRxx-BVA-005 | OFF (upper) | <max+1> | Rejected: "<error msg>" | | |
| TC-FRxx-BVA-006 | OUT (low) | <extreme low> | Rejected | | |
| TC-FRxx-BVA-007 | OUT (high) | <extreme high> | Rejected | | |
```

---

## Worked Example: FR-09 Discount Coupons

### Variable: Discount Percentage (0–100%)

| TC ID | Point | Value | Expected |
|-------|-------|-------|----------|
| TC-FR09-BVA-001 | ON lower | 0% | Accepted (0% discount = no discount) |
| TC-FR09-BVA-002 | OFF lower | -1% | Rejected: "Discount cannot be negative" |
| TC-FR09-BVA-003 | IN | 50% | Accepted, order total halved |
| TC-FR09-BVA-004 | ON upper | 100% | Accepted (free item) |
| TC-FR09-BVA-005 | OFF upper | 101% | Rejected: "Discount cannot exceed 100%" |
| TC-FR09-BVA-006 | OUT high | 999% | Rejected |

### Variable: Coupon Code Length (e.g., 6–20 chars)

| TC ID | Point | Value | Expected |
|-------|-------|-------|----------|
| TC-FR09-BVA-007 | ON lower | 6-char code | Accepted |
| TC-FR09-BVA-008 | OFF lower | 5-char code | Rejected |
| TC-FR09-BVA-009 | IN | 13-char code | Accepted |
| TC-FR09-BVA-010 | ON upper | 20-char code | Accepted |
| TC-FR09-BVA-011 | OFF upper | 21-char code | Rejected |
| TC-FR09-BVA-012 | OUT low | 1-char code | Rejected |
| TC-FR09-BVA-013 | OUT high | 50-char code | Rejected |

---

## Common BVA Mistakes

1. **Treating OFF as "any invalid value"** — OFF must be exactly one unit
   outside the boundary (7 for min=8, not 5).
2. **Skipping the upper boundary** — Always do both lower and upper.
3. **Wrong unit** — For string length, unit=1 char. For price, unit=0.01.
4. **Forgetting OUT** — The extreme cases catch overflow and type errors.
5. **Using the same value for ON and IN** — They must be different values.
