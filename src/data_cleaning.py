import pandas as pd
import os

DATA_RAW = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
DATA_PROCESSED = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
os.makedirs(DATA_PROCESSED, exist_ok=True)

def load_taxi_zones():
    return pd.read_csv(os.path.join(DATA_RAW, "taxi_zone_lookup.csv"))

def clean_trip_data(df):
    print(f"Raw rows: {len(df):,}")
    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"])
    print(f"After dropping null time/location: {len(df):,}")
    df = df[(df["passenger_count"] > 0) & (df["passenger_count"] <= 8)]
    df = df[df["trip_distance"] > 0]
    df = df[df["fare_amount"] > 0]
    df = df[df["total_amount"] >= 0]
    df = df[df["tpep_dropoff_datetime"] > df["tpep_pickup_datetime"]]
    dur = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 3600
    df = df[(dur > 0) & (dur < 6)]
    print(f"After cleaning: {len(df):,}")
    return df

def add_features(df):
    df = df.copy()
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
    df["pickup_day"] = df["tpep_pickup_datetime"].dt.day_name()
    df["pickup_dow"] = df["tpep_pickup_datetime"].dt.dayofweek
    df["is_weekend"] = df["pickup_dow"].isin([5, 6]).astype(int)
    return df

def process():
    zones = load_taxi_zones()
    print(f"Loaded {len(zones)} taxi zones")
    path = os.path.join(DATA_RAW, "yellow_tripdata_2025-01.parquet")
    df = pd.read_parquet(path)
    df = clean_trip_data(df)
    df = add_features(df)
    z = zones.rename(columns={"LocationID": "PULocationID"})
    df = df.merge(z[["PULocationID", "Borough", "Zone"]], on="PULocationID", how="left")
    z2 = z.rename(columns={"PULocationID": "DOLocationID"})
    df = df.merge(z2[["DOLocationID", "Borough", "Zone"]], on="DOLocationID", how="left", suffixes=("_pu", "_do"))
    out_path = os.path.join(DATA_PROCESSED, "trips_clean.parquet")
    df.to_parquet(out_path, index=False)
    print(f"Saved clean data: {out_path} ({len(df):,} rows)")
    sample = df.sample(min(100000, len(df)), random_state=42)
    sample.to_parquet(os.path.join(DATA_PROCESSED, "trips_sample.parquet"), index=False)
    print("Saved sample")
    return df

if __name__ == "__main__":
    process()
