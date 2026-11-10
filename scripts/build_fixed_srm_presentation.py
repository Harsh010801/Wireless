"""
Generate a professional, fully corrected 16-slide PowerPoint presentation
titled 'SRM_Wireless_Propagation_Final.pptx' for SRM IST Department of Computing Technologies.
Fixes all technical errors, layout flaws, undefined variables in code, and conceptual inaccuracies.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# --- Color Palette (SRM Blue & Gold Academic Theme) ---
NAVY_HEADER = RGBColor(15, 32, 67)     # SRM Dark Navy
SRM_BLUE    = RGBColor(27, 85, 155)    # SRM Emblem Blue
ACCENT_GOLD = RGBColor(212, 175, 55)   # SRM Academic Gold
BG_LIGHT    = RGBColor(248, 250, 252)  # Clean off-white background
CARD_BG     = RGBColor(255, 255, 255)  # Crisp white card
CARD_BORDER = RGBColor(226, 232, 240)  # Subtle border
TEXT_MAIN   = RGBColor(30, 41, 59)     # Slate 800
TEXT_MUTED  = RGBColor(100, 116, 139)  # Slate 500
CODE_BG     = RGBColor(15, 23, 42)     # Dark slate for code
CODE_TEXT   = RGBColor(241, 245, 249)  # Code text
HIGHLIGHT_GREEN = RGBColor(16, 185, 129)
HIGHLIGHT_RED   = RGBColor(239, 68, 68)
HIGHLIGHT_BLUE  = RGBColor(59, 130, 246)

def set_slide_background(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_LIGHT

def add_header(slide, title_text, slide_num):
    # Top banner bar
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    banner.fill.solid()
    banner.fill.fore_color.rgb = NAVY_HEADER
    banner.line.fill.background()
    
    # Institution & Department branding in header
    brand_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.35))
    tf_b = brand_box.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.text = "SRM INSTITUTE OF SCIENCE & TECHNOLOGY | SCHOOL OF COMPUTING | DEPT. OF COMPUTING TECHNOLOGIES"
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = ACCENT_GOLD
    
    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(10.5), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(255, 255, 255)
    
    # Slide number badge in header right
    num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.42), Inches(1.0), Inches(0.5))
    tf_n = num_box.text_frame
    p_n = tf_n.paragraphs[0]
    p_n.text = f"{slide_num} / 16"
    p_n.alignment = PP_ALIGN.RIGHT
    p_n.font.size = Pt(13)
    p_n.font.bold = True
    p_n.font.color.rgb = ACCENT_GOLD
    
    # Gold accent line below header
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_GOLD
    line.line.fill.background()

    # Footer
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.733), Inches(0.35))
    tf_f = footer_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "21CSE458T — Wireless & Mobile Communication  |  Team: Harsh Yadav, Utkarsh Dabas, Tamanna Singh  |  Date: 10/11/2026"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = TEXT_MUTED

# =========================================================================
# SLIDE 1: Title Slide
# =========================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Large Navy Backdrop Block
top_block = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(4.3))
top_block.fill.solid()
top_block.fill.fore_color.rgb = NAVY_HEADER
top_block.line.fill.background()

# Gold accent separator
gold_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(4.3), Inches(13.333), Inches(0.06))
gold_bar.fill.solid()
gold_bar.fill.fore_color.rgb = ACCENT_GOLD
gold_bar.line.fill.background()

# Institution Title Box
inst_box = s1.shapes.add_textbox(Inches(1.0), Inches(0.4), Inches(11.333), Inches(0.8))
tf_inst = inst_box.text_frame
p_i1 = tf_inst.paragraphs[0]
p_i1.text = "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY"
p_i1.font.size = Pt(14)
p_i1.font.bold = True
p_i1.font.color.rgb = ACCENT_GOLD

p_i2 = tf_inst.add_paragraph()
p_i2.text = "SCHOOL OF COMPUTING  •  DEPARTMENT OF COMPUTING TECHNOLOGIES"
p_i2.font.size = Pt(11)
p_i2.font.color.rgb = RGBColor(226, 232, 240)
p_i2.space_before = Pt(3)

# Project Title
proj_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.333), Inches(2.5))
tf_proj = proj_box.text_frame
tf_proj.word_wrap = True

p_p1 = tf_proj.paragraphs[0]
p_p1.text = "Comparative Analysis of Wireless Signal Propagation Models"
p_p1.font.size = Pt(30)
p_p1.font.bold = True
p_p1.font.color.rgb = RGBColor(255, 255, 255)

p_p2 = tf_proj.add_paragraph()
p_p2.text = "Free Space  •  Okumura  •  Hata   |   A MATLAB Simulation Case Study"
p_p2.font.size = Pt(17)
p_p2.font.color.rgb = RGBColor(147, 197, 253)
p_p2.space_before = Pt(10)

p_p3 = tf_proj.add_paragraph()
p_p3.text = "Course: 21CSE458T — Wireless and Mobile Communication   |   B.Tech CSE (7th Semester)"
p_p3.font.size = Pt(12)
p_p3.font.color.rgb = ACCENT_GOLD
p_p3.space_before = Pt(12)

# Student Credentials Cards (3 Clean Cards)
students = [
    ("Student 1", "HARSH YADAV", "RA2311003011546"),
    ("Student 2", "UTKARSH DABAS", "RA2311003011550"),
    ("Student 3", "TAMANNA SINGH", "RA2311003011570"),
]

for idx, (label, name, regno) in enumerate(students):
    left = Inches(1.0 + idx * 3.9)
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(4.7), Inches(3.6), Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1.5)
    
    tf_c = card.text_frame
    tf_c.word_wrap = True
    
    p0 = tf_c.paragraphs[0]
    p0.text = label.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = SRM_BLUE
    
    p1 = tf_c.add_paragraph()
    p1.text = name
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MAIN
    p1.space_before = Pt(4)
    
    p2 = tf_c.add_paragraph()
    p2.text = f"Reg No: {regno}"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(4)
    
    p3 = tf_c.add_paragraph()
    p3.text = "B.Tech Computer Science & Engg."
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(6)

# =========================================================================
# HELPER: Make 4-Card Slide
# =========================================================================
def make_4card_slide(slide_num, title, cards_data):
    s = prs.slides.add_slide(blank_layout)
    set_slide_background(s)
    add_header(s, title, slide_num)
    
    coords = [
        (Inches(0.8), Inches(1.5)),
        (Inches(6.8), Inches(1.5)),
        (Inches(0.8), Inches(4.2)),
        (Inches(6.8), Inches(4.2)),
    ]
    
    for idx, (c_title, c_desc, icon) in enumerate(cards_data):
        left, top = coords[idx]
        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)
        
        tf = card.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"{icon}  {c_title}"
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = SRM_BLUE
        
        p1 = tf.add_paragraph()
        p1.text = c_desc
        p1.font.size = Pt(12)
        p1.font.color.rgb = TEXT_MAIN
        p1.space_before = Pt(8)

# SLIDE 2: Objectives
make_4card_slide(2, "Project Objectives", [
    ("Understand Path Loss Mechanics", "Investigate how radiated electromagnetic radio frequency power decays logarithmically as the distance between the transmitter tower and user terminal increases.", "📡"),
    ("Comparative Theoretical Evaluation", "Critically analyze Free Space, Okumura, and Hata models: evaluating foundational physics assumptions, environmental clutter factors, and domain constraints.", "🔍"),
    ("Vectorized Simulation & Visualization", "Implement clean numerical pipelines in MATLAB & Python to compute path loss across 1 km – 20 km at 900 MHz and plot synchronized comparison curves on a single unified graph.", "💻"),
    ("RF Engineering Link Budget Decisions", "Formulate realistic cellular coverage conclusions: quantify why Free Space is overly optimistic and why Hata Urban is essential for real cellular network planning.", "🎯"),
])

# SLIDE 3: Tools Used
make_4card_slide(3, "Software Tools & Simulation Environment", [
    ("MATLAB R20xx", "Primary simulation platform for vectorized matrix computation, multi-curve visualization, and publication-quality graph generation (path_loss_simulation.m & path_loss_animation.m).", "⚙️"),
    ("GNU Octave (Open-Source)", "100% compatible open-source MATLAB alternative for headless execution, lab portability, and batch execution without proprietary license barriers.", "🐧"),
    ("Python 3 & NumPy / Matplotlib", "Secondary high-performance numerical cross-validation engine (path_loss_simulation.py) with interactive Streamlit web dashboard deployment.", "🐍"),
    ("Documentation & Reporting Tools", "Microsoft Word (.docx) formal technical report generator and PowerPoint (.pptx) deck for defense and viva voce presentation.", "📄"),
])

# SLIDE 4: Topic Overview
make_4card_slide(4, "Topic Overview: Wireless Channel Characterization", [
    ("Wireless Signal ≠ Constant Power", "As mobile users travel away from base stations, received radio power decays drastically due to geometric wave spreading, reflection, diffraction, and clutter absorption.", "📉"),
    ("Path Loss Definition", "Logarithmic ratio of transmitted power to received power: PL(dB) = 10 log10(Pt / Pr). It serves as the primary metric for coverage radius and link budget feasibility.", "📐"),
    ("The Critical Need for Accurate Modeling", "Underestimating path loss creates coverage holes and dropped calls; overestimating causes unnecessary tower overbuilding and bloated infrastructure capital expenditure (CAPEX).", "⚠️"),
    ("Propagation Model Categorization", "Models range from purely theoretical line-of-sight equations (Friis Free Space) to empirical drive-test models (Okumura) and closed-form standard equations (Hata).", "📚"),
])

# SLIDE 5: What We Are Doing
make_4card_slide(5, "Methodological Roadmap: Step-by-Step", [
    ("Step 1: Benchmark Parameter Definition", "Standardize cellular link parameters: carrier frequency f = 900 MHz (GSM band), tower height h_te = 30 m, mobile height h_re = 1.5 m, distance span d = 1 km to 20 km.", "1️⃣"),
    ("Step 2: Model Formulation & Computation", "Compute path loss values across d using Free Space (Friis), Hata Urban equation, and Okumura open-area empirical correction equations.", "2️⃣"),
    ("Step 3: Single-Graph Comparative Visualization", "Plot all 3 curves on a single unified MATLAB figure with distinct line styles, markers, gridlines, axis labels, and legend for direct visual comparison.", "3️⃣"),
    ("Step 4: Quantitative Divergence & viva Analysis", "Calculate discrete path loss delta values at 1 km and 20 km, analyze decay slope (dB/decade), and formulate conclusions for cellular engineering.", "4️⃣"),
])

# =========================================================================
# SLIDE 6: Models Overview (Proper Clean Table)
# =========================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Propagation Models Overview & Comparison", 6)

# Add Table
rows = 4
cols = 5
left = Inches(0.8)
top = Inches(1.6)
width = Inches(11.733)
height = Inches(4.5)

table_shape = s6.shapes.add_table(rows, cols, left, top, width, height)
tbl = table_shape.table

headers = ["Model", "Foundational Basis", "Target Environment", "Predicted Loss", "Practical Computational Ease"]
table_data = [
    ["Free Space (FSPL)", "Electromagnetic Theory\n(Friis LOS, no obstacles)", "Vacuum / Deep Space /\nClear Microwave LOS", "Lowest Loss\n(Overly Optimistic)", "Very Easy\n(Simple closed-form)"],
    ["Okumura Model", "Drive-test field measurements\n(Tokyo, Japan, 1968)", "Urban, suburban, and\nrural terrain with clutter", "High & Realistic\n(Tokyo empirical baseline)", "Complex / Manual\n(Requires reading charts)"],
    ["Hata Model", "Empirical parametric fitting\nof Okumura's curves (1980)", "Urban, suburban, and\nopen rural environments", "Realistic Macrocell Loss\n(Standard benchmark)", "Easy & Programmatic\n(Closed-form formulas)"],
]

for col_idx, h_text in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.text = h_text
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY_HEADER
    for p in cell.text_frame.paragraphs:
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

for row_idx, row_vals in enumerate(table_data):
    for col_idx, val in enumerate(row_vals):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 0 else RGBColor(241, 245, 249)
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = SRM_BLUE

# Bottom takeaway banner
callout = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.65))
callout.fill.solid()
callout.fill.fore_color.rgb = CARD_BG
callout.line.color.rgb = ACCENT_GOLD
callout.line.width = Pt(1.5)
tf_cal = callout.text_frame
p_cal = tf_cal.paragraphs[0]
p_cal.text = "🔑 Key Academic Takeaway: All three are standard curriculum models. The defining difference lies entirely in how each model treats terrestrial obstacle clutter, ground reflection, and rooftop diffraction."
p_cal.font.size = Pt(10.5)
p_cal.font.bold = True
p_cal.font.color.rgb = NAVY_HEADER

# =========================================================================
# HELPER: Make 2-Column Model Theory Slide
# =========================================================================
def make_theory_slide(slide_num, model_title, points, formula_lines, example_lines):
    s = prs.slides.add_slide(blank_layout)
    set_slide_background(s)
    add_header(s, model_title, slide_num)
    
    # Left Card: Theory & Key Points
    card_left = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = CARD_BG
    card_left.line.color.rgb = CARD_BORDER
    tf_l = card_left.text_frame
    tf_l.word_wrap = True
    
    p0 = tf_l.paragraphs[0]
    p0.text = "📋 Theoretical Principles & Scope"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = SRM_BLUE
    
    for pt in points:
        p = tf_l.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)
        
    # Right Card: Formulas & Calculations
    card_right = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.3))
    card_right.fill.solid()
    card_right.fill.fore_color.rgb = CARD_BG
    card_right.line.color.rgb = CARD_BORDER
    tf_r = card_right.text_frame
    tf_r.word_wrap = True
    
    pr0 = tf_r.paragraphs[0]
    pr0.text = "📐 Governing Mathematical Formulas"
    pr0.font.size = Pt(16)
    pr0.font.bold = True
    pr0.font.color.rgb = NAVY_HEADER
    
    for fl in formula_lines:
        p = tf_r.add_paragraph()
        p.text = fl
        p.font.size = Pt(12)
        p.font.bold = True if fl.startswith("L") or fl.startswith("a(") else False
        p.font.color.rgb = SRM_BLUE if fl.startswith("L") else TEXT_MAIN
        p.space_before = Pt(6)
        
    pr_ex = tf_r.add_paragraph()
    pr_ex.text = "🔢 Numerical Benchmark Calculation:"
    pr_ex.font.size = Pt(13)
    pr_ex.font.bold = True
    pr_ex.font.color.rgb = ACCENT_GOLD
    pr_ex.space_before = Pt(14)
    
    for el in example_lines:
        p = tf_r.add_paragraph()
        p.text = el
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

# SLIDE 7: Free Space Model
make_theory_slide(
    7, "Model 1: Free Space Path Loss (Friis Theory)",
    [
        "Assumes an idealized, unobstructed vacuum transmission medium.",
        "Governed strictly by Friis Transmission Law and spherical wave spreading.",
        "Signal power decays with the inverse-square of distance (path loss exponent n = 2).",
        "Path loss increases at exactly 20 dB per decade of distance (20 dB/decade).",
        "Provides an absolute theoretical LOWER BOUND on path loss for wireless links.",
        "Applications: Satellite downlinks, deep-space probes, cleared microwave LoS links."
    ],
    [
        "Governing Equation (Practical Engineering Units):",
        "L_FSPL (dB) = 20 log10(d) + 20 log10(f) + 32.44",
        "Where:",
        "  • d = link distance in kilometers (km)",
        "  • f = carrier frequency in megahertz (MHz)",
        "  • 32.44 = unit conversion constant: 20 log10(4π / c)"
    ],
    [
        "At f = 900 MHz, d = 1 km:",
        "L_FSPL = 20 log10(1) + 20 log10(900) + 32.44",
        "L_FSPL = 0 + 59.08 + 32.44 = 91.52 dB",
        "At d = 20 km: L_FSPL = 91.52 + 20 log10(20) = 117.55 dB"
    ]
)

# SLIDE 8: Okumura Model
make_theory_slide(
    8, "Model 2: Okumura Empirical Propagation Model",
    [
        "Pioneering empirical model based on extensive Tokyo field drive-tests (1968).",
        "Fully captures urban obstacles: buildings, vehicles, terrain undulations, and foliage.",
        "Originally formulated as graphical attenuation charts (nomograms) relative to free space.",
        "Requires manual chart lookup, making automated computer simulation cumbersome.",
        "Valid ranges: Frequency f = 150 to 1920 MHz, Distance d = 1 to 100 km, Tower height h_te = 30 to 1000 m.",
        "Standard modern implementation computes open-area loss via Hata's empirical correction."
    ],
    [
        "Nomogram Relationship:",
        "L_Okumura = L_FSPL + A_mu(f, d) - G(h_te) - G(h_re) - G_area",
        "Open Area Correction Formulation (used in modern simulation):",
        "Correction = -4.78 [log10(f)]^2 + 18.33 log10(f) - 40.94",
        "L_Okumura(open) = L_Hata(urban) + Correction",
        "At f = 900 MHz: Correction ≈ -28.50 dB"
    ],
    [
        "At f = 900 MHz, d = 1 km (open terrain):",
        "L_Okumura = 126.40 dB - 28.50 dB = 97.90 dB",
        "At d = 20 km: L_Okumura = 143.73 dB",
        "Observation: ~28.5 dB lower path loss than dense urban environment."
    ]
)

# SLIDE 9: Hata Urban Model
make_theory_slide(
    9, "Model 3: Hata Urban Propagation Model",
    [
        "Formulated by Masaharu Hata (1980) as a closed-form analytical fit to Okumura's curves.",
        "The global de-facto standard for macrocellular planning in VHF/UHF bands.",
        "Eliminated the need for graphical lookup charts, enabling automated RF computer simulation.",
        "Valid domain: f ∈ [150, 1500] MHz, d ∈ [1, 20] km, h_te ∈ [30, 200] m, h_re ∈ [1, 10] m.",
        "For h_te = 30 m, effective distance decay rate is [44.9 - 6.55 log10(30)] ≈ 35.22 dB/decade.",
        "Represents an effective terrestrial path loss exponent of n ≈ 3.52."
    ],
    [
        "Urban Path Loss Equation (f in MHz, d in km, h_te in m):",
        "L_Hata = 69.55 + 26.16 log10(f) - 13.82 log10(h_te) - a(h_re) + [44.9 - 6.55 log10(h_te)] log10(d)",
        "Mobile Antenna Height Correction Factor (Small/Medium City):",
        "a(h_re) = (1.1 log10(f) - 0.7) h_re - (1.56 log10(f) - 0.8)",
        "At f = 900 MHz, h_re = 1.5 m: a(h_re) ≈ 0.00 dB"
    ],
    [
        "At f = 900 MHz, h_te = 30 m, h_re = 1.5 m, d = 1 km:",
        "L_Hata = 69.55 + 77.28 - 20.41 - 0.02 + 0 = 126.40 dB",
        "At d = 20 km: L_Hata = 126.40 + 35.22 log10(20) = 172.23 dB",
        "Observation: 54.68 dB higher loss than Free Space at 20 km!"
    ]
)

# =========================================================================
# SLIDE 10: Methodology & Bug-Free MATLAB Code
# =========================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "Methodology & Verified MATLAB Implementation", 10)

# Left Column: Steps
c_left = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.2), Inches(5.3))
c_left.fill.solid()
c_left.fill.fore_color.rgb = CARD_BG
c_left.line.color.rgb = CARD_BORDER
tf_steps = c_left.text_frame
tf_steps.word_wrap = True

ps0 = tf_steps.paragraphs[0]
ps0.text = "⚙️ Simulation Execution Steps"
ps0.font.size = Pt(16)
ps0.font.bold = True
ps0.font.color.rgb = SRM_BLUE

steps_list = [
    "Step 1: Set Link Parameters — Define carrier frequency f = 900 MHz, tower height h_te = 30 m, mobile height h_re = 1.5 m, distance array d = 1:20 km.",
    "Step 2: Compute Free Space Loss — Vectorized evaluation of Friis equation L_fspl across all distance points.",
    "Step 3: Evaluate Mobile Correction a(h_re) — Closed-form correction for medium city geometry.",
    "Step 4: Compute Hata Urban Path Loss — Vectorized equation capturing rooftop diffraction and building clutter.",
    "Step 5: Apply Okumura Open Area Correction — Compute open-terrain path loss via standard empirical correction factor.",
    "Step 6: Render Multi-Curve Plot — Plot curves on one figure with grid, markers, legend, and high-res export."
]

for st_text in steps_list:
    p = tf_steps.add_paragraph()
    p.text = st_text
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(8)

# Right Column: Verified MATLAB Code (Dark IDE Style)
c_code = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.3), Inches(1.5), Inches(6.233), Inches(5.3))
c_code.fill.solid()
c_code.fill.fore_color.rgb = CODE_BG
c_code.line.color.rgb = ACCENT_GOLD
c_code.line.width = Pt(1.5)

tf_cd = c_code.text_frame
tf_cd.word_wrap = True

pcd0 = tf_cd.paragraphs[0]
pcd0.text = "💻 MATLAB Core Logic (path_loss_simulation.m)"
pcd0.font.size = Pt(13)
pcd0.font.bold = True
pcd0.font.color.rgb = ACCENT_GOLD

code_snippet = """% 1. Simulation Parameters
d = 1:20;  f = 900;  h_te = 30;  h_re = 1.5;

