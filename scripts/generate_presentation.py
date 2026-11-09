"""
Academic Presentation Generator (PowerPoint .pptx).

Generates a comprehensive 16-slide academic presentation with embedded
simulation figures for project defense and presentation.

Team Members:
- Harsh Yadav (RA2311003011546)
- Utkarsh Dabas (RA2311003011550)
- Tamanna Singh (RA2311003011570)
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

# Theme Colors
COLOR_PRIMARY = RGBColor(26, 54, 93)      # Deep Navy Blue
COLOR_ACCENT = RGBColor(43, 108, 176)     # Slate Blue
COLOR_TEXT_DARK = RGBColor(45, 55, 72)    # Dark Charcoal
COLOR_TEXT_LIGHT = RGBColor(113, 128, 150) # Light Slate
COLOR_BG_LIGHT = RGBColor(247, 250, 252)  # Soft Off-White


def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG_LIGHT


def add_header(slide, title_text, category_text="ACADEMIC RESEARCH PRESENTATION"):
    # Category / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8.4), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_ACCENT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(8.4), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(19)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY


def add_bullet_list(slide, left, top, width, height, items, font_size=12.5):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"•  {item}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(7)


def create_deck(output_path: Path):
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625) # 16:9 widescreen format
    blank_layout = prs.slide_layouts[6]
    fig_dir = ROOT_DIR / "outputs" / "figures"

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Featuring the 3 Team Members)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(8.4), Inches(2.3))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p_super = tf1.paragraphs[0]
    p_super.text = "CAPSTONE PROJECT DEFENSE & EVALUATION"
    p_super.font.size = Pt(11)
    p_super.font.bold = True
    p_super.font.color.rgb = COLOR_ACCENT
    p_super.space_after = Pt(8)

    p_main = tf1.add_paragraph()
    p_main.text = "Comparative Analysis of Wireless Signal Propagation Models"
    p_main.font.size = Pt(24)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_PRIMARY
    p_main.space_after = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Theoretical Derivations, Empirical Validations, and Numerical Simulations across Multi-Band Channels"
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = COLOR_TEXT_LIGHT

    # Team Members Block
    team_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(8.4), Inches(1.8))
    tf_team = team_box.text_frame
    tf_team.word_wrap = True

    p_tlabel = tf_team.paragraphs[0]
    p_tlabel.text = "PROJECT TEAM MEMBERS:"
    p_tlabel.font.size = Pt(11)
    p_tlabel.font.bold = True
    p_tlabel.font.color.rgb = COLOR_PRIMARY
    p_tlabel.space_after = Pt(4)

    p_m1 = tf_team.add_paragraph()
    p_m1.text = "1. Harsh Yadav — Reg No: RA2311003011546"
    p_m1.font.size = Pt(11)
    p_m1.font.color.rgb = COLOR_TEXT_DARK

    p_m2 = tf_team.add_paragraph()
    p_m2.text = "2. Utkarsh Dabas — Reg No: RA2311003011550"
    p_m2.font.size = Pt(11)
    p_m2.font.color.rgb = COLOR_TEXT_DARK

    p_m3 = tf_team.add_paragraph()
    p_m3.text = "3. Tamanna Singh — Reg No: RA2311003011570"
    p_m3.font.size = Pt(11)
    p_m3.font.color.rgb = COLOR_TEXT_DARK

    p_dept = tf_team.add_paragraph()
    p_dept.text = "Department of Electronics & Communication Engineering | Academic Year 2025–2026"
    p_dept.font.size = Pt(9.5)
    p_dept.font.color.rgb = COLOR_TEXT_LIGHT
    p_dept.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 2: Introduction
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Introduction to Wireless Signal Propagation")
    add_bullet_list(s2, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "Radio Frequency (RF) signals undergo severe physical degradation between transmitter and receiver.",
        "Primary propagation mechanisms include Free Space Loss, Specular Reflection, Diffraction over building edges, and Clutter Absorption.",
        "Radio channel models provide the mathematical foundation for cell sizing, link budgets, and interference mitigation.",
        "Engineers classify models into three families: Theoretical (Maxwell/optics), Empirical (measurement fits), and Stochastic (fading).",
        "Selecting an inappropriate model leads to severe network coverage blackspots or excessive interference."
    ])

    # -------------------------------------------------------------
    # SLIDE 3: Problem Statement
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Problem Statement & Research Motivation")
    add_bullet_list(s3, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "Theoretical models (Friis FSPL) ignore multipath and terrain clutter, severely underpredicting path loss.",
        "Classical empirical models (Okumura, Hata) are strictly calibrated up to 1.5 - 2.0 GHz and distances >= 1 km.",
        "Modern cellular systems operate across sub-6 GHz (3.5 GHz) and microcells (< 1 km), where classical models produce out-of-domain extrapolation errors.",
        "Network planners lack a unified, reproducible framework that compares all standard models under identical link budget parameters.",
        "Objective: Build an open-source, mathematically verified framework to quantify model discrepancies and boundaries."
    ])

    # -------------------------------------------------------------
    # SLIDE 4: Objectives
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Project Scope and Core Objectives")
    add_bullet_list(s4, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "1. Implement 7 distinct propagation models adhering to a unified, vectorized Python interface.",
        "2. Implement standard RF link budget calculations (EIRP, Received Power, Fade Margin).",
        "3. Evaluate model behavior across 5 controlled scenarios (Urban, Suburban, Rural, Indoor, 5G Mid-band).",
        "4. Quantify model divergence, percentage differences, and parameter sensitivity (antenna heights, frequencies).",
        "5. Characterize shadow fading through Monte Carlo realizations and closed-form outage probabilities.",
        "6. Ensure 100% reproducibility via automated pytest suites and YAML-based experiment pipelines."
    ])

    # -------------------------------------------------------------
    # SLIDE 5: Propagation Principles & Units
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Fundamental Electromagnetic Concepts & Unit Safety")
    add_bullet_list(s5, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "Wavelength & Frequency: lambda = c / f, where c = 299,792,458 m/s.",
        "Effective Antenna Aperture: Ae = lambda^2 / (4 * pi). Higher frequency reduces effective aperture.",
        "Path Loss Exponent (n): Governs the rate of power decay (n=2 in vacuum, n=3-4 in urban canyons, n=4 in ground multipath).",
        "Decibel Notation: Power in dBm = 10 * log10(Power in mW). Decibels allow linear addition across the RF link.",
        "Link Equation: Pr (dBm) = Pt (dBm) + Gt (dBi) + Gr (dBi) - PL (dB) - L_sys (dB)."
    ])

    # -------------------------------------------------------------
    # SLIDE 6: Propagation Models Overview
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Overview of the Seven Implemented Models")
    add_bullet_list(s6, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "1. Free Space Path Loss (Friis): Ideal unobstructed line-of-sight vacuum baseline.",
        "2. Two-Ray Ground Reflection: Direct LOS + earth reflection, exhibiting d^-4 decay beyond dc.",
        "3. Log-Distance Model: Generalized parametric model with environment-dependent exponent n.",
        "4. Okumura Model: Classical graphical Tokyo macrocell model (150 - 1920 MHz).",
        "5. Okumura-Hata Model: Analytical closed-form equations for urban, suburban, and rural cells.",
        "6. COST-231 Hata Model: European PCS extension covering 1500 - 2000 MHz with city factor CM.",
        "7. Log-Normal Shadowing: Stochastic model combining distance decay with Gaussian clutter noise."
    ])

    # -------------------------------------------------------------
    # SLIDE 7: Mathematical Formulations
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Mathematical Equations and Conventions")
    add_bullet_list(s7, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "FSPL (dB) = 20*log10(d) + 20*log10(f) + 20*log10(4*pi / c)",
        "Two-Ray Asymptotic: PL (dB) = 40*log10(d) - 20*log10(ht) - 20*log10(hr)",
        "Two-Ray Crossover: dc = (4 * pi * ht * hr) / lambda",
        "Log-Distance: PL(d) = PL(d0) + 10*n*log10(d / d0)",
        "Hata Urban: PL = 69.55 + 26.16*log10(f) - 13.82*log10(hb) - a(hm) + [44.9 - 6.55*log10(hb)]*log10(d)",
        "COST-231 Hata: PL = 46.3 + 33.9*log10(f) - 13.82*log10(hb) - a(hm) + [44.9 - 6.55*log10(hb)]*log10(d) + CM",
        "Shadowing Outage: P_outage = 0.5 * erfc( (Pr_mean - Sensitivity) / (sqrt(2) * sigma) )"
    ], font_size=11)

    # -------------------------------------------------------------
    # SLIDE 8: Software Architecture & Methodology
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Software Architecture and Methodology")
    add_bullet_list(s8, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "Modular OOP Design: 'PropagationModel' base class guarantees strict interface polymorphism.",
        "NumPy Vectorization: Eliminates python loops, enabling real-time array evaluations over thousands of points.",
        "Active Boundary Validation: Emits 'ModelRangeWarning' when parameters exceed calibration bounds.",
        "Reproducible Experiments: Predefined YAML scenarios dictate exact transmitter, antenna, and channel inputs.",
        "Automated Testing Suite: 32 pytest unit and integration tests guarantee numerical and physical correctness."
    ])

    # -------------------------------------------------------------
    # SLIDE 9: Simulation Scenarios
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Controlled Experimental Scenarios")
    add_bullet_list(s9, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "Scenario A (Rural): f = 900 MHz, d = 0.1-20 km, ht = 45 m, hr = 1.5 m, Pt = 46 dBm (High-power macrocell).",
        "Scenario B (Urban): f = 1800 MHz, d = 0.1-10 km, ht = 30 m, hr = 1.5 m, Pt = 43 dBm (PCS cellular macrocell).",
        "Scenario C (Suburban): f = 1800 MHz, d = 0.1-15 km, ht = 35 m, hr = 1.5 m, Pt = 43 dBm (Residential area).",
        "Scenario D (Indoor): f = 2.4 GHz, d = 1-100 m, ht = 2.5 m, hr = 1.0 m, Pt = 20 dBm (WLAN / Small cell).",
        "Scenario E (5G Mid-Band): f = 3.5 GHz, d = 0.05-5 km, ht = 15 m, hr = 1.5 m, Pt = 38 dBm (C-Band microcell)."
    ])

    # -------------------------------------------------------------
    # SLIDE 10: Path Loss Comparison (With Fig 1)
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Numerical Finding 1: Path Loss vs Distance")
    add_bullet_list(s10, Inches(0.8), Inches(1.4), Inches(3.8), Inches(3.8), [
        "Friis Free Space predicts the lowest path loss (77.6 to 117.6 dB).",
        "Urban empirical models (COST-231, Okumura) predict 101 to 172 dB.",
        "Clutter penalty exceeds 50 dB at a 10 km cell edge.",
        "Two-Ray model shows multipath ripples before d_c, then rolls off at 40 dB/dec."
    ], font_size=11)
    if (fig_dir / "fig01_path_loss_vs_distance.png").exists():
        s10.shapes.add_picture(str(fig_dir / "fig01_path_loss_vs_distance.png"), Inches(4.7), Inches(1.3), width=Inches(4.8))

    # -------------------------------------------------------------
    # SLIDE 11: Received Power Comparison (With Fig 2)
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Numerical Finding 2: Received Power vs Distance")
    add_bullet_list(s11, Inches(0.8), Inches(1.4), Inches(3.8), Inches(3.8), [
        "EIRP = 58 dBm (Pt = 43 dBm, Gt = 15 dBi).",
        "Receiver sensitivity threshold marked at -100 dBm.",
        "Under Free Space, cell radius extends well beyond 10 km.",
        "Under COST-231 Hata, signal drops below threshold at ~4.2 km (cell edge limit)."
    ], font_size=11)
    if (fig_dir / "fig02_received_power_vs_distance.png").exists():
        s11.shapes.add_picture(str(fig_dir / "fig02_received_power_vs_distance.png"), Inches(4.7), Inches(1.3), width=Inches(4.8))

    # -------------------------------------------------------------
    # SLIDE 12: Frequency Sensitivity (With Fig 3)
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Numerical Finding 3: Frequency Sensitivity")
    add_bullet_list(s12, Inches(0.8), Inches(1.4), Inches(3.8), Inches(3.8), [
        "Carrier frequency swept from 150 MHz to 3.5 GHz at fixed d = 2.0 km.",
        "Path loss increases with frequency: 20*log10(f) in FSPL and 33.9*log10(f) in COST-231.",
        "Scaling from 900 MHz to 3.5 GHz adds ~14 dB attenuation.",
        "Highlights the severe coverage penalty of high-frequency 5G bands."
    ], font_size=11)
    if (fig_dir / "fig03_path_loss_vs_frequency.png").exists():
        s12.shapes.add_picture(str(fig_dir / "fig03_path_loss_vs_frequency.png"), Inches(4.7), Inches(1.3), width=Inches(4.8))

    # -------------------------------------------------------------
    # SLIDE 13: Environmental Clutter Effects (With Fig 4)
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Numerical Finding 4: Environmental Clutter Effects")
    add_bullet_list(s13, Inches(0.8), Inches(1.4), Inches(3.8), Inches(3.8), [
        "Hata formulation evaluated at 900 MHz across environments.",
        "Urban Large City: 146.2 dB at 10 km.",
        "Urban Medium City: 143.1 dB at 10 km.",
        "Suburban: 133.2 dB (~10 dB lower loss than Urban Medium).",
        "Rural Open: 115.1 dB (~28 dB lower loss than Urban Medium)."
    ], font_size=11)
    if (fig_dir / "fig04_environmental_comparison.png").exists():
        s13.shapes.add_picture(str(fig_dir / "fig04_environmental_comparison.png"), Inches(4.7), Inches(1.3), width=Inches(4.8))

    # -------------------------------------------------------------
    # SLIDE 14: Shadow Fading Analysis (With Fig 6)
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Numerical Finding 5: Log-Normal Shadowing & Outage")
    add_bullet_list(s14, Inches(0.8), Inches(1.4), Inches(3.8), Inches(3.8), [
        "Simulates location-to-location clutter variation (sigma = 6 dB).",
        "Deterministic median path loss bounded by 95% confidence intervals (+/- 1.96 sigma).",
        "Monte Carlo analysis (1,500 runs) verifies a Gaussian PDF in decibels.",
        "Requires 12–16 dB fade margin to prevent cell-edge outages."
    ], font_size=11)
    if (fig_dir / "fig06_shadowing_distribution.png").exists():
        s14.shapes.add_picture(str(fig_dir / "fig06_shadowing_distribution.png"), Inches(4.7), Inches(1.3), width=Inches(4.8))

    # -------------------------------------------------------------
    # SLIDE 15: Formal Model Comparison Table
    # -------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Formal Comparative Analysis Matrix")

    rows, cols = 8, 4
    table_shape = s15.shapes.add_table(rows, cols, Inches(0.8), Inches(1.3), Inches(8.4), Inches(3.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.9)

    headers = ["Model", "Classification", "Calibrated Range", "Primary Engineering Takeaway"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("Free Space", "Theoretical", "Broadband (d > 0)", "Underestimates loss by 40-55 dB in cities"),
        ("Two-Ray", "Theoretical", "1 MHz - 60 GHz", "Exhibits d^-4 decay beyond crossover distance dc"),
        ("Log-Distance", "Empirical", "Calibrated range", "Highly versatile through configurable exponent n"),
        ("Okumura", "Empirical", "150 - 1920 MHz, 1-100 km", "Classical graphical standard; uncalibrated < 1 km"),
        ("Okumura-Hata", "Empirical", "150 - 1500 MHz, 1-20 km", "Closed-form standard for 2G/3G macrocells"),
        ("COST-231 Hata", "Empirical", "1500 - 2000 MHz, 1-20 km", "Standard for 1.8-2.0 GHz; invalid for 5G > 2 GHz"),
        ("Shadow Fading", "Stochastic", "All frequencies", "Requires 12-16 dB fade margin for 95% coverage"),
    ]

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(8.5)
                p.font.color.rgb = COLOR_TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 16: Conclusions and Future Work
    # -------------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "Key Findings, Conclusions & Next Steps")
    add_bullet_list(s16, Inches(0.8), Inches(1.4), Inches(8.4), Inches(3.8), [
        "Discrepancy Magnitude: Models diverge by up to 55 dB under identical distance and frequency parameters.",
        "Model Suitability: Theoretical models provide vital physical bounds; empirical and stochastic models are essential for cellular planning.",
        "Extrapolation Danger: Empirical models (Hata, COST-231) cannot be naively applied to 5G C-Band (3.5 GHz) or mmWave.",
        "Complete Implementation: Fully tested Python library, CLI, 10 publication figures, Jupyter notebooks, hardcopy PDF report, and Streamlit dashboard.",
        "Future Enhancements: Integration of 3GPP TR 38.901 3D channel models, OpenStreetMap GIS ray tracing, and ML-based channel prediction."
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    print(f"[+] Academic PowerPoint Presentation generated successfully at: {output_path}")


def main():
    print("=" * 70)
    print("  GENERATING 16-SLIDE ACADEMIC POWERPOINT PRESENTATION (.PPTX)")
    print("=" * 70)
    out_dir = ROOT_DIR / "outputs" / "presentation"
    out_dir.mkdir(parents=True, exist_ok=True)
    pptx_path = out_dir / "Wireless_Propagation_Analysis.pptx"
    create_deck(pptx_path)


if __name__ == "__main__":
    main()
