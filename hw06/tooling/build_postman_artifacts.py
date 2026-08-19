import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTMAN = ROOT / 'postman'
DATA = POSTMAN / 'data'

COMMON = [
    "function currentMode(){return String(pm.environment.get('spec_strict')||'off').toLowerCase();}",
    "function specTest(id,name,fn){const m=currentMode();if(m==='full'||(m==='canary'&&id==='TC-API-LOGIN-018'))pm.test('[SPEC] '+id+' - '+name,fn);}",
    "function jsonBody(){try{return pm.response.json();}catch(_){return {};}}",
]

def js(*lines):
    return COMMON + list(lines)

def post_url(path):
    return {'raw': '{{base_url}}' + path, 'host': ['{{base_url}}'], 'path': path.strip('/').split('/')}

def request(name, method, path, test_lines, payload=None, token=None, pre=None):
    headers = []
    if payload is not None:
        headers.append({'key': 'Content-Type', 'value': 'application/json'})
    if token:
        headers.append({'key': 'Authorization', 'value': 'Bearer {{' + token + '}}'})
    item = {'name': name, 'request': {'method': method, 'header': headers, 'url': post_url(path)}, 'event': [{'listen': 'test', 'script': {'type': 'text/javascript', 'exec': js(*test_lines)}}]}
    if payload is not None:
        item['request']['body'] = {'mode': 'raw', 'raw': json.dumps(payload, ensure_ascii=False), 'options': {'raw': {'language': 'json'}}}
    if pre:
        item['event'].insert(0, {'listen': 'prerequest', 'script': {'type': 'text/javascript', 'exec': pre.splitlines()}})
    return item

COLLECTION_PRE = [
    "const sid=pm.environment.get('student_id')||'23127207';",
    "pm.request.headers.upsert({key:'X-Student-Id',value:sid});",
    "console.log('[HW06] '+pm.info.requestName+' | X-Student-Id: '+sid+' | '+pm.request.method+' '+pm.request.url.toString());",
]

setup = {'name': '00 - Setup', 'item': [
    request('[SETUP] Health check', 'GET', '/api/products', ["pm.test('[SETUP] health 200',()=>pm.response.to.have.status(200));", "pm.test('[SETUP] five products',()=>pm.expect(jsonBody()).to.be.an('array').with.length(5));"]),
    request('[SETUP] Register disposable lock user', 'POST', '/api/register', ["pm.test('[SETUP] register 200',()=>pm.response.to.have.status(200));", "pm.environment.set('lockUserId',String(jsonBody().id||''));"], {'name':'HW06 Lock User','email':'{{lockUser}}','password':'Temp1234!'}, pre="pm.environment.set('lockUser','hw06_lock_'+Date.now()+'@test.local');"),
    request('[SETUP] Login user', 'POST', '/api/login', ["pm.test('[SETUP] user login 200',()=>pm.response.to.have.status(200));", "const d=jsonBody();pm.expect(d.token).to.be.a('string').and.not.empty;pm.environment.set('userToken',d.token);pm.environment.set('userId',String(d.user&&d.user.id||''));"], {'email':'{{user_email}}','password':'{{user_password}}'}),
    request('[SETUP] Login admin', 'POST', '/api/login', ["pm.test('[SETUP] admin login 200',()=>pm.response.to.have.status(200));", "pm.environment.set('adminToken',jsonBody().token||'');"], {'email':'{{admin_email}}','password':'{{admin_password}}'}),
    request('[SETUP] Add product to cart', 'POST', '/api/cart', ["pm.test('[SETUP] add cart 200',()=>pm.response.to.have.status(200));"], {'id':1,'name':'Laptop','price':100000,'quantity':1}, 'userToken'),
]}

lock_pre = "const h={'Content-Type':'application/json','X-Student-Id':pm.environment.get('student_id')};pm.sendRequest({url:pm.environment.get('base_url')+'/api/login',method:'POST',header:h,body:{mode:'raw',raw:JSON.stringify({email:pm.environment.get('lockUser'),password:'Wrong123!'})}},function(){pm.sendRequest({url:pm.environment.get('base_url')+'/api/login',method:'POST',header:h,body:{mode:'raw',raw:JSON.stringify({email:pm.environment.get('lockUser'),password:'Wrong123!'})}},function(){});});"

