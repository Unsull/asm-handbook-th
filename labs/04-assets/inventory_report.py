"""Synthetic asset-inventory completeness report (stdlib only)."""
import csv
from pathlib import Path


def analyze(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        records = list(csv.DictReader(f))
    if not records:
        raise ValueError("empty inventory")
    asset_ids = [r["asset_id"] for r in records]
    if len(asset_ids) != len(set(asset_ids)):
        raise ValueError("duplicate asset_id")
    missing = [r["asset_id"] for r in records if not r.get("owner", "").strip()]
    coverage = (len(records) - len(missing)) / len(records) * 100
    return len(records), missing, coverage


if __name__ == "__main__":
    count, no_owner, owner_coverage = analyze(Path(__file__).with_name("asset_inventory.csv"))
    print(f"Discovered/declared assets: {count}")
    print(f"Missing owner: {no_owner}")
    print(f"Owner coverage among these records: {owner_coverage:.1f}%")
    print("This does NOT measure organization-wide discovery coverage.")
