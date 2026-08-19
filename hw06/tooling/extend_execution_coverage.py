#!/usr/bin/env python3
"""Build reproducible DDT assets that execute the final HW06 inventory.

The script expands the three existing data files and replaces only the three
DDT request definitions in the Postman collection.  Expected values remain the
specification oracle from the final Markdown tables; known SUT defects are not
converted into passing expectations.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HW06 = ROOT / "hw06"
COLLECTION_PATH = HW06 / "postman" / "EShop-HW06-23127207.postman_collection.json"
DATA_DIR = HW06 / "postman" / "data"


def tc(prefix: str, number: int) -> str:
    return f"TC-API-{prefix}-{number:03d}"


def login_rows() -> list[dict[str, Any]]:
    blocked = {24, 41, 42}
    expected: dict[int, str] = {
        1: "200", 2: "401", 3: "401", 4: "400", 5: "400", 6: "400",
        7: "401", 8: "4xx", 9: "401", 10: "400", 11: "400", 12: "400",
        13: "400", 14: "400", 15: "400|415", 16: "200", 17: "401",
        18: "200", 19: "401", 20: "403", 21: "4xx", 22: "200", 23: "200",
        25: "401", 26: "401", 27: "4xx", 28: "200", 29: "200", 30: "200",
        31: "200", 32: "403", 33: "200", 34: "200", 35: "401", 36: "200",
        37: "200", 38: "200", 39: "200", 40: "200",
    }
    # Any case that can touch a real account uses a fresh user.  This prevents
    # an invalid-password partition from locking the shared seed user and
    # contaminating later iterations.
    register = set(range(1, 43)) - {3, 4, 6, 8, 10, 12, 14, 24, 25, 27, 41, 42}
    pre_failures = {18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 32: 2, 37: 2, 38: 2}
    delays = {21: 29_000, 22: 31_000, 38: 35_000}
    scenarios = {
        1: "valid credentials", 2: "wrong password", 3: "unknown email",
        4: "missing email", 5: "missing password", 6: "empty email",
        7: "short wrong password", 8: "invalid email format", 9: "email whitespace",
        10: "null email", 11: "null password", 12: "numeric email",
        13: "object password", 14: "array body", 15: "missing content type",
        16: "ignored rememberMe", 17: "first failure counter", 18: "two failures then correct",
        19: "third failure boundary", 20: "correct credential while locked",
        21: "locked at 29 seconds", 22: "unlock at 31 seconds", 23: "reset after success",
        25: "SQLi email", 26: "SQLi password", 27: "XSS non-reflection",
        28: "password leakage", 29: "internal auth fields", 30: "role mass assignment",
        31: "token usability", 32: "locked account enumeration", 33: "success schema",
        34: "JSON content type", 35: "error schema", 36: "negative schema",
        37: "two failures sequence", 38: "unlock at 35 seconds", 39: "sensitive root fields",
        40: "JWT exp claim",
    }
    rows = []
    for number in range(1, 43):
        if number in blocked:
            continue
        rows.append({
            "tc_id": tc("LOGIN", number),
            "scenario": scenarios[number],
            "expected_status": expected[number],
            "register_user": number in register,
            "pre_failures": pre_failures.get(number, 0),
            "delay_ms": delays.get(number, 0),
            "note": "Expected is the specification oracle; assertion runs in full mode.",
        })
    return rows


def checkout_rows() -> list[dict[str, Any]]:
    blocked = {29}
    expected: dict[int, str] = {
        1: "200", 2: "401", 3: "403", 4: "403", 5: "400", 6: "400",
        7: "400", 8: "400", 9: "not-5xx", 10: "not-5xx", 11: "not-5xx",
        12: "reject-or-sanitize", 13: "not-5xx", 14: "not-5xx", 15: "400",
        16: "not-5xx", 17: "200", 18: "not-5xx", 19: "200", 20: "200",
        21: "200", 22: "400", 23: "200", 24: "200", 25: "200", 26: "200",
        27: "401", 28: "403", 30: "200", 31: "401|403", 32: "reject-or-sanitize",
        33: "200", 34: "200", 35: "200", 36: "200", 37: "200", 38: "400",
        39: "200", 40: "400", 41: "401|403", 42: "reject-or-sanitize",
    }
    auth = {2: "none", 3: "malformed", 4: "invalid", 27: "none", 28: "invalid"}
    empty_cart = {2, 3, 4, 22, 27, 28, 40}
    scenarios = {
        1: "valid checkout and cart total", 2: "missing authorization", 3: "malformed authorization",
        4: "invalid JWT", 5: "zero total", 6: "negative total", 7: "string total",
        8: "null total", 9: "missing shipping address", 10: "empty shipping address",
        11: "long shipping address", 12: "persistent img XSS", 13: "SQLi address",
        14: "Unicode address", 15: "fractional total", 16: "very large total",
        17: "extra role field", 18: "scientific notation total", 19: "pending order flow",
        20: "cart cleared post-condition", 21: "duplicate checkout observation", 22: "empty cart",
        23: "order appears in my-orders", 24: "positive integer orderId", 25: "body user_id ignored",
        26: "login-cart-checkout ownership", 27: "missing auth security", 28: "tampered JWT",
        30: "cross-user body isolation", 31: "anonymous order IDOR", 32: "persistent script XSS",
        33: "success schema", 34: "JSON content type", 35: "orderId schema",
        36: "no secret fields", 37: "forged client total", 38: "negative total extension",
        39: "cart clear extension", 40: "empty cart extension", 41: "anonymous IDOR extension",
        42: "persistent img XSS extension",
    }
    rows = []
    for number in range(1, 43):
        if number in blocked:
            continue
        rows.append({
            "tc_id": tc("CHECKOUT", number),
            "scenario": scenarios[number],
            "expected_status": expected[number],
            "auth_kind": auth.get(number, "user"),
            "cart_setup": number not in empty_cart,
            "cart_total": 30_000_000 if number == 37 else 200_000,
            "note": "Fresh user/cart per iteration; expected remains the specification oracle.",
        })
    return rows


def order_status_rows() -> list[dict[str, Any]]:
    source = json.loads((DATA_DIR / "order-status-matrix.data.json").read_text(encoding="utf-8"))
    matrix = [row for row in source if 1 <= int(str(row["tc_id"]).rsplit("-", 1)[1]) <= 25]
    if len(matrix) != 25:
        raise ValueError("Expected the existing 25-row state matrix")
    extra: list[dict[str, Any]] = []
    expected = {
        26: "404", 27: "4xx", 28: "4xx", 29: "400", 30: "400", 31: "401",
        32: "403", 33: "403", 34: "403", 35: "200", 36: "400", 37: "200",
        38: "200", 39: "403", 40: "403", 42: "200", 43: "400", 44: "400",
    }
    scenarios = {
        26: "nonexistent order", 27: "negative order id", 28: "string order id",
        29: "missing status", 30: "uppercase status", 31: "missing authorization",
        32: "invalid JWT", 33: "user role escalation", 34: "user order mutation",
        35: "success message schema", 36: "error schema", 37: "JSON content type",
        38: "no secret fields", 39: "role escalation extension", 40: "cross-user mutation",
        42: "admin cancels shipping", 43: "user cancels shipping", 44: "status type confusion",
    }
    from_status = {42: "shipping", 43: "shipping"}
    for number in range(26, 45):
        if number == 41:
            continue
        extra.append({
            "tc_id": tc("ORDER-STATUS", number),
            "scenario": scenarios[number],
            "from_status": from_status.get(number, "pending"),
            "to_status": "confirmed",
            "expected_status": expected[number],
            "note": "Fresh order per iteration; expected remains the specification oracle.",
        })
    return matrix + extra


def lines(script: str) -> list[str]:
    return textwrap.dedent(script).strip().splitlines()


def find_item(items: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for item in items:
        if item.get("name") == name:
            return item
        child = item.get("item")
        if isinstance(child, list):
            try:
                return find_item(child, name)
            except KeyError:
                pass
    raise KeyError(name)


def event(script: str, listen: str) -> dict[str, Any]:
    return {"listen": listen, "script": {"type": "text/javascript", "exec": lines(script)}}


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    collection = json.loads(COLLECTION_PATH.read_text(encoding="utf-8"))

    login = find_item(collection["item"], "[DDT] login partitions")
    login["request"] = {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "url": {"raw": "{{base_url}}/api/login", "host": ["{{base_url}}"], "path": ["api", "login"]},
        "body": {"mode": "raw", "raw": "{{case_body}}", "options": {"raw": {"language": "json"}}},
    }
    login["event"] = [event(LOGIN_PRE_REQUEST, "prerequest"), event(LOGIN_TEST, "test")]

    checkout = find_item(collection["item"], "[DDT] checkout partitions")
    checkout["request"] = {
        "method": "POST",
        "header": [
            {"key": "Content-Type", "value": "application/json"},
            {"key": "Authorization", "value": "{{case_authorization}}"},
        ],
        "url": {"raw": "{{base_url}}/api/checkout", "host": ["{{base_url}}"], "path": ["api", "checkout"]},
        "body": {"mode": "raw", "raw": "{{case_body}}", "options": {"raw": {"language": "json"}}},
    }
    checkout["event"] = [event(CHECKOUT_PRE_REQUEST, "prerequest"), event(CHECKOUT_TEST, "test")]

    status = find_item(collection["item"], "[DDT] transition matrix")
    status["request"] = {
        "method": "PUT",
        "header": [
            {"key": "Content-Type", "value": "application/json"},
            {"key": "Authorization", "value": "{{case_authorization}}"},
        ],
        "url": "{{base_url}}{{case_status_path}}",
        "body": {"mode": "raw", "raw": "{{case_status_body}}", "options": {"raw": {"language": "json"}}},
    }
    status["event"] = [event(STATUS_PRE_REQUEST, "prerequest"), event(STATUS_TEST, "test")]

    write_json(DATA_DIR / "login-partitions.data.json", login_rows())
    write_json(DATA_DIR / "checkout-partitions.data.json", checkout_rows())
    write_json(DATA_DIR / "order-status-matrix.data.json", order_status_rows())
    write_json(COLLECTION_PATH, collection)
    print("Built DDT rows: login=39, checkout=41, order-status=43 (123 automated TC IDs).")


# JavaScript constants are defined below so the Python build logic stays easy
# to audit against the three DDT requests.

LOGIN_PRE_REQUEST = r"""
const tcId = String(pm.iterationData.get('tc_id') || '');
if (!tcId) { pm.execution.skipRequest(); return; }

