import pandas_version
import polars_version


def main():
    pandas_metrics = pandas_version.run_pipeline()
    polars_metrics = polars_version.run_pipeline()

    pandas_runtime = pandas_metrics["runtime"]
    polars_runtime = polars_metrics["runtime"]
    rows_processed = polars_metrics["rows_processed"]
    speedup = pandas_runtime / polars_runtime

    # Generate list of reports for markdown
    reports_list = "\n".join(
        f"- {report}" for report in polars_metrics.get("generated_reports", [])
    )

    markdown = f"""
# Benchmark Results: Pandas vs Polars

## Dataset: NYC Taxi January 2026

## Overview
- **Rows Processed**: {rows_processed:,}
- **Speedup**: **{speedup:.2f}x** faster with Polars

## Runtime Comparison

| Engine | Runtime (seconds) | Relative Speed |
| ---------- | ------------------- | ---------------- |
| Pandas | {pandas_runtime:.2f} s | 1.00x |
| **Polars** | **{polars_runtime:.2f} s** | **{speedup:.2f}x** |

## Generated Reports
{reports_list}

---

**Conclusion**: Polars is **{speedup:.2f}x faster** than Pandas on this dataset.
"""

    # Save to markdown file
    with open("reports/benchmark_results.md", "w", encoding="utf-8") as f:
        f.write(markdown.strip())

    print("Benchmark report generated successfully!")
    print(f"Speedup: {speedup:.2f}x")
    print("Report saved as 'reports/benchmark_results.md'")

    return markdown


if __name__ == "__main__":
    main()
