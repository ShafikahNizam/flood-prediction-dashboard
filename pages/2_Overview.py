import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Overview",
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
<h2>Flood Events & Rainfall Analytics Overview</h2>
<p>
This dashboard presents nationwide and state-level insights into rainfall patterns
and flood occurrences in Malaysia (2000–2010).
</p>
</div>
""", unsafe_allow_html=True)

# =================================================
# TABS
# =================================================
tab_overall, tab_state = st.tabs([
    "🌍 Overall (Malaysia)",
    "🗺️ By State"
])

# =================================================
# OVERALL TAB
# =================================================
with tab_overall:

    total_floods = int(df["FLOOD"].sum())
    avg_rainfall = round(df["TOTAL_ANNUAL"].mean(), 1)
    most_flood_state = df[df["FLOOD"] == 1]["STATE_NAME"].value_counts().idxmax()
    wettest_district = df.groupby("DISTRICT_NAME")["TOTAL_ANNUAL"].mean().idxmax()

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card'><small>Total Flood Events</small><h2>{total_floods}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><small>Avg Annual Rainfall</small><h2>{avg_rainfall} mm</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><small>Most Flood-Prone State</small><h2>{most_flood_state}</h2></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card'><small>Wettest District</small><h2>{wettest_district}</h2></div>", unsafe_allow_html=True)

    # =================================================
    # CHART 1: FLOOD EVENTS BY STATE
    # =================================================
    flood_by_state = (
        df[df["FLOOD"] == 1]
        .groupby("STATE_NAME")
        .size()
        .reset_index(name="Flood Events")
        .sort_values("Flood Events", ascending=False)
    )

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig1 = px.bar(
            flood_by_state,
            x="STATE_NAME",
            y="Flood Events",
            color="STATE_NAME",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig1.update_layout(
            height=340,
            showlegend=False,
            margin=dict(l=80, r=40, t=50, b=90)
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("<div class='table-title'>Flood Events by State</div>", unsafe_allow_html=True)
        st.dataframe(flood_by_state, use_container_width=True, hide_index=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Flood events are concentrated in several states, indicating
        regional vulnerability influenced by climatic and geographical factors.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 2: YEARLY RAINFALL vs FLOOD EVENTS
    # =================================================
    yearly = df.groupby("YEAR").agg(
        Avg_Rainfall=("TOTAL_ANNUAL", "mean"),
        Flood_Events=("FLOOD", "sum")
    ).reset_index()

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig2 = px.bar(
            yearly,
            x="YEAR",
            y="Avg_Rainfall",
            color="Avg_Rainfall",
            color_continuous_scale="Blues"
        )
        fig2.add_scatter(
            x=yearly["YEAR"],
            y=yearly["Flood_Events"] * 100,
            mode="lines+markers",
            name="Flood Events (scaled)"
        )
        fig2.update_layout(
            height=340,
            margin=dict(l=80, r=40, t=50, b=80),
            legend=dict(
                orientation="h",
                y=1.05,
                x=0.5,
                xanchor="center"
            )
        )
        fig2.update_yaxes(tickformat=",")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div class='table-title'>Yearly Rainfall & Flood Events</div>", unsafe_allow_html=True)
        st.dataframe(yearly, use_container_width=True, hide_index=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Although higher rainfall often aligns with increased flood events,
        rainfall alone does not fully explain flood occurrence trends.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 3: MONTHLY RAINFALL DISTRIBUTION
    # =================================================
    monthly_state = df.groupby("STATE_NAME")[monthly_cols].sum().reset_index()
    monthly_long = monthly_state.melt(
        id_vars="STATE_NAME",
        var_name="Month",
        value_name="Rainfall"
    )

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig3 = px.bar(
            monthly_long,
            x="STATE_NAME",
            y="Rainfall",
            color="Month",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig3.update_layout(
            height=360,
            margin=dict(l=80, r=40, t=50, b=120)
        )
        fig3.update_yaxes(tickformat=",")
        st.plotly_chart(fig3, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Monthly rainfall patterns reflect monsoon-driven seasonality,
        which significantly affects flood intensity across states.
        </p>
        </div>
        """, unsafe_allow_html=True)