const number = Number(tcId.slice(-3));
const base = pm.environment.get('base_url');
const sid = pm.environment.get('student_id') || '23127207';
const seedEmail = pm.environment.get('user_email');
const seedPassword = pm.environment.get('user_password');
const casePassword = 'Hw06-' + pm.variables.replaceIn('{{$guid}}');
const caseEmail = 'hw06-login-' + number + '-' + pm.info.iteration + '-' + Date.now() + '@test.local';

pm.variables.set('setup_error', '');
pm.variables.set('case_email', caseEmail);
pm.variables.set('case_password', casePassword);

function headers(token) {
  const result = [{key: 'X-Student-Id', value: sid}, {key: 'Content-Type', value: 'application/json'}];
  if (token) result.push({key: 'Authorization', value: 'Bearer ' + token});
  return result;
}
function send(method, path, body, token, callback) {
  pm.sendRequest({
    url: base + path,
    method,
    header: headers(token),
    body: body === undefined ? undefined : {mode: 'raw', raw: JSON.stringify(body)}
  }, callback);
}
function recordSetupError(label, err, response) {
  if (err) pm.variables.set('setup_error', label + ': ' + err.message);
  else if (!response || response.code >= 400) pm.variables.set('setup_error', label + ': HTTP ' + (response && response.code));
}
function bodyForCase() {
  const email = pm.iterationData.get('register_user') ? caseEmail : seedEmail;
  const password = pm.iterationData.get('register_user') ? casePassword : seedPassword;
  switch (number) {
    case 2: return {email, password: 'wrong-' + casePassword};
    case 3: return {email: 'missing-' + Date.now() + '@test.local', password: 'unknown'};
    case 4: return {password: seedPassword};
    case 5: return {email};
    case 6: return {email: '', password: seedPassword};
    case 7: return {email, password: 'abc'};
    case 8: return {email: 'not-an-email', password: 'unknown'};
    case 9: return {email: ' ' + email + ' ', password};
    case 10: return {email: null, password: seedPassword};
    case 11: return {email, password: null};
    case 12: return {email: 123, password: seedPassword};
    case 13: return {email, password: {value: password}};
    case 14: return [];
    case 16: return {email, password, rememberMe: true};
    case 17: return {email, password: 'wrong-' + casePassword};
    case 19: return {email, password: 'wrong-third-' + casePassword};
    case 25: return {email: "' OR 1=1 --", password: 'irrelevant'};
    case 26: return {email, password: "' OR 1=1 --"};
    case 27: return {email: '<script>alert(1)</script>', password: 'irrelevant'};
    case 30: return {email, password, role: 'admin'};
    case 35: return {email, password: 'wrong-' + casePassword};
    default: return {email, password};
  }
}

