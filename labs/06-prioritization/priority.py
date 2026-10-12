"""Illustrative multi-criteria asset ranking; NOT a formal crown jewel decision."""
import csv
from pathlib import Path

WEIGHTS = {"business": .25, "operational": .25, "data": .20, "dependency": .20, "exposure": .10}


def calculate(row):
    values = {key: float(row[key]) for key in WEIGHTS}
    if not all(1 <= v <= 5 for v in values.values()):
        raise ValueError("criteria must be 1..5")
    return round(sum(values[k] * w for k, w in WEIGHTS.items()), 2)


def main():
    with Path(__file__).with_name("priorities.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    ranked = sorted(((r["asset"], calculate(r)) for r in rows), key=lambda x: x[1], reverse=True)
    for n, (name, score) in enumerate(ranked, start=1):
        print(f"{n:>2}. {name:<24} {score:.2f}/5")
    print("Candidate ranking only; crown jewels require business approval.")


if __name__ == "__main__":
    main()
