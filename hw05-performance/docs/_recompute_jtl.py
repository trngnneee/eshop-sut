"""Independent recompute of p95 / error% from RAW .jtl (do not import P10).

Percentile estimators (0-based sorted list `s`, n=len(s)):
  linear  — NIST R7 / Excel PERCENTILE.INC: k=(n-1)*p/100, interpolate
  r6      — NIST R6 / Commons-Math LEGACY-like: h=(n+1)*p/100, interpolate (1-based)
  nearest — ceil(p/100 * n), 1-based, clamp 1..n

Error%: success=false vs responseCode not in 200–299, counted separately.
"""
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
OUT_MD = Path(__file__).with_name("p11-recompute.md")
OUT_CSV = Path(__file__).with_name("_recompute_jtl.csv")

FILES = {
    "Load": LOGS / "23127271_Load_20260814.jtl",
    "Stress": LOGS / "23127271_Stress_20260814.jtl",
    "Spike": LOGS / "23127271_Spike_20260814.jtl",
    "Soak": LOGS / "23127271_Soak_20260814.jtl",
}
HTML = {
    "Load": LOGS / "report_load" / "statistics.json",
    "Stress": LOGS / "report_stress" / "statistics.json",
    "Spike": LOGS / "report_spike" / "statistics.json",
    "Soak": LOGS / "report_soak" / "statistics.json",
}
LABELS = ["login", "search", "detail", "cart", "checkout"]

# P10 table (linear) — compared after we recompute, not used as input
P10_P95 = {
    ("Load", "overall"): 19.00,
    ("Load", "login"): 6.00,
    ("Load", "search"): 3.00,
    ("Load", "detail"): 4.00,
    ("Load", "cart"): 3.00,
    ("Load", "checkout"): 22.00,
    ("Stress", "overall"): 476.00,
    ("Stress", "login"): 506.00,
    ("Stress", "search"): 447.00,
    ("Stress", "detail"): 462.00,
    ("Stress", "cart"): 217.00,
    ("Stress", "checkout"): 534.00,
    ("Spike", "overall"): 381.00,
    ("Spike", "login"): 437.15,
    ("Spike", "search"): 332.00,
    ("Spike", "detail"): 354.00,
    ("Spike", "cart"): 163.00,
    ("Spike", "checkout"): 437.00,
    ("Soak", "overall"): 18.00,
    ("Soak", "login"): 6.00,
    ("Soak", "search"): 4.00,
    ("Soak", "detail"): 4.00,
    ("Soak", "cart"): 3.00,
    ("Soak", "checkout"): 23.00,
}
P10_ERR = {s: 0.0 for s in FILES}
P10_N = {"Load": 4972, "Stress": 104397, "Spike": 24330, "Soak": 5439}
P10_RPS = {"Load": 9.60, "Stress": 321.43, "Spike": 130.30, "Soak": 7.27}
P10_MEDIAN = {
    ("Load", "overall"): 2.00,
    ("Stress", "overall"): 233.00,
    ("Spike", "overall"): 73.00,
    ("Soak", "overall"): 2.00,
}
P10_TREND = {
    "Load": (20.00, 23.90, 19.00, 21.60),
    "Stress": (533.00, 603.30, 456.00, 481.00),
    "Spike": (371.00, 437.95, 18.00, 25.40),
    "Soak": (17.00, 20.00, 19.00, 24.00),
}


