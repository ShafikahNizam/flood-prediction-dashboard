import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import plotly.graph_objects as go

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(page_title="Flood Prediction", layout="wide")

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
<h2>🌧️ Flood Prediction</h2>
<p>
This module predicts future monthly rainfall and evaluates potential flood risk
using Random Forest models trained on historical rainfall data.
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

monthly_cols = [
    "JAN","FEB","MAR","APR","MAY","JUN",
    "JUL","AUG","SEP","OCT","NOV","DEC"
]

df["ANNUAL_RAINFALL"] = df[monthly_cols].sum(axis=1)

model_dir = "rf_models"
state_csv = os.path.join(model_dir, "state_model_summary.csv")

# =================================================
# FLOOD RISK RULES
# =================================================
def flood_risk_label(val):
    if val >= 350:
        return "High Risk"
    elif val >= 250:
        return "Medium Risk"
    else:
        return "Low Risk"

def flood_risk_color(val):
    if val >= 350:
        return "#d62828"
    elif val >= 250:
        return "#f77f00"
    else:
        return "#2a9d8f"

def monthly_risk_shapes():
    return [
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=350, y1=800,
             fillcolor="#d62828", opacity=0.25, layer="below", line_width=0),
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=250, y1=350,
             fillcolor="#f77f00", opacity=0.25, layer="below", line_width=0),
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=0, y1=250,
             fillcolor="#2a9d8f", opacity=0.25, layer="below", line_width=0),
    ]

def annual_risk_shapes():
    return [
        dict(type="rect", xref="paper", yref="y",
             x0=0, x1=1, y0=3000, y1=4000,
             fillcolor="#d62828", opacity=0.22, layer="below", line_width=0),
        dict(type="rect", xref="paper", yref="y",
             x0=0, x1=1, y0=2500, y1=3000,
             fillcolor="#f77f00", opacity=0.22, layer="below", line_width=0),
        dict(type="rect", xref="paper", yref="y",
             x0=0, x1=1, y0=0, y1=2500,
             fillcolor="#2a9d8f", opacity=0.22, layer="below", line_width=0),
    ]

# =================================================
# PREDICTION CHART
# =================================================
def prediction_chart(input_vals, preds, start_month, title):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(1, len(input_vals)+1)),
        y=input_vals,
        mode="lines+markers",
        name="Input Rainfall",
        line=dict(color="#6366f1", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=list(range(start_month, start_month+len(preds))),
        y=preds,
        mode="lines+markers",
        name="Predicted Rainfall",
        line=dict(color="#111827", width=3)
    ))

    # ---- Flood Risk legend entries (IMPORTANT) ----
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=12, color="#d62828"),
        name="High Risk (≥350 mm)"
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=12, color="#f77f00"),
        name="Medium Risk (250–349 mm)"
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=12, color="#2a9d8f"),
        name="Low Risk (<250 mm)"
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Month",
        yaxis_title="Rainfall (mm)",
        shapes=monthly_risk_shapes(),
        yaxis=dict(range=[0, 800]),
        height=420,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=130)
    )

    return fig


# =================================================
# TABS
# =================================================
tab_overall, tab_state = st.tabs(["🌎 Overall Malaysia", "🏞️ By State"])

