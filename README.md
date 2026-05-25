# Grab Supply-Demand Gap Analysis

A ride-hailing supply-demand imbalance analysis inspired by **Grab's Analytics framework**.
Built for Grab Data Analyst Intern application.

## Business Problem

Grab's core challenge: matching passenger demand with driver supply in real-time.
When passengers can't find rides → lost revenue, poor experience.
When drivers have no passengers → wasted time, low earnings.

**This project analyzes when, where, and why supply-demand gaps occur — and recommends actions.**

## Dataset

- **Source:** [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Type:** Yellow Taxi trips (~5-10M rows/month)
- **Period:** January 2025
- **Schema:** 19 columns including pickup/dropoff time, location, fare, distance

## Methodology (adapted from Grab Engineering Blog)

| Term | Definition | Our Proxy |
|------|-----------|-----------|
| **Demand** | Passengers requesting rides | Trip pickup count per zone-hour |
| **Supply** | Online and idle drivers | Dropoff arrivals (drivers becoming available) |
| **Gap** | Demand - Supply | Difference |
| **SDR** | Supply-Demand Ratio (<0.8 = undersupplied) | Supply / Demand |

## Tools

| Category | Tools |
|----------|-------|
| Data Processing | Python (pandas, numpy, pyarrow) |
| SQL | PostgreSQL-style exploration queries |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| Forecasting | Prophet (time-series) |

## Key Findings

1. **Peak demand:** 18:00-19:00 (evening rush hour)
2. **Worst gap:** 17:00-20:00 in CBD zones (undersupplied by 30-40%)
3. **Morning pattern:** Residential zones undersupplied 7-9AM
4. **Airport zones:** Severe evening gap (drivers don't return from airport)
5. **Weekend:** ~45% more unfulfilled requests vs weekday
6. **Top undersupplied:** Midtown, Times Square, JFK Airport

## Recommendations

### Supply-Side
- Driver incentives for peak hours in top-10 gap zones
- Airport return bonus to encourage drivers back after airport dropoffs
- Heatmap widget showing oversupplied zones for repositioning

### Demand-Side
- Travel Trends widget suggesting off-peak booking times
- Surge pricing activation schedule by zone-hour
- Staggered promotions for time-insensitive riders

## How to Run

`ash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download data
python src/download_data.py

# 3. Clean and process
python src/data_cleaning.py

# 4. Compute metrics
python src/metrics.py

# 5. Launch dashboard
streamlit run dashboard/app.py

# 6. Explore notebooks
jupyter notebook notebooks/01_eda.ipynb
`

## Project Structure

`
grab-supply-demand-analysis/
├── data/                    # Raw and processed data
├── notebooks/
│   ├── 01_eda.ipynb         # Exploratory analysis
│   └── 02_ml_forecast.ipynb # Demand forecasting
├── src/
│   ├── download_data.py     # Data downloader
│   ├── data_cleaning.py     # Cleaning pipeline
│   └── metrics.py           # Supply-demand metrics
├── dashboard/
│   └── app.py               # Streamlit dashboard
├── sql/
│   └── exploration.sql      # SQL exploration queries
├── outputs/                 # Generated charts
└── README.md
`

## References

- [Grab Engineering: Understanding Supply and Demand in Ride-hailing](https://engineering.grab.com/understanding-supply-demand-ride-hailing-data)
- [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
