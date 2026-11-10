"""
Interactive Streamlit Dashboard for Wireless Signal Propagation Model Analysis.

Launch with:
    streamlit run app.py
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Ensure src is in python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from propagation.analysis.comparator import ModelComparator
from propagation.models import (
    FreeSpacePathLoss,
    TwoRayGroundReflection,
    LogDistancePathLoss,
    OkumuraModel,
    HataModel,
    COST231HataModel,
    LogNormalShadowing,
)
from propagation.core.link_budget import LinkBudget
from propagation.visualization.plotting import MODEL_PALETTE, MODEL_LABELS, MODEL_STYLES


# Streamlit Page Config
st.set_page_config(
    page_title="Wireless Signal Propagation Models",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📡 Comparative Analysis of Wireless Signal Propagation Models")
st.markdown(
    "**Project Team:** Harsh Yadav (RA2311003011546), Utkarsh Dabas (RA2311003011550), Tamanna Singh (RA2311003011570)  \n"
    "**Department:** Electronics & Communication Engineering &nbsp;|&nbsp; **Academic Year:** 2025–2026 &nbsp;|&nbsp; **Version:** 1.0.0"
)
st.write(
    "Interactive simulation framework evaluating theoretical, empirical, and stochastic "
    "propagation models under configurable carrier frequencies, distances, antenna parameters, and environments."
)

# -------------------------------------------------------------
# SIDEBAR PARAMETERS
# -------------------------------------------------------------
st.sidebar.header("🔧 Simulation Parameters")

# Frequency & Environment
freq_mhz = st.sidebar.number_input("Carrier Frequency (MHz)", min_value=150.0, max_value=6000.0, value=1800.0, step=50.0)
environment = st.sidebar.selectbox(
    "Environment Preset",
    ["urban", "suburban", "rural", "indoor_obstructed"],
    index=0,
)

# Distance Range
st.sidebar.subheader("Distance Range")
col_d1, col_d2 = st.sidebar.columns(2)
min_d_km = col_d1.number_input("Min Distance (km)", min_value=0.01, max_value=10.0, value=0.1, step=0.05)
max_d_km = col_d2.number_input("Max Distance (km)", min_value=0.5, max_value=100.0, value=10.0, step=1.0)
num_points = st.sidebar.slider("Number of Points", min_value=50, max_value=500, value=200, step=25)

# Antenna & RF Power
st.sidebar.subheader("Antenna & RF Link")
tx_power_dbm = st.sidebar.number_input("Transmit Power Pt (dBm)", min_value=0.0, max_value=60.0, value=43.0, step=1.0)
tx_gain_dbi = st.sidebar.number_input("Tx Antenna Gain Gt (dBi)", min_value=0.0, max_value=30.0, value=15.0, step=1.0)
rx_gain_dbi = st.sidebar.number_input("Rx Antenna Gain Gr (dBi)", min_value=-5.0, max_value=15.0, value=0.0, step=1.0)
system_loss_db = st.sidebar.number_input("System Losses Lsys (dB)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
rx_sens_dbm = st.sidebar.number_input("Rx Sensitivity Threshold (dBm)", min_value=-130.0, max_value=-40.0, value=-100.0, step=5.0)

# Antenna Heights
col_h1, col_h2 = st.sidebar.columns(2)
ht_m = col_h1.number_input("Base Height ht (m)", min_value=1.5, max_value=500.0, value=30.0, step=5.0)
hr_m = col_h2.number_input("Mobile Height hr (m)", min_value=0.5, max_value=20.0, value=1.5, step=0.5)

# Model Selection
st.sidebar.subheader("Active Models")
all_models = ["fspl", "two_ray", "log_distance", "okumura", "hata", "cost231", "shadowing"]
selected_models = st.sidebar.multiselect(
    "Select Models to Compare",
    options=all_models,
    default=all_models,
    format_func=lambda k: MODEL_LABELS.get(k, k),
)

# -------------------------------------------------------------
# NUMERICAL COMPUTATION
# -------------------------------------------------------------
distances_km = np.geomspace(min_d_km, max_d_km, num_points)

budget = LinkBudget(
    tx_power_dbm=tx_power_dbm,
    tx_gain_dbi=tx_gain_dbi,
    rx_gain_dbi=rx_gain_dbi,
    system_loss_db=system_loss_db,
    rx_sensitivity_dbm=rx_sens_dbm,
)

pl_dict = {}
pr_dict = {}

model_instances = {
    "fspl": FreeSpacePathLoss(),
    "two_ray": TwoRayGroundReflection(ht_default=ht_m, hr_default=hr_m),
    "log_distance": LogDistancePathLoss(environment=environment if environment in ["urban", "suburban", "rural", "indoor_obstructed"] else "urban"),
    "okumura": OkumuraModel(hte_default=ht_m, hre_default=hr_m, environment="open" if environment == "rural" else environment),
    "hata": HataModel(hb_default=ht_m, hm_default=hr_m, environment="rural" if environment == "rural" else ("suburban" if environment == "suburban" else "urban_medium")),
    "cost231": COST231HataModel(hb_default=ht_m, hm_default=hr_m, environment="suburban" if environment == "suburban" else "medium_city"),
    "shadowing": LogNormalShadowing(n=3.0, sigma_db=6.0, seed=42),
}

for m_key in selected_models:
    model = model_instances[m_key]
    kwargs = {}
    if m_key == "two_ray":
        kwargs = {"ht": ht_m, "hr": hr_m}
    elif m_key in {"okumura", "hata", "cost231"}:
        kwargs = {"hb": ht_m, "hm": hr_m, "hte": ht_m, "hre": hr_m}
    elif m_key == "shadowing":
        kwargs = {"seed": 42}

    pl_arr = model.calculate_path_loss(
        distance=distances_km,
        frequency=freq_mhz,
        distance_unit="km",
        frequency_unit="MHz",
        strict=False,
        **kwargs,
    )
    pl_arr = np.asarray(pl_arr, dtype=np.float64)
    pr_arr = budget.calculate_received_power_dbm(pl_arr)

    pl_dict[m_key] = pl_arr
    pr_dict[m_key] = pr_arr

# -------------------------------------------------------------
# DASHBOARD TABS
# -------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Path Loss & Received Power",
    "🎬 Animated Simulation",
    "📊 Statistical Analysis",
    "📋 Model Comparison Matrix",
    "🎲 Shadowing & Outage Analysis",
    "⚡ Link Budget Calculator",
])

# TAB 1: Comparative Plots
with tab1:
    st.subheader("Comparative Propagation Curves")
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        fig1, ax1 = plt.subplots(figsize=(6.5, 4.5))
        for key in selected_models:
            ax1.plot(distances_km, pl_dict[key], label=MODEL_LABELS.get(key, key),
                     color=MODEL_PALETTE.get(key), linestyle=MODEL_STYLES.get(key, "-"), lw=1.8)
        ax1.set_xscale("log")
        ax1.set_xlabel("Distance (km)")
        ax1.set_ylabel("Path Loss (dB)")
        ax1.set_title(f"Path Loss vs Distance (f = {freq_mhz:.0f} MHz)")
        ax1.grid(True, which="both", ls=":")
        ax1.legend(fontsize=8, loc="upper left")
        st.pyplot(fig1)

    with col_p2:
        fig2, ax2 = plt.subplots(figsize=(6.5, 4.5))
        for key in selected_models:
            ax2.plot(distances_km, pr_dict[key], label=MODEL_LABELS.get(key, key),
                     color=MODEL_PALETTE.get(key), linestyle=MODEL_STYLES.get(key, "-"), lw=1.8)
        ax2.axhline(rx_sens_dbm, color="black", linestyle="--", lw=1.2, label=f"Sensitivity ({rx_sens_dbm:.0f} dBm)")
        ax2.set_xscale("log")
        ax2.set_xlabel("Distance (km)")
        ax2.set_ylabel("Received Power (dBm)")
        ax2.set_title(f"Received Power vs Distance (Pt = {tx_power_dbm:.0f} dBm)")
        ax2.grid(True, which="both", ls=":")
        ax2.legend(fontsize=8, loc="lower left")
        st.pyplot(fig2)

# TAB 2: Animated Simulation
with tab2:
    st.subheader("🎬 Animated Signal Propagation & Curve Tracing")
    gif_path = ROOT_DIR / "animated_path_loss.gif"
    
    col_a1, col_a2 = st.columns([3, 2])
    with col_a1:
        if gif_path.exists():
            st.image(str(gif_path), caption="Live Progressive Curve Tracing (Free Space vs Okumura vs Hata)", use_container_width=True)
        else:
            st.info("Animated GIF not found. Run scripts/generate_animation.py to generate.")
    with col_a2:
        st.markdown(
            """
            ### 📡 Animation Highlights
            - **Progressive Curve Drawing:** Visualizes signal decay from $1\\text{ km}$ to $20\\text{ km}$ across all three benchmark models.
            - **Real-Time Divergence:** Watch the delta between Hata Urban and Free Space expand from $+34.9\\text{ dB}$ at $1\\text{ km}$ to $+54.7\\text{ dB}$ at $20\\text{ km}$.
            - **Tip Tracker:** Moving points track the instantaneous path loss and received power at each step.
            
            #### Benchmark Readings (f = 900 MHz):
            - **At 1 km:**
              - Free Space: `91.5 dB`
              - Okumura Open: `97.9 dB`
              - Hata Urban: `126.4 dB`
            - **At 20 km:**
              - Free Space: `117.5 dB`
              - Okumura Open: `143.7 dB`
              - Hata Urban: `172.2 dB`
            """
        )

# TAB 3: Summary Stats
with tab3:
    st.subheader("Descriptive Summary Statistics Across Models")
    records = []
    for key in selected_models:
        pl = pl_dict[key]
        pr = pr_dict[key]
        records.append({
            "Model": MODEL_LABELS.get(key, key),
            "Min PL (dB)": f"{np.min(pl):.1f}",
            "Max PL (dB)": f"{np.max(pl):.1f}",
            "Mean PL (dB)": f"{np.mean(pl):.1f}",
            "Std PL (dB)": f"{np.std(pl):.1f}",
            "Min Pr (dBm)": f"{np.min(pr):.1f}",
            "Max Pr (dBm)": f"{np.max(pr):.1f}",
            "Mean Pr (dBm)": f"{np.mean(pr):.1f}",
        })
    df_stats = pd.DataFrame(records)
    st.dataframe(df_stats, use_container_width=True)

    # Downloadable CSV
    df_export = pd.DataFrame({"distance_km": distances_km})
    for key in selected_models:
        df_export[f"PL_{key}_dB"] = pl_dict[key]
        df_export[f"Pr_{key}_dBm"] = pr_dict[key]
    csv_bytes = df_export.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Simulation Data (CSV)", data=csv_bytes, file_name="simulation_results.csv", mime="text/csv")

# TAB 4: Comparison Matrix
with tab4:
    st.subheader("Formal Comparative Analysis Matrix")
    matrix_df = ModelComparator.get_comparison_table()
    st.dataframe(matrix_df, use_container_width=True)

# TAB 5: Shadowing Analysis
with tab5:
    st.subheader("Log-Normal Shadow Fading & Outage Probability")
    col_s1, col_s2 = st.columns(2)
    shadow_std = col_s1.slider("Shadow Fading Std Dev sigma (dB)", min_value=1.0, max_value=14.0, value=6.0, step=0.5)

    shadow_model = LogNormalShadowing(n=3.0, sigma_db=shadow_std, seed=42)
    p_outage = shadow_model.calculate_outage_probability(
        distance=distances_km,
        frequency=freq_mhz,
        rx_sensitivity_dbm=rx_sens_dbm,
        tx_power_dbm=tx_power_dbm,
        tx_gain_dbi=tx_gain_dbi,
        rx_gain_dbi=rx_gain_dbi,
        system_loss_db=system_loss_db,
        distance_unit="km",
        frequency_unit="MHz",
        sigma=shadow_std,
    )

    with col_s1:
        fig_out, ax_out = plt.subplots(figsize=(6.5, 4.0))
        ax_out.plot(distances_km, p_outage * 100.0, "r-", lw=2.2, label=f"Outage Probability (sigma={shadow_std} dB)")
        ax_out.axhline(5.0, color="green", linestyle="--", label="Target Outage <= 5% (95% Reliability)")
        ax_out.set_xscale("log")
        ax_out.set_xlabel("Distance (km)")
        ax_out.set_ylabel("Outage Probability (%)")
        ax_out.set_title("Link Outage Probability vs Distance")
        ax_out.grid(True, which="both", ls=":")
        ax_out.legend()
        st.pyplot(fig_out)

    with col_s2:
        st.markdown(
            f"""
            ### Shadow Fading Engineering Insights:
            - **Standard Deviation:** $\\sigma = {shadow_std:.1f}\\text{{ dB}}$ captures spatial clutter variance.
            - **95% Reliability Margin:** Requires an extra fade margin of $1.96 \\times \\sigma = {1.96 * shadow_std:.1f}\\text{{ dB}}$ above receiver sensitivity.
            - **Outage Transition:** Notice how the outage curve transitions sharply from 0% near the transmitter to 100% as distance approaches the cell edge.
            """
        )

# TAB 6: Link Budget Calculator
with tab6:
    st.subheader("Interactive RF Link Budget Calculator")
    eval_dist_km = st.slider("Select Target Distance (km)", min_value=float(min_d_km), max_value=float(max_d_km), value=float(min(3.0, max_d_km)), step=0.1)

    eval_idx = np.argmin(np.abs(distances_km - eval_dist_km))
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    kpi_col1.metric("EIRP", f"{budget.eirp_dbm:.1f} dBm")
    fspl_loss = pl_dict.get("fspl", [0])[eval_idx]
    kpi_col2.metric("Free Space Loss", f"{fspl_loss:.1f} dB")
    hata_loss = pl_dict.get("cost231", pl_dict.get("hata", [0]))[eval_idx]
    kpi_col3.metric("Cellular Path Loss", f"{hata_loss:.1f} dB")
    fade_margin = budget.calculate_fade_margin(hata_loss)
    kpi_col4.metric("Fade Margin", f"{fade_margin:.1f} dB", delta=f"{fade_margin:.1f} dB" if fade_margin > 0 else "Outage Risk!")