# =================================================
# ================= OVERALL =================
# =================================================
with tab_overall:

    st.markdown("""
    <div class="card">
    <h3>🌎 Nationwide Rainfall Trend & Prediction</h3>
    <p>
    This section visualizes historical rainfall trends and predicts future rainfall
    levels across Malaysia, with flood risk zones highlighted.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== Annual Rainfall Trend =====
    with tab_overall:

        yearly = df.groupby("YEAR")["ANNUAL_RAINFALL"].mean().reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=yearly["YEAR"],
            y=yearly["ANNUAL_RAINFALL"],
            mode="lines+markers",
            name="Avg Annual Rainfall",
            line=dict(color="#2563eb", width=3)
        ))

        # Legend entries for risk
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
            marker=dict(size=12, color="#d62828"), name="High Risk (≥3000 mm)"))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
            marker=dict(size=12, color="#f77f00"), name="Medium Risk (2500–2999 mm)"))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
            marker=dict(size=12, color="#2a9d8f"), name="Low Risk (<2500 mm)"))

        fig.update_layout(
            title="Average Annual Rainfall (Malaysia)",
            xaxis_title="Year",
            yaxis_title="Rainfall (mm)",
            yaxis=dict(range=[0, 3500]),
            shapes=annual_risk_shapes(),
            height=420,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.15,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=120)
        )

        st.plotly_chart(fig, use_container_width=True)

    # ===== INPUT =====
        n_input = st.slider("Number of past months used as input", 6, 11, 6, key="overall_input")

        model_file = os.path.join(model_dir, f"rf_overall_{n_input}m.sav")

        if not os.path.exists(model_file):
            st.warning("⚠️ Overall Random Forest model not found.")
        else:
            model = joblib.load(model_file)
            st.success("✅ Overall RF model loaded")

            monthly_input = []
            cols = st.columns(n_input)
            for i in range(n_input):
                with cols[i]:
                    monthly_input.append(
                        st.number_input(
                            f"Month {i+1} (mm)",
                            min_value=0.0,
                            value=200.0,
                            step=1.0,
                            key=f"overall_val_{i}"
                        )
                    )

            n_predict = st.slider("Number of future months to predict", 1, 12, 6, key="overall_predict")

            if st.button("🔮 Predict Malaysia Rainfall"):
                seq = monthly_input.copy()
                preds = []

                for _ in range(n_predict):
                    p = model.predict([seq[-n_input:]])[0]
                    preds.append(p)
                    seq.append(p)

                start_month = n_input + 1

                result_df = pd.DataFrame({
                    "Month": [f"Month {start_month+i}" for i in range(n_predict)],
                    "Predicted Rainfall (mm)": np.round(preds, 2),
                    "Flood Risk": [flood_risk_label(p) for p in preds]
                })

                styled = result_df.style.apply(
                    lambda r: [
                        f"background-color:{flood_risk_color(r['Predicted Rainfall (mm)'])}; color:white"
                    ] * len(r),
                    axis=1
                )

                st.markdown("<div class='card'><h4>📊 Prediction Output</h4></div>", unsafe_allow_html=True)
                st.dataframe(styled, use_container_width=True)

                fig_pred = prediction_chart(
                    monthly_input, preds, start_month,
                    "Rainfall Prediction with Flood Risk Zones (Malaysia)"
                )
                st.plotly_chart(fig_pred, use_container_width=True)

# =================================================
# ================= BY STATE =================
# =================================================
with tab_state:

    st.markdown("""
    <div class="card">
    <h3>🏞️ State-Level Rainfall Prediction</h3>
    </div>
    """, unsafe_allow_html=True)

    if not os.path.exists(state_csv):
        st.warning("⚠️ State model summary not found.")
        st.stop()

    summary_df = pd.read_csv(state_csv)

    selected_state = st.selectbox(
        "Select State",
        summary_df["State"].unique(),
        key="state_select"
    )

    df_state = df[df["STATE_NAME"] == selected_state]
    yearly_state = df_state.groupby("YEAR")["ANNUAL_RAINFALL"].mean().reset_index()

    fig_state = go.Figure()

    fig_state.add_trace(go.Scatter(
        x=yearly_state["YEAR"],
        y=yearly_state["ANNUAL_RAINFALL"],
        mode="lines+markers",
        name="Avg Annual Rainfall",
        line=dict(color="#2563eb", width=3)
    ))

    fig_state.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
        marker=dict(size=12, color="#d62828"), name="High Risk (≥3000 mm)"))
    fig_state.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
        marker=dict(size=12, color="#f77f00"), name="Medium Risk (2500–2999 mm)"))
    fig_state.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
        marker=dict(size=12, color="#2a9d8f"), name="Low Risk (<2500 mm)"))

    fig_state.update_layout(
        title=f"Annual Rainfall Trend – {selected_state}",
        xaxis_title="Year",
        yaxis_title="Rainfall (mm)",
        yaxis=dict(range=[0, 3500]),
        shapes=annual_risk_shapes(),
        height=420,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=120)
    )

    st.plotly_chart(fig_state, use_container_width=True)

    n_input = st.slider("Number of past months used as input", 6, 11, 6, key="state_input")

    row = summary_df[
        (summary_df["State"] == selected_state) &
        (summary_df["Input_Months"] == n_input)
    ]

    if row.empty:
        st.warning("⚠️ Model not available.")
        st.stop()

    import os
    import joblib
    
    model_filename = row["Model_File"].values[0]
    
    model_path = os.path.join(
        "rf_models",
        model_filename
    )
    
    model = joblib.load(model_path)
    st.success("✅ State RF model loaded")


    monthly_input = []
    cols = st.columns(n_input)
    for i in range(n_input):
        with cols[i]:
            monthly_input.append(
                st.number_input(
                    f"Month {i+1} (mm)",
                    min_value=0.0,
                    value=200.0,
                    step=1.0,
                    key=f"state_val_{i}"
                )
            )

    n_predict = st.slider("Number of future months to predict", 1, 12, 6, key="state_predict")

    if st.button(f"🔮 Predict for {selected_state}"):
        seq = monthly_input.copy()
        preds = []

        for _ in range(n_predict):
            p = model.predict([seq[-n_input:]])[0]
            preds.append(p)
            seq.append(p)

        start_month = n_input + 1

        result_df = pd.DataFrame({
            "Month": [f"Month {start_month+i}" for i in range(n_predict)],
            "Predicted Rainfall (mm)": np.round(preds, 2),
            "Flood Risk": [flood_risk_label(p) for p in preds]
        })

        styled = result_df.style.apply(
            lambda r: [
                f"background-color:{flood_risk_color(r['Predicted Rainfall (mm)'])}; color:white"
            ] * len(r),
            axis=1
        )

        st.markdown("<div class='card'><h4>📊 Prediction Output</h4></div>", unsafe_allow_html=True)
        st.dataframe(styled, use_container_width=True)

        fig_pred = prediction_chart(
            monthly_input, preds, start_month,
            f"Rainfall Prediction with Flood Risk Zones ({selected_state})"
        )
        st.plotly_chart(fig_pred, use_container_width=True)

# =================================================
# FOOTER
# =================================================
st.markdown("""
<div class="app-footer">
© 2026 MFPS Dashboard | Shafikah Binti Asrul Nizam
</div>
""", unsafe_allow_html=True)
