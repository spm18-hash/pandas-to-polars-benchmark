# Benchmark Results: Pandas vs Polars

## Dataset: NYC Taxi January 2026

## Overview
- **Rows Processed**: 3,560,862
- **Speedup**: **8.70x** faster with Polars

## Runtime Comparison

| Engine | Runtime (seconds) | Relative Speed |
| ---------- | ------------------- | ---------------- |
| Pandas | 1.75 s | 1.00x |
| **Polars** | **0.20 s** | **8.70x** |

## Generated Reports
- revenue_by_day.csv
- trips_by_pickup_hour.csv
- avg_fare_by_vendor.csv
- avg_distance_by_payment.csv

---

**Conclusion**: Polars is **8.70x faster** than Pandas on this dataset.