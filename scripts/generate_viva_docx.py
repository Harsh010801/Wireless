"""
Generates a comprehensive, cleanly styled Word Document:
Viva_Questions_and_Explanations.docx
Contains 20 viva questions organized across 4 sections with spoken answers + deep explanations.
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


def set_paragraph_shading(paragraph, fill_hex: str):
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    p_pr.append(shd)


def add_section_header(doc: Document, title: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    set_paragraph_shading(p, "134729")
    run = p.add_run(f"  {title}")
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)


def add_viva_qa(doc: Document, q_num: int, question: str, spoken_answer: str, explanation: str):
    # Question Heading
    qp = doc.add_paragraph()
    qp.paragraph_format.space_before = Pt(10)
    qp.paragraph_format.space_after = Pt(3)
    q_run = qp.add_run(f"Q{q_num}. {question}")
    q_run.font.name = "Calibri"
    q_run.font.size = Pt(11.5)
    q_run.font.bold = True
    q_run.font.color.rgb = RGBColor(19, 71, 41)

    # Spoken Answer
    ap = doc.add_paragraph()
    ap.paragraph_format.space_after = Pt(4)
    lbl = ap.add_run("Quick Spoken Answer: ")
    lbl.font.name = "Calibri"
    lbl.font.size = Pt(10.5)
    lbl.font.bold = True
    lbl.font.color.rgb = RGBColor(17, 24, 39)

    ans = ap.add_run(spoken_answer)
    ans.font.name = "Calibri"
    ans.font.size = Pt(10.5)
    ans.font.color.rgb = RGBColor(31, 41, 55)

    # Detailed Explanation Card
    ep = doc.add_paragraph()
    ep.paragraph_format.left_indent = Inches(0.2)
    ep.paragraph_format.right_indent = Inches(0.15)
    ep.paragraph_format.space_after = Pt(8)
    set_paragraph_shading(ep, "F3F4EF")

    elbl = ep.add_run("Detailed Explanation & Proof: ")
    elbl.font.name = "Calibri"
    elbl.font.size = Pt(10)
    elbl.font.bold = True
    elbl.font.color.rgb = RGBColor(88, 125, 30)

    etxt = ep.add_run(explanation)
    etxt.font.name = "Calibri"
    etxt.font.size = Pt(10)
    etxt.font.color.rgb = RGBColor(55, 65, 81)


def build_viva_doc():
    doc = Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.85)
        sec.bottom_margin = Inches(0.85)
        sec.left_margin = Inches(0.9)
        sec.right_margin = Inches(0.9)

    # Title Banner
    tp = doc.add_paragraph()
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tp.paragraph_format.space_before = Pt(12)
    tr = tp.add_run("VIVA VOCE & ORAL DEFENSE GUIDE")
    tr.font.name = "Calibri"
    tr.font.size = Pt(22)
    tr.font.bold = True
    tr.font.color.rgb = RGBColor(19, 71, 41)

    sp = doc.add_paragraph()
    sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sp.paragraph_format.space_after = Pt(14)
    sr = sp.add_run(
        "Project: Comparative Analysis of Wireless Signal Propagation Models\n"
        "(Free Space, Okumura, Hata, COST-231, Two-Ray & Log-Normal Shadowing)\n"
        "20 Project-Specific Questions with Ready-to-Speak Answers & Technical Explanations"
    )
    sr.font.name = "Calibri"
    sr.font.size = Pt(11)
    sr.font.italic = True
    sr.font.color.rgb = RGBColor(75, 85, 99)

    # Team Table
    tbl = doc.add_table(rows=4, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(("Project Team Member", "Registration Number")):
        c = tbl.cell(0, j)
        c.paragraphs[0].text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(10)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_bg(c, "134729")

    for i, (name, reg) in enumerate(
        [
            ("Harsh Yadav", "RA2311003011546"),
            ("Utkarsh Dabas", "RA2311003011550"),
            ("Tamanna Singh", "RA2311003011570"),
        ],
        start=1,
    ):
        for j, val in enumerate((name, reg)):
            c = tbl.cell(i, j)
            c.paragraphs[0].text = val
            c.paragraphs[0].runs[0].font.size = Pt(10)
            if i % 2 == 1:
                set_cell_bg(c, "F3F4EF")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==============================================================
    # SECTION A
    # ==============================================================
    add_section_header(doc, "SECTION A: CORE CONCEPTS & MODEL FUNDAMENTALS (Q1 – Q6)")

    add_viva_qa(
        doc, 1,
        "What is Path Loss, and why is it crucial in wireless communication design?",
        "Path loss (PL) is the reduction in signal power density as an electromagnetic wave travels from a transmitter to a receiver. It determines the maximum cell coverage radius, required tower transmit power, and handover boundaries.",
        "Mathematically, PL(dB) = 10 * log10(Pt / Pr). Without accurate path loss estimation before installing towers, underestimating loss causes dead zones and dropped calls, while overestimating wastes capital expenditure (CAPEX) by building unnecessary base stations."
    )

    add_viva_qa(
        doc, 2,
        "Why is the Free Space Path Loss (FSPL) model considered an optimistic lower bound?",
        "FSPL assumes a pure vacuum with 100% unobstructed Line-of-Sight (LOS), ignoring buildings, trees, ground reflection, and atmospheric absorption. Therefore, it always predicts the lowest possible signal loss (highest received power).",
        "Under Friis' formula, PL_FSPL(dB) = 20*log10(d) + 20*log10(f) + 32.44 (d in km, f in MHz), which decays gently at n = 2 (20 dB/decade). Real urban environments suffer diffraction and clutter, raising the effective exponent to n = 3.5 to 4.5. In our 900 MHz simulation at 20 km, FSPL predicts 117.55 dB whereas real Hata Urban predicts 172.23 dB — a 54.68 dB optimism error."
    )

    add_viva_qa(
        doc, 3,
        "What is the fundamental difference between Theoretical, Empirical, and Stochastic models?",
        "Theoretical models (Free Space, Two-Ray) come directly from electromagnetic physics laws; Empirical models (Okumura, Hata, COST-231) come from curve-fitting real city field measurements; Stochastic models (Log-Normal Shadowing) treat clutter blockage as a random Gaussian variable.",
        "Theoretical models need zero city tuning but fail when obstacles appear. Empirical models accurately predict real city clutter attenuation inside their calibrated bounds (e.g., 150-1500 MHz for Hata). Stochastic models go one step further by computing link outage probability (%) across random terrain."
    )

    add_viva_qa(
        doc, 4,
        "What is the difference between the Okumura (1968) and Hata (1980) models?",
        "Okumura collected physical drive-test data in Tokyo and published graphical lookup charts (nomograms), which were slow and hard to program. Masaharu Hata converted Okumura's graphs into closed-form algebraic equations so RF engineers could run computer simulations.",
        "Okumura computes loss using graphical curves A_mu(f,d), G(hte), G(hre), and G_area. Hata fitted parametric log equations directly to those curves for Urban, Suburban, and Rural environments with near-identical accuracy."
    )

    add_viva_qa(
        doc, 5,
        "What are the valid operating parameter ranges of the Hata model?",
        "The standard Okumura-Hata model is strictly calibrated for: Carrier Frequency 150 to 1500 MHz, Base Station Height 30 to 200 m, Mobile Height 1 to 10 m, and Distance 1 to 20 km.",
        "In our Python framework (src/propagation/models/hata.py), passing parameters outside these bounds automatically emits a ModelRangeWarning instead of silently misleading the user. For frequencies between 1500 and 2000 MHz, our system switches to COST-231 Hata."
    )

    add_viva_qa(
        doc, 6,
        "Why was the COST-231 Hata model created?",
        "Original Hata stopped at 1500 MHz, which could not cover 1800 MHz / 1900 MHz 2G DCS and PCS cellular networks. The European COST-231 committee extended Hata's equations from 1500 MHz up to 2000 MHz.",
        "COST-231 modifies the frequency constant to 46.3 + 33.9*log10(f) and adds a metropolitan environment offset C_M (0 dB for medium cities/suburban areas, +3 dB for dense metropolitan centers)."
    )

    # ==============================================================
    # SECTION B
    # ==============================================================
    add_section_header(doc, "SECTION B: PHYSICS, FORMULAS & LINK BUDGETING (Q7 – Q12)")

    add_viva_qa(
        doc, 7,
        "How does carrier frequency affect path loss?",
        "Higher frequency always produces higher path loss. Doubling frequency increases Free Space loss by roughly 6 dB, and increases Hata Urban loss by almost 8 dB.",
        "In Free Space, receive antenna effective aperture is A_e = lambda^2 / (4*pi) = c^2 / (4*pi*f^2), giving a 20*log10(f) loss dependence. In Hata Urban, the coefficient rises to 26.16*log10(f) because shorter wavelengths diffract poorly over concrete rooftops and suffer stronger foliage/wall absorption."
    )

    add_viva_qa(
        doc, 8,
        "What is the significance of the mobile antenna height correction factor a(h_re) in Hata?",
        "a(h_re) corrects path loss for the clutter surrounding a street-level user terminal. Raising the mobile device above ground obstacles reduces local scattering and lowers total path loss.",
        "For medium cities: a(h_re) = (1.1*log10(f) - 0.7)*h_re - (1.56*log10(f) - 0.8). At our benchmark f = 900 MHz and h_re = 1.5 m, a(h_re) evaluates to approximately 0.00 dB. Because a(h_re) is subtracted in the Hata equation, taller vehicular antennas (h_re = 3 m) gain positive dB reduction."
    )

    add_viva_qa(
        doc, 9,
        "Why does the Two-Ray Ground Reflection model decay at 40 dB/decade instead of 20 dB/decade?",
        "At large distances, the direct ray and the ground-reflected ray have nearly equal lengths, and ground reflection flips the reflected wave's phase by 180 degrees. Their fields partially cancel each other out, causing power to fall much faster as 1/d^4 (40 dB/decade).",
        "Beyond the crossover distance d_c = (4*pi*h_t*h_r) / lambda, path length difference delta_d = (2*h_t*h_r)/d becomes tiny relative to wavelength, while grazing angle reflection coefficient approaches -1. Summing E_total results in amplitude ~ 1/d^2, so received power P_r ~ |E|^2 ~ 1/d^4 (-40*log10(d))."
    )

    add_viva_qa(
        doc, 10,
        "If base station tower height doubles from 30 m to 60 m, how does path loss change in Hata?",
        "Doubling the tower height reduces urban path loss by approximately 6.13 dB at 10 km — effectively quadrupling the received signal power and significantly expanding cell radius.",
        "In Hata's equation, h_te appears in two terms: -13.82*log10(h_te) and -6.55*log10(h_te)*log10(d). Since log10(2) = 0.3010, doubling h_te yields -13.82*(0.3010) = -4.16 dB from the constant term and -6.55*(0.3010)*log10(10) = -1.97 dB from the slope term at 10 km, totaling -6.13 dB improvement."
    )

    add_viva_qa(
        doc, 11,
        "What is Log-Normal Shadowing, and how is Fade Margin computed for 95% reliability?",
        "Shadowing (slow fading) models random dB variations around median path loss due to unpredictable large obstructions like skyscrapers or hills. To achieve 95% reliability, engineers allocate a Fade Margin proportional to standard deviation sigma.",
        "PL(d) = PL(d0) + 10*n*log10(d/d0) + X_sigma, where X_sigma ~ Normal(0, sigma^2). Received power in Watts is log-normal, so in dB it is Normal (Gaussian). Using normal CDF tables, 95% reliability requires z * sigma = 1.645 * sigma (one-tailed) or 1.96 * sigma (two-tailed; e.g., 1.96 * 6 dB = 11.76 dB extra buffer above Rx sensitivity)."
    )

    add_viva_qa(
        doc, 12,
        "What is EIRP, and how do you calculate Link Budget Fade Margin?",
        "EIRP (Effective Isotropic Radiated Power) is the total equivalent power radiated in the antenna's peak beam: EIRP = Transmit Power Pt + Antenna Gain Gt. Fade Margin is how much surplus power remains above the mobile phone's minimum sensitivity.",
        "In our project dashboard (Link Budget tab): P_r(dBm) = Pt(43 dBm) + Gt(15 dBi) + Gr(0 dBi) - PathLoss(dB) - SystemLoss(3 dB). Note EIRP = 58 dBm. Fade Margin = P_r - Rx_Sensitivity(-100 dBm). If Fade Margin > 0, the link works; if <= 0, the phone drops the call."
    )

    # ==============================================================
    # SECTION C
    # ==============================================================
    add_section_header(doc, "SECTION C: SIMULATION RESULTS, MATLAB & LIMITATIONS (Q13 – Q17)")

    add_viva_qa(
        doc, 13,
        "What are your exact simulation readings at 900 MHz (1 km & 20 km), and what is the Reality Gap?",
        "At 1 km: Free Space = 91.52 dB, Okumura Open = 97.90 dB, Hata Urban = 126.40 dB. At 20 km: Free Space = 117.55 dB, Okumura Open = 143.73 dB, Hata Urban = 172.23 dB.",
        "Notice the divergence ('Reality Gap') between Hata Urban and Free Space grows from +34.88 dB at 1 km to +54.68 dB at 20 km. In linear power units, 10^(54.68/10) equals 293,765 times more signal power attenuation in a city than Free Space theory predicts."
    )

    add_viva_qa(
        doc, 14,
        "When should an engineer pick Okumura Open Area instead of Hata Urban?",
        "Select Okumura Open Area for rural farmlands, open deserts, coastal highways, or unpopulated plains where there are no dense multi-story concrete buildings within 300–400 meters of the signal corridor.",
        "Via Hata's open-area empirical adjustment: Correction = -4.78*(log10(f))^2 + 18.33*log10(f) - 40.94. At f = 900 MHz, Correction = -28.50 dB, meaning rural open terrain suffers 28.5 dB less path loss than urban cores."
    )

    add_viva_qa(
        doc, 15,
        "How does your MATLAB code (path_loss_simulation.m) compute all 20 distances simultaneously?",
        "Instead of slow loops, we used MATLAB vectorized array operations: defining distance as a row vector d = 1:20 and applying element-wise log10(d) and .* multiplication.",
        "Key lines from path_loss_simulation.m: fspl = 20*log10(d) + 20*log10(f) + 32.44; hata_urban = 69.55 + 26.16*log10(f) - 13.82*log10(h_te) - a_hre + (44.9 - 6.55*log10(h_te)).*log10(d); okumura = hata_urban + correction. We also created path_loss_animation.m using animatedline and drawnow for live curve tracing."
    )

    add_viva_qa(
        doc, 16,
        "Why cannot Hata or COST-231 be used for 5G networks at 3.5 GHz or 28 GHz mmWave?",
        "Two critical failures occur: first, 3.5 GHz and 28 GHz are far outside Hata's 1.5 GHz and COST-231's 2.0 GHz ceiling; second, 5G uses street-level small cells (< 500 m radius, height < 15 m), violating Hata's macrocell tower assumptions.",
        "At 28 GHz mmWave, diffraction around building corners becomes negligible, atmospheric oxygen/rain attenuation rises sharply, and building glass blocks 25–40 dB. 5G requires 3GPP TR 38.901 stochastic channel models or 3D ray-tracing."
    )

    add_viva_qa(
        doc, 17,
        "What is the difference between Large-Scale Path Loss and Small-Scale Multipath Fading?",
        "Large-scale models (Free Space, Okumura, Hata, Shadowing) predict average signal drop over hundreds of meters or kilometers to determine tower coverage. Small-scale fading models rapid wave interference over centimeters (half-wavelengths).",
        "Our project focuses on Large-Scale Propagation Models used for macrocell link budgets and tower placement. Small-scale fading causes deep momentary notches every few centimeters due to Doppler shift and multipath phase shifts, handled via Rayleigh/Rician distributions and MIMO diversity."
    )

    # ==============================================================
    # SECTION D
    # ==============================================================
    add_section_header(doc, "SECTION D: SOFTWARE ARCHITECTURE & WEB APP DEFENSE (Q18 – Q20)")

    add_viva_qa(
        doc, 18,
        "Why did you structure the web platform with separate frontend/ (React) and backend/ (FastAPI) folders?",
        "Separating presentation (React + Vite + Tailwind + Recharts in frontend/) from scientific computation (FastAPI REST API in backend/ wrapping src/propagation/) ensures clean architecture, single source of truth for formulas, and zero code duplication.",
        "Every slider update in the React Simulator Studio calls POST /api/simulate, which executes the exact Python physics classes in src/propagation/models/ and returns validated JSON arrays. Our core library also powers the Case Study DOCX download endpoint (GET /api/download-case-study)."
    )

    add_viva_qa(
        doc, 19,
        "Explain your live Wavefront Motion Graphics simulator in the React UI.",
        "WaveCanvas.jsx renders an interactive HTML5 Canvas showing concentric electromagnetic pulses propagating from a base station tower past urban buildings toward a moving receiver.",
        "Blue arcs (Free Space) reach farthest, Lime arcs (Okumura Open) reach medium distance, and Red arcs (Hata Urban) shrink earliest due to building clutter attenuation. Changing frequency or tower height dynamically updates both the visual wave decay and the real-time dB counters below the canvas."
    )

    add_viva_qa(
        doc, 20,
        "How did you verify that all mathematical formulas and unit conversions in your codebase are error-free?",
        "We built an automated test suite of 32 unit tests using pytest covering unit conversions, Friis benchmarks, Two-Ray crossover slopes, Hata environmental ordering, COST-231 offsets, and reproducible seeded shadowing.",
        "Running 'python -m pytest tests/' passes all 32/32 tests in ~1 second. Additionally, the MATLAB outputs (91.52 dB, 97.90 dB, 126.40 dB at 1 km; 117.55 dB, 143.73 dB, 172.23 dB at 20 km) match the Python engine to 2 decimal places."
    )

    out_path = ROOT_DIR / "Viva_Questions_and_Explanations.docx"
    doc.save(out_path)
    print(f"[+] Viva Document successfully generated at: {out_path}")


if __name__ == "__main__":
    build_viva_doc()
