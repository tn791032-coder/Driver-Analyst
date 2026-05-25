import os
import requests
from tqdm import tqdm

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

def download_tlc_data(year=2025, month=1, vehicle_type="yellow"):
    filename = f"{vehicle_type}_tripdata_{year}-{month:02d}.parquet"
    url = f"{BASE_URL}/{filename}"
    dest = os.path.join(DATA_DIR, filename)
    if os.path.exists(dest):
        print(f"{filename} already exists, skipping")
        return dest
    print(f"Downloading {filename}...")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    with open(dest, "wb") as f, tqdm(total=total, unit="B", unit_scale=True) as pbar:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))
    print(f"Saved to {dest}")
    return dest

def download_zone_lookup():
    url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    dest = os.path.join(DATA_DIR, "taxi_zone_lookup.csv")
    if os.path.exists(dest):
        print("taxi_zone_lookup.csv already exists")
        return dest
    resp = requests.get(url)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        f.write(resp.content)
    print(f"Saved zone lookup to {dest}")
    return dest

if __name__ == "__main__":
    download_zone_lookup()
    download_tlc_data(year=2025, month=1, vehicle_type="yellow")
    print("All downloads complete")
