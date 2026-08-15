#!/usr/bin/env python3
"""
HW05 - Sinh 4 test plan JMeter (Load / Stress / Spike / Soak) cho workflow
"Category-guided buy" cua Dang Truong Nguyen - 23127438.

Workflow (1 VU / 1 iteration):
  1. POST /api/login                (auth-heavy)   -> extract token
  2. GET  /api/categories           (read-heavy)
  3. GET  /api/products?search=...  (read-heavy)
  4. POST /api/cart                 (transactional, Bearer)
  5. POST /api/checkout             (transactional, Bearer) -> extract orderId

Data-driven bang nguyen_users.csv (60 users, recycle).
"""
import os

STUDENT = "23127438"
DATE = "20260815"
OUT = os.path.join(os.path.dirname(__file__), "..", "testplans")

CSV_VARS = "email,password,category_hint,search,product_id,product_name,quantity,price,total_amount,shipping_address"


def timer(delay_ms, range_ms, label):
    return f"""
<UniformRandomTimer guiclass="UniformRandomTimerGui" testclass="UniformRandomTimer" testname="{label}" enabled="true">
  <stringProp name="ConstantTimer.delay">{delay_ms}</stringProp>
  <stringProp name="RandomTimer.range">{range_ms}</stringProp>
</UniformRandomTimer>
<hashTree/>"""


def assert_code(code="200"):
    return f"""
<ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Assert HTTP {code}" enabled="true">
  <collectionProp name="Asserion.test_strings">
    <stringProp name="0">{code}</stringProp>
  </collectionProp>
  <stringProp name="Assertion.custom_message"></stringProp>
  <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
  <boolProp name="Assertion.assume_success">false</boolProp>
  <intProp name="Assertion.test_type">8</intProp>
</ResponseAssertion>
<hashTree/>"""


def assert_contains(text, label):
    return f"""
<ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="{label}" enabled="true">
  <collectionProp name="Asserion.test_strings">
    <stringProp name="0">{text}</stringProp>
  </collectionProp>
  <stringProp name="Assertion.custom_message"></stringProp>
  <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
  <boolProp name="Assertion.assume_success">false</boolProp>
  <intProp name="Assertion.test_type">16</intProp>
</ResponseAssertion>
<hashTree/>"""


def assert_jsonpath(path, label):
    return f"""
<JSONPathAssertion guiclass="JSONPathAssertionGui" testclass="JSONPathAssertion" testname="{label}" enabled="true">
  <stringProp name="JSON_PATH">{path}</stringProp>
  <stringProp name="EXPECTED_VALUE"></stringProp>
  <boolProp name="JSONVALIDATION">false</boolProp>
  <boolProp name="EXPECT_NULL">false</boolProp>
  <boolProp name="INVERT">false</boolProp>
  <boolProp name="ISREGEX">true</boolProp>
</JSONPathAssertion>
<hashTree/>"""


def json_extract(var, path, default):
    return f"""
<JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="Extract {var}" enabled="true">
  <stringProp name="JSONPostProcessor.referenceNames">{var}</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">{path}</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
  <stringProp name="JSONPostProcessor.defaultValues">{default}</stringProp>
</JSONPostProcessor>
<hashTree/>"""


def auth_header():
    return """
<HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="Authorization Bearer" enabled="true">
  <collectionProp name="HeaderManager.headers">
    <elementProp name="" elementType="Header">
      <stringProp name="Header.name">Authorization</stringProp>
      <stringProp name="Header.value">Bearer ${token}</stringProp>
    </elementProp>
  </collectionProp>
</HeaderManager>
<hashTree/>"""


def http_sampler(name, method, path, body=None, query_args=None):
    if body is not None:
        args = f"""<elementProp name="" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">{body}</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>"""
        raw = '<boolProp name="HTTPSampler.postBodyRaw">true</boolProp>\n  '
    elif query_args:
        args = "".join(f"""<elementProp name="{k}" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">true</boolProp>
        <stringProp name="Argument.name">{k}</stringProp>
        <stringProp name="Argument.value">{v}</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
        <boolProp name="HTTPArgument.use_equals">true</boolProp>
      </elementProp>""" for k, v in query_args.items())
        raw = ""
    else:
        args, raw = "", ""
    return f"""
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{name}" enabled="true">
  {raw}<elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables">
    <collectionProp name="Arguments.arguments">{args}</collectionProp>
  </elementProp>
  <stringProp name="HTTPSampler.domain"></stringProp>
  <stringProp name="HTTPSampler.port"></stringProp>
  <stringProp name="HTTPSampler.protocol"></stringProp>
  <stringProp name="HTTPSampler.path">{path}</stringProp>
  <stringProp name="HTTPSampler.method">{method}</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
  <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
  <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
  <stringProp name="HTTPSampler.connect_timeout">10000</stringProp>
  <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
</HTTPSamplerProxy>"""


