"""P10: compute metrics from RAW JMeter .jtl (not HTML summaries)."""
from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

LOGS = Path(__file__).resolve().parents[1] / "logs"
FILES = {
    "Load": LOGS / "23127271_Load_20260814.jtl",
    "Stress": LOGS / "23127271_Stress_20260814.jtl",
    "Spike": LOGS / "23127271_Spike_20260814.jtl",
    "Soak": LOGS / "23127271_Soak_20260814.jtl",
}
LABELS = ["login", "search", "detail", "cart", "checkout"]
ICT = timezone(timedelta(hours=7))


def pct(sorted_vals, p):
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def stats(elapsed):
    if not elapsed:
        return None
    s = sorted(elapsed)
    n = len(s)
    return {
        "n": n,
        "mean": sum(s) / n,
        "median": pct(s, 50),
        "p90": pct(s, 90),
        "p95": pct(s, 95),
        "p99": pct(s, 99),
        "max": s[-1],
        "min": s[0],
    }


def fmt(x, nd=2):
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def load_rows(path: Path):
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                ts = int(r["timeStamp"])
                el = int(r["elapsed"])
            except (KeyError, ValueError):
                continue
            code = (r.get("responseCode") or "").strip()
            success = (r.get("success") or "").strip().lower() == "true"
            label = (r.get("label") or "").strip()
            rows.append(
                {
                    "ts": ts,
                    "elapsed": el,
                    "label": label,
                    "code": code,
                    "success": success,
                    "failmsg": r.get("failureMessage") or "",
                    "grp": r.get("grpThreads") or "",
                }
            )
    rows.sort(key=lambda x: x["ts"])
    return rows


def code_bucket(code: str) -> str:
    if not code:
        return "empty"
    if code.isdigit():
        n = int(code)
        if 200 <= n < 300:
            return "2xx"
        if n in (401, 403):
            return "401/403"
        if 400 <= n < 500:
            return "4xx-other"
        if 500 <= n < 600:
            return "5xx"
        return f"http-{n}"
    return code  # Non HTTP Status, Connection refused, etc.


def analyze(name, rows):
    n = len(rows)
    if n == 0:
        return {"name": name, "empty": True}

    t0, t1 = rows[0]["ts"], rows[-1]["ts"]
    wall_s = max((t1 - t0) / 1000.0, 0.001)
    fail = [r for r in rows if not r["success"]]
    non2xx = [r for r in rows if code_bucket(r["code"]) != "2xx"]
    login_lock = [
        r
        for r in rows
        if r["label"] == "login" and r["code"] in ("401", "403")
    ]
    buckets = Counter(code_bucket(r["code"]) for r in rows)
    fail_codes = Counter(r["code"] for r in fail)
    fail_labels = Counter(r["label"] for r in fail)
    fail_msgs = Counter((r["failmsg"] or "(empty)")[:120] for r in fail)

    by_label = defaultdict(list)
    for r in rows:
        by_label[r["label"]].append(r["elapsed"])

    # first vs last 20% of timestamp span
    span = t1 - t0
    cut_lo = t0 + 0.20 * span
    cut_hi = t1 - 0.20 * span
    first = [r for r in rows if r["ts"] <= cut_lo]
    last = [r for r in rows if r["ts"] >= cut_hi]
    mid = [r for r in rows if cut_lo < r["ts"] < cut_hi]

    # Stress: after ramp (P04: drop first 25s if Stress 100 / 25s ramp; first guess was 15s)
    after_ramp = [r for r in rows if r["ts"] >= t0 + 25000]

    # Spike phases from P01: 30s baseline, jump 2s, hold 60s, drop 5s, recover 90s
    # Use timestamp relative to first sample
    def phase(r):
        rel = (r["ts"] - t0) / 1000.0
        if rel < 30:
            return "baseline_0_30s"
        if rel < 32:
            return "jump_30_32s"
        if rel < 92:
            return "hold_32_92s"
        if rel < 97:
            return "drop_92_97s"
        return "recover_97_end"

    phases = defaultdict(list)
    for r in rows:
        phases[phase(r)].append(r)

    # max grpThreads
    max_thr = 0
    for r in rows:
        try:
            max_thr = max(max_thr, int(r["grp"] or 0))
        except ValueError:
            pass

    return {
        "name": name,
        "empty": False,
        "n": n,
        "t0": t0,
        "t1": t1,
        "wall_s": wall_s,
        "rps": n / wall_s,
        "max_thr": max_thr,
        "fail_n": len(fail),
        "fail_pct": 100.0 * len(fail) / n,
        "non2xx_n": len(non2xx),
        "non2xx_pct": 100.0 * len(non2xx) / n,
        "login_lock_n": len(login_lock),
        "buckets": buckets,
        "fail_codes": fail_codes,
        "fail_labels": fail_labels,
        "fail_msgs": fail_msgs,
        "overall": stats([r["elapsed"] for r in rows]),
        "by_label": {lab: stats(by_label.get(lab, [])) for lab in LABELS},
        "other_labels": sorted(set(by_label) - set(LABELS)),
        "first": {
            "n": len(first),
            "fail_pct": 100.0 * sum(1 for r in first if not r["success"]) / max(len(first), 1),
            "overall": stats([r["elapsed"] for r in first]),
            "checkout": stats([r["elapsed"] for r in first if r["label"] == "checkout"]),
            "login": stats([r["elapsed"] for r in first if r["label"] == "login"]),
        },
        "last": {
            "n": len(last),
            "fail_pct": 100.0 * sum(1 for r in last if not r["success"]) / max(len(last), 1),
            "overall": stats([r["elapsed"] for r in last]),
            "checkout": stats([r["elapsed"] for r in last if r["label"] == "checkout"]),
            "login": stats([r["elapsed"] for r in last if r["label"] == "login"]),
        },
        "after_ramp": {
            "n": len(after_ramp),
            "fail_pct": 100.0 * sum(1 for r in after_ramp if not r["success"]) / max(len(after_ramp), 1),
            "overall": stats([r["elapsed"] for r in after_ramp]),
            "checkout": stats([r["elapsed"] for r in after_ramp if r["label"] == "checkout"]),
        },
        "phases": {
            k: {
                "n": len(v),
                "fail_pct": 100.0 * sum(1 for r in v if not r["success"]) / max(len(v), 1),
                "rps": len(v) / max((v[-1]["ts"] - v[0]["ts"]) / 1000.0, 0.001) if v else 0,
                "overall": stats([r["elapsed"] for r in v]),
                "checkout": stats([r["elapsed"] for r in v if r["label"] == "checkout"]),
                "login": stats([r["elapsed"] for r in v if r["label"] == "login"]),
                "max_thr": max((int(r["grp"] or 0) for r in v), default=0),
            }
            for k, v in phases.items()
        },
    }


