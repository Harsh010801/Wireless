"""
Generate a 15-slide PowerPoint presentation matching PPT_Outline.md.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette
BG_DARK = RGBColor(15, 23, 42)      # Deep slate
CARD_BG = RGBColor(30, 41, 59)      # Slate card
ACCENT_BLUE = RGBColor(56, 189, 248) # Cyan accent
ACCENT_GOLD = RGBColor(251, 191, 36) # Gold accent
TEXT_LIGHT = RGBColor(241, 245, 249) # Off-white text
TEXT_MUTED = RGBColor(148, 163, 184) # Muted text

def apply_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_header(slide, title_text, category="21CSE458T — WIRELESS & MOBILE COMMUNICATION"):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_GOLD
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_LIGHT

# Slide 1: Title Slide
slide_layout = prs.slide_layouts[6] # blank
s1 = prs.slides.add_slide(slide_layout)
apply_background(s1)

tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "COURSE: 21CSE458T — WIRELESS AND MOBILE COMMUNICATION"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_GOLD

p2 = tf1.add_paragraph()
p2.text = "Comparative Analysis of Wireless Signal Propagation Models\n(Free Space, Okumura and Hata)"
p2.font.size = Pt(32)
p2.font.bold = True
p2.font.color.rgb = TEXT_LIGHT
p2.space_before = Pt(14)

p3 = tf1.add_paragraph()
p3.text = "Numerical Simulation, Empirical Validation & RF Engineering Case Study using MATLAB & Python"
p3.font.size = Pt(16)
p3.font.color.rgb = ACCENT_BLUE
p3.space_before = Pt(10)

# Team box
team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.8), Inches(11.3), Inches(1.8))
team_box.fill.solid()
team_box.fill.fore_color.rgb = CARD_BG
team_box.line.color.rgb = ACCENT_BLUE
team_tf = team_box.text_frame
team_tf.word_wrap = True

tp0 = team_tf.paragraphs[0]
tp0.text = "PROJECT TEAM MEMBERS (B.Tech CSE, 7th Semester)"
tp0.font.size = Pt(12)
tp0.font.bold = True
tp0.font.color.rgb = ACCENT_GOLD

tp1 = team_tf.add_paragraph()
tp1.text = "• Harsh Yadav  (Reg No: RA2311003011546)       • Utkarsh Dabas  (Reg No: RA2311003011550)       • Tamanna Singh  (Reg No: RA2311003011570)"
tp1.font.size = Pt(13)
tp1.font.bold = True
tp1.font.color.rgb = TEXT_LIGHT
tp1.space_before = Pt(8)

# Helper for card slides
def make_bullet_slide(slide_num, title, bullets, image_path=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(s)
    add_header(s, f"Slide {slide_num}: {title}")
    
    if image_path and os.path.exists(image_path):
        # 2 column layout: text left, image right
        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ACCENT_BLUE
        tf = card.text_frame
        tf.word_wrap = True
        
        for i, b in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(14)
            p.font.color.rgb = TEXT_LIGHT
            if i > 0:
                p.space_before = Pt(10)
        
        # Add image on the right
        s.shapes.add_picture(image_path, Inches(7.1), Inches(1.8), width=Inches(5.4))
    else:
        # Full width 2-card or 1-card layout
        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ACCENT_BLUE
        tf = card.text_frame
        tf.word_wrap = True
        
        for i, b in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(15)
            p.font.color.rgb = TEXT_LIGHT
            if i > 0:
                p.space_before = Pt(12)

slides_data = [
    (2, "Introduction & Motivation", [
        "• What is Path Loss? The fundamental reduction in power density of an electromagnetic wave as it propagates.",
        "• Formulation: Expressed in decibels as PL(dB) = 10 * log10(Pt / Pr).",
        "• Crucial Importance in Wireless Design: Governs cellular coverage radius, base station transmitter sizing, link budgeting, and frequency reuse planning.",
        "• Why Theoretical Models Fall Short: Real environments exhibit reflection, diffraction, scattering, and building clutter that deviate sharply from ideal inverse-square decay.",
        "• Project Objective: Compare Free Space, Okumura, and Hata models using numerical simulation in MATLAB and Python."
    ]),
    (3, "Theoretical Foundation: Free Space Path Loss (FSPL)", [
        "• Friis Transmission Theory: Assumes unobstructed, vacuum line-of-sight (LOS) propagation between isotropic antennas.",
        "• Governing Formula: L_fspl(dB) = 20*log10(d) + 20*log10(f) + 32.44  [d in km, f in MHz].",
        "• Inverse-Square Law (n = 2): Signal power attenuates strictly at 20 dB per decade of distance.",
        "• Free Space Constant (32.44): Derived directly from 20*log10(4*pi / c) with unit conversions.",
        "• Role in Wireless Engineering: Serves as an absolute theoretical lower bound on signal loss; unattainable in terrestrial clutter."
    ]),
    (4, "Empirical Foundation: Okumura Propagation Model", [
        "• Historical Background: Developed by Yoshihisa Okumura (1968) from extensive drive-test measurements in Tokyo, Japan.",
        "• Classic Nomogram Methodology: Graphical curves of median attenuation A_mu(f, d) plotted relative to free space.",
        "• Open Area Empirical Correction: Standard formulation for rural/open terrain:",
        "    Correction(dB) = -4.78*(log10(f))^2 + 18.33*log10(f) - 40.94",
        "    L_okumura = L_hata + Correction",
        "• Physical Behavior: Open area attenuation is ~28.5 dB lower than dense urban loss at 900 MHz."
    ]),
    (5, "Empirical Foundation: Hata Urban Model", [
        "• Closed-Form Standardization: Formulated by Masaharu Hata (1980) to convert Okumura's graphical curves into mathematical equations.",
        "• Mobile Antenna Correction Factor (Small/Medium City):",
        "    a(h_re) = (1.1*log10(f) - 0.7)*h_re - (1.56*log10(f) - 0.8)",
        "    At f = 900 MHz, h_re = 1.5 m -> a(h_re) = 0.00 dB.",
        "• Urban Path Loss Equation:",
        "    L_hata(dB) = 69.55 + 26.16*log10(f) - 13.82*log10(h_te) - a(h_re) + [44.9 - 6.55*log10(h_te)]*log10(d)",
        "• Distance Decay Exponent: For h_te = 30 m, slope is 35.22 dB/decade (effective n ~ 3.52)."
    ]),
    (6, "Simulation Parameters & Benchmark Setup", [
        "• Standard Cellular Benchmark Configuration:",
        "    - Carrier Frequency (f): 900 MHz (Standard GSM-900 / 3G / LTE Band 8)",
        "    - Base Station Antenna Height (h_te): 30 meters (Macrocell tower)",
        "    - Mobile Station Antenna Height (h_re): 1.5 meters (Handheld receiver)",
        "    - Distance Range (d): 1 km to 20 km (Macrocellular coverage zone)",
        "• Computational Methodology: Vectorized distance array d = 1:0.1:20 km for smooth plotting.",
        "• Outputs: Tabular comparisons at 1 km steps and publication-grade graph export."
    ]),
    (7, "Simulation Methodology & Dual Engine Pipeline", [
        "• Dual Implementation Architecture: Identical algorithms implemented in both Python 3 and MATLAB.",
        "• Python Engine (path_loss_simulation.py): NumPy vectorized array arithmetic with Matplotlib visualization.",
        "• MATLAB Engine (path_loss_simulation.m): Native matrix operations with grid, legends, and high-res figure export.",
        "• Execution Workflow:",
        "    1. Parameter bounds validation (f in 150-1500 MHz, h_te in 30-200 m).",
        "    2. Evaluate correction factors a(h_re) and rural open-area factor.",
        "    3. Vectorized calculation of L_fspl, L_okumura, and L_hata.",
        "    4. Console tabular reporting and graphical export (path_loss_graph.png)."
    ]),
    (8, "Numerical Simulation Results (Tabular Comparison)", [
        "• Exact Quantitative Readings at Key Distance Benchmarks:",
        "    - At 1 km:   Free Space = 91.52 dB  | Okumura = 97.90 dB   | Hata = 126.40 dB",
        "    - At 2 km:   Free Space = 97.55 dB  | Okumura = 108.50 dB  | Hata = 137.01 dB",
        "    - At 5 km:   Free Space = 105.50 dB | Okumura = 122.52 dB  | Hata = 151.02 dB",
        "    - At 10 km:  Free Space = 111.52 dB | Okumura = 133.12 dB  | Hata = 161.63 dB",
        "    - At 15 km:  Free Space = 115.05 dB | Okumura = 139.32 dB  | Hata = 167.83 dB",
        "    - At 20 km:  Free Space = 117.55 dB | Okumura = 143.73 dB  | Hata = 172.23 dB",
        "• Discrepancy at 20 km: Hata urban model predicts 54.68 dB higher loss than Free Space!"
    ]),
    (9, "Comparative Path Loss Visualization", [
        "• Visual Analysis of path_loss_graph.png:",
        "    - Blue Dash-Dot Curve: Free Space Path Loss (slope = 20 dB/decade)",
        "    - Green Dashed Curve: Okumura Open Area (slope = 35.22 dB/decade)",
        "    - Red Solid Curve: Hata Urban Model (slope = 35.22 dB/decade)",
        "• Visual Curve Separation: Curves diverge sharply with distance due to the exponent difference (n=2 vs n=3.52).",
        "• Constant Urban-Rural Delta: Hata urban curve sits exactly 28.5 dB above Okumura open-area curve at all distances."
    ], "path_loss_graph.png"),
    (10, "Quantitative Divergence Analysis", [
        "• At 1 km Distance:",
        "    - Hata Urban vs Free Space: 126.40 - 91.52 = +34.88 dB penalty.",
        "    - Okumura Open vs Free Space: 97.90 - 91.52 = +6.38 dB penalty.",
        "• At 20 km Distance:",
        "    - Hata Urban vs Free Space: 172.23 - 117.55 = +54.68 dB penalty.",
        "    - Okumura Open vs Free Space: 143.73 - 117.55 = +26.18 dB penalty.",
        "• Physical Meaning of 54.68 dB Penalty:",
        "    - 10^(54.68 / 10) = 293,765 times more signal attenuation in linear power!",
        "    - Demonstrates why cellular networks cannot rely on free-space equations."
    ]),
    (11, "Environmental Clutter & Physical Decay Mechanisms", [
        "• Ground Reflection & Multipath: Two-ray destructive interference accelerates signal decay from 1/d^2 to 1/d^4 at long ranges.",
        "• Rooftop Diffraction (Knife-Edge): Signals diffract over building rows, introducing 20-30 dB of non-line-of-sight (NLOS) shadow loss.",
        "• Street Canyon Scattering: Multipath reflections from concrete building facades cause Rayleigh fading and severe local attenuation.",
        "• Foliage & Canopy Losses: Open areas experience minor seasonal attenuation, while dense urban areas suffer continuous clutter."
    ]),
    (12, "Cellular Network Planning & Link Budget Implications", [
        "• Macrocell Link Budget Example (900 MHz):",
        "    - Transmit Power (Pt): +43 dBm (20 W tower amplifier)",
        "    - Base Station Antenna Gain: +15 dBi | Mobile Gain: 0 dBi",
        "    - Receiver Sensitivity (P_min): -104 dBm",
        "    - Maximum Allowable Path Loss (MAPL): 43 + 15 - (-104) = 162 dB",
        "• Real Coverage Impact:",
        "    - Free Space: Coverage would exceed 100 km (completely unrealistic).",
        "    - Hata Urban: Maximum coverage radius is restricted to ~10.4 km.",
        "    - Result: Cellular engineers must deploy microcells and frequency reuse."
    ]),
    (13, "Model Assumptions & Validity Boundaries", [
        "• Free Space Model Validity: Outer space satellite communications or cleared microwave links with 100% 1st Fresnel zone clearance.",
        "• Hata Model Operating Boundaries:",
        "    - Frequency (f): 150 MHz to 1500 MHz (Unsuitable for 3.5 GHz 5G NR)",
        "    - Base Station Height (h_te): 30 m to 200 m (Tower above average rooftop)",
        "    - Mobile Height (h_re): 1 m to 10 m (Handheld or vehicular terminal)",
        "    - Distance (d): 1 km to 20 km (Cannot be used for indoor or microcells < 1 km)",
        "• Warning: Applying Hata for d < 1 km yields mathematically unstable values."
    ]),
    (14, "Future Scope: 5G/6G & Machine Learning Extensions", [
        "• Extension to High-Frequency Bands: COST-231 Hata (up to 2 GHz), mmWave models (28 GHz / 39 GHz / 60 GHz).",
        "• 3GPP Standardized Propagation Models: 3GPP TR 38.901 for Urban Micro (UMi), Urban Macro (UMa), and Indoor Office (InH).",
        "• 3D Ray-Tracing Simulation: Incorporating high-resolution 3D GIS building databases and LiDAR elevation scans.",
        "• AI/ML Predictive Path Loss: Neural network regressors trained on real-time drive-test data to predict path loss with < 3 dB RMSE."
    ]),
    (15, "Conclusion & Academic References", [
        "• Summary of Findings:",
        "    1. Free Space is an idealized lower bound (optimistic by 35 to 55 dB).",
        "    2. Okumura Open Area represents ideal rural deployment (moderate decay).",
        "    3. Hata Urban is the essential baseline for macrocellular link budgeting.",
        "• Academic References:",
        "    [1] T. S. Rappaport, Wireless Communications: Principles and Practice, 2nd ed., Prentice Hall, 2002.",
        "    [2] Y. Okumura et al., 'Field strength and its variability in VHF and UHF land-mobile radio service,' Rev. Elec. Commun. Lab., vol. 16, pp. 825-873, 1968.",
        "    [3] M. Hata, 'Empirical formula for propagation loss in land mobile radio services,' IEEE Trans. Veh. Technol., vol. VT-29, no. 3, pp. 317-325, 1980."
    ])
]

for s_num, title, bullets, *img in slides_data:
    image_path = img[0] if img else None
    make_bullet_slide(s_num, title, bullets, image_path)

output_path = os.path.join(os.getcwd(), "Mini_Project_Presentation_15Slides.pptx")
prs.save(output_path)
print(f"[+] 15-Slide Presentation successfully saved at: {output_path}")