% 2. Free Space Path Loss (FSPL)
fspl = 20*log10(d) + 20*log10(f) + 32.44;

% 3. Mobile Antenna Correction Factor
a_hre = (1.1*log10(f) - 0.7)*h_re - (1.56*log10(f) - 0.8);

% 4. Hata Urban Model
hata_urban = 69.55 + 26.16*log10(f) - 13.82*log10(h_te) ...
             - a_hre + (44.9 - 6.55*log10(h_te)).*log10(d);

% 5. Okumura Model (Open Area Correction)
correction = -4.78*(log10(f)^2) + 18.33*log10(f) - 40.94;
okumura = hata_urban + correction;

% 6. Multi-Curve Plotting
figure;
plot(d, fspl, 'b-o', d, okumura, 'g--s', d, hata_urban, 'r-.^');
grid on; xlabel('Distance (km)'); ylabel('Path Loss (dB)');
legend('Free Space', 'Okumura (Open)', 'Hata (Urban)');"""

p_code = tf_cd.add_paragraph()
p_code.text = code_snippet
p_code.font.size = Pt(10)
p_code.font.name = "Consolas"
p_code.font.color.rgb = CODE_TEXT
p_code.space_before = Pt(8)

# =========================================================================
# SLIDE 11: Results Graph & Numerical Table
# =========================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, "Simulation Results & Multi-Curve Graph", 11)

# Embed High-Res Graph on Left
graph_path = os.path.join(os.getcwd(), "path_loss_graph.png")
if os.path.exists(graph_path):
    s11.shapes.add_picture(graph_path, Inches(0.8), Inches(1.5), width=Inches(6.8))

# Right Column: Results Table & Numerical Insights
c_res = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.3))
c_res.fill.solid()
c_res.fill.fore_color.rgb = CARD_BG
c_res.line.color.rgb = CARD_BORDER
tf_res = c_res.text_frame
tf_res.word_wrap = True

pr_0 = tf_res.paragraphs[0]
pr_0.text = "📊 Key Benchmark Values"
pr_0.font.size = Pt(16)
pr_0.font.bold = True
pr_0.font.color.rgb = SRM_BLUE

res_points = [
    "At Distance d = 1.0 km:\n  • Free Space: 91.52 dB\n  • Okumura (Open): 97.90 dB\n  • Hata Urban: 126.40 dB\n  • Delta (Hata - FSPL): +34.88 dB",
    "At Distance d = 10.0 km:\n  • Free Space: 111.52 dB\n  • Okumura (Open): 133.12 dB\n  • Hata Urban: 161.63 dB\n  • Delta (Hata - FSPL): +50.11 dB",
    "At Distance d = 20.0 km:\n  • Free Space: 117.55 dB\n  • Okumura (Open): 143.73 dB\n  • Hata Urban: 172.23 dB\n  • Delta (Hata - FSPL): +54.68 dB",
    "Critical Takeaway:\nThe 54.68 dB divergence at 20 km means actual urban signal power is 293,765 times weaker than Free Space theory predicts!"
]

for rp in res_points:
    p = tf_res.add_paragraph()
    p.text = rp
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(8)

# SLIDE 12: Key Learnings
make_4card_slide(12, "Key Learnings & Comparative Observations", [
    ("The Reality Gap in Modeling", "Free Space severely underestimates actual loss by 35 to 55 dB. Real terrestrial environments have ground reflections, building blockage, and diffraction that cannot be ignored.", "⚠️"),
    ("Okumura vs Hata Relationship", "Okumura provided the foundational drive-test empirical data; Hata converted Okumura's graphical curves into standard closed-form mathematical equations for automated RF design.", "🔄"),
    ("Distance Attenuation Slope", "Free Space path loss increases at 20 dB/decade (n = 2.0). Terrestrial Hata Urban path loss increases at 35.22 dB/decade (effective n ≈ 3.52) due to multipath clutter.", "📈"),
    ("Practical RF Planning Impact", "RF cell dimensioning, base station tower placement, and link budgets must use realistic models like Hata to avoid creating severe mobile coverage dead zones.", "🏗️"),
])

# SLIDE 13: Conclusion & Engineering Takeaway (CORRECTED LOWER BOUND)
make_4card_slide(13, "Conclusion & Engineering Recommendations", [
    ("Free Space: Theoretical Lower Bound", "Mathematically represents the MINIMUM possible path loss (highest possible received power). Valid strictly as a lower-bound reference or for satellite/clear LoS microwave links.", "🟢"),
    ("Okumura: Historical Empirical Pioneer", "Highly accurate for Japanese urban clutter based on real measurements, but impractical for daily modern computer automated network design due to manual nomograms.", "🟡"),
    ("Hata Urban: Macrocell Industry Standard", "Delivers the optimal balance between mathematical simplicity and real-world accuracy; universally adopted for 2G/3G/4G macrocellular RF engineering.", "🔴"),
    ("Definitive Engineering Takeaway", "For terrestrial cellular planning, Hata (urban/suburban) must always be used. Free Space must only be treated as an absolute lower-bound reference on path loss.", "🏆"),
])

# SLIDE 14: Future Scope
make_4card_slide(14, "Future Scope & Advanced Extensions", [
    ("COST-231 Hata Model Extension", "Extends classic Hata formulations from 1500 MHz up to 2000 MHz (2.0 GHz) to support modern 3G UMTS, 4G LTE Band 1/3, and PCS cellular networks.", "📡"),
    ("5G mmWave & Sub-THz Propagation", "Incorporate high-frequency 3GPP TR 38.901 channel models for 28 GHz and 39 GHz bands, accounting for atmospheric oxygen and rain attenuation.", "📶"),
    ("Stochastic Fading Integration", "Augment large-scale median path loss models with small-scale Rayleigh/Rician multipath fading and log-normal shadow fading distributions.", "🎲"),
    ("Machine Learning & 3D Ray Tracing", "Combine high-resolution 3D GIS city maps, LiDAR building data, and deep learning regressors to predict site-specific cellular path loss with < 3 dB error.", "🤖"),
])

# =========================================================================
# SLIDE 15: Academic References
# =========================================================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_background(s15)
add_header(s15, "Formal Academic References", 15)

c_ref = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.3))
c_ref.fill.solid()
c_ref.fill.fore_color.rgb = CARD_BG
c_ref.line.color.rgb = CARD_BORDER
tf_rf = c_ref.text_frame
tf_rf.word_wrap = True

prf0 = tf_rf.paragraphs[0]
prf0.text = "📚 Foundational Textbooks & Peer-Reviewed Literature"
prf0.font.size = Pt(16)
prf0.font.bold = True
prf0.font.color.rgb = SRM_BLUE

references = [
    "[1] T. S. Rappaport, Wireless Communications: Principles and Practice, 2nd ed. Upper Saddle River, NJ: Prentice Hall, 2002, ch. 3 & 4 (Large-Scale Path Loss).",
    "[2] Y. Okumura, E. Ohmori, T. Kawano, and K. Fukuda, 'Field strength and its variability in VHF and UHF land-mobile radio service,' Review of the Electrical Communication Laboratory, vol. 16, no. 9–10, pp. 825–873, 1968.",
    "[3] M. Hata, 'Empirical formula for propagation loss in land mobile radio services,' IEEE Transactions on Vehicular Technology, vol. VT-29, no. 3, pp. 317–325, Aug. 1980.",
    "[4] European Cooperative in Science and Technology (COST 231), 'Digital mobile radio towards future generation systems,' Final report, COST Telecom Secretariat, Brussels, Belgium, 1999.",
    "[5] Course Syllabus & Class Lectures, 21CSE458T — Wireless and Mobile Communication, Units 1–3, Department of Computing Technologies, SRM Institute of Science and Technology, 2026."
]

for ref in references:
    p = tf_rf.add_paragraph()
    p.text = ref
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

# =========================================================================
# SLIDE 16: Thank You / Q&A Slide
# =========================================================================
s16 = prs.slides.add_slide(blank_layout)
set_slide_background(s16)

# Large Center Banner
banner_q = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(4.5))
banner_q.fill.solid()
banner_q.fill.fore_color.rgb = NAVY_HEADER
banner_q.line.fill.background()

gold_bar_q = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(4.5), Inches(13.333), Inches(0.06))
gold_bar_q.fill.solid()
gold_bar_q.fill.fore_color.rgb = ACCENT_GOLD
gold_bar_q.line.fill.background()

tf_q = banner_q.text_frame
tf_q.word_wrap = True

pq1 = tf_q.paragraphs[0]
pq1.text = "THANK YOU!"
pq1.font.size = Pt(44)
pq1.font.bold = True
pq1.font.color.rgb = ACCENT_GOLD
pq1.alignment = PP_ALIGN.CENTER
pq1.space_before = Pt(40)

pq2 = tf_q.add_paragraph()
pq2.text = "Questions & Academic Discussion Welcome"
pq2.font.size = Pt(22)
pq2.font.bold = True
pq2.font.color.rgb = RGBColor(255, 255, 255)
pq2.alignment = PP_ALIGN.CENTER
pq2.space_before = Pt(10)

pq3 = tf_q.add_paragraph()
pq3.text = "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY  •  DEPARTMENT OF COMPUTING TECHNOLOGIES"
pq3.font.size = Pt(12)
pq3.font.color.rgb = RGBColor(147, 197, 253)
pq3.alignment = PP_ALIGN.CENTER
pq3.space_before = Pt(12)

# Team members box on bottom
bot_box = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(5.0), Inches(10.333), Inches(1.8))
bot_box.fill.solid()
bot_box.fill.fore_color.rgb = CARD_BG
bot_box.line.color.rgb = CARD_BORDER
bot_box.line.width = Pt(1.5)

tf_b = bot_box.text_frame
tf_b.word_wrap = True

pb0 = tf_b.paragraphs[0]
pb0.text = "PROJECT TEAM (21CSE458T — WIRELESS AND MOBILE COMMUNICATION)"
pb0.font.size = Pt(11)
pb0.font.bold = True
pb0.font.color.rgb = SRM_BLUE
pb0.alignment = PP_ALIGN.CENTER

pb1 = tf_b.add_paragraph()
pb1.text = "Harsh Yadav (RA2311003011546)    •    Utkarsh Dabas (RA2311003011550)    •    Tamanna Singh (RA2311003011570)"
pb1.font.size = Pt(14)
pb1.font.bold = True
pb1.font.color.rgb = TEXT_MAIN
pb1.alignment = PP_ALIGN.CENTER
pb1.space_before = Pt(8)

pb2 = tf_b.add_paragraph()
pb2.text = "MATLAB Code  •  Python Simulation  •  Word Report (.docx)  •  Live Interactive Dashboard Available"
pb2.font.size = Pt(10.5)
pb2.font.color.rgb = TEXT_MUTED
pb2.alignment = PP_ALIGN.CENTER
pb2.space_before = Pt(6)

output_file = os.path.join(os.getcwd(), "SRM_Wireless_Propagation_Final.pptx")
prs.save(output_file)
print(f"[+] Successfully generated: {output_file}")

