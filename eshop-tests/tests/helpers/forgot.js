// tests/helpers/forgot.js
// API helpers for FR-03 forgot-password flows (OTP retrieval & password restore)

const { API_URL } = require('../fixtures/test-data');

async function requestOtpViaAPI(page, email) {
  const response = await page.request.post(`${API_URL}/api/forgot-password`, {
    data: { email },
  });
  return { response, body: await response.json().catch(() => ({})) };
}

async function resetPasswordViaAPI(page, email, resetToken, newPassword) {
  return page.request.post(`${API_URL}/api/reset-password`, {
    data: { email, resetToken, newPassword },
  });
}

/** Restore a seeded account password after a successful UI reset test. */
async function restoreUserPassword(page, email, password) {
  const { response, body } = await requestOtpViaAPI(page, email);
  if (!response.ok() || !body.resetToken) return false;
  const resetRes = await resetPasswordViaAPI(page, email, body.resetToken, password);
  return resetRes.ok();
}

module.exports = { requestOtpViaAPI, resetPasswordViaAPI, restoreUserPassword };
