import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def pct(s, p):
    if not s:
        return None
    s = sorted(s)
    n = len(s)
    k = (n - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(s[int(k)])
    return s[f] + (s[c] - s[f]) * (k - f)


logs = Path(r"c:\DiskD\HCMUS\Semester9\SoftwareTesting\SoftwareTesting-HW\HW5\23127271\logs")

for scen in ("Load", "Stress", "Spike", "Soak"):
    p = logs / f"23127271_{scen}_20260814.json"
    metrics = Counter()
    statuses = Counter()
    names = Counter()
    n_dur = 0
    n_fail = 0
    n_fail_true = 0
    with p.open(encoding="utf-8") as f:
        for line in f:
            if '"type":"Point"' not in line:
                continue
            o = json.loads(line)
            if o.get("type") != "Point":
                continue
            m = o.get("metric")
            metrics[m] += 1
            tags = (o.get("data") or {}).get("tags") or {}
            if m == "http_req_duration":
                n_dur += 1
                statuses[tags.get("status", "")] += 1
                names[tags.get("name", "")] += 1
            elif m == "http_req_failed":
                n_fail += 1
                val = (o.get("data") or {}).get("value")
                if val:
                    n_fail_true += 1
    print(f"{scen} k6 duration points", n_dur)
    print(" statuses", dict(statuses))
    print(" names", dict(names))
    print(" http_reqs", metrics.get("http_reqs"), "failed_points", n_fail, "failed_true", n_fail_true)
    print(" metric tops", metrics.most_common(4))

jp = logs / "23127271_Spike_20260814.jtl"
rows = []
with jp.open(encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        rows.append(
            (
                int(r["timeStamp"]),
                r["label"],
                int(r["elapsed"]),
                r["success"],
                r["responseCode"],
            )
        )
t0 = min(x[0] for x in rows)


def phase(ts):
    rel = (ts - t0) / 1000.0
    if rel < 30:
        return "baseline"
    if rel < 32:
        return "jump"
    if rel < 92:
        return "hold"
    if rel < 97:
        return "drop"
    return "recover"


ph = defaultdict(list)
phck = defaultdict(list)
fail = 0
codes = Counter()
for ts, lab, el, ok, code in rows:
    codes[code] += 1
    if ok.lower() != "true":
        fail += 1
    p = phase(ts)
    ph[p].append(el)
    if lab == "checkout":
        phck[p].append(el)
print("JMETER spike n", len(rows), "fail", fail, "codes", dict(codes))
for p in ["baseline", "jump", "hold", "drop", "recover"]:
    print(
        " JMeter",
        p,
        "n",
        len(ph[p]),
        "p95",
        round(pct(ph[p], 95), 2) if ph[p] else None,
        "ck p95",
        round(pct(phck[p], 95), 2) if phck[p] else None,
    )

pairs = [
    ("Load", 22.00, 21.29),
    ("Stress", 534.00, 598.56),
    ("Spike-hold", 464.00, 369.44),
    ("Spike-recover", 23.65, 22.78),
    ("Soak", 23.00, 20.66),
]
print("CHECKOUT p95 delta k6 vs JMeter:")
for name, j, k in pairs:
    print(
        f"  {name}: JMeter={j} k6={k} delta_ms={k-j:.2f} delta_pct={100*(k-j)/j:.1f}%"
    )
