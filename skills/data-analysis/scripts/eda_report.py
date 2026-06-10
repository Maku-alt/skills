#!/usr/bin/env python3
"""
Quick EDA helper.

Usage:
    python scripts/eda_report.py path/to/data.csv --delimiter , --encoding utf-8
Outputs:
    reports/eda_report.md with summary stats, missing values, and correlations.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd


def load_dataframe(path: Path, delimiter: str, encoding: str) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path, delimiter=delimiter, encoding=encoding)


def build_report(df: pd.DataFrame) -> str:
    lines: list[str] = []
    lines.append("# EDA Report")
    lines.append("")
    lines.append("## Shape")
    lines.append(f"- Rows: {df.shape[0]:,}")
    lines.append(f"- Columns: {df.shape[1]:,}")
    lines.append("")

    lines.append("## Missing values (top 20)")
    missing = (
        df.isna().sum().sort_values(ascending=False).head(20).reset_index()
    )
    missing.columns = ["column", "missing_count"]
    total = len(df)
    for _, row in missing.iterrows():
        percent = (row["missing_count"] / total) * 100
        lines.append(
            f"- {row['column']}: {row['missing_count']:,} ({percent:.2f}%)"
        )
    lines.append("")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        lines.append("## Numeric summary (first 5 columns)")
        desc = df[numeric_cols].describe().round(3).iloc[:, :5]
        lines.append(desc.to_markdown())
        lines.append("")

        corr = df[numeric_cols].corr(numeric_only=True).round(3)
        lines.append("## Correlation matrix (numeric columns)")
        lines.append(corr.to_markdown())
        lines.append("")
    else:
        lines.append("## Numeric summary")
        lines.append("- No numeric columns detected.")
        lines.append("")

    lines.append("## Next steps")
    lines.append("- Review high-missing columns and decide on imputation or drop.")
    lines.append("- Investigate strong correlations or unexpected patterns.")
    lines.append("- Create domain-specific visualizations as needed.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Quick EDA helper")
    parser.add_argument("path", help="Path to CSV/Parquet file")
    parser.add_argument("--delimiter", default=",", help="Field delimiter (default ,)")
    parser.add_argument("--encoding", default="utf-8", help="File encoding (default utf-8)")
    parser.add_argument(
        "--output",
        default=Path("reports/eda_report.md"),
        type=Path,
        help="Output markdown path",
    )
    args = parser.parse_args()

    data_path = Path(args.path).expanduser()
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = load_dataframe(data_path, args.delimiter, args.encoding)
    report = build_report(df)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()