def workflow(think):
    """5 samplers + children. think = dict buoc -> (delay, range)."""
    login_body = '{"email":"${email}","password":"${password}"}'
    cart_body = ('{"product_id":${product_id},"quantity":${quantity},'
                 '"name":"${product_name}","price":${price}}')
    checkout_body = '{"total_amount":${total_amount},"shipping_address":"${shipping_address}"}'
    x = http_sampler("01 POST /api/login", "POST", "/api/login", body=login_body)
    x += "\n<hashTree>"
    x += json_extract("token", "$.token", "TOKEN_MISSING")
    x += assert_code()
    x += assert_jsonpath("$.token", "Assert body has token")
    x += timer(*think["login"], "Think-time sau login")
    x += "\n</hashTree>"

    x += http_sampler("02 GET /api/categories", "GET", "/api/categories")
    x += "\n<hashTree>"
    x += assert_code()
    x += assert_jsonpath("$[0].name", "Assert categories array non-empty")
    x += timer(*think["categories"], "Think-time xem danh muc")
    x += "\n</hashTree>"

    x += http_sampler("03 GET /api/products?search", "GET", "/api/products",
                      query_args={"search": "${search}"})
    x += "\n<hashTree>"
    x += assert_code()
    x += assert_jsonpath("$[0].id", "Assert search co ket qua")
    x += timer(*think["search"], "Think-time chon san pham")
    x += "\n</hashTree>"

    x += http_sampler("04 POST /api/cart", "POST", "/api/cart", body=cart_body)
    x += "\n<hashTree>"
    x += auth_header()
    x += assert_code()
    x += assert_contains("Added to cart", "Assert cart message")
    x += timer(*think["cart"], "Think-time truoc checkout")
    x += "\n</hashTree>"

    x += http_sampler("05 POST /api/checkout", "POST", "/api/checkout", body=checkout_body)
    x += "\n<hashTree>"
    x += auth_header()
    x += json_extract("orderId", "$.orderId", "ORDER_MISSING")
    x += assert_code()
    x += assert_jsonpath("$.orderId", "Assert co orderId")
    x += timer(*think["checkout"], "Think-time ket thuc phien")
    x += "\n</hashTree>"
    return x


def thread_group(name, threads, ramp, duration, delay, think):
    return f"""
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="{name}" enabled="true">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller">
    <boolProp name="LoopController.continue_forever">false</boolProp>
    <intProp name="LoopController.loops">-1</intProp>
  </elementProp>
  <stringProp name="ThreadGroup.num_threads">{threads}</stringProp>
  <stringProp name="ThreadGroup.ramp_time">{ramp}</stringProp>
  <boolProp name="ThreadGroup.scheduler">true</boolProp>
  <stringProp name="ThreadGroup.duration">{duration}</stringProp>
  <stringProp name="ThreadGroup.delay">{delay}</stringProp>
  <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
  <boolProp name="ThreadGroup.delayedStart">false</boolProp>
</ThreadGroup>
<hashTree>{workflow(think)}
</hashTree>"""


SAVE_CONFIG = """<objProp>
    <name>saveConfig</name>
    <value class="SampleSaveConfiguration">
      <time>true</time><latency>true</latency><timestamp>true</timestamp><success>true</success>
      <label>true</label><code>true</code><message>true</message><threadName>true</threadName>
      <dataType>true</dataType><encoding>false</encoding><assertions>true</assertions>
      <subresults>true</subresults><responseData>false</responseData><samplerData>false</samplerData>
      <xml>false</xml><fieldNames>true</fieldNames><responseHeaders>false</responseHeaders>
      <requestHeaders>false</requestHeaders><responseDataOnError>false</responseDataOnError>
      <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
      <assertionsResultsToSave>0</assertionsResultsToSave><bytes>true</bytes><sentBytes>true</sentBytes>
      <url>true</url><threadCounts>true</threadCounts><idleTime>true</idleTime><connectTime>true</connectTime>
    </value>
  </objProp>"""