pm.variables.set('case_body', JSON.stringify(bodyForCase()));
if (number === 15) pm.request.headers.remove('Content-Type');
else pm.request.headers.upsert({key: 'Content-Type', value: 'application/json'});

function delayThenFinish() {
  const delay = Number(pm.iterationData.get('delay_ms') || 0);
  if (delay > 0) setTimeout(function () {}, delay);
}
function injectFailures(remaining) {
  if (remaining <= 0) { delayThenFinish(); return; }
  send('POST', '/api/login', {email: caseEmail, password: 'wrong-' + remaining + '-' + casePassword}, null,
    function (err, response) {
      if (err || !response || (response.code !== 401 && response.code !== 403)) {
        recordSetupError('pre-failure', err, response);
        return;
      }
      injectFailures(remaining - 1);
    });
}

if (pm.iterationData.get('register_user')) {
  send('POST', '/api/register', {name: 'HW06 Coverage ' + number, email: caseEmail, password: casePassword}, null,
    function (err, response) {
      recordSetupError('register', err, response);
      if (!err && response && response.code < 400) injectFailures(Number(pm.iterationData.get('pre_failures') || 0));
    });
} else {
  delayThenFinish();
}
"""


LOGIN_TEST = r"""
const tcId = String(pm.iterationData.get('tc_id') || '');
if (!tcId) return;
const number = Number(tcId.slice(-3));
const mode = String(pm.environment.get('spec_strict') || 'off').toLowerCase();

