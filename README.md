# Pandas → Polars Analytics Benchmark

Benchmarking a migration from pandas to Polars using the NYC Taxi January 2026 parquet dataset.

## Dataset

* [NYC Taxi January 2026 parquet data]("https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet")
* Rows processed: 3,560,862

## Workflow

Both pipelines implement the same analytics workflow:

* parquet processing
* data cleaning/filtering
* datetime extraction
* aggregations
* CSV report generation

## Generated Reports

* revenue_by_day.csv
* trips_by_pickup_hour.csv
* avg_fare_by_vendor.csv
* avg_distance_by_payment.csv

## Benchmark Results

| Engine | Runtime (seconds) | Relative Speed |
| ------ | ----------------: | -------------: |
| Pandas |            1.75 s |          1.00x |
| Polars |            0.20 s |          8.70x |

## Conclusion

Polars achieved an 8.70x speedup over pandas on the same analytics workload.

## Project Structure

```text
.
├── benchmark.py
├── pandas_version.py
├── polars_version.py
├── data/
├── output_pandas/
├── output_polars/
└── reports/
```

## Run Benchmark

```bash
uv run benchmark.py
```

The benchmark script automatically:

* runs both pipelines
* generates analytics reports
* compares runtimes
* creates a markdown benchmark report

## Technologies

* Python
* Pandas
* Polars
* Parquet
