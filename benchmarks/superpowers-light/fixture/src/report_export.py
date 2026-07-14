import csv
from pathlib import Path


def export_rows(destination: str, rows: list[dict[str, str]]) -> Path:
    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "email", "balance"])
        writer.writeheader()
        writer.writerows(rows)
    return output
