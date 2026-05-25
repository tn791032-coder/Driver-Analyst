import pandas as pd
import numpy as np
import os

DATA_PROCESSED = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
DATA_RAW = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

def compute_supply_demand_metrics(df):
    demand = (df.groupby(["PULocationID", "pickup_dow", "pickup_hour"])
              .agg(demand=("VendorID", "count")).reset_index())
    demand.columns = ["zone_id", "dow", "hour", "demand"]
    supply = (df.groupby(["DOLocationID", "pickup_dow", "pickup_hour"])
              .agg(supply=("VendorID", "count")).reset_index())
    supply.columns = ["zone_id", "dow", "hour", "supply"]
    metrics = demand.merge(supply, on=["zone_id", "dow", "hour"], how="outer").fillna(0)
    metrics["gap"] = metrics["demand"] - metrics["supply"]
    metrics["sdr"] = np.where(metrics["demand"] > 0, metrics["supply"] / metrics["demand"], np.nan)
    return metrics

def run():
    df = pd.read_parquet(os.path.join(DATA_PROCESSED, "trips_clean.parquet"))
    metrics = compute_supply_demand_metrics(df)
    out = os.path.join(DATA_PROCESSED, "supply_demand_metrics.parquet")
    metrics.to_parquet(out, index=False)
    print(f"Saved metrics: {out} ({len(metrics):,} rows)")
    print(f"Avg gap: {metrics['gap'].mean():.1f}")
    print(f"Undersupplied (SDR<0.8): {(metrics['sdr'] < 0.8).sum():,} / {len(metrics):,}")
    return metrics

if __name__ == "__main__":
    run()