function shouldRun() { return mode === 'full' || (mode === 'canary' && tcId === 'TC-API-LOGIN-018'); }
function specTest(name, fn) { if (shouldRun()) pm.test(tcId + ' - ' + name, fn); }
function jsonOf(response) { try { return response.json(); } catch (_) { return {}; } }
function expectedStatus(code) {
  const expected = String(pm.iterationData.get('expected_status'));
  if (expected === '4xx') return code >= 400 && code < 500;
  return expected.split('|').map(Number).indexOf(code) !== -1;
}
function noSecrets(value) {
  const text = JSON.stringify(value || {}).toLowerCase();
  return ['password', 'reset_token', 'login_attempts', 'locked_until'].every(key => text.indexOf(key) === -1);
}
function setupOk() { pm.expect(pm.variables.get('setup_error') || '').to.eql(''); }
function request(method, path, token, callback) {
  const headers = [{key: 'X-Student-Id', value: pm.environment.get('student_id') || '23127207'}];
  if (token) headers.push({key: 'Authorization', value: 'Bearer ' + token});
  pm.sendRequest({url: pm.environment.get('base_url') + path, method, header: headers}, callback);
}

const payload = jsonOf(pm.response);
if (number === 17) {
  request('GET', '/api/admin/users', pm.environment.get('adminToken'), function (err, response) {
    specTest('first failure increments the counter exactly once', function () {
      setupOk();
      pm.expect(pm.response.code).to.eql(401);
      pm.expect(err).to.eql(null);
      pm.expect(response.code).to.eql(200);
      const user = jsonOf(response).find(item => item.email === pm.variables.get('case_email'));
      pm.expect(user, 'registered user is observable').to.be.an('object');
      pm.expect(user.login_attempts).to.eql(1);
    });
  });
} else if (number === 31) {
  request('GET', '/api/users/me', payload.token, function (err, response) {
    specTest('issued token resolves to the same user', function () {
      setupOk();
      pm.expect(pm.response.code).to.eql(200);
      pm.expect(err).to.eql(null);
      pm.expect(response.code).to.eql(200);
      pm.expect(jsonOf(response).id).to.eql(payload.user.id);
    });
  });
} else if (number === 20 || number === 32) {
  specTest('locked response keeps the generic public contract', function () {
    setupOk();
    pm.expect(expectedStatus(pm.response.code)).to.eql(true);
    pm.expect(payload).to.not.have.property('token');
    pm.expect(payload.error).to.eql('Invalid email or password');
  });
} else if ([28, 29, 36, 39].indexOf(number) !== -1) {
  specTest('successful response excludes sensitive fields', function () {
    setupOk();
    pm.expect(pm.response.code).to.eql(200);
    pm.expect(noSecrets(payload)).to.eql(true);
  });
} else if (number === 30) {
  specTest('body role cannot elevate the authenticated user', function () {
    setupOk();
    pm.expect(pm.response.code).to.eql(200);
    pm.expect(payload.user.role).to.eql('user');
  });
} else if (number === 33) {
  specTest('success schema is typed', function () {
    setupOk();
    pm.expect(pm.response.code).to.eql(200);
    pm.expect(payload.token).to.be.a('string').and.not.empty;
    pm.expect(payload.user.id).to.be.a('number');
    pm.expect(payload.user.email).to.be.a('string');
    pm.expect(payload.user.role).to.be.a('string');
  });
} else if (number === 34) {
  specTest('response content type is JSON', function () {
    setupOk();
    pm.expect(pm.response.code).to.eql(200);
    pm.expect(pm.response.headers.get('Content-Type') || '').to.match(/application\/json/i);
  });
} else if (number === 35) {
  specTest('wrong-password error uses the generic JSON schema', function () {
    setupOk();
    pm.expect(pm.response.code).to.eql(401);
    pm.expect(payload.error).to.be.a('string');
    pm.expect(payload).to.not.have.property('token');
  });
} else if (number === 27) {
  specTest('XSS input is not reflected', function () {
    setupOk();
    pm.expect(expectedStatus(pm.response.code)).to.eql(true);
    pm.expect(JSON.stringify(payload)).to.not.include('<script>alert(1)</script>');
  });
} else if (number === 40) {
  specTest('JWT has iat and exp with a maximum 24-hour TTL', function () {
    setupOk();
    pm.expect(pm.response.code).to.eql(200);
    const segment = String(payload.token || '').split('.')[1] || '';
    const normalized = segment.replace(/-/g, '+').replace(/_/g, '/');
    const decoded = JSON.parse(atob(normalized.padEnd(Math.ceil(normalized.length / 4) * 4, '=')));
    pm.expect(decoded.iat).to.be.a('number');
    pm.expect(decoded.exp).to.be.a('number');
    pm.expect(decoded.exp - decoded.iat).to.be.at.most(86400);
  });
} else {
  specTest(String(pm.iterationData.get('scenario')), function () {
    setupOk();
    pm.expect(expectedStatus(pm.response.code), 'HTTP status follows specification').to.eql(true);
    if ([1, 16].indexOf(number) !== -1) {
      pm.expect(payload.token).to.be.a('string').and.not.empty;
      pm.expect(payload.user).to.be.an('object');
    }
    if (number === 21) pm.expect(payload).to.not.have.property('token');
  });
}
"""


CHECKOUT_PRE_REQUEST = r"""
const tcId = String(pm.iterationData.get('tc_id') || '');
if (!tcId) { pm.execution.skipRequest(); return; }

