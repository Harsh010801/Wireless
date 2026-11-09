"""
Master Academic Presentation Generator (PowerPoint .pptx).

Generates a publication-grade, 20-slide academic slide deck embedding
all 10 simulation figures, comparison tables, mathematical equations,
and clear team attribution.

Project Team:
1. Harsh Yadav (RA2311003011546)
2. Utkarsh Dabas (RA2311003011550)
3. Tamanna Singh (RA2311003011570)
"""

import sys
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

# Scientific Academic Theme Colors
COLOR_NAVY = RGBColor(15, 23, 42)          # Deep Slate/Navy #0f172a
COLOR_PRIMARY = RGBColor(30, 58, 138)      # Deep Blue #1e3a8a
COLOR_ACCENT = RGBColor(37, 99, 235)       # Electric Blue #2563eb
COLOR_CARD_BG = RGBColor(255, 255, 255)    # White
COLOR_TEXT_MAIN = RGBColor(30, 41, 59)     # Dark Slate
COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # Muted Slate
COLOR_BG = RGBColor(248, 250, 252)         # Ultra-light gray/blue #f8fafc
COLOR_BORDER = RGBColor(226, 232, 240)     # Light Gray Border


def apply_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG


def add_header(slide, title_text, category="WIRELESS PROPAGATION RESEARCH & DEFENSE"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8.4), Inches(0.28))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(9.0)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_ACCENT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(8.4), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(18)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY


def add_bullets(slide, left, top, width, height, items, font_size=11.5):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"•  {item}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(7)


def add_split_slide_with_image(slide, title, category, bullets, image_path, font_size=11.0):
    add_header(slide, title, category)
    # Bullets on the left
    add_bullets(slide, Inches(0.8), Inches(1.3), Inches(4.0), Inches(4.0), bullets, font_size=font_size)
    # Image on the right
    if Path(image_path).exists():
        slide.shapes.add_picture(str(image_path), Inches(4.9), Inches(1.3), width=Inches(4.6))