def pct_linear(s, p):
    n = len(s)
    if n == 0:
        return None
    if n == 1:
        return float(s[0])
    k = (n - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(s[int(k)])
    return s[f] + (s[c] - s[f]) * (k - f)


def pct_r6(s, p):
    """h = (n+1)*p/100, 1-based interpolate (Commons Math LEGACY / NIST R6)."""
    n = len(s)
    if n == 0:
        return None
    h = (n + 1) * p / 100.0
    if h < 1:
        return float(s[0])
    if h >= n:
        return float(s[-1])
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return float(s[lo - 1])
    return s[lo - 1] + (s[hi - 1] - s[lo - 1]) * (h - lo)


def pct_nearest(s, p):
    n = len(s)
    if n == 0:
        return None
    rank = math.ceil(p / 100.0 * n)
    rank = min(max(rank, 1), n)
    return float(s[rank - 1])


def load_rows(path: Path):
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            try:
                ts = int(r["timeStamp"])
                el = int(r["elapsed"])
            except (KeyError, ValueError):
                continue
            code = (r.get("responseCode") or "").strip()
            success = (r.get("success") or "").strip().lower() == "true"
            label = (r.get("label") or "").strip()
            rows.append((ts, el, label, code, success))
    rows.sort(key=lambda x: x[0])
    return rows


def is_2xx(code: str) -> bool:
    return code.isdigit() and 200 <= int(code) < 300


def summarize(elapsed):
    if not elapsed:
        return None
    s = sorted(elapsed)
    n = len(s)
    return {
        "n": n,
        "mean": sum(s) / n,
        "median_linear": pct_linear(s, 50),
        "median_r6": pct_r6(s, 50),
        "p90_linear": pct_linear(s, 90),
        "p95_linear": pct_linear(s, 95),
        "p95_r6": pct_r6(s, 95),
        "p95_nearest": pct_nearest(s, 95),
        "p99_linear": pct_linear(s, 99),
        "p99_r6": pct_r6(s, 99),
        "max": s[-1],
        "min": s[0],
    }


def close(a, b, tol=0.51):
    if a is None or b is None:
        return False
    return abs(float(a) - float(b)) <= tol


def html_map(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for key, row in data.items():
        lab = "overall" if key == "Total" else key
        out[lab] = {
            "n": row["sampleCount"],
            "errorPct": row["errorPct"],
            "mean": row["meanResTime"],
            "median": row["medianResTime"],
            "p90": row["pct1ResTime"],
            "p95": row["pct2ResTime"],
            "p99": row["pct3ResTime"],
            "throughput": row["throughput"],
        }
    return out


def main():
    csv_rows = []
    blocks = []
    verdicts = []

    for name, path in FILES.items():
        rows = load_rows(path)
        n = len(rows)
        t0, t1 = rows[0][0], rows[-1][0]
        wall = max((t1 - t0) / 1000.0, 0.001)
        fail = sum(1 for r in rows if not r[4])
        non2 = sum(1 for r in rows if not is_2xx(r[3]))
        lock = sum(1 for r in rows if r[2] == "login" and r[3] in ("401", "403"))
        codes = defaultdict(int)
        for r in rows:
            codes[r[3]] += 1
        by = defaultdict(list)
        for r in rows:
            by[r[2]].append(r[1])
        overall_el = [r[1] for r in rows]
        ov = summarize(overall_el)
        html = html_map(HTML[name])

        span = t1 - t0
        first = [r for r in rows if r[0] <= t0 + 0.2 * span]
        last = [r for r in rows if r[0] >= t1 - 0.2 * span]
        first_ov = summarize([r[1] for r in first])
        last_ov = summarize([r[1] for r in last])
        first_ck = summarize([r[1] for r in first if r[2] == "checkout"])
        last_ck = summarize([r[1] for r in last if r[2] == "checkout"])

        fail_pct = 100.0 * fail / n
        non2_pct = 100.0 * non2 / n
        rps = n / wall

        err_ok = fail == 0 and non2 == 0 and close(fail_pct, P10_ERR[name], 0.0001)
        n_ok = n == P10_N[name]
        rps_ok = close(rps, P10_RPS[name], 0.02)

        blocks.append(f"### {name}")
        blocks.append("")
        blocks.append(
            f"File `{path.name}` · N={n} · wall={wall:.3f}s · rps={rps:.4f} · "
            f"`success=false`={fail} ({fail_pct:.4f}%) · non-2xx={non2} ({non2_pct:.4f}%) · "
            f"login 401/403={lock} · codes={dict(codes)}"
        )
        blocks.append("")
        blocks.append(
            "| Label | n | mean | median linear | p95 linear | p95 R6 | p95 nearest | "
            "P10 p95 | HTML pct2 (p95) | vs P10 | vs HTML |"
        )
        blocks.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")

        def row_for(lab, st):
            p10 = P10_P95[(name, lab)]
            h = html.get(lab, {})
            hp95 = h.get("p95")
            vs_p10 = "MATCH" if close(st["p95_linear"], p10) else "MISMATCH"
            # HTML often matches R6 better than linear
            vs_html_lin = "MATCH" if close(st["p95_linear"], hp95) else "diff"
            vs_html_r6 = "MATCH" if close(st["p95_r6"], hp95) else "diff"
            vs_html = f"linear {vs_html_lin}; R6 {vs_html_r6}"
            csv_rows.append(
                {
                    "scenario": name,
                    "label": lab,
                    "n": st["n"],
                    "mean": round(st["mean"], 4),
                    "median_linear": round(st["median_linear"], 4),
                    "p95_linear": round(st["p95_linear"], 4),
                    "p95_r6": round(st["p95_r6"], 4),
                    "p95_nearest": round(st["p95_nearest"], 4),
                    "p99_linear": round(st["p99_linear"], 4),
                    "p10_p95": p10,
                    "html_p95": hp95,
                    "html_median": h.get("median"),
                    "html_errorPct": h.get("errorPct"),
                    "vs_p10": vs_p10,
                }
            )
            if vs_p10 != "MATCH":
                verdicts.append(
                    f"- **{name} / {lab} p95:** P10={p10} → linear={st['p95_linear']:.2f} "
                    f"(R6={st['p95_r6']:.2f}, HTML={hp95})"
                )
            blocks.append(
                f"| {lab} | {st['n']} | {st['mean']:.2f} | {st['median_linear']:.2f} | "
                f"**{st['p95_linear']:.2f}** | {st['p95_r6']:.2f} | {st['p95_nearest']:.2f} | "
                f"{p10:.2f} | {hp95} | {vs_p10} | {vs_html} |"
            )

        row_for("overall", ov)
        for lab in LABELS:
            row_for(lab, summarize(by[lab]))

        p10_tr = P10_TREND[name]
        tr_ok = (
            close(first_ov["p95_linear"], p10_tr[0])
            and close(first_ck["p95_linear"], p10_tr[1])
            and close(last_ov["p95_linear"], p10_tr[2])
            and close(last_ck["p95_linear"], p10_tr[3])
        )
        blocks.append("")
        blocks.append(
            f"First-20% n={len(first)} overall p95={first_ov['p95_linear']:.2f} "
            f"checkout p95={first_ck['p95_linear']:.2f} · "
            f"Last-20% n={len(last)} overall p95={last_ov['p95_linear']:.2f} "
            f"checkout p95={last_ck['p95_linear']:.2f} · trend vs P10: "
            f"{'MATCH' if tr_ok else 'MISMATCH'}"
        )
        blocks.append(
            f"Headline vs P10: N {'MATCH' if n_ok else 'MISMATCH'} · "
            f"error% {'MATCH' if err_ok else 'MISMATCH'} · "
            f"rps {'MATCH' if rps_ok else 'MISMATCH'} "
            f"(computed {rps:.4f} vs P10 {P10_RPS[name]}) · "
            f"overall median linear={ov['median_linear']:.2f} vs P10 {P10_MEDIAN[(name,'overall')]} "
            f"vs HTML {html['overall']['median']}"
        )
        blocks.append("")

        if not err_ok:
            verdicts.append(f"- **{name} error%:** P10={P10_ERR[name]} → false={fail_pct:.4f} non2xx={non2_pct:.4f}")
        if not n_ok:
            verdicts.append(f"- **{name} N:** P10={P10_N[name]} → {n}")
        if not rps_ok:
            verdicts.append(f"- **{name} rps:** P10={P10_RPS[name]} → {rps:.4f}")
        if not tr_ok:
            verdicts.append(
                f"- **{name} first/last 20% p95:** P10={p10_tr} → "
                f"({first_ov['p95_linear']:.2f}, {first_ck['p95_linear']:.2f}, "
                f"{last_ov['p95_linear']:.2f}, {last_ck['p95_linear']:.2f})"
            )
        med_p10 = P10_MEDIAN[(name, "overall")]
        if not close(ov["median_linear"], med_p10):
            verdicts.append(
                f"- **{name} overall median:** P10={med_p10} → linear={ov['median_linear']:.2f} "
                f"(HTML={html['overall']['median']})"
            )

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)

    md = []
    md.append("# Independent recompute — p95 / error% from raw `.jtl`")
    md.append("")
    md.append("**Purpose:** do **not** trust `p10-analysis.md` until these numbers are checked.")
    md.append("**Script:** `docs/_recompute_jtl.py` (stdlib `csv` only; does not import `_p10_analyze.py`).")
    md.append("**Columns:** `elapsed`, `success`, `responseCode`, `label`, `timeStamp`.")
    md.append("**p95 linear:** sorted `elapsed`, index `(n−1)×0.95`, interpolate — same formula P10 claimed.")
    md.append("**p95 R6:** index `(n+1)×0.95` (1-based interpolate) — closer to JMeter HTML `pct2ResTime`.")
    md.append("**error%:** `success=false` count / N **and** non-2xx / N, separately.")
    md.append("**Not used as input:** HTML dashboards, Interaction 15 console, archive-first-guess.")
    md.append("")
    md.append("## Verdict vs P10")
    md.append("")
    if not verdicts:
        md.append(
            "Every P10 **linear-p95**, **N**, **error%**, **rps** (±0.02), and **first/last 20% p95** "
            "cell **MATCH**es this recompute (tolerance 0.51 ms). "
            "Do **not** treat JMeter HTML `pct2ResTime` as the same estimator — see per-label `vs HTML`."
        )
    else:
        md.append("Mismatches against P10 (tolerance 0.51 ms / 0.02 rps):")
        md.append("")
        md.extend(verdicts)
    md.append("")
    md.append("## Per-scenario tables")
    md.append("")
    md.extend(blocks)
    md.append("## How to read this for P11")
    md.append("")
    md.append("- Cite **p95 linear** when checking P10 claims (same formula).")
    md.append("- Cite **HTML pct2** only as a *different* estimator; a gap there is not a P10 arithmetic bug.")
    md.append("- Stress/Spike HTML overall median ≠ linear median of all `elapsed` — HTML Total uses another aggregator; raw middle order-statistic is the linear median.")
    md.append(f"- Machine-readable copy: `{OUT_CSV.name}`.")
    md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print("mismatch count:", len(verdicts))
    for v in verdicts:
        print(v)


if __name__ == "__main__":
    main()
