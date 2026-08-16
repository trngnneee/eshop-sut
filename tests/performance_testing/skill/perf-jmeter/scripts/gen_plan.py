#!/usr/bin/env python3
"""
perf-jmeter skill — sinh 4 test plan JMeter (Load / Stress / Spike / Soak) cho
BẤT KỲ endpoint group nào, từ một file spec JSON (không hard-code workflow).

Usage:
    python3 gen_plan.py <spec.json> [output_dir]

Spec JSON schema (xem examples/category_guided_buy.json):
{
  "plan_prefix": "23127438",              # tiền tố tên file .jmx
  "date": "20260815",                      # optional, mặc định = hôm nay
  "base": {"host": "localhost", "port": 3000, "protocol": "http"},
  "csv":  {"file": "users.csv", "variables": ["email","password", ...]},
  "steps": [
    {
      "name": "01 POST /api/login",
      "method": "POST",
      "path": "/api/login",
      "body": "{\"email\":\"${email}\",\"password\":\"${password}\"}",
      "auth": false,                        # true => gắn header Bearer ${token}
      "extract": [{"var":"token","jsonpath":"$.token","default":"MISSING"}],
      "assert_code": 200,
      "assert_jsonpath": ["$.token"],
      "assert_contains": [],
      "think_ms": [1000, 1000]              # [delay, random-range]
    }
  ],
  "scenarios": {                            # optional — có default hợp lý
    "load":  {"vu": 20, "ramp": 60, "duration": 300},
    "stress":{"peak": 200},
    "spike": {"baseline": 10, "burst": 150, "at": 90, "for": 60, "total": 300},
    "soak":  {"vu": 30, "minutes": 12}
  }
}
"""
import json, os, sys
from datetime import datetime

# ---------------------------------------------------------------- XML emitters
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


_HEADER_TMPL = """
<HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="Authorization Bearer" enabled="true">
  <collectionProp name="HeaderManager.headers">
    <elementProp name="" elementType="Header">
      <stringProp name="Header.name">Authorization</stringProp>
      <stringProp name="Header.value">Bearer ${__TOKEN__}</stringProp>
    </elementProp>
  </collectionProp>
</HeaderManager>
<hashTree/>"""


def auth_header(token_var="token"):
    return _HEADER_TMPL.replace("__TOKEN__", token_var)


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


# ---------------------------------------------------------------- build from spec
def step_xml(step, factor):
    x = http_sampler(step["name"], step["method"].upper(), step["path"],
                     body=step.get("body"), query_args=step.get("query"))
    x += "\n<hashTree>"
    if step.get("auth"):
        x += auth_header(step.get("token_var", "token"))
    for ex in step.get("extract", []):
        x += json_extract(ex["var"], ex["jsonpath"], ex.get("default", "MISSING"))
    x += assert_code(str(step.get("assert_code", 200)))
    for jp in step.get("assert_jsonpath", []):
        x += assert_jsonpath(jp, f"Assert jsonpath {jp}")
    for c in step.get("assert_contains", []):
        x += assert_contains(c, f"Assert contains: {c}")
    d, r = step.get("think_ms", [1000, 1000])
    x += timer(int(d * factor), int(r * factor), f"Think-time {step['name']}")
    x += "\n</hashTree>"
    return x


def workflow_xml(steps, factor):
    return "".join(step_xml(s, factor) for s in steps)


def thread_group(name, threads, ramp, duration, delay, wf_xml):
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
<hashTree>{wf_xml}
</hashTree>"""


_SAVE_CONFIG = """<objProp>
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
  {_SAVE_CONFIG}
  <stringProp name="filename"></stringProp>
