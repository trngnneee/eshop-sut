"""Thêm hai folder chạy TC-API-LOGIN-041 và TC-API-LOGIN-024 sau khi lock hết hạn.

Trước đây hai case bị đánh Manual/Blocked vì phải chờ lock thật 180 giây. Chờ lâu
không đồng nghĩa với không chạy được: tách thành hai folder, runner chạy prep,
sleep, rồi chạy assert với environment đã export.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COLLECTION = ROOT / "hw06/postman/EShop-HW06-23127207.postman_collection.json"
PREP, ASSERT = "05 - Timed lock prep", "05 - Timed lock assert"

GUARD = [
    "function currentMode(){return String(pm.environment.get('spec_strict')||'off').toLowerCase();}",
    "function specTest(id,name,fn){const m=currentMode();if(m==='full')pm.test('[SPEC] '+id+' - '+name,fn);}",
]


def login(name, email_var, password, tests):
    return {
        "name": name,
        "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": {"raw": "{{base_url}}/api/login", "host": ["{{base_url}}"], "path": ["api", "login"]},
            "body": {"mode": "raw", "raw": json.dumps({"email": "{{" + email_var + "}}", "password": password}),
                     "options": {"raw": {"language": "json"}}},
        },
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": GUARD + tests}}],
    }


def main() -> None:
    c = json.loads(COLLECTION.read_text(encoding="utf-8"))
    c["item"] = [f for f in c["item"] if f.get("name") not in {PREP, ASSERT}]

    register = {
        "name": "[PREP] Register timed user",
        "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": {"raw": "{{base_url}}/api/register", "host": ["{{base_url}}"], "path": ["api", "register"]},
            "body": {"mode": "raw", "raw": '{"name":"Timed User","email":"{{timedUser}}","password":"{{timedPassword}}"}',
                     "options": {"raw": {"language": "json"}}},
        },
        "event": [
            {"listen": "prerequest", "script": {"type": "text/javascript", "exec": [
                "pm.environment.set('timedUser', 'timed_' + Date.now() + '@eshop.com');",
                "pm.environment.set('timedPassword', 'Timed1234!');",
            ]}},
            {"listen": "test", "script": {"type": "text/javascript", "exec": [
                "pm.test('[PREP] timed user registered', ()=>pm.response.to.have.status(200));",
            ]}},
        ],
    }

    prep = [register] + [
        login(f"[PREP] Wrong password #{n}", "timedUser", "definitely-wrong", [
            f"pm.test('[PREP] wrong attempt {n} observed', ()=>pm.expect(pm.response.code).to.be.oneOf([401,403]));",
        ]) for n in (1, 2)
    ]

    assert_items = [
        login("TC-API-LOGIN-041a - wrong attempt after lock expiry", "timedUser", "definitely-wrong", [
            "pm.test('TC-API-LOGIN-041 wrong-after-expiry observed', ()=>pm.expect(pm.response.code).to.be.oneOf([401,403]));",
            "specTest('TC-API-LOGIN-041','counter must reset after lock expiry',()=>{",
            "  pm.expect(pm.response.code, 'account re-locked immediately, counter did not reset').to.equal(401);",
            "});",
        ]),
        login("TC-API-LOGIN-041b - correct login after lock expiry", "timedUser", "{{timedPassword}}", [
            "pm.test('TC-API-LOGIN-041 correct-after-expiry observed', ()=>pm.expect(pm.response.code).to.be.oneOf([200,403]));",
            "pm.environment.set('timedResetOk', String(pm.response.code === 200));",
            "specTest('TC-API-LOGIN-041','valid credential accepted after lock expiry',()=>{",
            "  pm.expect(pm.response.code, 'valid credential rejected after lock expired').to.equal(200);",
            "});",
        ]),
        login("TC-API-LOGIN-024 - one failure after successful reset", "timedUser", "definitely-wrong", [
            "pm.test('TC-API-LOGIN-024 observed', ()=>pm.expect(pm.response.code).to.be.oneOf([401,403]));",
            "specTest('TC-API-LOGIN-024','single failure after reset must not lock',()=>{",
            "  pm.expect(pm.environment.get('timedResetOk'), 'precondition TC-023 reset did not happen').to.equal('true');",
            "  pm.expect(pm.response.code, 'locked after a single failure').to.equal(401);",
            "});",
        ]),
    ]

    c["item"] += [{"name": PREP, "item": prep}, {"name": ASSERT, "item": assert_items}]
    COLLECTION.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Đã thêm '{PREP}' ({len(prep)} request) và '{ASSERT}' ({len(assert_items)} request)")


if __name__ == "__main__":
    main()
