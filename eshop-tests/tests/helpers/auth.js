// tests/helpers/auth.js
// Reusable login helpers shared across test files

const { ACCOUNTS, API_URL } = require('../fixtures/test-data');

/**
 * Log in via the UI login form.
 * After calling this, the page session is authenticated.
 */
async function loginViaUI(page, email = ACCOUNTS.user.email, password = ACCOUNTS.user.password) {
  await page.goto('/login');
  await page.waitForLoadState('networkidle');
  await page.locator('input[type="email"]').fill(email);
  await page.locator('input[type="password"]').fill(password);
  await page.locator('button[type="submit"]').click();
  // Wait for redirect away from /login
  await page.waitForURL(url => !url.includes('/login'), { timeout: 8000 });
}

/**
 * Log in via the API directly and inject the JWT token into localStorage.
 * Faster than UI login — use for tests where the login flow itself is NOT under test.
 */
async function loginViaAPI(page, email = ACCOUNTS.user.email, password = ACCOUNTS.user.password) {
  const response = await page.request.post(`${API_URL}/api/auth/login`, {
    data: { email, password },
  });
  if (!response.ok()) {
    throw new Error(`API login failed: ${response.status()} — check that SUT is running`);
  }
  const body = await response.json();
  const token = body.token ?? body.data?.token ?? body.accessToken;
  if (!token) throw new Error('No token in API login response — check API response shape');

  // Inject into localStorage so the React app recognises the session
  await page.goto('/');
  await page.evaluate((t) => {
    localStorage.setItem('token', t);
    localStorage.setItem('authToken', t);  // cover both common key names
  }, token);
  await page.reload();
  await page.waitForLoadState('networkidle');
  return token;
}

/**
 * Clear auth state (logout).
 */
async function logout(page) {
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });
}

module.exports = { loginViaUI, loginViaAPI, logout };
