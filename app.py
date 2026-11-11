"""
Interactive Streamlit Dashboard for Wireless Signal Propagation Model Analysis.

Launch with:
    streamlit run app.py
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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


# =====================================================================
#  PAGE CONFIG & CUSTOM CSS
# =====================================================================
st.set_page_config(
    page_title="Wireless Signal Propagation Models",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global styling ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1524 0%, #162032 100%);
    border-right: 1px solid rgba(56,189,248,0.15);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span { color: #cbd5e1 !important; }

/* ── Glowing cards ── */
.metric-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95));
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(56,189,248,0.5);
    box-shadow: 0 8px 40px rgba(56,189,248,0.15), 0 4px 20px rgba(0,0,0,0.4);
}
.metric-card .label { color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.metric-card .value { font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.metric-card .unit { color: #64748b; font-size: 12px; margin-top: 2px; }
.metric-card .hint { color: #475569; font-size: 11px; margin-top: 8px; font-style: italic; }

/* ── Section Titles ── */
.section-header {
    background: linear-gradient(90deg, rgba(56,189,248,0.08) 0%, transparent 70%);
    border-left: 4px solid #38bdf8;
    padding: 12px 20px;
    border-radius: 0 12px 12px 0;
    margin: 12px 0 16px 0;
}
.section-header h3 { color: #e2e8f0 !important; margin: 0 !important; font-weight: 700 !important; font-size: 18px !important; }
.section-header .hint { color: #64748b; font-size: 13px; margin-top: 4px; }

/* ── Info banner ── */
.info-banner {
    background: linear-gradient(135deg, rgba(56,189,248,0.08), rgba(129,140,248,0.08));
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 12px;
    padding: 14px 18px;
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 12px;
}
.info-banner strong { color: #e2e8f0; }
.info-banner code { background: rgba(56,189,248,0.1); color: #38bdf8; padding: 2px 6px; border-radius: 4px; font-size: 12px; }

/* ── Graph legend card ── */
.graph-legend {
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 10px;
}
.graph-legend .item { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; color: #cbd5e1; font-size: 13px; }
.graph-legend .dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.graph-legend .line-sample { width: 24px; height: 3px; display: inline-block; flex-shrink: 0; border-radius: 2px; }

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] { gap: 6px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(30,41,59,0.6) !important;
    border: 1px solid rgba(56,189,248,0.12) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: all 0.3s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(129,140,248,0.15)) !important;
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
}

/* ── Streamlit metric override ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95));
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: rgba(56,189,248,0.4);
    box-shadow: 0 4px 20px rgba(56,189,248,0.1);
}

/* ── DataFrame / Table ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ── Buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
.stDownloadButton > button:hover { box-shadow: 0 4px 20px rgba(59,130,246,0.4) !important; transform: translateY(-1px) !important; }

/* ── Hide streamlit default branding ── */
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
header[data-testid="stHeader"] { background: transparent !important; }

/* ── Pulse Animation ── */
@keyframes pulse-glow { 0%, 100% { box-shadow: 0 0 5px rgba(56,189,248,0.3); } 50% { box-shadow: 0 0 20px rgba(56,189,248,0.6); } }
.pulse-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    animation: pulse-glow 2.5s ease-in-out infinite;
}

/* ── Smooth page header ── */
.page-header {
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9));
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.page-header h1 { color: #f1f5f9 !important; font-size: 28px !important; font-weight: 800 !important; margin-bottom: 4px !important; }
.page-header .subtitle { color: #94a3b8; font-size: 14px; line-height: 1.5; }
.page-header .badge { background: rgba(56,189,248,0.15); color: #38bdf8; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# =====================================================================
#  HERO HEADER
# =====================================================================
st.markdown("""
<div class="page-header">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
        <div>
            <h1>📡 Comparative Analysis of Wireless Signal Propagation Models</h1>
            <p class="subtitle">
                Interactive simulation framework evaluating <strong>theoretical</strong>, <strong>empirical</strong>, and <strong>stochastic</strong>
                propagation models — adjusting carrier frequencies, distances, antenna heights, and environmental clutter in real time.
            </p>
        </div>
        <div style="text-align:right;">
            <span class="badge">21CSE458T — Wireless & Mobile Communication</span><br>
            <p style="color:#64748b; font-size:12px; margin-top:8px;">
                <strong style="color:#cbd5e1;">Harsh Yadav</strong> (RA2311003011546)<br>
                <strong style="color:#cbd5e1;">Utkarsh Dabas</strong> (RA2311003011550)<br>
                <strong style="color:#cbd5e1;">Tamanna Singh</strong> (RA2311003011570)
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================================
#  SIDEBAR — Annotated Parameters with Descriptions
# =====================================================================