def ts_ict(ms):
    return datetime.fromtimestamp(ms / 1000.0, tz=ICT).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def print_st(st, prefix=""):
    if not st:
        print(f"{prefix}—")
        return
    print(
        f"{prefix}n={st['n']}  mean={st['mean']:.2f}  med={st['median']:.2f}  "
        f"p90={st['p90']:.2f}  p95={st['p95']:.2f}  p99={st['p99']:.2f}  max={st['max']}  min={st['min']}"
    )


def main():
    for name, path in FILES.items():
        print("=" * 80)
        print(name, path.name, "exists" if path.exists() else "MISSING", "bytes", path.stat().st_size if path.exists() else 0)
        rows = load_rows(path)
        a = analyze(name, rows)
        if a["empty"]:
            print("EMPTY")
            continue
        print(f"samples={a['n']}  wall={a['wall_s']:.3f}s  rps={a['rps']:.4f}  maxThreads={a['max_thr']}")
        print(f"t0={a['t0']} ({ts_ict(a['t0'])} ICT)  t1={a['t1']} ({ts_ict(a['t1'])} ICT)")
        print(f"success=false: {a['fail_n']} ({a['fail_pct']:.4f}%)")
        print(f"non-2xx:       {a['non2xx_n']} ({a['non2xx_pct']:.4f}%)")
        print(f"login 401/403: {a['login_lock_n']}")
        print("code buckets:", dict(a["buckets"]))
        if a["fail_n"]:
            print("fail codes:", dict(a["fail_codes"]))
            print("fail labels:", dict(a["fail_labels"]))
            print("fail msgs (top 8):", a["fail_msgs"].most_common(8))
        print("OVERALL elapsed ms:")
        print_st(a["overall"], "  ")
        print("BY LABEL:")
        for lab in LABELS:
            print(f"  {lab}:")
            print_st(a["by_label"][lab], "    ")
        if a["other_labels"]:
            print("  OTHER LABELS:", a["other_labels"])
        print("FIRST 20% of timestamp span:")
        print(f"  n={a['first']['n']} fail%={a['first']['fail_pct']:.4f}")
        print("  overall p95:", fmt(a["first"]["overall"]["p95"] if a["first"]["overall"] else None))
        print("  checkout p95:", fmt(a["first"]["checkout"]["p95"] if a["first"]["checkout"] else None))
        print("  login p95:", fmt(a["first"]["login"]["p95"] if a["first"]["login"] else None))
        print("LAST 20% of timestamp span:")
        print(f"  n={a['last']['n']} fail%={a['last']['fail_pct']:.4f}")
        print("  overall p95:", fmt(a["last"]["overall"]["p95"] if a["last"]["overall"] else None))
        print("  checkout p95:", fmt(a["last"]["checkout"]["p95"] if a["last"]["checkout"] else None))
        print("  login p95:", fmt(a["last"]["login"]["p95"] if a["last"]["login"] else None))
        print("AFTER +25s (ramp-aware):")
        print(f"  n={a['after_ramp']['n']} fail%={a['after_ramp']['fail_pct']:.4f}")
        print_st(a["after_ramp"]["overall"], "  overall ")
        print_st(a["after_ramp"]["checkout"], "  checkout ")
        if name == "Spike":
            print("SPIKE PHASES:")
            for k in ["baseline_0_30s", "jump_30_32s", "hold_32_92s", "drop_92_97s", "recover_97_end"]:
                ph = a["phases"].get(k)
                if not ph:
                    print(f"  {k}: missing")
                    continue
                print(f"  {k}: n={ph['n']} fail%={ph['fail_pct']:.4f} rps={ph['rps']:.2f} maxThr={ph['max_thr']}")
                print_st(ph["overall"], "    overall ")
                print_st(ph["checkout"], "    checkout ")
                print_st(ph["login"], "    login ")


if __name__ == "__main__":
    main()