const number = Number(tcId.slice(-3));
const base = pm.environment.get('base_url');
const sid = pm.environment.get('student_id') || '23127207';
const caseEmail = 'hw06-checkout-' + number + '-' + pm.info.iteration + '-' + Date.now() + '@test.local';
const casePassword = 'Hw06-' + pm.variables.replaceIn('{{$guid}}');
const cartTotal = Number(pm.iterationData.get('cart_total') || 200000);

pm.variables.set('setup_error', '');
pm.variables.set('case_email', caseEmail);
pm.variables.set('case_password', casePassword);
pm.variables.set('case_cart_total', cartTotal);

function headers(token) {
  const result = [{key: 'X-Student-Id', value: sid}, {key: 'Content-Type', value: 'application/json'}];
  if (token) result.push({key: 'Authorization', value: 'Bearer ' + token});
  return result;
}
function send(method, path, body, token, callback) {
  pm.sendRequest({
    url: base + path,
    method,
    header: headers(token),
    body: body === undefined ? undefined : {mode: 'raw', raw: JSON.stringify(body)}
  }, callback);
}
function fail(label, err, response) {
  if (err) pm.variables.set('setup_error', label + ': ' + err.message);
  else if (!response || response.code >= 400) pm.variables.set('setup_error', label + ': HTTP ' + (response && response.code));
}
function bodyForCase() {
  const body = {total_amount: 200000, shipping_address: '123 Le Loi'};
  switch (number) {
    case 5: body.total_amount = 0; break;
    case 6: case 38: body.total_amount = -500000; break;
    case 7: body.total_amount = '200000'; break;
    case 8: body.total_amount = null; break;
    case 9: delete body.shipping_address; break;
    case 10: body.shipping_address = ''; break;
    case 11: body.shipping_address = 'A'.repeat(1001); break;
    case 12: case 42: body.shipping_address = '<img src=x onerror=alert(1)>'; break;
    case 13: body.shipping_address = "' OR 1=1 --"; break;
    case 14: body.shipping_address = '12 Lê Lợi, Quận 1, TP.HCM'; break;
    case 15: body.total_amount = 200000.5; break;
    case 16: body.total_amount = 9000000000000000000; break;
    case 17: body.role = 'admin'; break;
    case 22: case 40: body.total_amount = 1; break;
    case 25: case 30: body.user_id = 999; break;
    case 32: body.shipping_address = '<script>alert(1)</script>'; break;
    case 37: body.total_amount = 1; break;
  }
  return body;
}

const caseBody = bodyForCase();
pm.variables.set('case_body_object', JSON.stringify(caseBody));
pm.variables.set('case_body', number === 18
  ? '{"total_amount":2e5,"shipping_address":"123 Le Loi"}'
  : JSON.stringify(caseBody));

