import time

import polars as pl

FILE_PATH = "data/yellow_tripdata_2026-01.parquet"


def load_data(file: str) -> pl.LazyFrame:
    return pl.scan_parquet(file)


def clean_data(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.filter((pl.col("fare_amount") > 0) & (pl.col("trip_distance") > 0))


def generate_revenue_by_day(df: pl.LazyFrame):
    revenue_by_day = (
        df.with_columns(pl.col("tpep_pickup_datetime").dt.date().alias("pickup_date"))
        .group_by("pickup_date")
        .agg(pl.col("fare_amount").sum().alias("total_revenue"))
        .sort("pickup_date")
        .collect(engine="streaming")
    )

    revenue_by_day.write_csv("output_polars/revenue_by_day.csv")

    return "revenue_by_day.csv"


def generate_trips_by_pickup_hour(df: pl.LazyFrame):
    trips_by_pickup_hour = (
        df.with_columns(pl.col("tpep_pickup_datetime").dt.hour().alias("pickup_hour"))
        .group_by("pickup_hour")
        .agg(pl.len().alias("total_trips"))
        .sort("pickup_hour")
        .collect(engine="streaming")
    )

    trips_by_pickup_hour.write_csv("output_polars/trips_by_pickup_hour.csv")

    return "trips_by_pickup_hour.csv"


def generate_avg_fare_by_vendor(df: pl.LazyFrame):
    avg_fare_by_vendor = (
        df.group_by("VendorID")
        .agg(pl.col("fare_amount").mean().alias("avg_fare"))
        .sort("VendorID")
        .collect(engine="streaming")
    )

    avg_fare_by_vendor.write_csv("output_polars/avg_fare_by_vendor.csv")

    return "avg_fare_by_vendor.csv"


def generate_avg_distance_by_payment(df: pl.LazyFrame):
    avg_distance_by_payment = (
        df.group_by(pl.col("payment_type"))
        .agg(pl.col("trip_distance").mean().alias("avg_distance"))
        .sort("payment_type")
        .collect(engine="streaming")
    )

    avg_distance_by_payment.write_csv("output_polars/avg_distance_by_payment.csv")

    return "avg_distance_by_payment.csv"


def run_pipeline():
    start_time = time.perf_counter()

    df = load_data(FILE_PATH)

    cleaned_df = clean_data(df)

    generated_reports = []

    generated_reports.append(generate_revenue_by_day(cleaned_df))
    generated_reports.append(generate_trips_by_pickup_hour(cleaned_df))
    generated_reports.append(generate_avg_fare_by_vendor(cleaned_df))
    generated_reports.append(generate_avg_distance_by_payment(cleaned_df))

    end_time = time.perf_counter()

    rows_processed = cleaned_df.select(pl.len()).collect().item()

    return {
        "rows_processed": rows_processed,
        "runtime": end_time - start_time,
        "generated_reports": generated_reports,
    }


if __name__ == "__main__":
    print(run_pipeline())
