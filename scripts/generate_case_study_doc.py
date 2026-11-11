"""
Generates a comprehensive, publication-grade Case Study Word Document:
Case_Study_Document.docx
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT_DIR = Path(__file__).resolve().parent.parent


def set_cell_bg(cell, hex_color: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def add_styled_heading(doc: Document, text: str, level: int = 1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Calibri"
        run.font.color.rgb = RGBColor(19, 71, 41) if level == 1 else RGBColor(17, 24, 39)
    h.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    h.paragraph_format.space_after = Pt(6)
    return h


def build_case_study():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.95)
        section.right_margin = Inches(0.95)

    # ---------------------------------------------------------
    # COVER / TITLE HEADER
    # ---------------------------------------------------------
    badge_p = doc.add_paragraph()
    badge_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    badge_p.paragraph_format.space_before = Pt(24)
    badge_run = badge_p.add_run("TECHNICAL CASE STUDY DOCUMENT")
    badge_run.font.name = "Calibri"
    badge_run.font.size = Pt(11)
    badge_run.font.bold = True
    badge_run.font.color.rgb = RGBColor(88, 185, 44)

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(8)
    title_p.paragraph_format.space_after = Pt(12)
    t_run = title_p.add_run(
        "Comparative Analysis of Wireless Signal Propagation Models\n"
        "for Urban Macrocellular Network Planning"
    )
    t_run.font.name = "Calibri"
    t_run.font.size = Pt(22)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(19, 71, 41)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(22)
    s_run = sub_p.add_run(
        "A Simulation-Based Engineering Case Study Using MATLAB, Python (FastAPI), and React\n"
        "Course: Wireless and Mobile Communication  |  B.Tech Computer Science & Engineering"
    )
    s_run.font.name = "Calibri"
    s_run.font.size = Pt(11.5)
    s_run.font.italic = True
    s_run.font.color.rgb = RGBColor(75, 85, 99)

    # Team Table on Cover
    team_tbl = doc.add_table(rows=4, cols=3)
    team_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Team Member", "Registration Number", "Primary Case Study Role"]
    for j, h_text in enumerate(t_headers):
        cell = team_tbl.cell(0, j)
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10.5)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_bg(cell, "134729")

    members = [
        ("Harsh Yadav", "RA2311003011546", "Mathematical Modeling, Python Engine & Backend API"),
        ("Utkarsh Dabas", "RA2311003011550", "MATLAB Simulation, Sensitivity Sweeps & Validation"),
        ("Tamanna Singh", "RA2311003011570", "UI/UX Architecture, Link Budget & Comparative Analysis"),
    ]
    for idx, (name, reg, role) in enumerate(members, start=1):
        for j, val in enumerate((name, reg, role)):
            cell = team_tbl.cell(idx, j)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            if idx % 2 == 1:
                set_cell_bg(cell, "F3F4EF")

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # ---------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # ---------------------------------------------------------
    add_styled_heading(doc, "1. Executive Summary & Case Study Scenario", level=1)
    doc.add_paragraph(
        "Modern cellular operators designing 4G LTE and 5G networks face a critical RF planning challenge: "
        "predicting how fast radio frequency signals attenuate between a macrocell base station tower and "
        "mobile subscribers across heterogeneous terrain. Selecting an overly optimistic theoretical model "
        "causes severe urban dead zones and dropped calls, while overestimating loss leads to excessive base "
        "station deployments and inflated capital expenditure (CAPEX)."
    )
    doc.add_paragraph(
        "Case Scenario Evaluated: A telecommunications provider is deploying a 900 MHz macrocellular tower "
        "(antenna height h_te = 30 m, transmit power Pt = 43 dBm = 20 W, directional sector gain Gt = 15 dBi) "
        "serving handheld mobile devices (h_re = 1.5 m, receiver sensitivity threshold -100 dBm) across a "
        "1 km to 20 km service radius. This case study quantitatively evaluates how theoretical, empirical, "
        "and stochastic propagation models diverge under identical RF conditions."
    )

    # ---------------------------------------------------------
    # 2. MODELS EVALUATED IN THE CASE STUDY
    # ---------------------------------------------------------
    add_styled_heading(doc, "2. Propagation Models Evaluated", level=1)
    doc.add_paragraph(
        "Seven core propagation models were implemented in modular Python and MATLAB engines and exposed "
        "through the interactive WavePulse RF web application:"
    )
    model_bullets = [
        "Free Space Path Loss (FSPL): Friis inverse-square law baseline assuming unobstructed Line-of-Sight "
        "(PL = 20 log10(d) + 20 log10(f) + 32.44). Path loss exponent n = 2.0 (20 dB/decade).",
        "Okumura Model (Tokyo Empirical, 1968): Derived from drive-test measurements in Tokyo; evaluated for "
        "open-area terrain via the empirical frequency correction (-4.78*(log10(f))^2 + 18.33*log10(f) - 40.94).",
        "Okumura-Hata Urban Model (1980): Closed-form analytical macrocell equation incorporating urban rooftop "
        "diffraction, street clutter, base station height (30-200 m), and mobile height correction a(h_re).",
        "COST-231 Hata Extension: Extends Hata urban/suburban modeling to 1500-2000 MHz PCS and LTE frequency bands.",
        "Two-Ray Ground Reflection Model: Captures interference between the direct LOS ray and ground-reflected wave, "
        "transitioning to 40 dB/decade decay beyond the Fresnel crossover distance.",
        "Log-Distance & Log-Normal Shadowing: Introduces environment-tunable exponent n and zero-mean Gaussian "
        "shadowing X_sigma (dB) to predict cell-edge outage probability.",
    ]
    for b in model_bullets:
        p = doc.add_paragraph(b, style="List Bullet")
        p.paragraph_format.space_after = Pt(3)

    # ---------------------------------------------------------
    # 3. SIMULATION ARCHITECTURE (BACKEND + REACT + MATLAB)
    # ---------------------------------------------------------
    add_styled_heading(doc, "3. System Architecture & Simulation Pipeline", level=1)
    doc.add_paragraph(
        "To guarantee cross-platform reproducibility, all computations were validated across three synchronized layers:\n"
        "1. Core Scientific Package (src/propagation/): Independent Python modules validated by 32 automated pytest assertions.\n"
        "2. MATLAB Benchmark Scripts (path_loss_simulation.m & path_loss_animation.m): Native matrix implementation "
        "printing formatted tables and animated curve trajectories.\n"
        "3. Full-Stack Web Studio (backend/ FastAPI + frontend/ React & Tailwind): Live REST endpoints powering "
        "real-time Recharts path loss plots, HTML5 electromagnetic wavefront motion graphics, and interactive link budget calculators."
    )

    # ---------------------------------------------------------
    # 4. QUANTITATIVE CASE STUDY RESULTS (900 MHz BENCHMARK)
    # ---------------------------------------------------------
    add_styled_heading(doc, "4. Case Study Quantitative Findings (f = 900 MHz)", level=1)
    doc.add_paragraph(
        "Table 1 summarizes exact numerical path loss predictions across 1 km to 20 km for the three primary "
        "macrocell benchmark models (Free Space, Okumura Open Area, and Hata Urban)."
    )

    res_tbl = doc.add_table(rows=8, cols=5)
    res_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["Distance (km)", "Free Space (dB)", "Okumura Open (dB)", "Hata Urban (dB)", "Reality Gap (Hata - FSPL)"]
    for j, h in enumerate(r_headers):
        cell = res_tbl.cell(0, j)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_bg(cell, "134729")

    rows_data = [
        ("1 km", "91.52 dB", "97.90 dB", "126.40 dB", "+34.88 dB"),
        ("2 km", "97.55 dB", "108.50 dB", "137.01 dB", "+39.46 dB"),
        ("5 km", "105.50 dB", "122.52 dB", "151.02 dB", "+45.52 dB"),
        ("10 km", "111.52 dB", "133.12 dB", "161.63 dB", "+50.11 dB"),
        ("15 km", "115.05 dB", "139.32 dB", "167.83 dB", "+52.78 dB"),
        ("18 km", "116.63 dB", "142.11 dB", "170.62 dB", "+53.99 dB"),
        ("20 km", "117.55 dB", "143.73 dB", "172.23 dB", "+54.68 dB"),
    ]
    for i, row_vals in enumerate(rows_data, start=1):
        for j, val in enumerate(row_vals):
            cell = res_tbl.cell(i, j)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if i % 2 == 1:
                set_cell_bg(cell, "F3F4EF")

    graph_path = ROOT_DIR / "path_loss_graph.png"
    if graph_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(graph_path), width=Inches(5.7))
        cap = doc.add_paragraph(
            "Figure 1: Path Loss vs Distance (f = 900 MHz, h_te = 30 m, h_re = 1.5 m) comparing Free Space, Okumura, and Hata Urban."
        )
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].font.italic = True
        cap.runs[0].font.size = Pt(9.5)

    # ---------------------------------------------------------
    # 5. ENGINEERING INTERPRETATION & RECOMMENDATIONS
    # ---------------------------------------------------------
    add_styled_heading(doc, "5. Case Study Analysis & RF Design Conclusions", level=1)
    findings = [
        "1. Free Space Represents a Strict Lower Bound: With 91.52 dB at 1 km and 117.55 dB at 20 km, Free Space "
        "assumes a vacuum with zero obstacles. Using it for urban cell sizing leads to catastrophic coverage holes.",
        "2. Dramatic 54.68 dB Urban Clutter Penalty: At the 20 km boundary, Hata Urban predicts 172.23 dB — "
        "54.68 dB higher attenuation than Free Space (nearly 294,000x weaker linear received power).",
        "3. Link Budget Coverage Impact: For our scenario (EIRP = 58 dBm, Rx sensitivity = -100 dBm, Lsys = 3 dB), "
        "Maximum Allowable Path Loss is 155 dB. Free Space falsely predicts > 20 km coverage, whereas Hata Urban "
        "reveals actual reliable urban coverage drops below threshold around ~6.5 km.",
        "4. Recommendation: Urban and suburban macrocell RF planning must rely on Hata / COST-231 Hata models "
        "paired with a Log-Normal Shadowing fade margin (typically >= 11.8 dB for 95% reliability at sigma = 6 dB).",
    ]
    for f_txt in findings:
        p = doc.add_paragraph(f_txt)
        p.paragraph_format.space_after = Pt(5)

    # ---------------------------------------------------------
    # 6. REFERENCES
    # ---------------------------------------------------------
    add_styled_heading(doc, "6. Academic References", level=1)
    refs = [
        "[1] T. S. Rappaport, Wireless Communications: Principles and Practice, 2nd ed. Prentice Hall, 2002.",
        "[2] Y. Okumura et al., 'Field strength and its variability in VHF and UHF land-mobile radio service,' Rev. Elec. Commun. Lab., vol. 16, pp. 825-873, 1968.",
        "[3] M. Hata, 'Empirical formula for propagation loss in land mobile radio services,' IEEE Trans. Veh. Technol., vol. VT-29, no. 3, pp. 317-325, Aug. 1980.",
    ]
    for r in refs:
        p = doc.add_paragraph(r)
        p.runs[0].font.size = Pt(10)

    out_path = ROOT_DIR / "Case_Study_Document.docx"
    doc.save(out_path)
    print(f"[+] Case Study Document generated at: {out_path}")


if __name__ == "__main__":
    build_case_study()
