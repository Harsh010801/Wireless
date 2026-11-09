"""
Tests for comparative analysis and sensitivity analysis modules.
"""

import pytest
import numpy as np

from propagation.analysis.comparator import ModelComparator, FORMAL_MODEL_COMPARISON
from propagation.analysis.sensitivity import SensitivityAnalyzer
from propagation.simulation.scenario import ScenarioConfig
from propagation.simulation.engine import SimulationEngine


class TestAnalysis:
    """Test suite for comparative analysis."""

    def test_formal_comparison_table(self):
        df = ModelComparator.get_comparison_table()
        assert len(df) == 7
        assert "Model" in df.columns
        assert "Main Advantage" in df.columns
        assert "Main Limitation" in df.columns

    def test_pairwise_differences_and_stats(self):
        cfg = ScenarioConfig.from_yaml("experiments/scenarios/urban.yaml")
        cfg.num_distance_points = 20
        engine = SimulationEngine()
        sim_res = engine.run_distance_sweep(cfg)

        diff_df = ModelComparator.calculate_pairwise_differences(sim_res, baseline_model="fspl")
        assert "Delta_PL_hata_vs_fspl_dB" in diff_df.columns
        # Urban Hata path loss must exceed Free Space
        assert np.all(diff_df["Delta_PL_hata_vs_fspl_dB"] > 0)

        stats_df = ModelComparator.calculate_summary_statistics(sim_res)
        assert len(stats_df) == len(cfg.models)
        assert "Mean Path Loss (dB)" in stats_df.columns

    def test_sensitivity_sweeps(self):
        df_ht = SensitivityAnalyzer.sweep_tx_antenna_height(
            min_ht_m=30.0, max_ht_m=100.0, num_points=10, distance_km=5.0
        )
        assert len(df_ht) == 10
        # Increasing transmitter height should decrease path loss
        assert df_ht["PL_Hata_dB"].iloc[-1] < df_ht["PL_Hata_dB"].iloc[0]

        D, F, PL = SensitivityAnalyzer.generate_2d_heatmap_grid(
            distances_km=np.linspace(1, 5, 5), frequencies_mhz=np.linspace(1500, 1800, 4)
        )
        assert D.shape == (4, 5)
        assert PL.shape == (4, 5)

