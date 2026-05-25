import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

DATA_P = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
DATA_R = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

st.set_page_config(page_title="Supply-Demand Gap Analysis", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_parquet(os.path.join(DATA_P, "trips_clean.parquet"))
    metrics = pd.read_parquet(os.path.join(DATA_P, "supply_demand_metrics.parquet"))
    zones = pd.read_csv(os.path.join(DATA_R, "taxi_zone_lookup.csv"))
    metrics = metrics.merge(zones, left_on="zone_id", right_on="LocationID", how="left")
    return df, metrics, zones

df, metrics, zones = load_data()

st.title("Ride-Hailing Supply-Demand Gap Analysis")
st.markdown("Inspired by **Grab's Analytics framework** — measuring supply-demand imbalance")

st.sidebar.header("Filters")
boroughs = ["All"] + sorted(metrics["Borough"].dropna().unique().tolist())
sel_b = st.sidebar.selectbox("Borough", boroughs)
if sel_b != "All":
    metrics = metrics[metrics["Borough"] == sel_b]

z_opt = ["All"] + sorted(metrics["Zone"].dropna().unique().tolist())
sel_z = st.sidebar.selectbox("Zone", z_opt)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Trips", f"{len(df):,}")
c2.metric("Avg Hourly Demand", f"{metrics['demand'].mean():.0f}")
avg_gap = metrics["gap"].mean()
pct = (avg_gap/metrics['demand'].mean()*100) if metrics['demand'].mean()>0 else 0
c3.metric("Avg Gap", f"{avg_gap:.0f}", delta=f"{pct:.1f}%")
c4.metric("Hours Undersupplied", f"{(metrics['sdr']<0.8).mean()*100:.1f}%")

st.subheader("Hourly Demand Pattern")
hr = metrics.groupby("hour")[["demand","supply","gap"]].mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=hr.index, y=hr["demand"], mode="lines+markers", name="Demand", line=dict(color="#e74c3c", width=3)))
fig.add_trace(go.Scatter(x=hr.index, y=hr["supply"], mode="lines+markers", name="Supply", line=dict(color="#2ecc71", width=3)))
fig.add_trace(go.Bar(x=hr.index, y=hr["gap"], name="Gap", marker_color="rgba(231,76,60,0.3)"))
fig.update_layout(hovermode="x unified", height=400)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top 20 Zones by Gap")
if sel_z != "All":
    disp = metrics[metrics["Zone"] == sel_z]
else:
    disp = metrics
za = disp.groupby(["Zone","Borough"])[["demand","supply","gap","sdr"]].mean().sort_values("gap", ascending=False).head(20)
fig2 = px.bar(za, x="gap", y="Zone", color="Borough", orientation="h", height=500)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("SDR Heatmap (Hour x Day)")
pv = metrics.pivot_table(values="sdr", index="hour", columns="dow", aggfunc="mean")
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
fig3 = px.imshow(pv.values, x=days, y=list(range(24)), color_continuous_scale="RdYlGn", aspect="auto",
                  labels=dict(x="Day", y="Hour", color="SDR"))
fig3.update_layout(height=400, title="Green=Oversupplied, Red=Undersupplied")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Business Recommendations")
ca, cb = st.columns(2)
with ca:
    st.info("**Supply-Side Actions**")
    bad = za[za["sdr"] < 0.8].head(5)
    for _, r in bad.iterrows():
        st.write(f"- **{r['Zone']}**: Gap {r['gap']:.0f} → Incentivize drivers")
with cb:
    st.info("**Demand-Side Actions**")
    st.write("- Travel Trends widget for peak hours")
    st.write("- Surge pricing 7-9AM residential & 5-7PM CBD")
    st.write("- 'Book earlier to save' push notification")

st.caption("Data: NYC TLC | Framework: Grab Engineering Blog")
