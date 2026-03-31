"""
streamlit_app.py
================
EV Charging Infrastructure Dashboard
Author: Nisrina Afnan Walyadin
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="EV Charging Infrastructure — Germany",
    page_icon="⚡",
    layout="wide"
)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(base, "outputs", "germany_stations_clustered.csv"))
    return df

df = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.title("⚡ Filters")

speed_options = ["All"] + sorted(df["speed_category"].dropna().unique().tolist())
selected_speed = st.sidebar.selectbox("Speed Category", speed_options)

cluster_options = ["All"] + sorted(df["cluster"].unique().tolist())
selected_cluster = st.sidebar.selectbox("Cluster", cluster_options)

desert_options = {"All": None, "Charging Deserts Only": True, "Non-Desert Only": False}
selected_desert = st.sidebar.selectbox("Desert Zone", list(desert_options.keys()))

year_min, year_max = int(df["year_created"].min()), int(df["year_created"].max())
selected_years = st.sidebar.slider("Year Created", year_min, year_max, (year_min, year_max))

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = df.copy()
if selected_speed != "All":
    filtered = filtered[filtered["speed_category"] == selected_speed]
if selected_cluster != "All":
    filtered = filtered[filtered["cluster"] == selected_cluster]
if desert_options[selected_desert] is not None:
    filtered = filtered[filtered["is_desert"] == desert_options[selected_desert]]
filtered = filtered[filtered["year_created"].between(selected_years[0], selected_years[1])]

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("⚡ EV Charging Infrastructure Analysis — Germany")
st.caption("Portfolio Project · Nisrina Afnan Walyadin · MSc Mathematics, TU Munich")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total = len(filtered)
ultra_fast = len(filtered[filtered["speed_category"] == "Ultra-Fast (≥100 kW)"])
pct_ultra = (ultra_fast / total * 100) if total > 0 else 0
desert_count = filtered["is_desert"].sum()
avg_power = filtered["max_power_kw"].mean()

col1.metric("Total Stations", f"{total:,}")
col2.metric("Ultra-Fast (≥100 kW)", f"{ultra_fast:,}", f"{pct_ultra:.1f}% of total")
col3.metric("Charging Deserts", f"{int(desert_count):,}")
col4.metric("Avg Max Power", f"{avg_power:.1f} kW" if not pd.isna(avg_power) else "N/A")

st.divider()

# ── Row 1: Map + Speed Distribution ──────────────────────────────────────────
col_map, col_pie = st.columns([2, 1])

with col_map:
    st.subheader("Station Locations")
    map_df = filtered.dropna(subset=["lat", "lon"])
    color_map = {
        "Ultra-Fast (≥100 kW)": "#E63946",
        "Fast (50-99 kW)":       "#F4A261",
        "Medium (22-49 kW)":     "#2A9D8F",
        "Slow (<22 kW)":         "#457B9D",
        "Unknown":               "#CCCCCC",
    }
    fig_map = px.scatter_mapbox(
        map_df,
        lat="lat", lon="lon",
        color="speed_category",
        color_discrete_map=color_map,
        hover_data={"city": True, "max_power_kw": True, "operator": True, "lat": False, "lon": False},
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 51.2, "lon": 10.4},
        height=450,
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend_title="Speed")
    st.plotly_chart(fig_map, use_container_width=True)

with col_pie:
    st.subheader("Speed Distribution")
    speed_counts = filtered["speed_category"].value_counts()
    fig_pie = px.pie(
        values=speed_counts.values,
        names=speed_counts.index,
        color=speed_counts.index,
        color_discrete_map=color_map,
        hole=0.4,
    )
    fig_pie.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=True)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Desert Zones")
    desert_counts = filtered["is_desert"].value_counts()
    labels = {True: "Desert", False: "Normal"}
    fig_desert = px.pie(
        values=desert_counts.values,
        names=[labels.get(i, i) for i in desert_counts.index],
        color_discrete_sequence=["#E63946", "#2A9D8F"],
        hole=0.4,
    )
    fig_desert.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_desert, use_container_width=True)

# ── Row 2: Growth Over Time + Cluster ────────────────────────────────────────
col_line, col_bar = st.columns(2)

with col_line:
    st.subheader("Station Growth Over Time")
    growth = filtered.groupby("year_created").size().reset_index(name="count")
    fig_line = px.line(
        growth, x="year_created", y="count",
        markers=True,
        color_discrete_sequence=["#2A9D8F"],
    )
    fig_line.update_layout(xaxis_title="Year", yaxis_title="New Stations", margin=dict(t=10))
    st.plotly_chart(fig_line, use_container_width=True)

with col_bar:
    st.subheader("Stations by Cluster")
    cluster_counts = filtered.groupby("cluster").size().reset_index(name="count")
    fig_bar = px.bar(
        cluster_counts, x="cluster", y="count",
        color="count",
        color_continuous_scale="Teal",
        text="count",
    )
    fig_bar.update_layout(xaxis_title="Cluster", yaxis_title="Stations", margin=dict(t=10), coloraxis_showscale=False)
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Raw Data Table ────────────────────────────────────────────────────────────
with st.expander("View Raw Data"):
    st.dataframe(
        filtered[["title", "city", "speed_category", "max_power_kw", "num_points", "cluster", "is_desert", "year_created"]],
        use_container_width=True,
        height=300,
    )