# =================================================
# BY STATE TAB
# =================================================
with tab_state:

    st.markdown("""
    <div class="card">
    <h3>🗺️ State-Level Analysis</h3>
    <p>
    Detailed flood and rainfall characteristics for the selected state.
    </p>
    </div>
    """, unsafe_allow_html=True)

    selected_state = st.selectbox(
        "Select State",
        sorted(df["STATE_NAME"].unique()),
        key="overview_state_select"
    )

    df_state = df[df["STATE_NAME"] == selected_state]

    state_floods = int(df_state["FLOOD"].sum())
    state_avg_rain = round(df_state["TOTAL_ANNUAL"].mean(), 1)
    worst_district = df_state[df_state["FLOOD"] == 1]["DISTRICT_NAME"].value_counts().idxmax()

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><small>Total Flood Events</small><h2>{state_floods}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><small>Avg Annual Rainfall</small><h2>{state_avg_rain} mm</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><small>Most Flood-Prone District</small><h2>{worst_district}</h2></div>", unsafe_allow_html=True)

    # =================================================
    # CHART 1: FLOOD EVENTS BY DISTRICT
    # =================================================
    district_floods = (
        df_state[df_state["FLOOD"] == 1]
        .groupby("DISTRICT_NAME")
        .size()
        .reset_index(name="Flood Events")
        .sort_values("Flood Events", ascending=False)
    )

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig4 = px.bar(
            district_floods,
            x="DISTRICT_NAME",
            y="Flood Events",
            color="Flood Events",
            color_continuous_scale="Reds"
        )
        fig4.update_layout(
            height=330,
            margin=dict(l=80, r=40, t=50, b=120)
        )
        st.plotly_chart(fig4, use_container_width=True)

        st.markdown("<div class='table-title'>Flood Events by District</div>", unsafe_allow_html=True)
        st.dataframe(district_floods, use_container_width=True, hide_index=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Flood events within the selected state are concentrated
        in specific districts, indicating localized flood hotspots.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 2: MONTHLY RAINFALL CONTRIBUTION
    # =================================================
    monthly_sum = df_state[monthly_cols].sum().reset_index()
    monthly_sum.columns = ["Month", "Rainfall"]

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig5 = px.bar(
            monthly_sum,
            x="Month",
            y="Rainfall",
            color="Month",
            text_auto=".2s",
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        fig5.update_layout(
            title="Monthly Rainfall Contribution",
            height=360,
            xaxis_title="Month",
            yaxis_title="Total Rainfall (mm)",
            legend_title="Month",
            legend=dict(
                orientation="v",
                y=0.5,
                x=1.02,
                xanchor="left"
            ),
            margin=dict(l=80, r=140, t=60, b=80)
        )

        st.plotly_chart(fig5, use_container_width=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Monthly rainfall distribution highlights monsoon-driven peaks,
        where specific months contribute disproportionately to annual rainfall,
        increasing seasonal flood risk.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # CHART 3: FLOOD TREND BY YEAR
    # =================================================
    flood_trend = df_state.groupby("YEAR")["FLOOD"].sum().reset_index()

    col_c, col_i = st.columns([3, 2])

    with col_c:
        fig6 = px.bar(
            flood_trend,
            x="YEAR",
            y="FLOOD",
            color="FLOOD",
            color_continuous_scale="Blues"
        )
        fig6.update_layout(
            height=300,
            margin=dict(l=80, r=40, t=50, b=80)
        )
        st.plotly_chart(fig6, use_container_width=True)

        st.markdown("<div class='table-title'>Flood Trend by Year</div>", unsafe_allow_html=True)
        st.dataframe(flood_trend, use_container_width=True, hide_index=True)

    with col_i:
        st.markdown("""
        <div class="interpretation-card">
        <h4>📘 Interpretation</h4>
        <p>
        Flood frequency varies across years, reflecting
        inter-annual climate variability within the state.
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
