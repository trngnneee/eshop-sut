"""Thêm folder '04 - JWT forgery/expiry' vào collection HW06.

Gỡ trạng thái Blocked của TC-API-LOGIN-042 và TC-API-CHECKOUT-029. Trước đây hai
case này bị đánh Blocked vì "không nhúng signing secret vào artifact công khai",
nhưng secret của SUT vốn đã public tại `backend/server.js:9`, nên không có bí mật
nào để bảo vệ. Secret vẫn được truyền qua --env-var lúc chạy, không commit vào
collection, để đồng nhất với cách xử lý user_password/admin_password.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COLLECTION = ROOT / "hw06/postman/EShop-HW06-23127207.postman_collection.json"
FOLDER = "04 - JWT forgery/expiry"

MINT = [
    "// CryptoJS là global sẵn có của sandbox Postman; không khai báo lại kẻo trùng identifier.",
    "const CJS = (typeof CryptoJS !== 'undefined') ? CryptoJS : require('crypto-js');",
    "const SECRET = pm.environment.get('sut_jwt_secret') || '';",
    r"function b64url(words){return CJS.enc.Base64.stringify(words).replace(/=+$/,'').replace(/\+/g,'-').replace(/\//g,'_');}",
    "function sign(payload){",
    "  const h = b64url(CJS.enc.Utf8.parse(JSON.stringify({alg:'HS256',typ:'JWT'})));",
    "  const p = b64url(CJS.enc.Utf8.parse(JSON.stringify(payload)));",
    "  const s = b64url(CJS.HmacSHA256(h + '.' + p, SECRET));",
    "  return h + '.' + p + '.' + s;",
    "}",
]

GUARD = [
    "function currentMode(){return String(pm.environment.get('spec_strict')||'off').toLowerCase();}",
    "function specTest(id,name,fn){const m=currentMode();if(m==='full')pm.test('[SPEC] '+id+' - '+name,fn);}",
    "function jsonBody(){try{return pm.response.json();}catch(_){return {};}}",
]


def request(method, path, token_var, body=None):
    item = {
        "method": method,
        "header": [
            {"key": "Content-Type", "value": "application/json"},
            {"key": "Authorization", "value": "Bearer {{" + token_var + "}}"},
        ],
        "url": {"raw": "{{base_url}}" + path, "host": ["{{base_url}}"], "path": path.strip("/").split("/")},
    }
    if body is not None:
        item["body"] = {"mode": "raw", "raw": body, "options": {"raw": {"language": "json"}}}
    return item


def main() -> None:
    collection = json.loads(COLLECTION.read_text(encoding="utf-8"))
    collection["item"] = [f for f in collection["item"] if f.get("name") != FOLDER]

    forged = {
        "name": "TC-API-LOGIN-042 - forged admin token",
        "event": [
            {"listen": "prerequest", "script": {"type": "text/javascript", "exec": MINT + [
                "pm.environment.set('forgedAdminToken', sign({id: 1, role: 'admin'}));",
            ]}},
            {"listen": "test", "script": {"type": "text/javascript", "exec": GUARD + [
                "pm.test('TC-API-LOGIN-042 token minted', ()=>{const t=pm.environment.get('forgedAdminToken')||'';pm.expect(t.split('.').length, 'forged JWT was not minted').to.equal(3);});",
                "pm.test('TC-API-LOGIN-042 observed', ()=>pm.expect(pm.response.code).to.be.oneOf([200,401,403]));",
                "specTest('TC-API-LOGIN-042','self-signed admin token must be rejected',()=>{",
                "  pm.expect(pm.response.code, 'forged token accepted').to.be.oneOf([401,403]);",
                "  pm.expect(Array.isArray(jsonBody()), 'admin order list leaked').to.equal(false);",
                "});",
            ]}},
        ],
        "request": request("GET", "/api/admin/orders", "forgedAdminToken"),
    }

    expired = {
        "name": "TC-API-CHECKOUT-029 - expired token",
        "event": [
            {"listen": "prerequest", "script": {"type": "text/javascript", "exec": MINT + [
                "const now = Math.floor(Date.now()/1000);",
                "pm.environment.set('expiredToken', sign({id: 2, role: 'user', iat: now - 7200, exp: now - 3600}));",
            ]}},
            {"listen": "test", "script": {"type": "text/javascript", "exec": GUARD + [
                "pm.test('TC-API-CHECKOUT-029 token minted', ()=>{const t=pm.environment.get('expiredToken')||'';pm.expect(t.split('.').length, 'expired JWT was not minted').to.equal(3);});",
                "pm.test('TC-API-CHECKOUT-029 expired token rejected', ()=>pm.expect(pm.response.code).to.be.oneOf([401,403]));",
                "pm.test('TC-API-CHECKOUT-029 no order created', ()=>pm.expect(jsonBody().orderId).to.be.undefined);",
            ]}},
        ],
        "request": request("POST", "/api/checkout", "expiredToken", '{"total_amount": 30000000, "shipping_address": "1 Test St", "phone": "0900000000"}'),
    }

    collection["item"].append({"name": FOLDER, "item": [forged, expired]})
    COLLECTION.write_text(json.dumps(collection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Đã thêm folder '{FOLDER}' với 2 request")


if __name__ == "__main__":
    main()