def listener(guiclass, name):
    return f"""
<ResultCollector guiclass="{guiclass}" testclass="ResultCollector" testname="{name}" enabled="true">
  <boolProp name="ResultCollector.error_logging">false</boolProp>
  {SAVE_CONFIG}
  <stringProp name="filename"></stringProp>
</ResultCollector>
<hashTree/>"""


def test_plan(plan_name, thread_groups_xml, listener_xml):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="{plan_name}" enabled="true">
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
    </TestPlan>
    <hashTree>
      <ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP Request Defaults" enabled="true">
        <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables">
          <collectionProp name="Arguments.arguments"/>
        </elementProp>
        <stringProp name="HTTPSampler.domain">localhost</stringProp>
        <stringProp name="HTTPSampler.port">3000</stringProp>
        <stringProp name="HTTPSampler.protocol">http</stringProp>
      </ConfigTestElement>
      <hashTree/>
      <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="Content-Type JSON" enabled="true">
        <collectionProp name="HeaderManager.headers">
          <elementProp name="" elementType="Header">
            <stringProp name="Header.name">Content-Type</stringProp>
            <stringProp name="Header.value">application/json</stringProp>
          </elementProp>
        </collectionProp>
      </HeaderManager>
      <hashTree/>
      <CSVDataSet guiclass="TestBeanGUI" testclass="CSVDataSet" testname="CSV nguyen_users" enabled="true">
        <stringProp name="delimiter">,</stringProp>
        <stringProp name="fileEncoding">UTF-8</stringProp>
        <stringProp name="filename">nguyen_users.csv</stringProp>
        <boolProp name="ignoreFirstLine">true</boolProp>
        <boolProp name="quotedData">true</boolProp>
        <boolProp name="recycle">true</boolProp>
        <stringProp name="shareMode">shareMode.all</stringProp>
        <boolProp name="stopThread">false</boolProp>
        <stringProp name="variableNames">{CSV_VARS}</stringProp>
      </CSVDataSet>
      <hashTree/>{thread_groups_xml}{listener_xml}
    </hashTree>
  </hashTree>
</jmeterTestPlan>
"""


# ---- Think-time profiles (ms) ----
THINK_NORMAL = {"login": (1000, 1000), "categories": (1000, 1000),
                "search": (1000, 2000), "cart": (1000, 0), "checkout": (1000, 0)}
THINK_STRESS = {k: (500, 500) for k in THINK_NORMAL}
THINK_SPIKE = {k: (300, 400) for k in THINK_NORMAL}

PLANS = {
    # Load: 20 VU, ramp 60s, giu 5 phut - tai binh thuong, think-time thuc te
    f"{STUDENT}_Load_{DATE}": (
        thread_group("Load 20 VU", 20, 60, 300, 0, THINK_NORMAL),
        listener("SummaryReport", "Summary Report"),
    ),
    # Stress: bac thang 50 -> 100 -> 200 VU, moi bac +60s ramp, tong 7 phut
    f"{STUDENT}_Stress_{DATE}": (
        thread_group("Step 1: 50 VU (t=0s)", 50, 60, 420, 0, THINK_STRESS)
        + thread_group("Step 2: +50 VU (t=120s)", 50, 60, 300, 120, THINK_STRESS)
        + thread_group("Step 3: +100 VU (t=240s)", 100, 60, 180, 240, THINK_STRESS),
        listener("StatVisualizer", "Aggregate Report"),
    ),
    # Spike: nen 10 VU trong 5 phut, dot bien +150 VU tai t=90s trong 60s
    f"{STUDENT}_Spike_{DATE}": (
        thread_group("Baseline 10 VU", 10, 10, 300, 0, THINK_SPIKE)
        + thread_group("SPIKE +150 VU (t=90s, 60s)", 150, 10, 60, 90, THINK_SPIKE),
        listener("ViewResultsFullVisualizer", "View Results Tree"),
    ),
    # Soak: 30 VU giu 12 phut - tim endurance threshold
    f"{STUDENT}_Soak_{DATE}": (
        thread_group("Soak 30 VU x 12 phut", 30, 60, 720, 0, THINK_NORMAL),
        listener("GraphVisualizer", "Graph Results"),
    ),
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, (tgs, lst) in PLANS.items():
        path = os.path.join(OUT, name + ".jmx")
        with open(path, "w", encoding="utf-8") as f:
            f.write(test_plan(name, tgs, lst))
        print("written:", os.path.abspath(path))
