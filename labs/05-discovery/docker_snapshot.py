"""Read-only Docker runtime discovery for your OWN engine/context."""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def parse_docker_lines(text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows.append({
            "id": row.get("ID", ""),
            "names": row.get("Names", ""),
            "image": row.get("Image", ""),
            "state": row.get("State", ""),
            "ports": row.get("Ports", ""),
        })
    return rows


def differences(before, after):
    old = {r["id"]: r for r in before}
    new = {r["id"]: r for r in after}
    return {
        "new_instances": [new[k] for k in new.keys() - old.keys()],
        "missing_instances": [old[k] for k in old.keys() - new.keys()],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="docker_snapshot.json")
    p.add_argument("--baseline", help="an existing snapshot JSON to compare")
    args = p.parse_args()
    context = subprocess.run(["docker", "context", "show"], check=True, text=True, capture_output=True).stdout.strip()
    print("Docker context:", context)
    if "prod" in context.lower():
        raise SystemExit("Context name contains 'prod'; inspect manually before running discovery.")
    data = subprocess.run(["docker", "ps", "-a", "--format", "{{json .}}"], check=True, text=True, capture_output=True)
    snapshot = {"observed_utc": datetime.now(timezone.utc).isoformat(), "context": context, "containers": parse_docker_lines(data.stdout)}
    if args.baseline:
        previous = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        if previous.get("context") != context:
            raise SystemExit("Docker contexts differ; cannot compare snapshots reliably.")
        print(json.dumps(differences(previous["containers"], snapshot["containers"]), indent=2))
    Path(args.out).write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved:", args.out)
    print("Note: instance ID changes are not necessarily new logical services.")


if __name__ == "__main__":
    main()