# --- Sidebar Header ---
st.sidebar.markdown("""
<div style="text-align:center; padding:16px 0 8px 0;">
    <span style="font-size:24px;">⚙️</span>
    <h3 style="color:#e2e8f0; margin:4px 0 0 0; font-size:17px;">Simulation Controls</h3>
    <p style="color:#64748b; font-size:11px; margin-top:2px;">Adjust parameters below to re-run the simulation in real time</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

# --- Carrier Frequency ---
st.sidebar.markdown("**📻 Carrier Frequency** *(The radio wave frequency transmitted by the base station tower)*")
freq_mhz = st.sidebar.number_input(
    "Carrier Frequency (MHz)  [e.g., 900 = GSM, 1800 = LTE, 2400 = Wi-Fi]",
    min_value=150.0, max_value=6000.0, value=1800.0, step=50.0,
    help="Higher frequency → higher path loss. Standard bands: 900 MHz (GSM-900), 1800 MHz (LTE Band 3), 2100 MHz (3G UMTS), 2400 MHz (Wi-Fi 2.4G)."
)

# --- Environment Preset ---
st.sidebar.markdown("**🏙️ Environment Preset** *(Physical terrain and clutter type around the signal path)*")
environment = st.sidebar.selectbox(
    "Select the deployment environment",
    ["urban", "suburban", "rural", "indoor_obstructed"],
    index=0,
    format_func=lambda x: {
        "urban": "🏢 Urban — Dense buildings, narrow streets (n ≈ 3.5–4.5)",
        "suburban": "🏘️ Suburban — Houses, trees, moderate spacing (n ≈ 2.8–3.5)",
        "rural": "🌾 Rural — Open fields, farmland, minimal clutter (n ≈ 2.0–2.5)",
        "indoor_obstructed": "🏠 Indoor — Walls, partitions, furniture (n ≈ 4.0–6.0)",
    }.get(x, x),
    help="The environment determines the path loss exponent 'n'. Urban has many obstacles → higher loss. Rural is open → lower loss. The exponent 'n' represents how fast signal power decays with distance."
)

st.sidebar.divider()

# --- Distance Range ---
st.sidebar.markdown("**📏 Distance Range** *(How far from the tower to compute signal decay)*")
col_d1, col_d2 = st.sidebar.columns(2)
min_d_km = col_d1.number_input(
    "Min Distance (km) [Near tower]",
    min_value=0.01, max_value=10.0, value=0.1, step=0.05,
    help="Closest evaluation point to the base station. Typical minimum: 0.1 km (100 m) for macrocells."
)
max_d_km = col_d2.number_input(
    "Max Distance (km) [Cell edge]",
    min_value=0.5, max_value=100.0, value=10.0, step=1.0,
    help="Farthest coverage boundary. Typical values: 5–20 km for macrocells, 0.5–2 km for microcells."
)
num_points = st.sidebar.slider(
    "Number of Evaluation Points  [Resolution of the plotted curves]",
    min_value=50, max_value=500, value=200, step=25,
    help="More points = smoother curves but slightly slower computation. 200 points is a good balance."
)

st.sidebar.divider()

# --- Antenna & RF Link ---
st.sidebar.markdown("**📶 Antenna & RF Link Budget** *(Transmitter power, antenna gains, and receiver sensitivity)*")

tx_power_dbm = st.sidebar.number_input(
    "Transmit Power Pt (dBm)  [Base station RF output power]",
    min_value=0.0, max_value=60.0, value=43.0, step=1.0,
    help="RF power from the base station amplifier. 43 dBm = 20 Watts (standard macrocell tower). 30 dBm = 1 Watt (small cell). Measured at the transmitter output before antenna gain."
)
tx_gain_dbi = st.sidebar.number_input(
    "Tx Antenna Gain Gt (dBi)  [Tower antenna directional gain]",
    min_value=0.0, max_value=30.0, value=15.0, step=1.0,
    help="How much the tower antenna focuses energy toward users. 15 dBi = typical 120° sector antenna. 0 dBi = omnidirectional. EIRP = Pt + Gt."
)
rx_gain_dbi = st.sidebar.number_input(
    "Rx Antenna Gain Gr (dBi)  [Mobile handset antenna gain]",
    min_value=-5.0, max_value=15.0, value=0.0, step=1.0,
    help="Mobile phone antenna gain. Typically 0 dBi (omnidirectional dipole). Negative values indicate lossy/inefficient antennas."
)
system_loss_db = st.sidebar.number_input(
    "System Losses Lsys (dB)  [Cable, connector & body losses]",
    min_value=0.0, max_value=10.0, value=3.0, step=0.5,
    help="Combined losses from coaxial cable, connectors, duplexer, and human body absorption. Typically 2–4 dB."
)
rx_sens_dbm = st.sidebar.number_input(
    "Rx Sensitivity Threshold (dBm)  [Minimum detectable signal]",
    min_value=-130.0, max_value=-40.0, value=-100.0, step=5.0,
    help="Minimum received power for the mobile to successfully decode the signal. -100 dBm = typical GSM. -104 dBm = LTE with coding gain. Below this → call drops / no service."
)

st.sidebar.divider()

# --- Antenna Heights ---
st.sidebar.markdown("**🗼 Antenna Heights** *(Physical heights of the tower and mobile device)*")
col_h1, col_h2 = st.sidebar.columns(2)
ht_m = col_h1.number_input(
    "Tower Height hₜ (m)",
    min_value=1.5, max_value=500.0, value=30.0, step=5.0,
    help="Base station antenna height above ground. 30 m = standard macro tower. Taller tower → better coverage, lower path loss."
)
hr_m = col_h2.number_input(
    "Mobile Height hᵣ (m)",
    min_value=0.5, max_value=20.0, value=1.5, step=0.5,
    help="Height of the user's handset. 1.5 m = person holding phone to ear. 1.0 m = phone in hand at waist. 3 m = vehicle-mounted."
)

st.sidebar.divider()

# --- Model Selection ---
st.sidebar.markdown("**🧮 Active Propagation Models** *(Select which models to compute and compare)*")
all_models = ["fspl", "two_ray", "log_distance", "okumura", "hata", "cost231", "shadowing"]

# Annotated model descriptions for multiselect
MODEL_DESCRIPTIONS = {
    "fspl": "📐 Free Space (Friis) — Theoretical LOS, no obstacles",
    "two_ray": "🌊 Two-Ray Ground Reflection — Direct + ground-bounce interference",
    "log_distance": "📊 Log-Distance — Configurable exponent n for any environment",
    "okumura": "🗾 Okumura Model — Empirical, from Tokyo drive-test data (1968)",
    "hata": "📱 Okumura-Hata — Closed-form standard for macrocellular planning",
    "cost231": "🇪🇺 COST-231 Hata — Extended Hata for PCS bands (1.5–2.0 GHz)",
    "shadowing": "🎲 Log-Normal Shadowing — Stochastic fading with random variation σ",
}

selected_models = st.sidebar.multiselect(
    "Select Models to Compare",
    options=all_models,
    default=all_models,
    format_func=lambda k: MODEL_DESCRIPTIONS.get(k, MODEL_LABELS.get(k, k)),
    help="Each model captures different physical effects. Select multiple models to see how their predictions diverge with distance. The spread between models reveals the 'reality gap' between theory and practice."
)

st.sidebar.divider()
st.sidebar.markdown("""
<div style="text-align:center; padding:8px; color:#475569; font-size:11px;">
    🧪 <strong>SRM IST</strong> — Dept. of Computing Technologies<br>
    21CSE458T — Wireless & Mobile Communication<br>
    B.Tech CSE, 7th Semester — AY 2025–2026
</div>
""", unsafe_allow_html=True)


# =====================================================================
#  NUMERICAL COMPUTATION (unchanged logic)
# =====================================================================
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


# =====================================================================
#  LIVE KPI CARDS (Top Row)
# =====================================================================
st.markdown("""
<div class="section-header">
    <h3>⚡ Real-Time Simulation Dashboard</h3>
    <p class="hint">These values update instantly when you change any parameter in the sidebar</p>
</div>
""", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Carrier Frequency</div>
        <div class="value">{freq_mhz:.0f}</div>
        <div class="unit">MHz</div>
        <div class="hint">Radio wave frequency</div>
    </div>""", unsafe_allow_html=True)

