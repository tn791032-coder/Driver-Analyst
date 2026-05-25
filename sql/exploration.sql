-- 1. Row count
SELECT COUNT(*) AS total_trips FROM yellow_tripdata_2025_01;

-- 2. Check nulls per column
SELECT
  COUNT(*) - COUNT(tpep_pickup_datetime) AS null_pickup_time,
  COUNT(*) - COUNT(tpep_dropoff_datetime) AS null_dropoff_time,
  COUNT(*) - COUNT(PULocationID) AS null_pu_location,
  COUNT(*) - COUNT(DOLocationID) AS null_do_location,
  COUNT(*) - COUNT(passenger_count) AS null_passengers,
  COUNT(*) - COUNT(trip_distance) AS null_distance,
  COUNT(*) - COUNT(fare_amount) AS null_fare
FROM yellow_tripdata_2025_01;

-- 3. Trips count by hour
SELECT
  EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
  COUNT(*) AS trip_count
FROM yellow_tripdata_2025_01
GROUP BY pickup_hour
ORDER BY pickup_hour;

-- 4. Hourly demand per zone
SELECT
  PULocationID,
  EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
  EXTRACT(DOW FROM tpep_pickup_datetime) AS dow,
  COUNT(*) AS demand
FROM yellow_tripdata_2025_01
GROUP BY PULocationID, hour, dow
ORDER BY PULocationID, hour;

-- 5. Supply proxy: completed dropoffs per zone per hour
SELECT
  DOLocationID AS zone_id,
  EXTRACT(HOUR FROM tpep_dropoff_datetime) AS hour,
  EXTRACT(DOW FROM tpep_dropoff_datetime) AS dow,
  COUNT(*) AS supply_proxy
FROM yellow_tripdata_2025_01
GROUP BY DOLocationID, hour, dow;

-- 6. Peak hours by borough
SELECT
  z.Borough,
  EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
  COUNT(*) AS trips
FROM yellow_tripdata_2025_01 t
JOIN taxi_zone_lookup z ON t.PULocationID = z.LocationID
GROUP BY z.Borough, hour
ORDER BY z.Borough, hour;

-- 7. Top 10 busiest pickup zones
SELECT
  z.Zone,
  z.Borough,
  COUNT(*) AS total_pickups
FROM yellow_tripdata_2025_01 t
JOIN taxi_zone_lookup z ON t.PULocationID = z.LocationID
GROUP BY z.Zone, z.Borough
ORDER BY total_pickups DESC
LIMIT 10;
