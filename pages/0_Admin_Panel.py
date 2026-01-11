import streamlit as st
import os
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Admin | Flood Dataset EDA",
    page_icon="🔐",
    layout="wide"
)

# =================================================
# LOAD CSS
# =================================================
def load_css():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_dir, "..", "assets", "style.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(base_dir, "assets", "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =================================================
# SESSION STATE
# =================================================
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "admin_user" not in st.session_state:
    st.session_state.admin_user = None

# =================================================
# LOAD ADMIN USERS
# =================================================
@st.cache_data
def load_admin_users():
    return pd.read_csv("data/admin_users.csv")

admins_df = load_admin_users()

# =================================================
# 🔐 LOGIN PAGE (SIDEBAR HIDDEN)
# =================================================
if not st.session_state.admin_authenticated:

    # ❌ HIDE SIDEBAR COMPLETELY
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="app-header">
    🔐 Malaysia Flood Dataset – Admin Panel
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:
        st.markdown("""
        <div class="admin-login-card">
            <h2>Admin Login</h2>
            <p>Please login to access the EDA dashboard</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("admin_login_form", clear_on_submit=True):

            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")

            login_btn = st.form_submit_button("🔓 Login", use_container_width=True)

            if login_btn:
                match = admins_df[
                    (admins_df["username"] == username) &
                    (admins_df["password"] == password)
                ]

                if not match.empty:
                    st.session_state.admin_authenticated = True
                    st.session_state.admin_user = username
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

        # ✅ HOME BUTTON
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("Home.py")  # pastikan file Home.py wujud

    st.markdown("""
    <div class="app-footer">
    © 2026 MFPS Dashboard | Admin Access
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# =================================================
# ✅ ADMIN DASHBOARD (SIDEBAR ENABLED)
# =================================================

st.markdown("""
<div class="app-header">
🔐 Malaysia Flood Dataset – Admin Panel
</div>
""", unsafe_allow_html=True)

# LOGOUT
colA, colB = st.columns([8, 1])
with colB:
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# INTRO
st.markdown(f"""
<div class="card">
    <h1>Admin Dashboard</h1>
    <p>
        Welcome, <b>{st.session_state.admin_user}</b>.  
        This section provides automated Exploratory Data Analysis (EDA)
        for the Malaysian Flood Dataset.
    </p>
</div>
""", unsafe_allow_html=True)

# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    return pd.read_csv("data/your_flood_data.csv")

df = load_data()

# =================================================
# METRICS
# =================================================
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"<div class='metric-card'><small>Total Records</small><h2>{df.shape[0]}</h2></div>", unsafe_allow_html=True)

with m2:
    st.markdown(f"<div class='metric-card'><small>Total Columns</small><h2>{df.shape[1]}</h2></div>", unsafe_allow_html=True)

with m3:
    st.markdown(f"<div class='metric-card'><small>Missing Values</small><h2>{int(df.isna().sum().sum())}</h2></div>", unsafe_allow_html=True)

# =================================================
# EDA REPORT
# =================================================
st.markdown("""
<div class="card">
    <h3>📊 Automated Exploratory Data Analysis Report</h3>
    <p>Interactive report below shows dataset characteristics.</p>
</div>
""", unsafe_allow_html=True)

profile = ProfileReport(df, explorative=True)
html(profile.to_html(), height=1100, scrolling=True)

# =================================================
# FOOTER
# =================================================
st.markdown("""
<div class="app-footer">
© 2026 Malaysia Flood Prediction System's Dashboard | Admin Panel
</div>
""", unsafe_allow_html=True)