function configureAuthorization(token) {
  pm.variables.set('case_token', token || '');
  const kind = String(pm.iterationData.get('auth_kind') || 'user');
  if (kind === 'none') {
    pm.request.headers.remove('Authorization');
    pm.variables.set('case_authorization', '');
  } else if (kind === 'malformed') {
    pm.request.headers.upsert({key: 'Authorization', value: 'abc'});
    pm.variables.set('case_authorization', 'abc');
  } else if (kind === 'invalid') {
    pm.request.headers.upsert({key: 'Authorization', value: 'Bearer invalid.signature.token'});
    pm.variables.set('case_authorization', 'Bearer invalid.signature.token');
  } else {
    pm.request.headers.upsert({key: 'Authorization', value: 'Bearer ' + token});
    pm.variables.set('case_authorization', 'Bearer ' + token);
  }
}
function addCartThenFinish(token) {
  configureAuthorization(token);
  if (!pm.iterationData.get('cart_setup')) return;
  send('POST', '/api/cart', {product_id: 1, quantity: 1, price: cartTotal, name: 'HW06 coverage item'}, token,
    function (err, response) { fail('add cart', err, response); });
}

send('POST', '/api/register', {name: 'HW06 Checkout ' + number, email: caseEmail, password: casePassword}, null,
  function (registerErr, registerResponse) {
    fail('register', registerErr, registerResponse);
    if (registerErr || !registerResponse || registerResponse.code >= 400) return;
    const registered = registerResponse.json();
    pm.variables.set('case_user_id', registered.id);
    send('POST', '/api/login', {email: caseEmail, password: casePassword}, null,
      function (loginErr, loginResponse) {
        fail('login', loginErr, loginResponse);
        if (loginErr || !loginResponse || loginResponse.code >= 400) return;
        addCartThenFinish(loginResponse.json().token);
      });
  });
"""


CHECKOUT_TEST = r"""
const tcId = String(pm.iterationData.get('tc_id') || '');
if (!tcId) return;
const number = Number(tcId.slice(-3));
const mode = String(pm.environment.get('spec_strict') || 'off').toLowerCase();

function specTest(name, fn) { if (mode === 'full') pm.test(tcId + ' - ' + name, fn); }
function jsonOf(response) { try { return response.json(); } catch (_) { return {}; } }
function setupOk() { pm.expect(pm.variables.get('setup_error') || '').to.eql(''); }
function statusMatches(code, expected) {
  expected = String(expected);
  if (expected === 'not-5xx') return code < 500;
  if (expected === '4xx') return code >= 400 && code < 500;
  if (expected === 'reject-or-sanitize') return code >= 200 && code < 500;
  return expected.split('|').map(Number).indexOf(code) !== -1;
}
function request(method, path, body, token, callback) {
  const headers = [
    {key: 'X-Student-Id', value: pm.environment.get('student_id') || '23127207'},
    {key: 'Content-Type', value: 'application/json'}
  ];
  if (token) headers.push({key: 'Authorization', value: 'Bearer ' + token});
  pm.sendRequest({
    url: pm.environment.get('base_url') + path,
    method,
    header: headers,
    body: body === undefined ? undefined : {mode: 'raw', raw: JSON.stringify(body)}
  }, callback);
}
function noSecrets(value) {
  const text = JSON.stringify(value || {}).toLowerCase();
  return ['password', 'reset_token', 'login_attempts', 'locked_until'].every(key => text.indexOf(key) === -1);
}
function assertMain() {
  setupOk();
  pm.expect(statusMatches(pm.response.code, pm.iterationData.get('expected_status')), 'HTTP status follows specification').to.eql(true);
}

const payload = jsonOf(pm.response);
const token = pm.variables.get('case_token');
const body = JSON.parse(pm.variables.get('case_body_object'));
const orderId = payload.orderId;

