# Grab Supply-Demand Gap Analysis 🚖

A ride-hailing supply-demand imbalance analysis inspired by **Grab's Analytics framework**.
Built for Grab Data Analyst Intern application.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)](https://streamlit.io)
[![Data](https://img.shields.io/badge/Data-NYC_TLC_2.8M-green)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
[![ML](https://img.shields.io/badge/Forecasting-Prophet-orange)](https://facebook.github.io/prophet/)

---

## Business Impact Summary

| Metric | Value |
|--------|-------|
| **Trips analyzed** | 2,814,457 |
| **Undersupplied hours** | 5,193 (14.5% of all hours) |
| **Peak demand hour** | 17:00 (5 PM) |
| **Avg gap during undersupply** | 107 trips/hour |
| **Est. monthly lost revenue** | **~$49,900** |
| **Est. annual recovered (20% gap reduction)** | **~$119,700** |

> If Grab reduces the supply-demand gap by just 20% through better driver allocation,
> that's **~$120K/year recovered revenue per market**.

---

## Business Problem

Grab's core challenge: matching **passenger demand** with **driver supply** in real-time.

- Passengers can't find rides → **lost revenue, poor experience**
- Drivers waiting idly → **wasted time, low earnings**

**This project identifies *when, where, and why* gaps occur — and recommends data-driven actions.**

---

## Dataset

- **Source:** [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Type:** Yellow Taxi (proxy for ride-hailing)
- **Period:** January 2025 (~2.8M trips after cleaning)
- **Schema:** 19 columns (pickup/dropoff time, location ID, fare, distance)

---

## Methodology

Adapted from [Grab's Analytics framework](https://engineering.grab.com/understanding-supply-demand-ride-hailing-data):

| Term | Definition | Our Proxy |
|------|-----------|-----------|
| **Demand** | Passengers requesting rides | Pickup count per zone-hour |
| **Supply** | Online & idle drivers | Dropoff arrivals (drivers becoming free) |
| **Gap** | Demand - Supply | Difference |
| **SDR** | Supply-Demand Ratio (< 0.8 = undersupplied) | Supply / Demand |

---

## Key Findings

### 1. Peak demand hits at 17:00 (evening rush)
![Hourly Demand](outputs/chart1_hourly_demand.png)

### 2. Gap widens significantly during 17:00-20:00
![Demand Supply Gap](outputs/chart2_demand_supply_gap.png)

### 3. Manhattan dominates volume; Queens shows largest gap
![Borough Gap](outputs/chart3_borough_gap.png)

### 4. Undersupply concentrated in weekday evenings (red = undersupplied)
![SDR Heatmap](outputs/chart4_sdr_heatmap.png)

### 5. Top undersupplied zones need immediate attention
![Undersupplied Zones](outputs/chart5_undersupplied_zones.png)

---

## Recommendations

### Supply-Side (for Operations)
| Action | Target | Expected Impact |
|--------|--------|----------------|
| **Driver surge incentives** | Top-10 gap zones @ 17:00-20:00 | Reduce gap by ~15% |
| **Airport return bonus** | JFK/LaGuardia → Manhattan | Increase city supply by ~8% |
| **Heatmap repositioning** | Drivers in oversupplied zones | Better spatial distribution |

### Demand-Side (for Product)
| Action | Target | Expected Impact |
|--------|--------|----------------|
| **Travel Trends widget** | Residential areas @ 7-9AM | Shift time-insensitive demand |
| **Surge pricing schedule** | Zone-hour SDR < 0.8 | Balance supply-demand |
| **"Book earlier" notification** | CBD @ 16:30-17:00 | Reduce peak load |

---

## Tools & Skills Demonstrated

| Skill | Where |
|-------|-------|
| **SQL** | `sql/exploration.sql` — window functions, aggregation, joins |
| **Python** | `src/` — pandas, numpy, data pipeline |
| **Data Visualization** | `notebooks/01_eda.ipynb` — matplotlib, seaborn, plotly |
| **Dashboard** | `dashboard/app.py` — Streamlit (interactive filters, charts) |
| **Machine Learning** | `notebooks/02_ml_forecast.ipynb` — Prophet time-series |
| **Geospatial** | GeoPandas, taxi zone mapping |
| **Business Communication** | This README + executive summary |

---

## How to Run

```bash
pip install -r requirements.txt
python src/download_data.py
python src/data_cleaning.py
python src/metrics.py
streamlit run dashboard/app.py
jupyter notebook notebooks/01_eda.ipynb
```

---

## Project Structure

```
grab-supply-demand-analysis/
├── data/                    # Raw (59MB) + processed (63MB)
├── notebooks/
│   ├── 01_eda.ipynb         # Exploratory analysis with visualizations
│   └── 02_ml_forecast.ipynb # Prophet demand forecasting
├── src/
│   ├── download_data.py     # NYC TLC data downloader
│   ├── data_cleaning.py     # Cleaning + feature engineering
│   └── metrics.py           # Supply-demand metrics computation
├── dashboard/
│   └── app.py               # Interactive Streamlit dashboard
├── sql/
│   └── exploration.sql      # 7 SQL exploration queries
├── outputs/                 # Generated charts
└── README.md
```

---

## References

- [Grab Engineering: Understanding Supply & Demand in Ride-hailing](https://engineering.grab.com/understanding-supply-demand-ride-hailing-data)
- [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Prophet Forecasting](https://facebook.github.io/prophet/)

---

## Interview Talking Points

When asked about this project in an interview:

1. **Problem:** "Grab's core challenge — matching supply and demand in real-time"
2. **Approach:** "Adapted Grab's own SDR framework from their Engineering Blog"
3. **Data:** "2.8M NYC taxi trips as ride-hailing proxy, cleaned 19% of raw data"
4. **Insight:** "Gap peaks 17:00-20:00 in CBD; root cause: drivers don't return from airport"
5. **Action:** "5 recommendations with estimated $120K/year impact per market"
6. **Tools:** "SQL + Python + Streamlit + Prophet (forecast)"
