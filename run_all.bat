@echo off
TITLE Wireless Signal Propagation Framework - Automated Execution
echo ===============================================================================
echo   COMPARATIVE ANALYSIS OF WIRELESS SIGNAL PROPAGATION MODELS
echo   Team: Harsh Yadav (RA2311003011546), Utkarsh Dabas (RA2311003011550), Tamanna Singh (RA2311003011570)
echo ===============================================================================
echo.

echo [1/5] Running Automated Pytest Test Suite (32 Tests)...
python -m pytest
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Test suite failed!
    pause
    exit /b %ERRORLEVEL%
)
echo [OK] All tests passed!
echo.

echo [2/5] Running Scenario Simulations (Batch CSV Export)...
python scripts\run_simulation.py --scenario all
echo.

echo [3/5] Generating 10 Publication-Quality Figures (outputs/figures/)...
python scripts\generate_figures.py
echo.

echo [4/5] Compiling Print-Ready PDF Report (outputs/reports/ & root)...
python scripts\generate_report.py
python -c "import shutil; shutil.copy2('outputs/reports/Wireless_Propagation_Comparative_Report.pdf', 'Wireless_Propagation_Comparative_Report.pdf')"
echo.

echo [5/5] Compiling 20-Slide Master Academic PowerPoint (outputs/presentation/ & root)...
python scripts\generate_presentation.py
python -c "import shutil; shutil.copy2('outputs/presentation/Wireless_Propagation_Analysis.pptx', 'Wireless_Propagation_Analysis.pptx')"
echo.

echo ===============================================================================
echo   EXECUTION COMPLETE!
echo   - Presentation: Wireless_Propagation_Analysis.pptx
echo   - PDF Report:   Wireless_Propagation_Comparative_Report.pdf
echo   - Web App:      Run 'streamlit run app.py' to launch interactive dashboard
echo ===============================================================================
pause
