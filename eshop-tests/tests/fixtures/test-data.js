// tests/fixtures/test-data.js
// Centralized test data aligned with EShop SUT spec (README v2.0, 2026-05-14)
// All IDs reference TC-[MODULE]-NNN in tests/test-cases/

const BASE_URL = 'http://localhost:5173';
const API_URL  = 'http://localhost:3000';

// ── Existing SUT accounts ────────────────────────────────────────────────────
const ACCOUNTS = {
  admin: { email: 'admin@eshop.com',  password: 'Admin123!' },
  user:  { email: 'test@eshop.com',   password: 'Test1234!' },
};

// ── Coupon codes seeded in the SUT ───────────────────────────────────────────
const COUPONS = {
  percent10:  { code: 'SAVE10',  type: 'percent', value: 10,      minOrder: 300_000 },
  fixed50k:   { code: 'BIGBUY',  type: 'fixed',   value: 50_000,  minOrder: 500_000 },
  fixed100k:  { code: 'VIP100',  type: 'fixed',   value: 100_000, minOrder: 300_000 },
  expired:    { code: 'EXPIRED', type: 'percent', value: 20,      minOrder: 100_000 },
};

// ── Registration test data ────────────────────────────────────────────────────
// Uses timestamps to avoid duplicate-email collisions across runs.
function uniqueEmail(prefix = 'testuser') {
  return `${prefix}_${Date.now()}@test.com`;
}

const REGISTER = {
  valid: {
    name:     'Nguyen Van A',
    email:    () => uniqueEmail('valid'),
    password: 'Valid@123',
    confirm:  'Valid@123',
  },
  // BVA: password length boundaries (min = 8)
  pwdMin7:   'Abc@123',           // 7 chars → invalid (min−)
  pwdMin8:   'Abc@1234',          // 8 chars → valid   (min)
  pwdMin9:   'Abc@12345',         // 9 chars → valid   (min+)
  // Domain: missing character class
  pwdNoUpper:  'valid@123',       // no uppercase → invalid
  pwdNoLower:  'VALID@123',       // no lowercase → invalid
  pwdNoDigit:  'Valid@abc',       // no digit → invalid
  pwdNoSpecial:'Valid1234',       // no special char → invalid
};

// ── Login test data ───────────────────────────────────────────────────────────
const LOGIN = {
  wrongPassword: 'WrongPass!1',
  nonExistentEmail: 'ghost@nowhere.com',
};

// ── Profile test data ─────────────────────────────────────────────────────────
const PROFILE = {
  // BVA: phone length boundaries (min=10, max=11, must start with 0)
  phoneMin9:   '012345678',        // 9 digits → invalid (min−)
  phoneMin10:  '0123456789',       // 10 digits → valid (min)
  phoneMin11:  '01234567890',      // 11 digits → valid (max)
  phoneMax12:  '012345678901',     // 12 digits → invalid (max+)
  phoneNoZero: '1234567890',       // doesn't start with 0 → invalid
};


// ── Forgot-password / Reset-password test data (FR-03) ───────────────────────
// Aligned with tests/test-cases/forgot/TC-FORGOT-001 … TC-FORGOT-044
const FORGOT = {
  registeredEmail:   'test@eshop.com',
  adminEmail:        'admin@eshop.com',
  unregisteredEmail: 'unknown.user@eshop.com',
  malformedEmail:    'not-an-email',

  newPwdValid:     'NewPass1!',
  newPwdAlt:       'NewPass2!',
  newPwdTooShort:  'Test1!@',      // 7 chars (TC-FORGOT-012, TC-FORGOT-030)
  newPwdMin7:      'Abc@123',      // 7 chars BVA
  newPwdMin8:      'Abc@1234',     // 8 chars BVA min on-point
  newPwdMin9:      'Abc@12345',    // 9 chars BVA min+
  newPwdNoUpper:   'test1234!',
  newPwdNoLower:   'TEST1234!',
  newPwdNoDigit:   'TestTest!',
  newPwdNoSpecial: 'Test1234',
  pwdMax49:        'Aa1!' + 'x'.repeat(45),
  pwdMax50:        'Aa1!' + 'x'.repeat(46),
  pwdMax51:        'Aa1!' + 'x'.repeat(47),

  otpWrongLength5: '12345',
  otpWrongLength7: '1234567',
  otpAllZeros:     '000000',
  otpNonNumeric:   '12AB56',

  emailMin4:  'aaaa',
  emailMin5:  'aaaaa',
  emailMin6:  'aaaaaa',
  emailMax99: 'a'.repeat(99),
  emailMax100:'a'.repeat(100),
  emailMax101:'a'.repeat(101),
};

// ── Checkout test data (FR-08) ────────────────────────────────────────────────
const CHECKOUT = {
  // FR-08: only logged-in users; backend must recalculate total
  tamperedTotal: 1,               // client-sent tampered amount (should be rejected)
};

// ── Product management test data (FR-15, Admin) ───────────────────────────────
const PRODUCT = {
  // BVA: product name length (max = 255 chars per spec)
  nameValid:      'Valid Product Name',
  nameEmpty:      '',
  nameMax255:     'A'.repeat(255),    // 255 chars → valid (max on-point)
  nameMax256:     'A'.repeat(256),    // 256 chars → invalid (max+)
  nameMax254:     'A'.repeat(254),    // 254 chars → valid (max−)
  // Domain: price values
  priceZero:      0,                  // 0  → invalid (must be > 0)
  priceNegative:  -1,                 // negative → invalid
  priceMin:       0.01,               // smallest positive → valid (min on-point)
  priceValid:     99000,              // clearly valid
  priceString:    'abc',              // non-numeric → invalid
  // Domain: category
  validCategoryId: 1,                 // assumed to exist; confirmed at runtime
};

// ── GUI / Form requirements test data (FR-22) ─────────────────────────────────
// No specific data values needed — tests inspect DOM structure.
const GUI = {
  pages: [
    { path: '/register',        name: 'Register' },
    { path: '/login',           name: 'Login'    },
    { path: '/forgot-password', name: 'Forgot Password' },
    { path: '/profile',         name: 'Profile'  },
    { path: '/cart',            name: 'Cart'     },
    { path: '/checkout',        name: 'Checkout' },
  ],
};

module.exports = {
  BASE_URL, API_URL, ACCOUNTS, COUPONS,
  REGISTER, LOGIN, PROFILE,
  FORGOT, CHECKOUT, PRODUCT, GUI,
  uniqueEmail,
};
