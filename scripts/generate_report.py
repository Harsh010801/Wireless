"""
Hard-Copy PDF & Markdown Research Report Generator.

Compiles numerical simulation findings, comparison tables, and high-resolution
figures into an academic research report in PDF format (outputs/reports/).
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from propagation.analysis.comparator import ModelComparator, FORMAL_MODEL_COMPARISON
from propagation.simulation.scenario import ScenarioConfig
from propagation.simulation.engine import SimulationEngine


def generate_pdf_report(output_pdf_path: Path):
    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1a365d"),
        alignment=1,
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#4a5568"),
        alignment=1,
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2b6cb0"),
        spaceAfter=8,
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=6,
    )
    cell_style = ParagraphStyle(
        "Cell_Custom",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1a202c"),
    )
    cell_bold_style = ParagraphStyle(
        "CellBold_Custom",
        parent=cell_style,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#ffffff"),
    )

    story = []

    # Title & Header
    story.append(Paragraph("Comparative Analysis of Wireless Signal Propagation Models", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A Rigorous Academic Evaluation of Theoretical, Empirical, and Stochastic Channel Models", subtitle_style))
    story.append(Paragraph("<b>Project Team:</b> Harsh Yadav (RA2311003011546), Utkarsh Dabas (RA2311003011550), Tamanna Singh (RA2311003011570)", subtitle_style))
    story.append(Paragraph("<b>Department:</b> Electronics & Communication Engineering &nbsp;|&nbsp; <b>Academic Year:</b> 2025–2026", subtitle_style))
    story.append(Spacer(1, 14))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    exec_summary_text = (
        "This research report presents an end-to-end comparative investigation into wireless signal "
        "propagation models spanning Friis Free Space, Two-Ray Ground Reflection, Log-Distance Path Loss, "
        "Okumura, Okumura-Hata, COST-231 Hata, and Log-Normal Shadow Fading. The simulation evaluates "
        "path loss, received power, link margins, and spatial variability across carrier frequencies "
        "from 150 MHz to 3.5 GHz and transmission distances from 1 meter to 20 kilometers under urban, "
        "suburban, rural, and indoor propagation environments."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 10))

    # Formal Model Comparison Table
    story.append(Paragraph("2. Model Taxonomy and Architectural Comparison", h1_style))
    raw_comp = ModelComparator.get_comparison_table()

    table_data = [[
        Paragraph("<b>Model</b>", cell_bold_style),
        Paragraph("<b>Type</b>", cell_bold_style),
        Paragraph("<b>Valid Freq</b>", cell_bold_style),
        Paragraph("<b>Valid Dist</b>", cell_bold_style),
        Paragraph("<b>Primary Advantage</b>", cell_bold_style),
        Paragraph("<b>Main Limitation</b>", cell_bold_style),
    ]]

    for _, row in raw_comp.iterrows():
        table_data.append([
            Paragraph(row["Model"], cell_style),
            Paragraph(row["Classification"], cell_style),
            Paragraph(row["Frequency Range"], cell_style),
            Paragraph(row["Distance Range"], cell_style),
            Paragraph(row["Main Advantage"], cell_style),
            Paragraph(row["Main Limitation"], cell_style),
        ])

    t = Table(table_data, colWidths=[1.1*inch, 1.0*inch, 1.1*inch, 1.1*inch, 1.6*inch, 1.6*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2b6cb0")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Numerical Simulation Findings (Urban Scenario B)
    story.append(Paragraph("3. Numerical Simulation Results (Urban Macrocell Scenario)", h1_style))
    urban_cfg = ScenarioConfig.from_yaml(ROOT_DIR / "experiments" / "scenarios" / "urban.yaml")
    engine = SimulationEngine()
    sim_res = engine.run_distance_sweep(urban_cfg)
    stats_df = ModelComparator.calculate_summary_statistics(sim_res)

    stat_table_data = [[
        Paragraph("<b>Model Identifier</b>", cell_bold_style),
        Paragraph("<b>Min PL (dB)</b>", cell_bold_style),
        Paragraph("<b>Max PL (dB)</b>", cell_bold_style),
        Paragraph("<b>Mean PL (dB)</b>", cell_bold_style),
        Paragraph("<b>Median PL (dB)</b>", cell_bold_style),
        Paragraph("<b>Min Rx Power (dBm)</b>", cell_bold_style),
        Paragraph("<b>Max Rx Power (dBm)</b>", cell_bold_style),
    ]]

    for _, row in stats_df.iterrows():
        stat_table_data.append([
            Paragraph(f"<b>{row['Model']}</b>", cell_style),
            Paragraph(f"{row['Min Path Loss (dB)']:.1f}", cell_style),
            Paragraph(f"{row['Max Path Loss (dB)']:.1f}", cell_style),
            Paragraph(f"{row['Mean Path Loss (dB)']:.1f}", cell_style),
            Paragraph(f"{row['Median Path Loss (dB)']:.1f}", cell_style),
            Paragraph(f"{row['Min Rx Power (dBm)']:.1f}", cell_style),
            Paragraph(f"{row['Max Rx Power (dBm)']:.1f}", cell_style),
        ])

    st = Table(stat_table_data, colWidths=[1.4*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.1*inch, 1.0*inch])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2d3748")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#edf2f7")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(st)
    story.append(Spacer(1, 14))

    # Page Break for Figures
    story.append(PageBreak())

    # Key Graphical Results
    story.append(Paragraph("4. Graphical Simulation Findings & Comparative Curves", h1_style))
    fig_dir = ROOT_DIR / "outputs" / "figures"

    # Embedding Fig 1 and Fig 2
    if (fig_dir / "fig01_path_loss_vs_distance.png").exists():
        story.append(Paragraph("<b>Figure 1:</b> Path Loss vs Distance across all models (Urban Scenario B, 1800 MHz)", h2_style))
        story.append(Image(str(fig_dir / "fig01_path_loss_vs_distance.png"), width=6.8*inch, height=3.8*inch))
        story.append(Spacer(1, 10))

    if (fig_dir / "fig02_received_power_vs_distance.png").exists():
        story.append(Paragraph("<b>Figure 2:</b> Received Power vs Distance with link budget threshold (-100 dBm)", h2_style))
        story.append(Image(str(fig_dir / "fig02_received_power_vs_distance.png"), width=6.8*inch, height=3.8*inch))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Embedding Fig 4 and Fig 6
    if (fig_dir / "fig04_environmental_comparison.png").exists():
        story.append(Paragraph("<b>Figure 3:</b> Environmental Comparison across Urban Large, Urban Medium, Suburban, and Rural", h2_style))
        story.append(Image(str(fig_dir / "fig04_environmental_comparison.png"), width=6.8*inch, height=3.8*inch))
        story.append(Spacer(1, 10))

    if (fig_dir / "fig06_shadowing_distribution.png").exists():
        story.append(Paragraph("<b>Figure 4:</b> Log-Normal Shadow Fading Trajectories and Probability Density Function", h2_style))
        story.append(Image(str(fig_dir / "fig06_shadowing_distribution.png"), width=6.8*inch, height=3.0*inch))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Section 5: 5G/6G mmWave, 3GPP TR 38.901 & Transition Dynamics
    story.append(Paragraph("5. 5G / 6G Millimeter-Wave & Sub-THz Propagation Dynamics (2026 Standards)", h1_style))
    mmwave_text = (
        "Modern wireless communication standards (3GPP Rel-19, 6G FR3 7-24 GHz, and mmWave bands up to 100 GHz) "
        "deviate fundamentally from classical VHF/UHF models. Higher frequencies incur heightened diffraction loss, "
        "necessitating dual-slope path loss with breakpoint distance d'BP, explicit distinction between Line-of-Sight (LoS) "
        "and Non-Line-of-Sight (NLoS) channel states, and probabilistic LoS-NLoS state transition models (Inam Ullah et al., "
        "IEEE Access 2026, DOI: 10.1109/ACCESS.2026.3741615)."
    )
    story.append(Paragraph(mmwave_text, body_style))
    story.append(Spacer(1, 8))

    if (fig_dir / "fig11_mmwave_vs_classical_28ghz.png").exists():
        story.append(Paragraph("<b>Figure 5:</b> Path Loss vs. Distance at 28 GHz mmWave (Classical vs. 3GPP / CI / ABG)", h2_style))
        story.append(Image(str(fig_dir / "fig11_mmwave_vs_classical_28ghz.png"), width=6.8*inch, height=3.6*inch))
        story.append(Spacer(1, 10))

    if (fig_dir / "fig12_broadband_pl_vs_frequency.png").exists():
        story.append(Paragraph("<b>Figure 6:</b> Broadband Frequency Dependence (0.5 to 100 GHz) with Calibration Boundaries", h2_style))
        story.append(Image(str(fig_dir / "fig12_broadband_pl_vs_frequency.png"), width=6.8*inch, height=3.6*inch))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    if (fig_dir / "fig13_los_probability_and_mixture.png").exists():
        story.append(Paragraph("<b>Figure 7:</b> LoS Probability Roll-Off & Stochastic LoS-NLoS State Transitions (IEEE Access 2026)", h2_style))
        story.append(Image(str(fig_dir / "fig13_los_probability_and_mixture.png"), width=6.8*inch, height=4.2*inch))
        story.append(Spacer(1, 10))

    if (fig_dir / "fig14_benchmark_barchart_3_5ghz_and_28ghz.png").exists():
        story.append(Paragraph("<b>Figure 8:</b> Benchmark Model Path Loss at 5G Mid-Band (3.5 GHz) vs mmWave (28 GHz)", h2_style))
        story.append(Image(str(fig_dir / "fig14_benchmark_barchart_3_5ghz_and_28ghz.png"), width=6.8*inch, height=3.6*inch))
        story.append(Spacer(1, 10))

    # Key Insights & Practical Takeaways
    story.append(Paragraph("6. Critical Engineering Insights & Conclusions", h1_style))
    conclusions_text = (
        "<b>1. Model Divergence:</b> Free Space (Friis) predicts the lowest path loss (77.5 - 117.5 dB) "
        "because it ignores multipath cancellation and building clutter. COST-231 Hata and Okumura "
        "predict 30 to 45 dB higher attenuation, matching realistic cluttered urban micro/macrocells.<br/>"
        "<b>2. Distance Scaling:</b> Beyond the two-ray crossover distance dc = 4*pi*ht*hr/lambda, Two-Ray "
        "decays at 40 dB/decade (n=4), whereas cellular empirical models decay at approximately 35 dB/decade (n=3.5).<br/>"
        "<b>3. Shadowing Fading Margins:</b> Under log-normal shadowing (sigma = 6-8 dB), maintaining 95% "
        "link reliability requires an extra fade margin of at least 1.96*sigma (12 to 16 dB) above receiver sensitivity.<br/>"
        "<b>4. Failure of Classical Empirical Models at GHz:</b> Classical Hata and Okumura formulations are strictly invalid above "
        "1.5 - 2.0 GHz or below 1 km. Extrapolating them to mmWave yields erroneous path losses differing by 30-50 dB from physics.<br/>"
        "<b>5. 3GPP TR 38.901 & Close-In Models:</b> For 5G/6G deployments (0.5 to 100 GHz), 3GPP TR 38.901 and Close-In (CI) models "
        "provide physically consistent path loss predictions anchored to a 1 m free-space reference, with robust parameter stability across bands.<br/>"
        "<b>6. Stochastic LoS-NLoS Dynamics:</b> As demonstrated in Inam Ullah et al. (IEEE Access 2026), mobile corner-turning causes sharp "
        "20+ dB step-transitions, requiring beam-tracking margins and probabilistic state transition modeling."
    )
    story.append(Paragraph(conclusions_text, body_style))

    doc.build(story)
    print(f"[+] Publication PDF Report successfully generated at: {output_pdf_path}")


def main():
    print("=" * 70)
    print("  GENERATING COMPREHENSIVE HARD-COPY PDF REPORT")
    print("=" * 70)
    out_dir = ROOT_DIR / "outputs" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "Wireless_Propagation_Comparative_Report.pdf"
    generate_pdf_report(pdf_path)


if __name__ == "__main__":
    main()