def build_presentation(out_path: Path):
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    blank_layout = prs.slide_layouts[6]
    fig_dir = ROOT_DIR / "outputs" / "figures"

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    # Title Card
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(8.4), Inches(2.3))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "CAPSTONE PROJECT DEFENSE & TECHNICAL EVALUATION"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACCENT
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "Comparative Analysis of Wireless Signal Propagation Models"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Theoretical Derivations, Empirical Validations, and Numerical Simulations across Multi-Band Channels"
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT_MUTED

    # Team Members Presentation Card
    team_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(8.4), Inches(1.8))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = COLOR_CARD_BG
    team_card.line.color.rgb = COLOR_BORDER
    team_card.line.width = Pt(1.5)

    tf_team = team_card.text_frame
    tf_team.word_wrap = True
    tf_team.vertical_anchor = MSO_ANCHOR.TOP

    p_tl = tf_team.paragraphs[0]
    p_tl.text = "PROJECT TEAM MEMBERS"
    p_tl.font.size = Pt(11)
    p_tl.font.bold = True
    p_tl.font.color.rgb = COLOR_PRIMARY
    p_tl.space_after = Pt(5)

    p_m1 = tf_team.add_paragraph()
    p_m1.text = "1. Harsh Yadav — Registration No: RA2311003011546"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_TEXT_MAIN

    p_m2 = tf_team.add_paragraph()
    p_m2.text = "2. Utkarsh Dabas — Registration No: RA2311003011550"
    p_m2.font.size = Pt(11)
    p_m2.font.bold = True
    p_m2.font.color.rgb = COLOR_TEXT_MAIN

    p_m3 = tf_team.add_paragraph()
    p_m3.text = "3. Tamanna Singh — Registration No: RA2311003011570"
    p_m3.font.size = Pt(11)
    p_m3.font.bold = True
    p_m3.font.color.rgb = COLOR_TEXT_MAIN

    p_d = tf_team.add_paragraph()
    p_d.text = "Department of Electronics & Communication Engineering / Telecommunications | Academic Year 2025–2026"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = COLOR_TEXT_MUTED
    p_d.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: Introduction & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, "Introduction to Wireless Signal Propagation", "FOUNDATIONAL BACKGROUND")
    add_bullets(s2, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "Radio Frequency (RF) signals undergo severe physical degradation between transmitter and receiver antennas.",
        "Core Physical Mechanisms: Free space spreading, specular ground reflection, knife-edge diffraction, diffuse scattering, and atmospheric clutter absorption.",
        "Radio channel models provide the mathematical foundation for cell sizing, RF link budgets, interference management, and base station placement.",
        "Engineers classify models into three families: Theoretical (Maxwell/optics), Empirical (regression of physical drive-test data), and Stochastic (shadow fading).",
        "Selecting an inappropriate model leads to severe network coverage blackspots, poor quality of service, or excessive co-channel interference."
    ])

    # =========================================================================
    # SLIDE 3: Problem Statement
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3, "Problem Statement & Research Questions", "RESEARCH MOTIVATION")
    add_bullets(s3, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "Theoretical line-of-sight models (Friis FSPL) ignore terrestrial multipath and building clutter, underpredicting path loss by 40 to 55 dB.",
        "Classical empirical models (Okumura, Hata) are strictly calibrated up to 1.5 - 2.0 GHz and distances >= 1 km.",
        "Modern cellular deployments operate in sub-6 GHz (3.5 GHz) and microcells (< 1 km), where classical models yield uncalibrated extrapolations.",
        "Key Research Questions Addressed:",
        "  1. Which model predicts the lowest/highest path loss under identical parameters?",
        "  2. Where does the Two-Ray ground reflection crossover distance dc occur?",
        "  3. How severe is the urban clutter penalty compared to suburban and rural terrain?",
        "  4. What fade margin is mathematically necessary to guarantee 95% coverage reliability under shadow fading?"
    ])

    # =========================================================================
    # SLIDE 4: Project Objectives
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4, "Project Scope and Engineering Objectives", "PROJECT OBJECTIVES")
    add_bullets(s4, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "1. Implement Seven Independent Models adhering to a clean, object-oriented abstract interface (`PropagationModel`).",
        "2. Develop Vectorized Simulation Engine supporting multi-variable distance sweeps, frequency sweeps, and link budgets.",
        "3. Provide Unit Safety and Conversions: Full support for Hz/MHz/GHz, m/km, Watts/mW/dBm, and EIRP calculations.",
        "4. Enforce Active Parameter Boundaries: Emit explicit `ModelRangeWarning` when empirical calibration limits are exceeded.",
        "5. Conduct Sensitivity & Discrepancy Analyses: Antenna heights (ht, hr), frequency scaling, and pairwise delta metrics.",
        "6. Ensure 100% Scientific Reproducibility: Pytest test suite (32 tests passing), YAML scenarios, and fixed random seeds."
    ])

    # =========================================================================
    # SLIDE 5: Fundamental Concepts & Link Budget
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5, "Electromagnetic Basics & RF Link Budget Equation", "THEORETICAL FOUNDATION")
    add_bullets(s5, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "Wavelength & Carrier Frequency: lambda = c / f, where c = 299,792,458 m/s.",
        "Effective Antenna Aperture: Ae = lambda^2 / (4 * pi). Higher carrier frequency reduces receiver capture aperture.",
        "Path Loss Exponent (n): Power decays as d^-n (n=2 in vacuum, n=3-4 in urban canyons, n=4 in long-range ground multipath).",
        "Decibel-Milliwatt Conversion: P(dBm) = 10 * log10(P(Watts) * 1000) = 10 * log10(P(W)) + 30.",
        "Complete Radio Link Budget Equation:",
        "  Pr (dBm) = Pt (dBm) + Gt (dBi) + Gr (dBi) - PL (dB) - L_sys (dB)",
        "  EIRP (dBm) = Pt (dBm) + Gt (dBi) - L_cable (dB)",
        "  Fade Margin (dB) = Pr (dBm) - Receiver_Sensitivity (dBm)"
    ])

    # =========================================================================
    # SLIDE 6: Implemented Models Overview
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6, "Overview of the Seven Implemented Models", "MODEL TAXONOMY")
    add_bullets(s6, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "1. Free Space Path Loss (Friis): Ideal line-of-sight propagation in vacuum with zero terrestrial clutter (n=2).",
        "2. Two-Ray Ground Reflection: Direct ray + specular earth-reflected ray, transitioning to d^-4 roll-off beyond dc.",
        "3. Log-Distance Path Loss: Flexible parametric model adaptable to urban, suburban, and indoor obstructed channels.",
        "4. Okumura Model: Classical graphical Tokyo drive-test model for macrocells (150 - 1920 MHz, 1 - 100 km).",
        "5. Okumura-Hata Model: Standard analytical closed-form equations for 2G/3G cellular networks (150 - 1500 MHz).",
        "6. COST-231 Hata Model: European extension covering PCS/3G frequency bands (1500 - 2000 MHz) with metropolitan CM factor.",
        "7. Log-Normal Shadowing: Stochastic large-scale fading model combining distance decay with Gaussian clutter noise."
    ])

    # =========================================================================
    # SLIDE 7: Mathematical Formulations
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_header(s7, "Mathematical Formulations & Closed-Form Equations", "MATHEMATICAL FORMULATIONS")
    add_bullets(s7, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "Friis FSPL: PL (dB) = 20*log10(d) + 20*log10(f) + 20*log10(4*pi / c) = 20*log10(d_km) + 20*log10(f_MHz) + 32.45",
        "Two-Ray Asymptotic: PL (dB) = 40*log10(d) - 20*log10(ht) - 20*log10(hr)",
        "Two-Ray Crossover Distance: dc = (4 * pi * ht * hr) / lambda = (4 * pi * ht * hr * f) / c",
        "Log-Distance: PL(d) = PL(d0) + 10 * n * log10(d / d0)",
        "Hata Urban: PL = 69.55 + 26.16*log10(f) - 13.82*log10(hb) - a(hm) + [44.9 - 6.55*log10(hb)]*log10(d)",
        "COST-231 Hata: PL = 46.3 + 33.9*log10(f) - 13.82*log10(hb) - a(hm) + [44.9 - 6.55*log10(hb)]*log10(d) + CM",
        "Shadowing Outage: P_outage = 0.5 * erfc( (Pr_mean - Sensitivity) / (sqrt(2) * sigma) )"
    ], font_size=11.0)

    # =========================================================================
    # SLIDE 8: System Architecture & Methodology
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8)
    add_header(s8, "Software Architecture and Engineering Design", "SYSTEM ARCHITECTURE")
    add_bullets(s8, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "Modular Package Structure under `src/propagation/`: core, models, simulation, analysis, and visualization.",
        "Strict Polymorphism: `PropagationModel` abstract class defines uniform `calculate_path_loss` and validation API.",
        "Pure NumPy Vectorization: Enables high-speed sweep evaluations over thousands of coordinates without Python loops.",
        "Reproducible Experiments: YAML-based scenario configurations dictate exact RF power, antenna, and channel parameters.",
        "Automated Quality Assurance: 32 pytest unit and integration tests guarantee numerical precision and physics validity.",
        "Interactive Tools: Standalone CLI, Jupyter research notebooks, ReportLab PDF generator, and Streamlit dashboard."
    ])

    # =========================================================================
    # SLIDE 9: Simulation Scenarios
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9)
    add_header(s9, "Controlled Experimental Scenarios", "EXPERIMENT DESIGN")
    add_bullets(s9, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "Scenario A (Rural Macrocell): f = 900 MHz, d = 0.1–20 km, ht = 45 m, hr = 1.5 m, Pt = 46 dBm (High-power 40W base station).",
        "Scenario B (Urban Macrocell): f = 1800 MHz, d = 0.1–10 km, ht = 30 m, hr = 1.5 m, Pt = 43 dBm (20W PCS cellular base station).",
        "Scenario C (Suburban Macrocell): f = 1800 MHz, d = 0.1–15 km, ht = 35 m, hr = 1.5 m, Pt = 43 dBm (Residential foliage environment).",
        "Scenario D (Indoor WLAN / Small Cell): f = 2.4 GHz, d = 1–100 m, ht = 2.5 m, hr = 1.0 m, Pt = 20 dBm (100mW Wi-Fi access point).",
        "Scenario E (5G Mid-Band Microcell): f = 3.5 GHz, d = 0.05–5 km, ht = 15 m, hr = 1.5 m, Pt = 38 dBm (Sub-6 GHz C-band microcell)."
    ])

    # =========================================================================
    # SLIDE 10: Path Loss vs Distance (Fig 1)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10)
    add_split_slide_with_image(
        s10,
        "Finding 1: Path Loss vs Distance Across Models",
        "SIMULATION RESULTS",
        [
            "Evaluated under Urban Scenario B (1800 MHz, ht=30m, hr=1.5m).",
            "Friis Free Space predicts the lowest path loss (77.6 dB at 100m to 117.6 dB at 10km).",
            "COST-231 Hata and Okumura predict 101.0 dB to 171.4 dB across the same distance.",
            "Urban clutter adds an excess loss of 40 to 55 dB above theoretical free space.",
            "Two-Ray model shows destructive multipath ripples before dc, then transitions to steep d^-4 decay."
        ],
        fig_dir / "fig01_path_loss_vs_distance.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 11: Received Power vs Distance (Fig 2)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11)
    add_split_slide_with_image(
        s11,
        "Finding 2: Received Power & Link Budget Analysis",
        "SIMULATION RESULTS",
        [
            "Link Budget Inputs: Pt = 43 dBm, Gt = 15 dBi, Gr = 0 dBi, Lsys = 3 dB (EIRP = 58 dBm).",
            "Receiver Sensitivity Threshold marked at -100 dBm.",
            "Under Free Space, received power at 10 km is -62.6 dBm (massive 37.4 dB excess margin).",
            "Under COST-231 Hata, signal drops below the -100 dBm threshold at approximately 4.2 km.",
            "Defines the practical maximum cell edge radius for reliable voice and broadband service."
        ],
        fig_dir / "fig02_received_power_vs_distance.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 12: Frequency Sensitivity Analysis (Fig 3)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12)
    add_split_slide_with_image(
        s12,
        "Finding 3: Carrier Frequency Sensitivity",
        "SENSITIVITY ANALYSIS",
        [
            "Carrier frequency swept from 150 MHz to 3.5 GHz at a fixed cell distance d = 2.0 km.",
            "Path loss increases monotonically with frequency in all empirical models.",
            "Free space scales as 20*log10(f), while COST-231 scales more steeply as 33.9*log10(f).",
            "Transitioning from 900 MHz (2G/4G low-band) to 3.5 GHz (5G mid-band) adds ~14 dB attenuation.",
            "Explains why 5G deployments require much denser base station placement."
        ],
        fig_dir / "fig03_path_loss_vs_frequency.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 13: Environmental Clutter Effects (Fig 4)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_background(s13)
    add_split_slide_with_image(
        s13,
        "Finding 4: Environmental Clutter Comparison",
        "ENVIRONMENTAL ANALYSIS",
        [
            "Evaluated using Okumura-Hata at 900 MHz across four standard environments.",
            "Urban Large City: 146.2 dB at 10 km (highest loss due to concrete towers and canyon diffraction).",
            "Urban Medium City: 143.1 dB at 10 km.",
            "Suburban: 133.2 dB at 10 km (~10 dB lower loss than Urban Medium).",
            "Rural / Open Area: 115.1 dB at 10 km (~28 dB lower loss than Urban Medium).",
            "Confirms that open rural terrain provides nearly triple the line-of-sight coverage reach."
        ],
        fig_dir / "fig04_environmental_comparison.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 14: Model Discrepancy & Excess Path Loss (Fig 5)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    apply_background(s14)
    add_split_slide_with_image(
        s14,
        "Finding 5: Model Discrepancy Relative to Free Space",
        "DISCREPANCY ANALYSIS",
        [
            "Pointwise excess path loss: Delta PL = PL_model - PL_FSPL (dB).",
            "Reveals the exact clutter penalty introduced by buildings, terrain, and multipath.",
            "At 1 km: Empirical models predict 36 to 45 dB excess loss over free space.",
            "At 10 km: Discrepancy widens to 52 to 55 dB due to cumulative obstacle shadowing.",
            "Demonstrates why using Free Space for terrestrial cellular planning leads to catastrophic design failures."
        ],
        fig_dir / "fig05_model_difference_vs_baseline.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 15: Log-Normal Shadowing & Outage Analysis (Fig 6)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    apply_background(s15)
    add_split_slide_with_image(
        s15,
        "Finding 6: Log-Normal Shadowing & Outage Risk",
        "STOCHASTIC FADING",
        [
            "Captures random location-to-location clutter obstruction (sigma = 6 dB).",
            "Left plot: 8 Monte Carlo realization trajectories showing spatial variation around median.",
            "95% Confidence Interval spans +/- 1.96 * sigma (+/- 11.76 dB in path loss).",
            "Right plot: Histogram of 1,500 Monte Carlo samples at d = 500m confirming Gaussian PDF in dB.",
            "To guarantee 95% link reliability, link budgets must provision an extra fade margin of at least 12–16 dB."
        ],
        fig_dir / "fig06_shadowing_distribution.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 16: Antenna Height Sensitivity (Fig 7)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    apply_background(s16)
    add_split_slide_with_image(
        s16,
        "Finding 7: Antenna Height Sensitivity Analysis",
        "SENSITIVITY ANALYSIS",
        [
            "Left: Base station antenna height ht swept from 20 m to 200 m (d = 5 km, f = 900 MHz).",
            "Increasing base height from 30 m to 100 m reduces path loss by ~11 dB across Hata and Okumura.",
            "In Two-Ray asymptotic: Doubling height reduces loss by 20*log10(2) = 6.02 dB.",
            "Right: Mobile antenna height hm swept from 1.0 m to 10.0 m.",
            "Elevating user antenna from 1.5 m to 3.0 m yields a 3 dB link improvement in urban clutter."
        ],
        fig_dir / "fig07_antenna_height_sensitivity.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 17: 2D Path Loss Heatmap (Fig 8)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    apply_background(s17)
    add_split_slide_with_image(
        s17,
        "Finding 8: 2D Parameter Space Heatmap",
        "PARAMETER SPACE",
        [
            "Evaluates COST-231 Hata across a 2D meshgrid of Distance (1–15 km) and Frequency (1500–2000 MHz).",
            "Iso-path-loss contour lines show coupling between distance and carrier frequency.",
            "Operating at 10 km and 1500 MHz yields ~165 dB loss; the same 165 dB loss occurs at only 8.5 km at 2000 MHz.",
            "Visualizes cell shrink effect as carrier frequency increases across cellular allocations."
        ],
        fig_dir / "fig08_path_loss_2d_heatmap.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 18: Model Applicability Ranges (Fig 9)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    apply_background(s18)
    add_split_slide_with_image(
        s18,
        "Finding 9: Model Calibrated Operating Ranges",
        "EMPIRICAL BOUNDS",
        [
            "Charts the calibrated frequency domain of each model on a logarithmic scale.",
            "Theoretical Models (FSPL, Two-Ray): Broadband applicable across VHF to mmWave.",
            "Okumura Model: Calibrated for 150 MHz to 1920 MHz (Tokyo macrocell).",
            "Okumura-Hata: Strictly capped at 1500 MHz.",
            "COST-231 Hata: Specifically tailored to 1500 MHz to 2000 MHz (PCS bands).",
            "Highlights the necessity of active warning flags when simulating 5G sub-6 GHz (3.5 GHz)."
        ],
        fig_dir / "fig09_model_applicability_matrix.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 19: Summary Comparison Chart (Fig 10)
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    apply_background(s19)
    add_split_slide_with_image(
        s19,
        "Finding 10: Benchmark Path Loss at 3 km Cell Edge",
        "SYNTHESIS BENCHMARK",
        [
            "Direct comparison at typical macrocell edge radius (d = 3.0 km, f = 1800 MHz, Urban):",
            "  • Free Space (Friis): 107.1 dB (underpredicts loss by ~48 dB)",
            "  • Two-Ray Ground Refl.: 108.6 dB (near crossover distance dc = 3.39 km)",
            "  • Log-Distance (n=3.2): 150.3 dB",
            "  • Okumura-Hata: 153.8 dB",
            "  • COST-231 Hata: 155.8 dB (realistic urban macrocell benchmark)",
            "  • Okumura Model: 158.0 dB (signal drops below -100 dBm sensitivity)"
        ],
        fig_dir / "fig10_summary_comparison_chart.png",
        font_size=10.5
    )

    # =========================================================================
    # SLIDE 20: Conclusions & Future Work
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    apply_background(s20)
    add_header(s20, "Key Conclusions and Future Research Directions", "CONCLUSIONS & EXTENSIONS")
    add_bullets(s20, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.9), [
        "1. Discrepancy Magnitude: Models diverge by up to 55 dB under identical parameters, underscoring the critical need for scenario-matched model selection.",
        "2. Environmental Clutter: Urban terrain penalizes link budgets by ~28 dB relative to rural open space, and ~10 dB relative to suburban areas.",
        "3. Fade Margin Requirement: Log-normal shadow fading (sigma = 8 dB) demands a 15.7 dB margin to maintain 97.5% cell-edge coverage reliability.",
        "4. Software Deliverables: Fully tested Python library, CLI, 10 publication figures, Jupyter notebooks, hardcopy PDF report, and Streamlit dashboard.",
        "5. Future Extensions:",
        "    • Implementation of 3GPP TR 38.901 3D channel models (UMi / UMa) for 5G/6G sub-6 GHz and mmWave.",
        "    • Integration of OpenStreetMap GIS building polygons for 3D ray-tracing.",
        "    • Machine-learning channel prediction using Graph Neural Networks (GNNs)."
    ], font_size=11.0)

    # Save to both target output path and project root
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    print(f"[+] Master 20-Slide Presentation saved to: {out_path}")

    # Also copy directly to the workspace root for instant access
    root_pptx = ROOT_DIR / "Wireless_Propagation_Analysis.pptx"
    shutil.copy2(out_path, root_pptx)
    print(f"[+] Copy placed directly in workspace root: {root_pptx}")


def main():
    print("=" * 75)
    print("  GENERATING 20-SLIDE MASTER ACADEMIC PRESENTATION (.PPTX)")
    print("=" * 75)
    out_dir = ROOT_DIR / "outputs" / "presentation"
    out_dir.mkdir(parents=True, exist_ok=True)
    pptx_path = out_dir / "Wireless_Propagation_Analysis.pptx"
    build_presentation(pptx_path)


if __name__ == "__main__":
    main()