if ([1, 17, 18, 19, 24, 25, 26, 30, 33, 35, 36, 37].indexOf(number) !== -1) {
  request('GET', '/api/orders/' + orderId, undefined, token, function (err, response) {
    specTest(String(pm.iterationData.get('scenario')), function () {
      assertMain();
      pm.expect(err).to.eql(null);
      pm.expect(response.code).to.eql(200);
      const order = jsonOf(response);
      if ([1, 18, 37].indexOf(number) !== -1) pm.expect(order.total_amount).to.eql(Number(pm.variables.get('case_cart_total')));
      if ([19, 26].indexOf(number) !== -1) pm.expect(order.status).to.eql('pending');
      if ([17, 25, 30].indexOf(number) !== -1) pm.expect(order.user_id).to.eql(Number(pm.variables.get('case_user_id')));
      if ([24, 35].indexOf(number) !== -1) pm.expect(orderId).to.be.a('number').and.above(0);
      if (number === 33) {
        pm.expect(payload.message).to.be.a('string');
        pm.expect(orderId).to.be.a('number');
      }
      if (number === 36) pm.expect(noSecrets(order)).to.eql(true);
    });
  });
} else if ([20, 39].indexOf(number) !== -1) {
  request('GET', '/api/cart', undefined, token, function (err, response) {
    specTest('successful checkout clears the cart', function () {
      assertMain();
      pm.expect(err).to.eql(null);
      pm.expect(response.code).to.eql(200);
      pm.expect(jsonOf(response)).to.be.an('array').that.is.empty;
    });
  });
} else if (number === 21) {
  request('POST', '/api/checkout', body, token, function (err, response) {
    specTest('duplicate checkout remains a controlled observable result', function () {
      assertMain();
      pm.expect(err).to.eql(null);
      pm.expect(response.code).to.be.below(500);
      const second = jsonOf(response);
      if (pm.response.code === 200 && response.code === 200) pm.expect(second.orderId).to.not.eql(orderId);
    });
  });
} else if (number === 23) {
  request('GET', '/api/orders/my-orders', undefined, token, function (err, response) {
    specTest('created order appears in the authenticated user history', function () {
      assertMain();
      pm.expect(err).to.eql(null);
      pm.expect(response.code).to.eql(200);
      const orders = jsonOf(response);
      pm.expect(orders.some(order => order.id === orderId && order.status === 'pending')).to.eql(true);
    });
  });
} else if ([31, 41].indexOf(number) !== -1) {
  request('GET', '/api/orders/' + orderId, undefined, null, function (err, response) {
    specTest('order detail rejects an anonymous IDOR read', function () {
      setupOk();
      pm.expect(pm.response.code).to.eql(200);
      pm.expect(err).to.eql(null);
      pm.expect([401, 403]).to.include(response.code);
    });
  });
} else if ([12, 32, 42].indexOf(number) !== -1) {
  if (pm.response.code >= 400 && pm.response.code < 500) {
    specTest('XSS address is rejected or safely persisted', function () { setupOk(); });
  } else {
    request('GET', '/api/orders/' + orderId, undefined, token, function (err, response) {
      specTest('XSS address is rejected or safely persisted', function () {
        setupOk();
        pm.expect(pm.response.code).to.eql(200);
        pm.expect(err).to.eql(null);
        pm.expect(response.code).to.eql(200);
        pm.expect(jsonOf(response).shipping_address).to.not.eql(body.shipping_address);
      });
    });
  }
} else if (number === 34) {
  specTest('response content type is JSON', function () {
    assertMain();
    pm.expect(pm.response.headers.get('Content-Type') || '').to.match(/application\/json/i);
  });
} else {
  specTest(String(pm.iterationData.get('scenario')), function () { assertMain(); });
}
"""


STATUS_PRE_REQUEST = r"""
const tcId = String(pm.iterationData.get('tc_id') || '');
if (!tcId) { pm.execution.skipRequest(); return; }

const number = Number(tcId.slice(-3));
const base = pm.environment.get('base_url');
const sid = pm.environment.get('student_id') || '23127207';
const userToken = pm.environment.get('userToken');
const adminToken = pm.environment.get('adminToken');
pm.variables.set('setup_error', '');

