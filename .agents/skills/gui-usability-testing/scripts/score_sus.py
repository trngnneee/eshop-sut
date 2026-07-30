#!/usr/bin/env python3
"""
Score the standard 10-item System Usability Scale (SUS) for one or more
participants and print per-participant scores, the average, and a
standard-benchmark interpretation.

Input: a CSV with one row per participant and columns q1..q10, each a
1-5 Likert rating (1 = Strongly disagree, 5 = Strongly agree), following
the standard SUS wording (odd items positively worded, even items
negatively worded):
  q1  I think I would like to use this system frequently.
  q2  I found the system unnecessarily complex.
  q3  I thought the system was easy to use.
  q4  I think I would need support to use this system.
  q5  I found the various functions well integrated.
  q6  I thought there was too much inconsistency.
  q7  Most people would learn to use this quickly.
  q8  I found the system very cumbersome to use.
  q9  I felt very confident using the system.
  q10 I needed to learn a lot before I could use it.

Usage:
  score_sus.py --csv responses.csv
  (optional: --participant-col participant_id)
"""
import argparse
import csv
import statistics
import sys


def score_row(row: dict) -> float:
    # Odd items (1,3,5,7,9): score = rating - 1
    # Even items (2,4,6,8,10): score = 5 - rating
    total = 0
    for i in range(1, 11):
        key = f"q{i}"
        val = int(row[key])
        if val < 1 or val > 5:
            raise ValueError(f"q{i} out of range 1-5: {val}")
        if i % 2 == 1:
            total += (val - 1)
        else:
            total += (5 - val)
    return total * 2.5  # 0-100 scale


def interpret(score: float) -> str:
    if score >= 90:
        return "A+ / Excellent (top ~10th percentile)"
    if score >= 80.3:
        return "A / Excellent"
    if score >= 68:
        return "B-C / Above average"
    if score >= 51:
        return "D / Below average"
    return "F / Poor"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True, help="CSV with columns q1..q10 (and optionally an id column)")
    ap.add_argument("--participant-col", default="participant_id", help="Name of the participant id column, if present")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No rows found in CSV.", file=sys.stderr)
        sys.exit(1)

    scores = []
    for row in rows:
        pid = row.get(args.participant_col, "?")
        try:
            s = score_row(row)
        except (KeyError, ValueError) as e:
            print(f"Skipping row (participant={pid}): {e}", file=sys.stderr)
            continue
        scores.append(s)
        print(f"{pid}: SUS = {s:.1f}  ({interpret(s)})")

    if scores:
        avg = statistics.mean(scores)
        print("-" * 40)
        print(f"n = {len(scores)}")
        print(f"Average SUS = {avg:.1f}  ({interpret(avg)})")
        if len(scores) > 1:
            print(f"Std dev = {statistics.stdev(scores):.1f}")


if __name__ == "__main__":
    main()