with kpi2:
    eirp_val = tx_power_dbm + tx_gain_dbi
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">EIRP (Effective Radiated Power)</div>
        <div class="value">{eirp_val:.1f}</div>
        <div class="unit">dBm = Pt ({tx_power_dbm:.0f}) + Gt ({tx_gain_dbi:.0f})</div>
        <div class="hint">Total radiated power including antenna gain</div>
    </div>""", unsafe_allow_html=True)

with kpi3:
    mid_idx = len(distances_km) // 2
    mid_d = distances_km[mid_idx]
    fspl_mid = pl_dict.get("fspl", np.zeros(len(distances_km)))[mid_idx]
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Free Space Loss @ {mid_d:.1f} km</div>
        <div class="value">{fspl_mid:.1f}</div>
        <div class="unit">dB (theoretical minimum loss)</div>
        <div class="hint">Lower bound — no obstacles</div>
    </div>""", unsafe_allow_html=True)

with kpi4:
    env_display = {"urban": "🏢 Urban", "suburban": "🏘️ Suburban", "rural": "🌾 Rural", "indoor_obstructed": "🏠 Indoor"}.get(environment, environment)
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Active Environment</div>
        <div class="value" style="font-size:22px;">{env_display}</div>
        <div class="unit">Terrain clutter preset</div>
        <div class="hint">Affects empirical model corrections</div>
    </div>""", unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Models Being Compared</div>
        <div class="value">{len(selected_models)}</div>
        <div class="unit">of {len(all_models)} available models</div>
        <div class="hint">Toggle models in the sidebar</div>
    </div>""", unsafe_allow_html=True)


# =====================================================================
#  MATPLOTLIB DARK THEME HELPER
# =====================================================================
DARK_BG = "#0f172a"
CARD_BG = "#1e293b"
GRID_COLOR = "#334155"
TEXT_COLOR = "#e2e8f0"
MUTED_COLOR = "#94a3b8"
ACCENT_CYAN = "#38bdf8"

