import streamlit as st
import os

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Malaysia Flood Prediction System's Dashboard",
    page_icon="🌊",
    layout="wide"
)

# -------------------------------------------------
# Load CSS
# -------------------------------------------------
def load_css():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_dir, "assets", "style.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(base_dir, "..", "assets", "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="app-header">
🌊 Malaysia Flood Prediction System's Dashboard
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# OVERVIEW
# -------------------------------------------------
st.markdown("""
<div class="card">
    <h1>Dashboard Overview</h1>
    <p style="max-width:850px; margin:auto;">
        Historical rainfall and flood-related records in Malaysia from
        <b>2000–2010</b>, enabling spatial and temporal exploration across
        states and districts.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# METRIC CARDS
# -------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""<div class="metric-card"><small>Total Records</small><h2>825</h2></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""<div class="metric-card"><small>States Covered</small><h2>11</h2></div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class="metric-card"><small>Districts</small><h2>67</h2></div>""", unsafe_allow_html=True)
with m4:
    st.markdown("""<div class="metric-card"><small>Years of Data</small><h2>11</h2></div>""", unsafe_allow_html=True)

# -------------------------------------------------
# FLOOD SUMMARY
# -------------------------------------------------
f1, f2 = st.columns(2)

with f1:
    st.markdown("""
    <div class="flood-card">
        <small>Flood Cases</small>
        <h2>347</h2>
        <p>42.1% of records</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="safe-card">
        <small>No Flood</small>
        <h2>478</h2>
        <p>Normal conditions</p>
    </div>
    """, unsafe_allow_html=True)



# -------------------------------------------------
# AVAILABLE MODULES (VISUAL MENU)
# -------------------------------------------------
st.markdown("""
<div class="card modules-card">
    <h3>Available Modules</h3>
    <ul style="text-align:left; max-width:500px; margin:auto;">
        <li><b>Admin Panel</b> – Dataset diagnostics & EDA</li>
        <li><b>Flood Information</b> – History & flood background in Malaysia</li>
        <li><b>Overview</b> – National flood & rainfall summary</li>
        <li><b>Rainfall Pattern</b> – Temporal rainfall analysis</li>
        <li><b>Interactive Map</b> – Spatial flood visualization</li>
        <li><b>Flood Prediction</b> – ML-based rainfall prediction</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div class="app-footer">
© 2026 MFPS Dashboard | Shafikah Binti Asrul Nizam
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR HINT
# -------------------------------------------------
st.sidebar.success("👉 Use the sidebar to navigate between modules")
