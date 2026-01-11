import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import json

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(page_title="Interactive Flood Map", layout="wide")

# =================================================
# LOAD CSS
# =================================================
def load_css():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_dir, "..", "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =================================================
# REMOVE BACKGROUND OVERLAY
# =================================================
st.markdown("""
<style>
.stApp::after { display: none !important; }
</style>
""", unsafe_allow_html=True)

# =================================================
# HEADER
# =================================================
st.markdown("""
<div class="app-header">
🌊 Malaysia Flood Prediction System's Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h1>🗺️ Malaysia Rainfall & Flood Risk Interactive Map</h1>
<p>
This interactive map presents district-level annual rainfall patterns across Malaysia
and highlights associated flood risk levels. Users can explore spatial variations by
state and year to identify flood-prone areas.
</p>
</div>
""", unsafe_allow_html=True)


# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/your_flood_data.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =================================================
# GEOJSON
# =================================================
geojson_path = "data/malaysia_districts.geojson"
if not os.path.exists(geojson_path):
    st.error("GeoJSON file not found")
    st.stop()

# =================================================
# STATE CENTERS
# =================================================
STATE_CENTERS = {
    "Johor": [1.85, 103.5],
    "Kedah": [6.1, 100.4],
    "Kelantan": [5.3, 102.0],
    "Melaka": [2.2, 102.3],
    "Negeri Sembilan": [2.7, 102.1],
    "Pahang": [3.8, 102.4],
    "Perak": [4.8, 101.0],
    "Perlis": [6.6, 100.2],
    "Pulau Pinang": [5.4, 100.3],
    "Sabah": [5.5, 117.0],
    "Sarawak": [2.5, 113.0],
    "Selangor": [3.1, 101.6],
    "Terengganu": [5.2, 103.1],
    "Wilayah Persekutuan": [3.15, 101.7],
}

# =================================================
# FLOOD RISK LOGIC
# =================================================
def assign_flood_risk(rainfall):
    if rainfall >= 3000:
        return "High"
    elif rainfall >= 2500:
        return "Medium"
    else:
        return "Low"

def popup_bg(risk):
    return {
        "High": "#f8d7da",
        "Medium": "#fff3cd",
        "Low": "#d4edda"
    }.get(risk, "#ffffff")

# =================================================
# FILTER CONTROLS
# =================================================
col1, col2 = st.columns(2)

with col1:
    state_to_map = st.selectbox(
        "Select State",
        ["All States"] + sorted(df["STATE_NAME"].unique())
    )

with col2:
    year_to_map = st.selectbox(
        "Select Year",
        sorted(df["YEAR"].unique())
    )

# =================================================
# FILTER & AGGREGATE DATA
# =================================================
map_df = df[df["YEAR"] == year_to_map].copy()

map_df = (
    map_df
    .groupby(["STATE_NAME", "DISTRICT_NAME"], as_index=False)
    .agg({"ANNUAL RAINFALL": "mean"})
)

map_df["flood_risk"] = map_df["ANNUAL RAINFALL"].apply(assign_flood_risk)

if state_to_map != "All States":
    map_df = map_df[map_df["STATE_NAME"] == state_to_map]
    center = STATE_CENTERS.get(state_to_map, [4.2, 101.9])
    zoom = 7
else:
    center = [4.2105, 101.9758]
    zoom = 6

# =================================================
# LOAD & FILTER GEOJSON
# =================================================
with open(geojson_path, encoding="utf-8") as f:
    geojson_data = json.load(f)

valid_districts = set(map_df["DISTRICT_NAME"])
geojson_data["features"] = [
    f for f in geojson_data["features"]
    if f["properties"]["NAME_2"] in valid_districts
]

lookup = map_df.set_index("DISTRICT_NAME").to_dict("index")

# =================================================
# MAP
# =================================================
m = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron")

# ===== CHOROPLETH (Annual Rainfall + BLACK BORDER) =====
folium.Choropleth(
    geo_data=geojson_data,
    data=map_df,
    columns=["DISTRICT_NAME", "ANNUAL RAINFALL"],
    key_on="feature.properties.NAME_2",
    fill_color="YlGnBu",
    fill_opacity=0.85,
    line_color="black",      
    line_weight=0.5,         
    line_opacity=1,
    nan_fill_color="transparent",
    legend_name="Annual Rainfall (mm)"
).add_to(m)

# ===== CUSTOM POPUP (COLORED BY FLOOD RISK) =====
for feature in geojson_data["features"]:
    d = feature["properties"]["NAME_2"]
    row = lookup[d]
    bg = popup_bg(row["flood_risk"])

    html = f"""
    <div style="
        background:{bg};
        padding:10px;
        border-radius:6px;
        font-size:14px;
        min-width:200px;">
        <b>State:</b> {row["STATE_NAME"]}<br>
        <b>District:</b> {d}<br>
        <b>Annual Rainfall:</b> {round(row["ANNUAL RAINFALL"],2)} mm<br>
        <b>Flood Risk:</b> {row["flood_risk"]}
    </div>
    """

    folium.GeoJson(
        feature,
        style_function=lambda x: {
            "fillOpacity": 0,
            "weight": 0,
            "color": "transparent"
        },
        popup=folium.Popup(html, max_width=300)
    ).add_to(m)

# =================================================
# FLOOD RISK LEGEND
# =================================================
legend_html = """
<div style="
position: fixed;
bottom: 40px;
left: 40px;
width: 260px;
background-color: white;
border: 2px solid grey;
z-index:9999;
font-size:14px;
padding: 10px;
border-radius: 6px;
">
<b>Flood Risk Level</b><br>
<span style="color:#dc3545;">■</span> High Risk (≥ 3000 mm)<br>
<span style="color:#ffc107;">■</span> Medium Risk (2500–2999 mm)<br>
<span style="color:#28a745;">■</span> Low Risk (&lt; 2500 mm)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# =================================================
# DISPLAY
# =================================================
st_folium(m, height=650, width="100%")

# =================================================
# FOOTER
# =================================================
st.markdown("""
<div class="app-footer">
© 2026 MFPS Dashboard | Shafikah Binti Asrul Nizam
</div>
""", unsafe_allow_html=True)