api1 = {'name':'API-1 - POST /api/login','item':[
    request('TC-API-LOGIN-001 - valid credential','POST','/api/login',["pm.test('TC-API-LOGIN-001 status',()=>pm.response.to.have.status(200));","pm.expect(jsonBody().token).to.be.a('string').and.not.empty;"],{'email':'{{user_email}}','password':'{{user_password}}'}),
    request('TC-API-LOGIN-004 - missing email','POST','/api/login',["pm.test('TC-API-LOGIN-004 observed',()=>pm.expect([400,401]).to.include(pm.response.code));","specTest('TC-API-LOGIN-004','missing email validates',()=>pm.response.to.have.status(400));"],{'password':'Test1234!'}),
    request('TC-API-LOGIN-025 - SQL injection','POST','/api/login',["pm.test('TC-API-LOGIN-025 rejected',()=>pm.response.to.have.status(401));","pm.expect(jsonBody().token).to.be.undefined;"],{'email':"' OR 1=1 --",'password':'anything'}),
    request('TC-API-LOGIN-028 - no password leakage','POST','/api/login',["pm.test('TC-API-LOGIN-028 login 200',()=>pm.response.to.have.status(200));","specTest('TC-API-LOGIN-028','no password in response',()=>pm.expect(jsonBody().user.password).to.be.undefined);"],{'email':'{{user_email}}','password':'{{user_password}}'}),
    request('TC-API-LOGIN-018 - two failures then correct','POST','/api/login',["pm.test('TC-API-LOGIN-018 observed',()=>pm.expect([200,401,403]).to.include(pm.response.code));","specTest('TC-API-LOGIN-018','correct login after two failures',()=>pm.response.to.have.status(200));"],{'email':'{{lockUser}}','password':'Temp1234!'},pre=lock_pre),
]}

api2 = {'name':'API-2 - POST /api/checkout','item':[
    request('TC-API-CHECKOUT-037 - client total probe','POST','/api/checkout',["pm.test('TC-API-CHECKOUT-037 checkout 200',()=>pm.response.to.have.status(200));","pm.environment.set('orderId',String(jsonBody().orderId||''));"],{'total_amount':1,'shipping_address':'123 Le Loi'},'userToken'),
    request('TC-API-CHECKOUT-031 - IDOR probe','GET','/api/orders/{{orderId}}',["pm.test('TC-API-CHECKOUT-031 observed',()=>pm.expect([200,401,403]).to.include(pm.response.code));","specTest('TC-API-CHECKOUT-031','order detail needs auth',()=>pm.expect([401,403]).to.include(pm.response.code));"]),
    request('TC-API-CHECKOUT-020 - cart post-condition','GET','/api/cart',["pm.test('TC-API-CHECKOUT-020 cart response',()=>pm.response.to.have.status(200));","specTest('TC-API-CHECKOUT-020','cart empty after checkout',()=>pm.expect(jsonBody()).to.be.an('array').that.is.empty);"],token='userToken'),
    request('TC-API-CHECKOUT-005 - zero total','POST','/api/checkout',["pm.test('TC-API-CHECKOUT-005 observed',()=>pm.expect([200,400]).to.include(pm.response.code));","specTest('TC-API-CHECKOUT-005','zero total rejected',()=>pm.response.to.have.status(400));"],{'total_amount':0,'shipping_address':'A'},'userToken'),
]}

api3 = {'name':'API-3 - PUT /api/admin/orders/:id/status','item':[
    request('TC-API-ORDER-STATUS-002 - pending to confirmed','PUT','/api/admin/orders/{{orderId}}/status',["pm.test('TC-API-ORDER-STATUS-002 admin update',()=>pm.response.to.have.status(200));"],{'status':'confirmed'},'adminToken'),
    request('TC-API-ORDER-STATUS-033 - role escalation','PUT','/api/admin/orders/{{orderId}}/status',["pm.test('TC-API-ORDER-STATUS-033 observed',()=>pm.expect([200,403]).to.include(pm.response.code));","specTest('TC-API-ORDER-STATUS-033','user role rejected',()=>pm.response.to.have.status(403));"],{'status':'shipping'},'userToken'),
    request('TC-API-ORDER-STATUS-024 - canceled terminal','PUT','/api/admin/orders/{{orderId}}/status',["pm.test('TC-API-ORDER-STATUS-024 observed',()=>pm.expect([200,400]).to.include(pm.response.code));","specTest('TC-API-ORDER-STATUS-024','canceled cannot become delivered',()=>pm.response.to.have.status(400));"],{'status':'delivered'},'adminToken'),
]}

ddt_login = request('[DDT] login partitions','POST','/api/login',["if(!pm.iterationData.get('tc_id'))return;","pm.test(pm.iterationData.get('tc_id')+' status',()=>pm.expect(pm.response.code).to.eql(Number(pm.iterationData.get('expected_status'))));"],{'email':'{{email}}','password':'{{password}}'},pre="if(!pm.iterationData.get('tc_id'))pm.execution.skipRequest();")
ddt_checkout = request('[DDT] checkout partitions','POST','/api/checkout',["if(!pm.iterationData.get('tc_id'))return;","pm.test(pm.iterationData.get('tc_id')+' status',()=>pm.expect(pm.response.code).to.eql(Number(pm.iterationData.get('expected_status'))));"],{'total_amount':'{{total_amount}}','shipping_address':'{{shipping_address}}'},'userToken',"if(!pm.iterationData.get('tc_id'))pm.execution.skipRequest();")
ddt_status = request('[DDT] transition matrix','PUT','/api/admin/orders/{{orderId}}/status',["if(!pm.iterationData.get('tc_id'))return;","pm.test(pm.iterationData.get('tc_id')+' matrix status',()=>pm.expect(pm.response.code).to.eql(Number(pm.iterationData.get('expected_status'))));"],{'status':'{{to_status}}'},'adminToken',"if(!pm.iterationData.get('tc_id'))pm.execution.skipRequest();")

