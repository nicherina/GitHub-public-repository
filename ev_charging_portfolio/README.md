# ⚡ EV Charging Infrastructure Analysis — Germany & Europe

> **Portfolio Project** | Nisrina Afnan Walyadin  
> Skills demonstrated: Python · SQL · K-Means Clustering · Geospatial Analytics · Power BI · Data Pipeline Design

---

## 🎯 Project Overview

This project analyses the current state of EV charging infrastructure across Germany and neighbouring European countries, with a focus on:

- **Geographic distribution** of charging stations and coverage gaps
- **Charger speed segmentation** (slow / medium / fast / ultra-fast ≥100 kW)
- **Cluster analysis** using K-Means to identify regional patterns
- **Charging desert detection** — areas with high mobility demand but low ultra-fast coverage
- **Growth trends** in EV infrastructure deployment (2010–2025)

The methodology mirrors real-world approaches used by EV network operators to plan infrastructure expansion and identify underserved regions.

---

## 📊 Key Findings

| Metric | Value |
|--------|-------|
| Total stations analysed (DE) | ~15,000+ |
| Ultra-fast stations (≥100 kW) | ~X% of total |
| Charging desert zones identified | X clusters |
| YoY growth rate (2020–2024) | ~X% |

*(Values populated after running the analysis)*

---

## 🗂️ Project Structure

```
ev_charging_portfolio/
│
├── utils/
│   └── fetch_data.py          # Pulls data from Open Charge Map API
│
├── notebooks/
│   └── ev_charging_analysis.py  # Main analysis: EDA, clustering, desert detection
│
├── dashboard/
│   └── folium_map.py          # Interactive HTML map (open in browser)
│
├── outputs/                   # Generated charts, CSVs, maps
│   ├── 01_eda_overview.png
│   ├── 02_elbow_silhouette.png
│   ├── 03_cluster_map.png
│   ├── 04_charging_deserts.png
│   ├── germany_stations_clustered.csv   ← Load into Power BI
│   └── ev_charging_map.html             ← Interactive map
│
├── data/                      # Raw + clean data (gitignored for size)
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Fetch data from Open Charge Map
```bash
python utils/fetch_data.py
```
*Free API, no key required. Fetches ~30,000+ stations across DE, AT, NL, FR, CH, PL, CZ.*

### 3. Run the analysis
```bash
python notebooks/ev_charging_analysis.py
```
*Outputs charts and a clustered CSV ready for Power BI.*

### 4. Generate the interactive map
```bash
python dashboard/folium_map.py
```
*Opens in any browser. Includes heatmap, clustered markers, and desert zones.*

### 5. Power BI Dashboard
Load `outputs/germany_stations_clustered.csv` into Power BI and build:
- 🗺️ Map visual using `lat` / `lon` fields
- 🔢 KPI cards: total stations, % ultra-fast, desert zones
- 🎛️ Slicers: `speed_category`, `cluster`, `is_desert`, `year_created`
- 📈 Line chart: station growth over time (`year_created`)

---

## 🔬 Methodology

### Data Source
[Open Charge Map](https://openchargemap.org/) — the largest open database of EV charging locations worldwide. Data includes station coordinates, operator info, charger power levels, and connection types.

### Charger Speed Categories
| Category | Power |
|----------|-------|
| Ultra-Fast | ≥ 100 kW |
| Fast | 50–99 kW |
| Medium | 22–49 kW |
| Slow | < 22 kW |

### Clustering Approach
K-Means clustering applied to geographic coordinates (lat/lon) to identify regional infrastructure hubs. Optimal k selected via:
- **Elbow method** (inertia vs. k)
- **Silhouette score** (cluster cohesion)

### Charging Desert Detection
Clusters where ultra-fast (≥100 kW) penetration falls below 5% are flagged as potential "charging deserts" — areas likely underserved by high-power EV infrastructure, representing expansion opportunities.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | Data wrangling |
| Scikit-learn | K-Means clustering |
| Matplotlib / Seaborn | Static visualisations |
| Folium | Interactive geospatial map |
| Power BI | Business intelligence dashboard |
| Open Charge Map API | Data source |

---

## 💡 Relevance to EV Industry

This analysis demonstrates skills directly applicable to roles in EV infrastructure companies:
- **Demand forecasting** based on geographic and usage patterns
- **Network planning** — identifying where new stations are needed
- **Data pipeline design** — from API to cleaned, analysis-ready dataset
- **BI dashboard development** — translating analysis into business decisions

---

## 👩‍💻 Author

**Nisrina Afwan Walyadin**  
MSc Mathematics, Technical University of Munich  
[LinkedIn](https://linkedin.com/in/nisrina-walyadin-5b7345178) · nisrinawalyadin@gmail.com
