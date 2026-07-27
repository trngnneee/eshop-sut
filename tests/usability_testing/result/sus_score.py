"""Cham diem SUS chuan tu sus_responses.csv (cot: participant,q1..q10, gia tri 1-5).

Cau le: diem - 1; cau chan: 5 - diem; tong x 2.5. Bao loi va thoat khac 0 neu
thieu/lech gia tri thay vi bo qua.
"""
import csv
import statistics
import sys
from pathlib import Path

CSV_PATH = Path(__file__).parent / "sus_responses.csv"

# Thang tinh tu cua Bangor et al. (2009), ap cho diem trung binh
ADJECTIVE_BANDS = [
    (84.1, "Best imaginable"),
    (80.8, "Excellent"),
    (71.4, "Good"),
    (51.0, "OK"),
    (25.1, "Poor"),
    (0.0, "Worst imaginable"),
]


def score_row(row: dict) -> float:
    total = 0
    for i in range(1, 11):
        raw = row.get(f"q{i}", "").strip()
        try:
            v = int(raw)
        except ValueError:
            sys.exit(f"LOI: {row['participant']} q{i} khong phai so nguyen: {raw!r}")
        if not 1 <= v <= 5:
            sys.exit(f"LOI: {row['participant']} q{i} ngoai khoang 1-5: {v}")
        total += (v - 1) if i % 2 == 1 else (5 - v)
    return total * 2.5


def adjective(mean: float) -> str:
    for threshold, label in ADJECTIVE_BANDS:
        if mean >= threshold:
            return label
    return ADJECTIVE_BANDS[-1][1]


def main() -> None:
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("LOI: CSV rong")

    scores = {}
    for row in rows:
        scores[row["participant"]] = score_row(row)

    print(f"{'Participant':<12}{'SUS':>6}")
    for p, s in scores.items():
        print(f"{p:<12}{s:>6.1f}")

    values = list(scores.values())
    mean = statistics.mean(values)
    print("-" * 18)
    print(f"{'Mean':<12}{mean:>6.1f}")
    print(f"{'Median':<12}{statistics.median(values):>6.1f}")
    print(f"{'Min-Max':<12}{min(values):>.1f}-{max(values):.1f}")
    print(f"Adjective band (mean): {adjective(mean)}")


if __name__ == "__main__":
    main()
