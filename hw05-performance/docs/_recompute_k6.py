"""Independent recompute of p95 / error% from k6 --out json (NDJSON)."""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

LOGS = Path(__file__).resolve().parents[1] / "logs"
LABELS = ["login", "search", "detail", "cart", "checkout"]
FILES = {
    "Load": LOGS / "23127271_Load_20260814.json",
    "Stress": LOGS / "23127271_Stress_20260814.json",
    "Spike": LOGS / "23127271_Spike_20260814.json",
    "Soak": LOGS / "23127271_Soak_20260814.json",
}


def pct(sorted_vals, p):
    if not sorted_vals:
        return None
    n = len(sorted_vals)
    if n == 1:
        return float(sorted_vals[0])
    k = (n - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_vals[int(k)])
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def parse_ts(s):
    if not s:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def st(ms_list):
    if not ms_list:
        return None
    s = sorted(ms_list)
    return {
        "n": len(s),
        "mean": sum(s) / len(s),
        "p50": pct(s, 50),
        "p90": pct(s, 90),
        "p95": pct(s, 95),
        "p99": pct(s, 99),
        "max": s[-1],
    }


def load_points(path: Path):
    durs = []
    fail_n = 0
    fail_tot = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            if '"type":"Point"' not in line:
                continue
            o = json.loads(line)
            if o.get("type") != "Point":
                continue
            metric = o.get("metric")
            data = o.get("data") or {}
            tags = data.get("tags") or {}
            val = data.get("value")
            name = tags.get("name") or ""
            if metric == "http_req_duration":
                durs.append((parse_ts(data.get("time")), name, float(val)))
            elif metric == "http_req_failed":
                fail_tot += 1
                if float(val) >= 1:
                    fail_n += 1
    return durs, fail_n, fail_tot


def print_st(label, s):
    if not s:
        print(f"  {label}: n=0")
        return
    print(
        f"  {label}: n={s['n']} mean={s['mean']:.2f} p50={s['p50']:.2f} "
        f"p90={s['p90']:.2f} p95={s['p95']:.2f} p99={s['p99']:.2f} max={s['max']:.2f}"
    )


def summarize(name, path: Path):
    if not path.exists():
        print(name, "MISSING")
        return
    print("=" * 72)
    print(name, path.name, "bytes", path.stat().st_size)
    durs, fail_n, fail_tot = load_points(path)
    print(f"http_req_duration n={len(durs)}")
    print(f"http_req_failed {fail_n}/{fail_tot} ({100.0 * fail_n / max(fail_tot, 1):.4f}%)")
    by = defaultdict(list)
    all_ms = []
    for _, lab, ms in durs:
        all_ms.append(ms)
        by[lab].append(ms)
    print("OVERALL")
    print_st("overall", st(all_ms))
    for lab in LABELS:
        print_st(lab, st(by.get(lab, [])))

    times = [t for t, _, _ in durs if t]
    if times:
        t0, t1 = min(times), max(times)
        span = (t1 - t0).total_seconds()
        print(f"t0={t0.isoformat()} t1={t1.isoformat()} span_s={span:.3f}")
        cut_lo = t0.timestamp() + 0.2 * (t1.timestamp() - t0.timestamp())
        cut_hi = t1.timestamp() - 0.2 * (t1.timestamp() - t0.timestamp())
        first = [ms for t, lab, ms in durs if t and t.timestamp() <= cut_lo]
        last = [ms for t, lab, ms in durs if t and t.timestamp() >= cut_hi]
        first_ck = [
            ms for t, lab, ms in durs if t and t.timestamp() <= cut_lo and lab == "checkout"
        ]
        last_ck = [
            ms for t, lab, ms in durs if t and t.timestamp() >= cut_hi and lab == "checkout"
        ]
        fs, ls = st(first), st(last)
        fck, lck = st(first_ck), st(last_ck)
        print(
            f"first20% n={len(first)} p95={fs['p95'] if fs else None} "
            f"checkout p95={fck['p95'] if fck else None}"
        )
        print(
            f"last20% n={len(last)} p95={ls['p95'] if ls else None} "
            f"checkout p95={lck['p95'] if lck else None}"
        )
        rps = len(durs) / max(span, 0.001)
        print(f"wall http_req_duration rps={rps:.4f} (sleep in wall-clock)")

        if name == "Spike":

            def phase(t):
                rel = (t - t0).total_seconds()
                if rel < 30:
                    return "baseline_0_30s"
                if rel < 32:
                    return "jump_30_32s"
                if rel < 92:
                    return "hold_32_92s"
                if rel < 97:
                    return "drop_92_97s"
                return "recover_97_end"

            ph = defaultdict(list)
            ph_ck = defaultdict(list)
            for t, lab, ms in durs:
                if not t:
                    continue
                p = phase(t)
                ph[p].append(ms)
                if lab == "checkout":
                    ph_ck[p].append(ms)
            print("SPIKE PHASES (relative to first http_req_duration sample)")
            for p in [
                "baseline_0_30s",
                "jump_30_32s",
                "hold_32_92s",
                "drop_92_97s",
                "recover_97_end",
            ]:
                s = st(ph[p])
                ck = st(ph_ck[p])
                print(
                    f"  {p}: n={s['n'] if s else 0} p95={s['p95'] if s else None} "
                    f"checkout p95={ck['p95'] if ck else None}"
                )


def main():
    for name, path in FILES.items():
        summarize(name, path)


if __name__ == "__main__":
    main()