function headers(token) {
  const result = [{key: 'X-Student-Id', value: sid}, {key: 'Content-Type', value: 'application/json'}];
  if (token) result.push({key: 'Authorization', value: 'Bearer ' + token});
  return result;
}
function send(method, path, body, token, callback) {
  pm.sendRequest({
    url: base + path,
    method,
    header: headers(token),
    body: body === undefined ? undefined : {mode: 'raw', raw: JSON.stringify(body)}
  }, callback);
}
function fail(label, err, response) {
  if (err) pm.variables.set('setup_error', label + ': ' + err.message);
  else if (!response || response.code >= 400) pm.variables.set('setup_error', label + ': HTTP ' + (response && response.code));
}
function transitionsFor(status) {
  if (status === 'confirmed') return ['confirmed'];
  if (status === 'shipping') return ['confirmed', 'shipping'];
  if (status === 'delivered') return ['confirmed', 'shipping', 'delivered'];
  if (status === 'canceled') return ['canceled'];
  return [];
}
function setState(orderId, transitions, index, done) {
  if (index >= transitions.length) { done(); return; }
  send('PUT', '/api/admin/orders/' + orderId + '/status', {status: transitions[index]}, adminToken,
    function (err, response) {
      fail('set state ' + transitions[index], err, response);
      if (!err && response && response.code < 400) setState(orderId, transitions, index + 1, done);
    });
}
function configure(orderId, attackerToken) {
  let path = '/api/admin/orders/' + orderId + '/status';
  let body = {status: pm.iterationData.get('to_status') || 'confirmed'};
  let auth = 'Bearer ' + adminToken;
  switch (number) {
    case 26: path = '/api/admin/orders/999999/status'; break;
    case 27: path = '/api/admin/orders/-1/status'; break;
    case 28: path = '/api/admin/orders/abc/status'; break;
    case 29: body = {}; break;
    case 30: body = {status: 'DELIVERED'}; break;
    case 31: auth = ''; break;
    case 32: auth = 'Bearer invalid.signature.token'; break;
    case 33: case 34: case 39: auth = 'Bearer ' + userToken; break;
    case 40: auth = 'Bearer ' + attackerToken; break;
    case 35: case 37: case 38: body = {status: 'confirmed'}; break;
    case 36: body = {status: 'delivered'}; break;
    case 42: body = {status: 'canceled'}; break;
    case 43:
      path = '/api/orders/' + orderId + '/cancel';
      body = {};
      auth = 'Bearer ' + userToken;
      break;
    case 44: body = {status: ['delivered']}; break;
  }
  pm.variables.set('case_status_path', path);
  pm.variables.set('case_status_body', JSON.stringify(body));
  pm.variables.set('case_authorization', auth);
  if (auth) pm.request.headers.upsert({key: 'Authorization', value: auth});
  else pm.request.headers.remove('Authorization');
}
function createAttackerThenConfigure(orderId) {
  if (number !== 40) { configure(orderId, ''); return; }
  const email = 'hw06-status-attacker-' + Date.now() + '@test.local';
  const password = 'Hw06-' + pm.variables.replaceIn('{{$guid}}');
  send('POST', '/api/register', {name: 'HW06 Status Attacker', email, password}, null,
    function (registerErr, registerResponse) {
      fail('register attacker', registerErr, registerResponse);
      if (registerErr || !registerResponse || registerResponse.code >= 400) return;
      send('POST', '/api/login', {email, password}, null, function (loginErr, loginResponse) {
        fail('login attacker', loginErr, loginResponse);
        if (!loginErr && loginResponse && loginResponse.code < 400) configure(orderId, loginResponse.json().token);
      });
    });
}

send('POST', '/api/checkout', {total_amount: 200000, shipping_address: 'HW06 status coverage'}, userToken,
  function (checkoutErr, checkoutResponse) {
    fail('create order', checkoutErr, checkoutResponse);
    if (checkoutErr || !checkoutResponse || checkoutResponse.code >= 400) return;
    const orderId = checkoutResponse.json().orderId;
    pm.variables.set('case_order_id', orderId);
    const desired = String(pm.iterationData.get('from_status') || 'pending');
    setState(orderId, transitionsFor(desired), 0, function () { createAttackerThenConfigure(orderId); });
  });
"""


STATUS_TEST = r"""
const tcId = String(pm.iterationData.get('tc_id') || '');
if (!tcId) return;
const number = Number(tcId.slice(-3));
const mode = String(pm.environment.get('spec_strict') || 'off').toLowerCase();

function specTest(name, fn) { if (mode === 'full') pm.test(tcId + ' - ' + name, fn); }
function jsonBody() { try { return pm.response.json(); } catch (_) { return {}; } }
function setupOk() { pm.expect(pm.variables.get('setup_error') || '').to.eql(''); }
function statusMatches(code) {
  const expected = String(pm.iterationData.get('expected_status'));
  if (expected === '4xx') return code >= 400 && code < 500;
  return expected.split('|').map(Number).indexOf(code) !== -1;
}
function noSecrets(value) {
  const text = JSON.stringify(value || {}).toLowerCase();
  return ['password', 'token', 'secret', 'reset_token', 'login_attempts', 'locked_until'].every(key => text.indexOf(key) === -1);
}

const payload = jsonBody();
specTest(String(pm.iterationData.get('scenario') || (pm.iterationData.get('from_status') + ' to ' + pm.iterationData.get('to_status'))), function () {
  setupOk();
  pm.expect(statusMatches(pm.response.code), 'HTTP status follows specification').to.eql(true);
  if (number === 26) pm.expect(payload.error).to.eql('Order not found');
  if (number === 35) pm.expect(payload.message).to.be.a('string');
  if (number === 36) pm.expect(payload.error).to.be.a('string');
  if (number === 37) pm.expect(pm.response.headers.get('Content-Type') || '').to.match(/application\/json/i);
  if (number === 38) pm.expect(noSecrets(payload)).to.eql(true);
  if (number === 44) pm.expect(String(payload.error || '').toLowerCase()).to.not.include('state transition');
});
"""


if __name__ == "__main__":
    main()
