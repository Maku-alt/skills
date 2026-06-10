---
name: data-analysis
description: "Structured workflow for exploring tabular datasets (CSV/Parquet) with pandas, producing descriptive stats, charts, and action items. Invoke when Agent must inspect a dataset, summarize patterns, or prepare quick visuals for stakeholders."
allowed-tools:
  - python
  - bash
---

# Data Analysis Workflow

## Overview
Use this skill whenever a user asks to analyze tabular data (CSV, TSV, Parquet) and deliver insights quickly. The workflow focuses on: loading data safely, profiling basic statistics, visualizing key relationships, and documenting findings + follow-ups.

## When to apply
- User provides a file path or attaches a dataset and wants summaries, outliers, or charts.
- You need to compare subsets, compute aggregates, or diagnose data quality before modeling.
- Quick exploratory work is needed prior to passing context to other agents (builder/narrator).

## Prerequisites
- Python 3.10+ with pandas, numpy, matplotlib, seaborn, jupyter (install via `pip install -r requirements.txt` if missing).
- Disk access to the dataset provided by the user.
- Enough free space to write intermediate artifacts (plots, markdown reports).

## Workflow
1. **Confirm inputs**
   - Ask for file path, delimiter, encoding, and expected row count.
   - Clarify target variable, segments of interest, and any privacy constraints.
2. **Set up environment**
   - Create (or reuse) a virtualenv/conda env.
   - Install requirements from `scripts/requirements.txt` if not already installed.
   - Open a notebook or run the helper script `scripts/eda_report.py`.
3. **Load data**
   - Use `pandas.read_csv` (specify encoding, `parse_dates`, `dtype` as needed).
   - Immediately check `df.head()`, `df.info()`, `df.describe()`.
   - Persist a cleaned version if heavy munging is needed (`data/processed/<name>.parquet`).
4. **Profile quality**
   - Missing values: `df.isna().sum() / len(df)`.
   - Cardinality of categorical fields.
   - Basic distribution plots (histograms, KDE, boxplots).
   - Flag obvious anomalies or unit mismatches.
5. **Explore relationships**
   - Correlation matrix / heatmap for numeric fields.
   - Grouped aggregations (means, sums) for key segments.
   - Time-series plots when a datetime column exists.
6. **Document insights**
   - Capture bullet points for trends, anomalies, data issues, and proposed next steps.
   - Export figures to `figures/` (PNG/SVG) and embed references in the final report.
   - Save a Markdown summary `reports/<dataset>_<date>_eda.md` with:
     - Context + questions answered
     - Data quality notes
     - Key metrics/plots
     - Recommended actions or follow-up analyses
7. **Handoff**
   - Share the summary + figures with downstream agents (Narrator for docs, Builder for prototypes).
   - Archive scripts/notebooks under `notebooks/` for reproducibility.

## Helper scripts
- `scripts/eda_report.py <path_to_csv> [--delimiter , --encoding utf-8]`
  - Generates a lightweight report (summary stats + missing values + correlations) and writes `reports/eda_report.md`.
- `scripts/requirements.txt`
  - Base Python packages for the workflow.

## Best practices
- Keep raw data immutable; write derived files under `data/processed/`.
- Always log the exact command and parameters used to load the data.
- Use ASCII filenames for portability.
- If data is sensitive, avoid copying it outside the approved workspace; delete temporary files when done.

## Example usage
```
User: Analiza D:\Desktop\Terpel\Consumo Energético\Marcobre\df_predict.csv y dime los drivers principales del consumo.
Assistant:
Loading skill: data-analysis — prepararé un EDA rápido con pandas y gráficos.
```
Follow the workflow: confirm context, run `scripts/eda_report.py` (or a notebook), export figures + report, summarize findings in chat.
