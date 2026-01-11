# pages/6_Flood_Information.py
import streamlit as st
import os

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Flood Information | Malaysia",
    layout="wide"
)

# =================================================
# LOAD CSS
# =================================================
def load_css():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_dir, "..", "assets", "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

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
<h2>Flood History & Overview in Malaysia</h2>
<p>
This page provides background information on flood events in Malaysia,
including historical floods, contributing factors, impacts, and national
flood management efforts.
</p>
</div>
""", unsafe_allow_html=True)

# =================================================
# SECTION 1: FLOOD OVERVIEW
# =================================================
st.markdown("""
<div class="card">
<h3>📌 Overview of Flooding in Malaysia</h3>
<p>
Flooding is the most frequent natural disaster in Malaysia and occurs almost
every year, particularly during the Northeast Monsoon season (November to March).
Low-lying areas, river basins, and coastal regions are especially vulnerable.
</p>

<p>
Major contributing factors include:
</p>
<ul style="text-align:left; max-width:900px; margin:auto;">
<li>Prolonged and intense monsoon rainfall</li>
<li>River overflow and poor drainage systems</li>
<li>Rapid urbanization and land-use changes</li>
<li>Tidal influences in coastal regions</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =================================================
# SECTION 2: HISTORICAL FLOODS
# =================================================
st.markdown("""
<div class="card">
<h2>🚨 Major Flood Events in Malaysia</h2>
<p>Click the links below to read detailed reports and news coverage.</p>

<ul style="text-align:left; max-width:900px; margin:auto; line-height:1.8;">
<li>
<b>Kelantan Flood (2014)</b> – One of the worst floods in Malaysia’s history  
🔗 <a href="https://reliefweb.int/report/malaysia/malaysian-flood-emergency-response-donor-report-2014" target="_blank">
New Straits Times Report</a>
</li>

<li>
<b>Johor Flood (2006–2007)</b> – Massive evacuation and infrastructure damage  
🔗 <a href="https://en.wikipedia.org/wiki/2006%E2%80%932007_Southeast_Asian_floods" target="_blank">
ReliefWeb Summary</a>
</li>

<li>
<b>Shah Alam & Klang Valley Flood (2021)</b> – Flash floods affecting urban areas  
🔗 <a href="https://insight.estate123.com/2021/12/20/a-short-summary-of-2021-the-great-klang-valley-flood/" target="_blank">
BBC News Coverage</a>
</li>

<li>
<b>Pahang Flood (2022)</b> – Prolonged monsoon rainfall  
🔗 <a href="https://adinet.ahacentre.org/report/malaysia-flooding-in-pahang-state-southeastern-peninsular-malaysia-20220510" target="_blank">
The Star Online</a>
</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =================================================
# SECTION 3: FLOOD IMPACTS
# =================================================
st.markdown("""
<div class="card">
<h3>⚠️ Impacts of Flooding</h3>

<p>
Floods in Malaysia result in wide-ranging impacts:
</p>

<ul style="text-align:left; max-width:900px; margin:auto;">
<li>Loss of lives and displacement of communities</li>
<li>Damage to homes, roads, and public infrastructure</li>
<li>Economic losses affecting businesses and agriculture</li>
<li>Health risks due to waterborne diseases</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =================================================
# SECTION 4: FLOOD IMAGE GALLERY
# =================================================
st.markdown("""
<div class="card">
<h3>🖼️ Flood Scenes in Malaysia</h3>
<p>
Examples of flood situations experienced across different regions in Malaysia.
</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        "assets/images/flood_klang_valley_2021.jpeg",
        caption="Urban Flooding – Klang Valley",
        use_container_width=True
    )

with col2:
    st.image(
        "assets/images/flood_kelantan_2014.jpg",
        caption="Severe Flooding – Kelantan (2014)",
        use_container_width=True
    )

with col3:
    st.image(
        "assets/images/flood_johor.jpg",
        caption="Residential Flood – Johor",
        use_container_width=True
    )

# =================================================
# SECTION 5: FLOOD MANAGEMENT
# =================================================
st.markdown("""
<div class="card">
<h3>🛠️ Flood Management & Mitigation</h3>

<p>
The Malaysian government has implemented various flood mitigation strategies,
including:
</p>

<ul style="text-align:left; max-width:900px; margin:auto;">
<li>Construction of flood retention ponds and dams</li>
<li>Improvement of drainage and river channel systems</li>
<li>Early warning systems and flood forecasting models</li>
<li>Public awareness and disaster preparedness programs</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =================================================
# FOOTER
# =================================================
st.markdown("""
<div class="app-footer">
© 2026 MFPS Dashboard | Shafikah Binti Asrul Nizam
</div>
""", unsafe_allow_html=True)
