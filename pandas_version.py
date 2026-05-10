import time

import pandas as pd

FILE_PATH = "data/yellow_tripdata_2026-01.parquet"


def load_data(file: str) -> pd.DataFrame:
    return pd.read_parquet(file)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["fare_amount"] > 0) & (df["trip_distance"] > 0)].copy()


def generate_revenue_by_day(df: pd.DataFrame):
    revenue_by_day = (
        df.assign(pickup_date=pd.to_datetime(df["tpep_pickup_datetime"]).dt.date)
        .groupby("pickup_date")["fare_amount"]
        .sum()
        .reset_index(name="total_revenue")
        .sort_values("pickup_date")
    )

    revenue_by_day.to_csv("output_pandas/revenue_by_day.csv", index=False)

    return "revenue_by_day.csv"


def generate_trips_by_pickup_hour(df: pd.DataFrame):
    trips_by_pickup_hour = (
        df.assign(pickup_hour=pd.to_datetime(df["tpep_pickup_datetime"]).dt.hour)
        .groupby("pickup_hour")
        .agg(total_trips=("fare_amount", "count"))
        .reset_index()
        .sort_values("pickup_hour")
    )

    trips_by_pickup_hour.to_csv("output_pandas/trips_by_pickup_hour.csv", index=False)

    return "trips_by_pickup_hour.csv"


def generate_avg_fare_by_vendor(df: pd.DataFrame):
    avg_fare_by_vendor = (
        df.groupby("VendorID")
        .agg(avg_fare=("fare_amount", "mean"))
        .sort_values("VendorID")
    )

    avg_fare_by_vendor.to_csv("output_pandas/avg_fare_by_vendor.csv", index=False)

    return "avg_fare_by_vendor.csv"


def generate_avg_distance_by_payment(df: pd.DataFrame):
    avg_distance_by_payment = (
        df.groupby("payment_type")
        .agg(avg_distance=("trip_distance", "mean"))
        .sort_values("payment_type")
    )

    avg_distance_by_payment.to_csv(
        "output_pandas/avg_distance_by_payment.csv", index=False
    )

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

    rows_processed = len(cleaned_df)

    return {
        "rows_processed": rows_processed,
        "runtime": end_time - start_time,
        "generated_reports": generated_reports,
    }


if __name__ == "__main__":
    print(run_pipeline())