def style_dark_axes(fig, ax, title="", xlabel="", ylabel="", xlabel_hint="", ylabel_hint=""):
    """Apply premium dark theme to matplotlib figure and axes."""
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT_COLOR, fontsize=14, fontweight='bold', pad=14)
    
    xl = f"{xlabel}  ({xlabel_hint})" if xlabel_hint else xlabel
    yl = f"{ylabel}  ({ylabel_hint})" if ylabel_hint else ylabel
    ax.set_xlabel(xl, color=MUTED_COLOR, fontsize=11, fontweight='medium')
    ax.set_ylabel(yl, color=MUTED_COLOR, fontsize=11, fontweight='medium')
    
    ax.tick_params(colors=MUTED_COLOR, labelsize=10)
    ax.grid(True, which="both", ls=":", color=GRID_COLOR, alpha=0.6)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    
    legend = ax.legend(fontsize=9, loc="upper left", frameon=True,
                       facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    return legend


# =====================================================================
#  DASHBOARD TABS
# =====================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Path Loss & Received Power",
    "🎬 Animated Simulation",
    "📊 Statistical Analysis",
    "📋 Model Comparison Matrix",
    "🎲 Shadowing & Outage Analysis",
    "⚡ Link Budget Calculator",
])


# ── TAB 1: Path Loss & Received Power ──
with tab1:
    st.markdown("""
    <div class="section-header">
        <h3>📈 Comparative Propagation Curves</h3>
        <p class="hint">Side-by-side visualization of how signal attenuates (Path Loss) and what power the mobile phone actually receives (Received Power) vs distance</p>
    </div>
    """, unsafe_allow_html=True)

    # Legend explainer
    st.markdown("""
    <div class="info-banner">
        <strong>📖 How to Read These Graphs:</strong><br>
        • <strong>Left Graph — Path Loss (dB):</strong> Shows signal <em>attenuation</em>. Higher values = more signal absorbed by environment. Curves going UP means worse reception.<br>
        • <strong>Right Graph — Received Power (dBm):</strong> Shows actual signal power arriving at the mobile phone. Curves going DOWN means weaker signal. When a curve drops below the <strong>black dashed sensitivity line</strong>, the phone loses connection.<br>
        • <strong>X-Axis (logarithmic):</strong> Distance from tower in kilometers. Log scale spreads out short distances for detail.<br>
        • <strong>Each colored line</strong> represents a different propagation model. Lines that are further apart show greater <em>disagreement</em> between models.
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        fig1, ax1 = plt.subplots(figsize=(7, 5))
        for key in selected_models:
            ax1.plot(distances_km, pl_dict[key], label=MODEL_LABELS.get(key, key),
                     color=MODEL_PALETTE.get(key), linestyle=MODEL_STYLES.get(key, "-"), lw=2.0)
        ax1.set_xscale("log")
        style_dark_axes(fig1, ax1,
                        title=f"Path Loss vs Distance  (f = {freq_mhz:.0f} MHz)",
                        xlabel="Distance", ylabel="Path Loss",
                        xlabel_hint="km, logarithmic scale",
                        ylabel_hint="dB — higher = more signal loss")
        st.pyplot(fig1)

    with col_p2:
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        for key in selected_models:
            ax2.plot(distances_km, pr_dict[key], label=MODEL_LABELS.get(key, key),
                     color=MODEL_PALETTE.get(key), linestyle=MODEL_STYLES.get(key, "-"), lw=2.0)
        ax2.axhline(rx_sens_dbm, color="#f87171", linestyle="--", lw=1.5,
                     label=f"Rx Sensitivity Threshold ({rx_sens_dbm:.0f} dBm)")
        ax2.set_xscale("log")
        style_dark_axes(fig2, ax2,
                        title=f"Received Power vs Distance  (Pt = {tx_power_dbm:.0f} dBm, Gt = {tx_gain_dbi:.0f} dBi)",
                        xlabel="Distance", ylabel="Received Power",
                        xlabel_hint="km, logarithmic scale",
                        ylabel_hint="dBm — power at mobile phone")
        ax2.legend(fontsize=9, loc="lower left", frameon=True,
                   facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        st.pyplot(fig2)

    # Annotated color legend
    legend_items = "".join([
        f'<div class="item"><span class="dot" style="background:{MODEL_PALETTE.get(k, "#999")};"></span>'
        f'<span><strong>{MODEL_LABELS.get(k, k)}</strong> — {MODEL_DESCRIPTIONS.get(k, "").split("—")[-1].strip() if "—" in MODEL_DESCRIPTIONS.get(k, "") else ""}</span></div>'
        for k in selected_models
    ])
    st.markdown(f"""
    <div class="graph-legend">
        <strong style="color:#e2e8f0; font-size:13px;">🎨 Color & Line Legend (What Each Curve Represents):</strong>
        <div style="margin-top:8px;">{legend_items}</div>
        <div class="item" style="margin-top:8px;"><span class="line-sample" style="background:#f87171; border-top: 2px dashed #f87171; height:0;"></span>
        <span><strong>⚠️ Red Dashed Line</strong> — Receiver sensitivity threshold. Below this line = no cellular service (dead zone).</span></div>
    </div>
    """, unsafe_allow_html=True)


# ── TAB 2: Animated Simulation ──
with tab2:
    st.markdown("""
    <div class="section-header">
        <h3>🎬 Animated Signal Propagation & Real-Time Wave Simulation</h3>
        <p class="hint">Live motion-graphics visualization of electromagnetic waves radiating from the tower (synced with your sidebar settings) + progressive path loss curve tracing</p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive HTML5 Canvas Wave Propagation Animation synced with sidebar parameters
    import streamlit.components.v1 as components
    live_wave_html = f"""
    <div style="background:#0f172a; border:1px solid rgba(56,189,248,0.25); border-radius:16px; padding:16px; font-family:Inter, sans-serif; color:#e2e8f0;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div>
                <strong style="font-size:15px; color:#38bdf8;">🗼 Live Electromagnetic Wavefront Simulation</strong>
                <span style="font-size:12px; color:#94a3b8; margin-left:10px;">
                    (Synced: f = {freq_mhz:.0f} MHz | hₜ = {ht_m:.0f} m | hᵣ = {hr_m:.1f} m | Max d = {max_d_km:.1f} km)
                </span>
            </div>
            <span style="background:rgba(34,197,94,0.2); color:#4ade80; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:700;">● LIVE MOTION</span>
        </div>
        <canvas id="waveSim" style="width:100%; height:240px; border-radius:10px; background:#090d16; display:block;"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; font-size:12px; color:#94a3b8;">
            <div>
                <span style="color:#38bdf8;">🔵 Blue Arc: Free Space (Longest Reach)</span> &nbsp;|&nbsp;
                <span style="color:#4ade80;">🟢 Green Arc: Okumura Open</span> &nbsp;|&nbsp;
                <span style="color:#f87171;">🔴 Red Arc: Hata Urban (Attenuated by Buildings)</span>
            </div>
            <div id="liveMetricReadout" style="font-family:monospace; color:#facc15; font-weight:bold;">Loading...</div>
        </div>
    </div>
    <script>
        const cvs = document.getElementById('waveSim');
        const ctx = cvs.getContext('2d');
        const freq = {freq_mhz};
        const ht = {ht_m};
        const hr = {hr_m};
        const maxD = {max_d_km};
        let t = 0;
        let pulses = [];

        function fspl(d) {{ return 20*Math.log10(Math.max(d,0.01)) + 20*Math.log10(freq) + 32.44; }}
        function hata(d) {{
            const a = (1.1*Math.log10(freq)-0.7)*hr - (1.56*Math.log10(freq)-0.8);
            return 69.55 + 26.16*Math.log10(freq) - 13.82*Math.log10(Math.max(ht,1)) - a + (44.9 - 6.55*Math.log10(Math.max(ht,1)))*Math.log10(Math.max(d,0.01));
        }}

        function draw() {{
            const rect = cvs.getBoundingClientRect();
            if (cvs.width !== rect.width) {{ cvs.width = rect.width; cvs.height = rect.height; }}
            const w = cvs.width, h = cvs.height;
            ctx.clearRect(0, 0, w, h);

            // Sky & Ground
            const grad = ctx.createLinearGradient(0, 0, 0, h*0.78);
            grad.addColorStop(0, '#090d16'); grad.addColorStop(1, '#1e293b');
            ctx.fillStyle = grad; ctx.fillRect(0, 0, w, h*0.78);
            ctx.fillStyle = '#0f172a'; ctx.fillRect(0, h*0.78, w, h*0.22);

            const baseLine = h * 0.78;
            const txX = 65;
            const towerH = Math.min(ht * 1.8 + 40, h * 0.62);
            const txY = baseLine - towerH;

            // Buildings (Urban Clutter)
            const blds = [0.22, 0.30, 0.39, 0.48, 0.58, 0.68, 0.78, 0.88];
            blds.forEach((bx, idx) => {{
                const x = w * bx;
                const bh = 35 + ((idx * 23) % 45);
                ctx.fillStyle = '#1e293b';
                ctx.strokeStyle = '#334155';
                ctx.fillRect(x, baseLine - bh, 32, bh);
                ctx.strokeRect(x, baseLine - bh, 32, bh);
            }});

            // Spawn signal pulses
            if (t % 35 === 0) pulses.push({{ r: 0 }});
            pulses = pulses.filter(p => p.r < w * 1.1);
            pulses.forEach(p => {{
                p.r += 2.6;
                const a = Math.max(0, 1 - p.r / (w * 0.95));
                // Free Space Wave
                ctx.beginPath(); ctx.arc(txX, txY, p.r, -0.45, 0.45);
                ctx.strokeStyle = `rgba(56, 189, 248, ${{a * 0.75}})`; ctx.lineWidth = 2.5; ctx.stroke();
                // Okumura Wave
                ctx.beginPath(); ctx.arc(txX, txY, p.r * 0.72, -0.45, 0.45);
                ctx.strokeStyle = `rgba(74, 222, 128, ${{a * 0.75}})`; ctx.lineWidth = 2.5; ctx.stroke();
                // Hata Urban Wave
                ctx.beginPath(); ctx.arc(txX, txY, p.r * 0.46, -0.45, 0.45);
                ctx.strokeStyle = `rgba(248, 113, 113, ${{a * 0.85}})`; ctx.lineWidth = 2.5; ctx.stroke();
            }});

            // Tower Mast
            ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(txX - 10, baseLine); ctx.lineTo(txX, txY); ctx.lineTo(txX + 10, baseLine); ctx.stroke();
            ctx.beginPath(); ctx.arc(txX, txY, 5, 0, Math.PI*2); ctx.fillStyle = '#ef4444'; ctx.fill();

            // Moving Mobile User
            const prog = (t % 400) / 400;
            const rxX = txX + 40 + prog * (w - txX - 100);
            const curD = Math.max(0.1, prog * maxD);
            ctx.fillStyle = '#38bdf8'; ctx.fillRect(rxX - 6, baseLine - 22, 12, 20);
            ctx.fillStyle = '#0f172a'; ctx.fillRect(rxX - 4, baseLine - 19, 8, 12);

            ctx.fillStyle = '#e2e8f0'; ctx.font = 'bold 12px monospace'; ctx.textAlign = 'center';
            ctx.fillText(`📱 ${{curD.toFixed(1)}} km`, rxX, baseLine + 16);

            const curFS = fspl(curD);
            const curHT = hata(curD);
            document.getElementById('liveMetricReadout').textContent =
                `d = ${{curD.toFixed(1)}} km | FSPL: ${{curFS.toFixed(1)}} dB | Hata: ${{curHT.toFixed(1)}} dB`;

            t++;
            requestAnimationFrame(draw);
        }}
        requestAnimationFrame(draw);
    </script>
    """
    components.html(live_wave_html, height=330)

    gif_path = ROOT_DIR / "animated_path_loss.gif"

    col_a1, col_a2 = st.columns([3, 2])
    with col_a1:
        if gif_path.exists():
            st.image(str(gif_path), caption="Progressive curve tracing: Blue = Free Space (lowest loss), Green = Okumura (moderate), Red = Hata Urban (highest loss)", width="stretch")
        else:
            st.info("⚠️ Animated GIF not found. Run `python scripts/generate_animation.py` to generate.")
    with col_a2:
        st.markdown("""
        <div class="info-banner">
            <strong>📡 What These Animations Show:</strong><br><br>
            <strong>1. Top Wavefront Simulator:</strong> Shows how radio waves radiate outward from the tower at your exact sidebar settings. Notice how building clutter shrinks the urban reach (red arc) compared to free space (blue arc).<br><br>
            <strong>2. Progressive Curve Tracing (Left):</strong> Draws all three curves simultaneously from <code>1 km</code> to <code>20 km</code> at <code>900 MHz</code>.<br><br>
            <strong>💡 Key Insight:</strong> The gap between Hata Urban and Free Space widens from <code>+34.9 dB</code> at 1 km to <code>+54.7 dB</code> at 20 km.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-banner">
            <strong>📊 Benchmark Readings (f = 900 MHz):</strong><br>
            <table style="width:100%; margin-top:8px; color:#cbd5e1; font-size:13px;">
                <tr style="color:#64748b;"><td></td><td><strong>Free Space</strong></td><td><strong>Okumura</strong></td><td><strong>Hata Urban</strong></td></tr>
                <tr><td><strong>1 km</strong></td><td><code>91.52 dB</code></td><td><code>97.90 dB</code></td><td><code>126.40 dB</code></td></tr>
                <tr><td><strong>20 km</strong></td><td><code>117.55 dB</code></td><td><code>143.73 dB</code></td><td><code>172.23 dB</code></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)


# ── TAB 3: Statistical Analysis ──
with tab3:
    st.markdown("""
    <div class="section-header">
        <h3>📊 Descriptive Summary Statistics Across All Models</h3>
        <p class="hint">Min/Max/Mean/Std of path loss (PL) and received power (Pr) across the evaluated distance range — useful for identifying model spread and variability</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <strong>📖 How to Read This Table:</strong><br>
        • <strong>Min PL / Max PL (dB):</strong> Path loss at the closest and farthest distance. Lower PL = stronger signal.<br>
        • <strong>Mean PL (dB):</strong> Average path loss across all distances — a single-number summary of model severity.<br>
        • <strong>Std PL (dB):</strong> Standard deviation — how much the path loss varies across the distance range. Higher std = steeper decay slope.<br>
        • <strong>Pr (dBm):</strong> Received power at the mobile phone, computed from the link budget (EIRP − Path Loss − System Losses + Rx Gain).
    </div>
    """, unsafe_allow_html=True)

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
    st.dataframe(df_stats, width="stretch")

    # Downloadable CSV
    st.markdown("---")
    st.markdown("**📥 Export Raw Simulation Data** *(Download the full distance-by-distance numerical data for all models as a CSV spreadsheet)*")
    df_export = pd.DataFrame({"distance_km": distances_km})
    for key in selected_models:
        df_export[f"PL_{key}_dB"] = pl_dict[key]
        df_export[f"Pr_{key}_dBm"] = pr_dict[key]
    csv_bytes = df_export.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Simulation Data as CSV File",
        data=csv_bytes, file_name="simulation_results.csv", mime="text/csv",
        help="Downloads a CSV file containing path loss (dB) and received power (dBm) for every model at every distance point. Open in Excel or Google Sheets for further analysis."
    )


# ── TAB 4: Model Comparison Matrix ──
with tab4:
    st.markdown("""
    <div class="section-header">
        <h3>📋 Formal Comparative Analysis Matrix</h3>
        <p class="hint">Side-by-side academic comparison of all 7 propagation models — including their mathematical basis, valid operating ranges, key assumptions, and recommended deployment scenarios</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <strong>📖 What This Matrix Shows:</strong><br>
        Each row is a different propagation model. Columns include the model's mathematical type (theoretical vs empirical vs stochastic),
        valid frequency and distance ranges, path loss exponent, complexity, and typical use cases.
        Use this table to quickly determine <strong>which model is appropriate for a given scenario</strong>.
    </div>
    """, unsafe_allow_html=True)

    matrix_df = ModelComparator.get_comparison_table()
    st.dataframe(matrix_df, width="stretch")


# ── TAB 5: Shadowing & Outage Analysis ──
with tab5:
    st.markdown("""
    <div class="section-header">
        <h3>🎲 Log-Normal Shadow Fading & Outage Probability</h3>
        <p class="hint">Analyzes stochastic signal variation due to random obstacles (buildings, trees) — shows the probability of losing cellular service at each distance</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <strong>📖 What is Shadow Fading?</strong><br>
        Even at the same distance, signal strength varies randomly due to unpredictable obstacles (a tall building, a hill, a truck passing by).
        This random variation follows a <strong>log-normal (Gaussian in dB)</strong> distribution characterized by its standard deviation <code>σ</code>.
        Larger <code>σ</code> means more unpredictable signal → higher outage probability at the cell edge.
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    shadow_std = col_s1.slider(
        "Shadow Fading Standard Deviation σ (dB)  [Typical: 6–8 dB for urban, 4–6 dB for suburban]",
        min_value=1.0, max_value=14.0, value=6.0, step=0.5,
        help="Standard deviation of log-normal shadow fading in dB. Represents the spatial randomness of signal strength at a fixed distance. Higher σ → wider signal fluctuation → more dead zones."
    )

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
        fig_out, ax_out = plt.subplots(figsize=(7, 4.5))
        ax_out.plot(distances_km, p_outage * 100.0, color="#ef4444", lw=2.5,
                     label=f"Outage Probability (σ = {shadow_std} dB)")
        ax_out.axhline(5.0, color="#22c55e", linestyle="--", lw=1.5,
                        label="Target: <= 5% Outage (95% Reliability)")
        ax_out.fill_between(distances_km, 0, p_outage * 100.0,
                             where=(p_outage * 100.0 <= 5.0), alpha=0.15, color="#22c55e")
        ax_out.fill_between(distances_km, 0, p_outage * 100.0,
                             where=(p_outage * 100.0 > 5.0), alpha=0.15, color="#ef4444")
        ax_out.set_xscale("log")
        style_dark_axes(fig_out, ax_out,
                        title="Link Outage Probability vs Distance",
                        xlabel="Distance from Tower", ylabel="Outage Probability",
                        xlabel_hint="km — logarithmic",
                        ylabel_hint="% — chance of losing service")
        ax_out.legend(fontsize=9, loc="upper left", frameon=True,
                      facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        st.pyplot(fig_out)

    with col_s2:
        st.markdown(f"""
        <div class="info-banner">
            <strong>🔬 Shadow Fading Engineering Insights:</strong><br><br>
            <strong>• Standard Deviation:</strong> σ = <code>{shadow_std:.1f} dB</code> — captures the random spatial variation in received signal power due to local obstacles and terrain irregularities.<br><br>
            <strong>• 95% Reliability Fade Margin:</strong> To guarantee service 95% of the time, the link budget must include an extra margin of <code>1.96 × σ = {1.96 * shadow_std:.1f} dB</code> above the minimum receiver sensitivity.<br><br>
            <strong>• How to Read the Graph:</strong><br>
            — <span style="color:#22c55e;"><strong>🟢 Green zone</strong></span> = Coverage is reliable (outage < 5%)<br>
            — <span style="color:#ef4444;"><strong>🔴 Red zone</strong></span> = Coverage is unreliable (outage > 5%)<br>
            — The <strong>green dashed line</strong> at 5% marks the industry-standard reliability target<br>
            — The point where the red curve crosses 5% defines the <strong>maximum reliable cell radius</strong><br><br>
            <strong>• Engineering Decision:</strong> If the curve crosses 5% too early, the RF engineer must either increase transmit power, use a higher tower, or deploy additional base stations.
        </div>
        """, unsafe_allow_html=True)


# ── TAB 6: Link Budget Calculator ──
with tab6:
    st.markdown("""
    <div class="section-header">
        <h3>⚡ Interactive RF Link Budget Calculator</h3>
        <p class="hint">Evaluate the complete signal power chain at a specific target distance — from transmitter output through antenna gain, path loss, and system losses to the power arriving at the mobile phone</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <strong>📖 What is a Link Budget?</strong><br>
        A link budget is the accounting of all signal gains and losses from the transmitter to the receiver:
        <code>Pᵣ = Pₜ + Gₜ + Gᵣ − PL − Lsys</code><br>
        The <strong>Fade Margin</strong> is how much extra signal power exists above the minimum required. Positive = service works. Zero or negative = dropped call / dead zone.
    </div>
    """, unsafe_allow_html=True)

    eval_dist_km = st.slider(
        "🎯 Select Target Distance (km)  [Drag to evaluate link budget at any point]",
        min_value=float(min_d_km), max_value=float(max_d_km),
        value=float(min(3.0, max_d_km)), step=0.1,
        help="Move this slider to evaluate the complete link budget at any distance from the base station."
    )

    eval_idx = np.argmin(np.abs(distances_km - eval_dist_km))

    # KPI Row
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    kpi_col1.metric(
        "EIRP  (Effective Isotropic Radiated Power)",
        f"{budget.eirp_dbm:.1f} dBm",
        help="EIRP = Transmit Power + Antenna Gain. This is the total power 'seen' by the signal leaving the tower. Higher EIRP = longer coverage range."
    )
    fspl_loss = pl_dict.get("fspl", np.zeros(len(distances_km)))[eval_idx]
    kpi_col2.metric(
        f"Free Space Path Loss @ {distances_km[eval_idx]:.2f} km",
        f"{fspl_loss:.1f} dB",
        help="The absolute minimum path loss at this distance, assuming a perfect vacuum with no obstacles. Real-world loss is always higher than this."
    )
    hata_loss = pl_dict.get("cost231", pl_dict.get("hata", np.zeros(len(distances_km))))[eval_idx]
    kpi_col3.metric(
        f"Cellular Path Loss (Hata/COST-231) @ {distances_km[eval_idx]:.2f} km",
        f"{hata_loss:.1f} dB",
        help="Realistic empirical path loss including urban clutter, building diffraction, and ground reflection effects."
    )
    fade_margin = budget.calculate_fade_margin(hata_loss)
    kpi_col4.metric(
        "Fade Margin  (Safety Buffer)",
        f"{fade_margin:.1f} dB",
        delta=f"{'✅ Link OK' if fade_margin > 0 else '❌ Outage Risk!'}",
        delta_color="normal" if fade_margin > 0 else "inverse",
        help="Fade Margin = EIRP − Path Loss − System Losses + Rx Gain − Rx Sensitivity. Positive = service works. Negative = dead zone. Engineers typically require ≥ 10 dB margin for 95% reliability."
    )

    # Visual link budget breakdown
    st.markdown("---")
    st.markdown(f"""
    <div class="info-banner">
        <strong>🔗 Link Budget Breakdown @ d = {distances_km[eval_idx]:.2f} km:</strong><br><br>
        <code>Pₜ</code> (Transmit Power) = <strong>{tx_power_dbm:.1f} dBm</strong><br>
        <code>+ Gₜ</code> (Tower Antenna Gain) = <strong>+{tx_gain_dbi:.1f} dBi</strong><br>
        <code>= EIRP</code> = <strong>{budget.eirp_dbm:.1f} dBm</strong><br>
        <code>− PL</code> (Cellular Path Loss) = <strong>−{hata_loss:.1f} dB</strong><br>
        <code>− Lsys</code> (System Losses) = <strong>−{system_loss_db:.1f} dB</strong><br>
        <code>+ Gᵣ</code> (Mobile Antenna Gain) = <strong>+{rx_gain_dbi:.1f} dBi</strong><br>
        ─────────────────────────<br>
        <code>= Pᵣ</code> (Received Power) = <strong>{budget.eirp_dbm - hata_loss - system_loss_db + rx_gain_dbi:.1f} dBm</strong><br>
        <code>− Sensitivity</code> = <strong>{rx_sens_dbm:.1f} dBm</strong><br>
        ─────────────────────────<br>
        <code>= Fade Margin</code> = <strong style="color:{'#22c55e' if fade_margin > 0 else '#ef4444'};">{fade_margin:.1f} dB {'✅ SERVICE OK' if fade_margin > 0 else '❌ DEAD ZONE'}</strong>
    </div>
    """, unsafe_allow_html=True)
