"""
Generates the formal academic Word document report (Project_Report.docx).
Course: 21CSE458T — Wireless and Mobile Communication (B.Tech CSE, 7th Semester)
"""

from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT_DIR = Path(__file__).resolve().parent.parent

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def generate_report():
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # -------------------------------------------------------------
    # TITLE PAGE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)

    title_run = title_p.add_run("COMPARATIVE ANALYSIS OF WIRELESS SIGNAL PROPAGATION MODELS\n(FREE SPACE, OKUMURA AND HATA) USING MATLAB")
    title_run.font.name = "Calibri"
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(30, 58, 138) # Deep Blue

    course_p = doc.add_paragraph()
    course_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    course_p.paragraph_format.space_after = Pt(24)
    run_course = course_p.add_run("A Case Study Mini-Project Submitted for the Course\n21CSE458T — WIRELESS AND MOBILE COMMUNICATION\nB.Tech Computer Science and Engineering (7th Semester)")
    run_course.font.name = "Calibri"
    run_course.font.size = Pt(12)
    run_course.font.italic = True
    run_course.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(24)

    # Submitted By Table / Box
    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("SUBMITTED BY:")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(15, 23, 42)

    team_p = doc.add_paragraph()
    team_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    team_p.paragraph_format.space_after = Pt(36)
    
    t1 = team_p.add_run("Harsh Yadav (Registration No: RA2311003011546)\n")
    t1.font.bold = True
    t1.font.size = Pt(11.5)
    t2 = team_p.add_run("Utkarsh Dabas (Registration No: RA2311003011550)\n")
    t2.font.bold = True
    t2.font.size = Pt(11.5)
    t3 = team_p.add_run("Tamanna Singh (Registration No: RA2311003011570)\n")
    t3.font.bold = True
    t3.font.size = Pt(11.5)

    dept_p = doc.add_paragraph()
    dept_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_dept = dept_p.add_run("Department of Computer Science and Engineering\nAcademic Year 2025–2026")
    run_dept.font.name = "Calibri"
    run_dept.font.size = Pt(11)
    run_dept.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ABSTRACT
    # -------------------------------------------------------------
    h_abs = doc.add_heading("ABSTRACT", level=1)
    h_abs.paragraph_format.space_after = Pt(8)

    p_abs = doc.add_paragraph(
        "Accurate modeling and prediction of radio signal propagation are fundamental to designing, "
        "dimensioning, and optimizing cellular wireless networks. In real-world environments, transmitted "
        "electromagnetic waves undergo distance-dependent attenuation, reflection, diffraction, and clutter absorption, "
        "collectively known as path loss. This mini-project conducts a rigorous computational and comparative case study "
        "evaluating three seminal wireless signal propagation models: the Free Space Path Loss (FSPL) model, the Okumura Model, "
        "and the Okumura-Hata Urban Model. Numerical simulations were executed over a distance range of 1 km to 20 km at a standard "
        "carrier frequency of 900 MHz (typical GSM/LTE cellular band), with a base station antenna height of 30 m and a mobile "
        "station height of 1.5 m. The simulation findings demonstrate that while the Free Space model predicts an overly optimistic "
        "path loss varying from 91.52 dB to 117.55 dB, the Hata Urban model accounts for severe structural clutter, predicting a realistic "
        "path loss ranging from 126.40 dB to 172.23 dB. The Okumura open-area model yields an intermediate path loss of 97.90 dB to 143.73 dB. "
        "This report details the mathematical formulations, numerical implementation in Python and MATLAB, comparative analysis, and "
        "practical engineering guidelines for cellular network planning."
    )
    p_abs.paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    doc.add_heading("1. INTRODUCTION", level=1)
    p_intro1 = doc.add_paragraph(
        "In wireless communications, signal propagation occurs through the Earth's atmosphere and built environments. "
        "As an electromagnetic wave radiates from a base station tower toward a user's mobile device, its power density "
        "decays significantly as a function of separation distance. This reduction in signal power density between transmitter "
        "and receiver is defined as Path Loss (PL)."
    )
    p_intro2 = doc.add_paragraph(
        "Why Propagation Models Matter:\n"
        "1. Network Dimensioning: Wireless telecommunication operators cannot perform costly, exhaustive physical drive-test "
        "measurements for every potential tower location. Reliable mathematical propagation models allow engineers to predict coverage "
        "footprints computationally.\n"
        "2. Link Budget Design: Radio link budgets depend critically on path loss calculations to allocate appropriate transmit power, "
        "determine antenna gains, and establish receiver sensitivity thresholds.\n"
        "3. Interference Management: Accurate loss prediction ensures adjacent cellular base stations provide continuous handovers "
        "without producing intolerable co-channel interference."
    )
    p_intro2.paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 2. THEORETICAL BACKGROUND
    # -------------------------------------------------------------
    doc.add_heading("2. THEORETICAL BACKGROUND & MATHEMATICAL MODELS", level=1)
    
    # 2.1 Free Space Model
    doc.add_heading("2.1 Free Space Path Loss (Friis) Model", level=2)
    doc.add_paragraph(
        "The Free Space Path Loss model represents an idealized theoretical propagation channel where the transmitter and receiver "
        "maintain an unobstructed Line-of-Sight (LOS) in an infinite, lossless dielectric medium. It assumes zero ground reflection, "
        "no atmospheric absorption, and no terrain obstacles. The received power is governed by the Friis transmission formula."
    )
    doc.add_paragraph(
        "Mathematical Equation (in dB):\n"
        "L_FSPL (dB) = 20 * log10(d) + 20 * log10(f) + 32.44\n\n"
        "Where:\n"
        "• d: Distance between transmitter and receiver in kilometers (km)\n"
        "• f: Carrier frequency in Megahertz (MHz)\n"
        "• 32.44: Wavelength constant derived from 20 * log10(4 * pi / c) with units in km and MHz."
    )

    # 2.2 Okumura Model
    doc.add_heading("2.2 Okumura Model", level=2)
    doc.add_paragraph(
        "The Okumura model is one of the most widely cited classical empirical models for cellular radio propagation. "
        "Developed by Yoshihisa Okumura in 1968, it is based on extensive field measurements conducted in Tokyo, Japan, across frequencies "
        "from 150 MHz to 1920 MHz and distances from 1 km to 100 km. It incorporates empirical correction factors for base station antenna "
        "height, mobile antenna height, and terrain clutter."
    )
    doc.add_paragraph(
        "Mathematical Formulation:\n"
        "L (dB) = L_FSL + A_mu(f, d) - G(h_te) - G(h_re) - G_area\n\n"
        "For an open/rural area, standard empirical formulations apply a terrain correction factor relative to urban baseline:\n"
        "Correction (dB) = -4.78 * (log10(f))^2 + 18.33 * log10(f) - 40.94\n"
        "L_Okumura = L_Hata_Urban + Correction"
    )

    # 2.3 Hata Urban Model
    doc.add_heading("2.3 Okumura-Hata Urban Model", level=2)
    doc.add_paragraph(
        "Although the Okumura model provided high real-world accuracy, its reliance on graphical charts made automated simulation "
        "cumbersome. In 1980, Masaharu Hata formulated closed-form parametric equations that fitted Okumura's graphical curves. "
        "The Hata model is valid for carrier frequencies from 150 MHz to 1500 MHz, tower heights from 30 m to 200 m, mobile heights "
        "from 1 m to 10 m, and distances from 1 km to 20 km."
    )
    doc.add_paragraph(
        "Mathematical Formulation (Urban Medium/Small City):\n"
        "a(h_re) = (1.1 * log10(f) - 0.7) * h_re - (1.56 * log10(f) - 0.8)\n"
        "L_Hata (dB) = 69.55 + 26.16 * log10(f) - 13.82 * log10(h_te) - a(h_re) + [44.9 - 6.55 * log10(h_te)] * log10(d)\n\n"
        "Where:\n"
        "• f: Frequency in MHz (900 MHz)\n"
        "• h_te: Base station antenna height in meters (30 m)\n"
        "• h_re: Mobile station antenna height in meters (1.5 m)\n"
        "• a(h_re): Mobile antenna height correction factor (dB)\n"
        "• d: Link distance in kilometers (1 to 20 km)"
    )

    # -------------------------------------------------------------
    # 3. METHODOLOGY
    # -------------------------------------------------------------
    doc.add_heading("3. SIMULATION METHODOLOGY & PARAMETERS", level=1)
    doc.add_paragraph(
        "The comparative simulation study was performed programmatically using Python (NumPy and Matplotlib) and MATLAB. "
        "The simulation workflow followed four structured steps:\n"
        "1. Parameter Initialization: Defined carrier frequency f = 900 MHz, tower antenna height h_te = 30 m, mobile antenna height h_re = 1.5 m, "
        "and link distance vector d ranging discretely from 1 km to 20 km in steps of 1 km.\n"
        "2. Path Loss Computation: Concurrently computed path loss vectors for Free Space, Okumura (open area), and Hata Urban models.\n"
        "3. Tabular Evaluation: Printed discrete readings at benchmark points (1 km, 5 km, 10 km, 15 km, 20 km).\n"
        "4. Graphical Rendering: Generated comparative plots on a unified coordinate frame with clear legends, gridlines, and markers."
    )

    # Simulation Parameter Table
    table = doc.add_table(rows=5, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Parameter Name", "Symbol & Units", "Assigned Value"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    params = [
        ("Carrier Frequency", "f (MHz)", "900 MHz"),
        ("Base Station Tower Height", "h_te (m)", "30 meters"),
        ("Mobile Station Antenna Height", "h_re (m)", "1.5 meters"),
        ("Distance Range", "d (km)", "1 km to 20 km (step 1 km)"),
    ]
    for i, row in enumerate(params, start=1):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.paragraphs[0].text = val
            if i % 2 == 1:
                set_cell_background(cell, "F1F5F9")

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 4. RESULTS
    # -------------------------------------------------------------
    doc.add_heading("4. SIMULATION RESULTS", level=1)
    doc.add_paragraph(
        "The numerical outputs computed across the 1 km to 20 km distance vector are tabulated below. "
        "The graph illustrating the three comparative attenuation curves is embedded in Figure 1."
    )

    # Embedded Graph
    graph_path = ROOT_DIR / "path_loss_graph.png"
    if graph_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(graph_path), width=Inches(5.8))
        caption = doc.add_paragraph("Figure 1: Comparative Plot of Path Loss vs Distance for Free Space, Okumura, and Hata Models (f = 900 MHz).")
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption.paragraph_format.space_after = Pt(12)

    # Results Table
    doc.add_heading("Numerical Readings Table (1 km to 20 km)", level=2)
    res_table = doc.add_table(rows=8, cols=4)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["Distance (km)", "Free Space (dB)", "Okumura (dB)", "Hata Urban (dB)"]
    for j, h in enumerate(r_headers):
        cell = res_table.cell(0, j)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "1E3A8A")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    sample_readings = [
        ("1 km (Cell Center)", "91.52 dB", "97.90 dB", "126.40 dB"),
        ("3 km", "101.07 dB", "114.70 dB", "143.21 dB"),
        ("5 km", "105.50 dB", "122.52 dB", "151.02 dB"),
        ("10 km", "111.52 dB", "133.12 dB", "161.63 dB"),
        ("15 km", "115.05 dB", "139.32 dB", "167.83 dB"),
        ("18 km", "116.63 dB", "142.11 dB", "170.62 dB"),
        ("20 km (Cell Edge)", "117.55 dB", "143.73 dB", "172.23 dB"),
    ]
    for i, row in enumerate(sample_readings, start=1):
        for j, val in enumerate(row):
            cell = res_table.cell(i, j)
            cell.paragraphs[0].text = val
            if i % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 5. ANALYSIS & CONCLUSION
    # -------------------------------------------------------------
    doc.add_heading("5. COMPARATIVE ANALYSIS & CONCLUSION", level=1)
    doc.add_paragraph(
        "Analysis of Simulation Findings:\n"
        "1. Free Space Path Loss (Optimistic Baseline): Free Space yields the absolute lowest path loss across all distances "
        "(91.52 dB at 1 km and 117.55 dB at 20 km). It assumes an impossible vacuum without ground multipath or building absorption. "
        "Consequently, relying on Free Space for cellular planning would drastically underestimate required transmit power.\n\n"
        "2. Okumura Model (Open Area Benchmark): The Okumura open-area curve predicts 97.90 dB at 1 km and 143.73 dB at 20 km. "
        "It provides approximately 6 to 26 dB higher loss than Free Space due to atmospheric and terrain ground reflection.\n\n"
        "3. Hata Urban Model (Realistic Planning Standard): The Hata urban model predicts the highest loss (126.40 dB at 1 km and "
        "172.23 dB at 20 km). At 20 km, Hata predicts 54.68 dB more attenuation than Free Space. This significant excess loss "
        "accurately captures the real-world impact of urban clutter, multi-building diffraction, and street canyon absorption.\n\n"
        "Conclusion: For practical cellular radio network engineering, the Okumura-Hata Urban model is the most dependable "
        "and realistic design standard, whereas Free Space serves strictly as an unattainable theoretical baseline."
    )

    # -------------------------------------------------------------
    # 6. FUTURE SCOPE
    # -------------------------------------------------------------
    doc.add_heading("6. FUTURE SCOPE", level=1)
    doc.add_paragraph(
        "Possible future extensions to this case study include:\n"
        "• High-Frequency Sub-6 GHz and mmWave Models: Evaluating 3GPP TR 38.901 channel models for 5G NR (3.5 GHz and 28 GHz).\n"
        "• 3D Ray-Tracing Simulation: Incorporating GIS building polygons and Digital Elevation Models (DEM) using tools like Wireless InSite.\n"
        "• Machine Learning Integration: Training neural network regressors on actual drive-test measurements to dynamically adjust empirical path loss exponents."
    )

    # -------------------------------------------------------------
    # 7. REFERENCES
    # -------------------------------------------------------------
    doc.add_heading("7. REFERENCES", level=1)
    doc.add_paragraph(
        "[1] T. S. Rappaport, Wireless Communications: Principles and Practice, 2nd ed. Upper Saddle River, NJ: Prentice Hall, 2002.\n"
        "[2] Y. Okumura, E. Ohmori, T. Kawano, and K. Fukuda, \"Field strength and its variability in VHF and UHF land-mobile radio service,\" "
        "Review of the Electrical Communication Laboratory, vol. 16, no. 9-10, pp. 825–873, Sep.–Oct. 1968.\n"
        "[3] M. Hata, \"Empirical formula for propagation loss in land mobile radio services,\" IEEE Transactions on Vehicular Technology, "
        "vol. VT-29, no. 3, pp. 317–325, Aug. 1980.\n"
        "[4] A. Goldsmith, Wireless Communications. Cambridge, UK: Cambridge University Press, 2005."
    )

    out_file = ROOT_DIR / "Project_Report.docx"
    doc.save(str(out_file))
    print(f"[+] Project Report successfully generated at: {out_file}")

if __name__ == "__main__":
    generate_report()