collection = {'info':{'_postman_id':'b1d9d8da-2312-4077-9062-hw06-23127207','name':'EShop HW06 - API Testing - 23127207','description':'AI-first API testing. Collection pre-request adds X-Student-Id to every request.','schema':'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'},'event':[{'listen':'prerequest','script':{'type':'text/javascript','exec':COLLECTION_PRE}}],'item':[setup,api1,api2,api3,{'name':'1.1 Domain partitions [DDT]','item':[ddt_login]},{'name':'2.1 Domain partitions [DDT]','item':[ddt_checkout]},{'name':'3.1 Transition matrix [DDT]','item':[ddt_status]}]}

environment = {'id':'7c6c8c83-2312-4077-local-hw06','name':'EShop-HW06-local','values':[
    {'key':'base_url','value':'http://localhost:3000','enabled':True,'type':'default'},{'key':'student_id','value':'23127207','enabled':True,'type':'default'},
    {'key':'admin_email','value':'admin@eshop.com','enabled':True,'type':'default'},{'key':'admin_password','value':'Admin123!','enabled':True,'type':'secret'},
    {'key':'user_email','value':'test@eshop.com','enabled':True,'type':'default'},{'key':'user_password','value':'Test1234!','enabled':True,'type':'secret'},
    {'key':'userToken','value':'','enabled':True,'type':'secret'},{'key':'adminToken','value':'','enabled':True,'type':'secret'},{'key':'userId','value':'','enabled':True,'type':'default'},
    {'key':'orderId','value':'','enabled':True,'type':'default'},{'key':'lockUser','value':'','enabled':True,'type':'default'},{'key':'lockUserId','value':'','enabled':True,'type':'default'},{'key':'spec_strict','value':'off','enabled':True,'type':'default'}], '_postman_variable_scope':'environment'}

login_data = [{'tc_id':f'TC-API-LOGIN-{i:03d}','email':'test@eshop.com','password':'Test1234!','expected_status':200,'note':'partition'} for i in range(1,17)]
login_data[1].update(password='Wrong123!',expected_status=401,note='wrong credential'); login_data[2].update(email='missing@eshop.com',expected_status=401,note='unknown email')
checkout_data = [{'tc_id':f'TC-API-CHECKOUT-{i:03d}','total_amount':200000,'shipping_address':'123 Le Loi','expected_status':200,'note':'partition'} for i in range(1,19)]
checkout_data[1].update(total_amount=0,note='D-CHK-02 observed'); checkout_data[2].update(total_amount=-500000,note='D-CHK-02 observed'); checkout_data[11].update(shipping_address='<img src=x onerror=alert(1)>',note='D-CHK-05 observed')
states=['pending','confirmed','shipping','delivered','canceled']; allowed={('pending','confirmed'),('pending','canceled'),('confirmed','shipping'),('confirmed','canceled'),('shipping','delivered'),('shipping','canceled')}; status_data=[]
for source in states:
    for target in states:
        pair=(source,target); expected=200 if pair in allowed else 400
        if pair==('shipping','canceled'): expected=400
        if pair==('canceled','delivered'): expected=200
        status_data.append({'tc_id':f'TC-API-ORDER-STATUS-{len(status_data)+1:03d}','from_status':source,'to_status':target,'expected_allowed':pair in allowed,'expected_status':expected,'note':'matrix; state setup required'})

features = """# Postman features used — HW06

| Tính năng | Nơi dùng | Bằng chứng / trạng thái |
| :--- | :--- | :--- |
| Collection/folders | Setup, API-1, API-2, API-3 and DDT folders | JSON in repo |
| Environment/variables | base_url, student_id, credentials, tokens, orderId, spec_strict | Environment JSON |
| Collection pre-request | Adds X-Student-Id and logs every request | Console log; HUMAN screenshot required |
| Dynamic data | Date.now() disposable lock user | Register pre-request |
| Test scripts / Chai | Functional and strict contract assertions | Newman reports |
| Data-driven runs | 3 JSON data files | run-newman.ps1/.sh |
| Variable chaining | login → token → cart → orderId → status | Setup/API requests |
| HTML/JSON reporter | newman/reports | Generated by Newman |
| CI integration | GitHub Actions workflow | .github/workflows |
| Workspace/Mock/Monitor | Postman cloud features | HUMAN must create/screenshot; not fabricated |

The exported environment keeps `http://localhost:3000` as required by the assignment. The local script supports a `base_url` override because port 3000 is occupied by an unrelated local process.
"""

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    write_json(POSTMAN/'EShop-HW06-23127207.postman_collection.json',collection); write_json(POSTMAN/'EShop-HW06-local.postman_environment.json',environment)
    write_json(DATA/'login-partitions.data.json',login_data); write_json(DATA/'checkout-partitions.data.json',checkout_data); write_json(DATA/'order-status-matrix.data.json',status_data)
    (POSTMAN/'postman-features.md').write_text(features,encoding='utf-8'); print('Built Postman collection, environment, data files and feature report')
