"""
Tests for simulation scenario loading and simulation engine execution.
"""

from pathlib import Path
import pytest
import numpy as np

from propagation.simulation.scenario import ScenarioConfig
from propagation.simulation.engine import SimulationEngine


class TestSimulation:
    """Test suite for simulation scenarios and sweep engine."""

    def test_load_all_yaml_scenarios(self):
        scenario_dir = Path("experiments/scenarios")
        yaml_files = list(scenario_dir.glob("*.yaml"))
        assert len(yaml_files) >= 5, f"Expected at least 5 scenarios, found {len(yaml_files)}"

        for yf in yaml_files:
            cfg = ScenarioConfig.from_yaml(yf)
            assert cfg.frequency > 0
            assert cfg.min_distance > 0
            assert cfg.max_distance > cfg.min_distance
            assert len(cfg.models) > 0

    def test_run_distance_sweep(self):
        cfg = ScenarioConfig.from_yaml("experiments/scenarios/urban.yaml")
        cfg.num_distance_points = 50  # fast test
        engine = SimulationEngine()
        res = engine.run_distance_sweep(cfg)

        assert res.sweep_type == "distance"
        assert len(res.sweep_values) == 50
        assert "fspl" in res.path_loss_db
        assert "cost231" in res.path_loss_db
        assert len(res.received_power_dbm["fspl"]) == 50

        # Test dataframe export
        df = res.to_dataframe()
        assert len(df) == 50 * len(cfg.models)
        assert "path_loss_db" in df.columns
        assert "received_power_dbm" in df.columns

        wide_df = res.to_wide_dataframe()
        assert "PL_fspl_dB" in wide_df.columns

    def test_run_frequency_sweep(self):
        cfg = ScenarioConfig.from_yaml("experiments/scenarios/urban.yaml")
        engine = SimulationEngine()
        res = engine.run_frequency_sweep(cfg, min_freq_mhz=500, max_freq_mhz=2000, num_freq_points=30, fixed_distance_km=2.0)

        assert res.sweep_type == "frequency"
        assert len(res.sweep_values) == 30
        assert "hata" in res.path_loss_db