</ResultCollector>
<hashTree/>"""


def test_plan(plan_name, base, csv_cfg, thread_groups_xml, listener_xml):
    variables = ",".join(csv_cfg["variables"])
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
        <stringProp name="HTTPSampler.domain">{base.get('host','localhost')}</stringProp>
        <stringProp name="HTTPSampler.port">{base.get('port',3000)}</stringProp>
        <stringProp name="HTTPSampler.protocol">{base.get('protocol','http')}</stringProp>
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
      <CSVDataSet guiclass="TestBeanGUI" testclass="CSVDataSet" testname="CSV data" enabled="true">
        <stringProp name="delimiter">,</stringProp>
        <stringProp name="fileEncoding">UTF-8</stringProp>
        <stringProp name="filename">{csv_cfg['file']}</stringProp>
        <boolProp name="ignoreFirstLine">true</boolProp>
        <boolProp name="quotedData">true</boolProp>
        <boolProp name="recycle">true</boolProp>
        <stringProp name="shareMode">shareMode.all</stringProp>
        <boolProp name="stopThread">false</boolProp>
        <stringProp name="variableNames">{variables}</stringProp>
      </CSVDataSet>
      <hashTree/>{thread_groups_xml}{listener_xml}
    </hashTree>
  </hashTree>
</jmeterTestPlan>
"""


# ---------------------------------------------------------------- scenarios
def build_scenarios(steps, sc):
    load = sc.get("load", {})
    stress = sc.get("stress", {})
    spike = sc.get("spike", {})
    soak = sc.get("soak", {})

    wf_n = workflow_xml(steps, 1.0)     # think-time thực tế
    wf_s = workflow_xml(steps, 0.5)     # stress: think-time ngắn hơn
    wf_k = workflow_xml(steps, 0.3)     # spike: think-time rất ngắn

    # Load
    lv = load.get("vu", 20)
    load_tg = thread_group(f"Load {lv} VU", lv, load.get("ramp", 60),
                           load.get("duration", 300), 0, wf_n)

    # Stress: bậc thang tới peak (25% / +25% / +50%)
    peak = stress.get("peak", 200)
    s1, s2 = max(1, peak // 4), max(1, peak // 4)
    s3 = max(1, peak - s1 - s2)
    stress_tg = (thread_group(f"Step 1: {s1} VU (t=0s)", s1, 60, 420, 0, wf_s)
                 + thread_group(f"Step 2: +{s2} VU (t=120s)", s2, 60, 300, 120, wf_s)
                 + thread_group(f"Step 3: +{s3} VU (t=240s)", s3, 60, 180, 240, wf_s))

    # Spike: nền + burst
    base_vu = spike.get("baseline", 10)
    burst = spike.get("burst", 150)
    at = spike.get("at", 90)
    dur = spike.get("for", 60)
    total = spike.get("total", 300)
    spike_tg = (thread_group(f"Baseline {base_vu} VU", base_vu, 10, total, 0, wf_k)
                + thread_group(f"SPIKE +{burst} VU (t={at}s, {dur}s)", burst, 10, dur, at, wf_k))

    # Soak
    kv = soak.get("vu", 30)
    kmin = soak.get("minutes", 12)
    soak_tg = thread_group(f"Soak {kv} VU x {kmin} phut", kv, 60, kmin * 60, 0, wf_n)

    return {
        "Load":   (load_tg,   listener("SummaryReport", "Summary Report")),
        "Stress": (stress_tg, listener("StatVisualizer", "Aggregate Report")),
        "Spike":  (spike_tg,  listener("ViewResultsFullVisualizer", "View Results Tree")),
        "Soak":   (soak_tg,   listener("GraphVisualizer", "Graph Results")),
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    os.makedirs(out, exist_ok=True)

    prefix = spec.get("plan_prefix", "PERF")
    date = spec.get("date") or datetime.now().strftime("%Y%m%d")
    base = spec.get("base", {})
    csv_cfg = spec["csv"]
    steps = spec["steps"]
    scenarios = build_scenarios(steps, spec.get("scenarios", {}))

    for scen, (tg_xml, lst_xml) in scenarios.items():
        name = f"{prefix}_{scen}_{date}"
        path = os.path.join(out, name + ".jmx")
        with open(path, "w", encoding="utf-8") as f:
            f.write(test_plan(name, base, csv_cfg, tg_xml, lst_xml))
        print("written:", os.path.abspath(path))


if __name__ == "__main__":
    main()
