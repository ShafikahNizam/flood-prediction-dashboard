# pages/5_Rainfall_Pattern.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Rainfall Pattern Analysis",
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
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/your_flood_data.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

monthly_cols = [
    "JAN","FEB","MAR","APR","MAY","JUN",
    "JUL","AUG","SEP","OCT","NOV","DEC"
]

df["TOTAL_ANNUAL"] = df[monthly_cols].sum(axis=1)
df["YEAR"] = df["YEAR"].astype(int)

# =================================================
# HEADER (GLOBAL DASHBOARD HEADER KEKAL)
# =================================================
st.markdown("""
<div class="app-header">
🌧️ Malaysia Flood Prediction System's Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h2>Rainfall Pattern Analysis & Exploration</h2>
<p>
This page analyzes rainfall distribution across Malaysia at national and state levels.
Users can explore long-term trends, seasonal patterns, and rainfall variability that
may contribute to flood risk.
</p>
</div>
""", unsafe_allow_html=True)

# =================================================
# TABS
# =================================================
tab_overall, tab_state = st.tabs(["📊 Overall Malaysia", "🗺️ By State"])

# =================================================
# OVERALL MALAYSIA
# =================================================
with tab_overall:

    st.markdown("""
    <div class="card">
    <h3>📌 National Rainfall Overview</h3>
    <p>
    This section highlights long-term rainfall trends and seasonal distribution
    across Malaysia.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # -------- Year Range Slider (UNIQUE KEY) --------
    year_min, year_max = df["YEAR"].min(), df["YEAR"].max()
    year_range = st.slider(
        "Select Year Range",
        int(year_min), int(year_max),
        (int(year_min), int(year_max)),
        key="overall_year_slider"
    )

    df_sel = df[
        (df["YEAR"] >= year_range[0]) &
        (df["YEAR"] <= year_range[1])
    ]

    # =================================================
    # CHART 1: ANNUAL RAINFALL TREND
    # =================================================
    yearly = df_sel.groupby("YEAR")["TOTAL_ANNUAL"].sum().reset_index()

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig1 = px.line(
            yearly,
            x="YEAR",
            y="TOTAL_ANNUAL",
            markers=True
        )
        fig1.add_hline(
            y=yearly["TOTAL_ANNUAL"].mean(),
            line_dash="dot",
            annotation_text="Long-Term Average"
        )
        fig1.update_layout(
            height=320,
            margin=dict(l=80, r=40, t=50, b=60)
        )
        fig1.update_yaxes(tickformat=",")
        st.plotly_chart(fig1, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Annual rainfall exhibits noticeable fluctuations across years. Periods
        exceeding the long-term average indicate increased exposure to extreme
        rainfall and potential flood risk.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 2: 5-YEAR MOVING AVERAGE
    # =================================================
    yearly["MA5"] = yearly["TOTAL_ANNUAL"].rolling(5, min_periods=1).mean()

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=yearly["YEAR"],
            y=yearly["TOTAL_ANNUAL"],
            mode="lines+markers",
            name="Annual Rainfall"
        ))
        fig2.add_trace(go.Scatter(
            x=yearly["YEAR"],
            y=yearly["MA5"],
            mode="lines",
            name="5-Year Moving Average",
            line=dict(color="red")
        ))
        fig2.update_layout(
            height=320,
            margin=dict(l=80, r=40, t=50, b=60),
            legend=dict(
                orientation="h",
                y=1.05,
                x=0.5,
                xanchor="center"
            )
        )
        fig2.update_yaxes(tickformat=",")
        st.plotly_chart(fig2, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        The moving average smooths short-term variability and highlights long-term
        rainfall tendencies. An upward trend suggests increasing rainfall intensity
        over time.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 3: MONTHLY RAINFALL DISTRIBUTION
    # =================================================
    monthly_total = df_sel[monthly_cols].sum().reset_index()
    monthly_total.columns = ["Month", "Rainfall"]

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig3 = px.bar(
            monthly_total,
            x="Month",
            y="Rainfall",
            color="Month",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig3.update_layout(
            height=320,
            margin=dict(l=80, r=40, t=40, b=80)
        )
        fig3.update_yaxes(tickformat=",")
        st.plotly_chart(fig3, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Rainfall is unevenly distributed throughout the year. Monsoon months
        contribute disproportionately to annual rainfall, increasing seasonal
        flood risk.
        </p>
        </div>
        """, unsafe_allow_html=True)

# =================================================
# BY STATE
# =================================================
with tab_state:

    st.markdown("""
    <div class="card">
    <h3>🗺️ State-Level Rainfall Analysis</h3>
    <p>
    This section focuses on rainfall trends and seasonal characteristics within
    individual states.
    </p>
    </div>
    """, unsafe_allow_html=True)

    selected_state = st.selectbox(
        "Select State",
        sorted(df["STATE_NAME"].unique()),
        key="state_select_rainfall"
    )

    df_state = df[df["STATE_NAME"] == selected_state]

    year_min_s, year_max_s = df_state["YEAR"].min(), df_state["YEAR"].max()
    year_range_state = st.slider(
        "Select Year Range (State)",
        int(year_min_s), int(year_max_s),
        (int(year_min_s), int(year_max_s)),
        key="state_year_slider"
    )

    df_state_sel = df_state[
        (df_state["YEAR"] >= year_range_state[0]) &
        (df_state["YEAR"] <= year_range_state[1])
    ]

    # =================================================
    # CHART 1: STATE YEARLY RAINFALL
    # =================================================
    state_yearly = df_state_sel.groupby("YEAR")["TOTAL_ANNUAL"].sum().reset_index()

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig4 = px.line(state_yearly, x="YEAR", y="TOTAL_ANNUAL", markers=True)
        fig4.update_layout(height=320)
        fig4.update_yaxes(tickformat=",")
        st.plotly_chart(fig4, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Rainfall trends vary across years within the selected state, reflecting
        localized climate influences and flood exposure.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 2: STATE 5-YEAR MOVING AVERAGE
    # =================================================
    state_yearly["MA5"] = state_yearly["TOTAL_ANNUAL"].rolling(5, min_periods=1).mean()

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=state_yearly["YEAR"],
            y=state_yearly["TOTAL_ANNUAL"],
            mode="lines+markers",
            name="Annual Rainfall"
        ))
        fig5.add_trace(go.Scatter(
            x=state_yearly["YEAR"],
            y=state_yearly["MA5"],
            mode="lines",
            name="5-Year Moving Average",
            line=dict(color="red")
        ))
        fig5.update_layout(
            height=320,
            legend=dict(
                orientation="h",
                y=1.05,
                x=0.5,
                xanchor="center"
            )
        )
        fig5.update_yaxes(tickformat=",")
        st.plotly_chart(fig5, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        The moving average smooths short-term fluctuations and highlights persistent
        rainfall patterns linked to flood susceptibility.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 3: STATE MONTHLY DISTRIBUTION
    # =================================================
    state_monthly = df_state[monthly_cols].sum().reset_index()
    state_monthly.columns = ["Month", "Rainfall"]

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig6 = px.bar(
            state_monthly,
            x="Month",
            y="Rainfall",
            color="Month",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig6.update_layout(
            height=340,
            legend_title_text="Month",
            legend=dict(
                orientation="h",
                y=-0.3,
                x=0.5,
                xanchor="center",
            ),
            margin=dict(b=140)
        )
        fig6.update_yaxes(tickformat=",")
        st.plotly_chart(fig6, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Seasonal rainfall peaks align with monsoon periods, which are
        closely associated with increased flood risk.
        </p>
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
