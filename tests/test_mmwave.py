"""
Comprehensive Unit Tests for 3GPP TR 38.901 (Rel 16-19), CI/CIF, ABG, and LoS-NLoS Transition Models.
Includes hand-checked vectors (tolerance 0.1 dB) specified by 3GPP specifications.
"""

import warnings
import numpy as np
import pytest

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import SPEED_OF_LIGHT
from propagation.models.three_gpp_tr38901 import (
    ThreeGPPUMiModel,
    ThreeGPPUMaModel,
    ThreeGPPInHOfficeModel,
    compute_atmospheric_absorption_db_per_km,
)
from propagation.models.ci_abg import CloseInModel, FloatingInterceptABGModel
from propagation.models.los_nlos_transition import StatisticalLoSNLoSTransitionModel
from propagation.models.free_space import FreeSpacePathLoss


class TestHandCheckedVectors:
    """Verify exact numerical benchmarks from 3GPP TR 38.901 & literature (tolerance 0.1 dB)."""

    def test_fspl_1m_at_28ghz(self):
        # FSPL(1 m) at 28 GHz -> about 61.4 dB
        fspl = FreeSpacePathLoss()
        val = fspl.calculate_path_loss(1.0, 28.0, distance_unit="m", frequency_unit="GHz")
        expected = 20.0 * np.log10(4.0 * np.pi * 1.0 * 28e9 / SPEED_OF_LIGHT)
        assert abs(val - 61.4) < 0.1
        assert abs(val - expected) < 1e-6

    def test_3gpp_umi_los_hand_checked_vector(self):
        # 3GPP UMi LoS, fc = 28 GHz, d3D = 100 m, hBS = 10, hUT = 1.5 -> about 103.3 dB
        umi_los = ThreeGPPUMiModel(mode="los", hbs_default=10.0, hut_default=1.5)
        # horizontal distance d2D = sqrt(d3D^2 - (hBS - hUT)^2)
        d3d = 100.0
        delta_h = 10.0 - 1.5
        d2d = np.sqrt(d3d**2 - delta_h**2)

        val = umi_los.calculate_path_loss(
            distance=d2d,
            frequency=28.0,
            distance_unit="m",
            frequency_unit="GHz",
            hbs=10.0,
            hut=1.5,
        )
        assert abs(val - 103.3) < 0.1

    def test_3gpp_umi_nlos_hand_checked_vector(self):
        # 3GPP UMi NLoS, fc = 28 GHz, d3D = 100 m, hBS = 10, hUT = 1.5 -> about 123.8 dB
        umi_nlos = ThreeGPPUMiModel(mode="nlos", hbs_default=10.0, hut_default=1.5)
        d3d = 100.0
        delta_h = 10.0 - 1.5
        d2d = np.sqrt(d3d**2 - delta_h**2)

        val = umi_nlos.calculate_path_loss(
            distance=d2d,
            frequency=28.0,
            distance_unit="m",
            frequency_unit="GHz",
            hbs=10.0,
            hut=1.5,
        )
        assert abs(val - 123.8) < 0.1

    def test_ci_model_hand_checked_vector(self):
        # CI, f = 28 GHz, d = 100 m, n = 3.19 (no shadowing) -> about 125.2 dB
        ci = CloseInModel(n=3.19, sigma_db=0.0)
        val = ci.calculate_path_loss(100.0, 28.0, distance_unit="m", frequency_unit="GHz")
        assert abs(val - 125.2) < 0.1


class TestPhysicalProperties:
    """Verify physical properties: monotonicity, LoS <= NLoS, LoS probability bounds."""

    def test_los_probability_bounds_and_decay(self):
        # 1. d2D <= 18m -> P_LoS == 1.0
        assert ThreeGPPUMiModel.calculate_los_probability(5.0) == 1.0
        assert ThreeGPPUMiModel.calculate_los_probability(18.0) == 1.0

        # 2. Monotonically decreasing and strictly bounded between 0 and 1
        d_vec = np.linspace(18.1, 1000.0, 100)
        p_vec = ThreeGPPUMiModel.calculate_los_probability(d_vec)

        assert np.all(p_vec >= 0.0)
        assert np.all(p_vec <= 1.0)
        assert np.all(np.diff(p_vec) < 0.0)

    def test_nlos_greater_or_equal_to_los(self):
        umi_los = ThreeGPPUMiModel(mode="los")
        umi_nlos = ThreeGPPUMiModel(mode="nlos")

        distances = np.geomspace(15.0, 2000.0, 50)
        pl_los = umi_los.calculate_path_loss(distances, 28.0, distance_unit="m", frequency_unit="GHz")
        pl_nlos = umi_nlos.calculate_path_loss(distances, 28.0, distance_unit="m", frequency_unit="GHz")

        assert np.all(pl_nlos >= pl_los)

    def test_path_loss_monotonicity_in_distance(self):
        # All models must show increasing path loss with distance
        distances = np.geomspace(20.0, 1000.0, 50)
        models = [
            ThreeGPPUMiModel(mode="los"),
            ThreeGPPUMiModel(mode="nlos"),
            ThreeGPPUMaModel(mode="los"),
            ThreeGPPUMaModel(mode="nlos"),
            CloseInModel(n=2.1),
            FloatingInterceptABGModel(preset="umi_nlos"),
        ]

        for m in models:
            pl = m.calculate_path_loss(distances, 28.0, distance_unit="m", frequency_unit="GHz")
            assert np.all(np.diff(pl) > 0.0), f"Model {m.name} is not strictly monotonic in distance."


class TestABGAndCIFModels:
    """Verify CIF frequency-dependent exponents and ABG Least Squares fitter."""

    def test_cif_model_exponent_scaling(self):
        cif_pos = CloseInModel(n=2.0, use_cif=True, b_cif=0.02, f0_hz=1e9)
        cif_flat = CloseInModel(n=2.0, use_cif=False)

        pl_high_f_cif = cif_pos.calculate_path_loss(100.0, 10.0, distance_unit="m", frequency_unit="GHz")
        pl_high_f_flat = cif_flat.calculate_path_loss(100.0, 10.0, distance_unit="m", frequency_unit="GHz")

        # Positive b_cif increases exponent with frequency
        assert pl_high_f_cif > pl_high_f_flat

    def test_abg_least_squares_fitter(self):
        # Generate synthetic noisy data from known alpha=3.0, beta=20.0, gamma=2.0
        true_alpha, true_beta, true_gamma = 3.0, 20.0, 2.0
        d_synth = np.array([20.0, 50.0, 100.0, 200.0, 500.0, 1000.0])
        f_synth = np.array([2e9, 5e9, 10e9, 28e9, 39e9, 73e9])

        D_grid, F_grid = np.meshgrid(d_synth, f_synth)
        D_flat = D_grid.flatten()
        F_flat = F_grid.flatten()
        PL_clean = (
            10.0 * true_alpha * np.log10(D_flat)
            + true_beta
            + 10.0 * true_gamma * np.log10(F_flat / 1e9)
        )

        fitted_model = FloatingInterceptABGModel.fit_from_data(D_flat, F_flat, PL_clean)
        assert abs(fitted_model.alpha - true_alpha) < 1e-3
        assert abs(fitted_model.beta - true_beta) < 1e-3
        assert abs(fitted_model.gamma - true_gamma) < 1e-3


class TestLoSNLoSTransitionMonteCarlo:
    """Verify seed-controlled reproducibility for LoS <-> NLoS transitions."""

    def test_monte_carlo_reproducibility(self):
        trans_model = StatisticalLoSNLoSTransitionModel(seed=42)
        d_vec = np.linspace(20.0, 200.0, 20)

        run1 = trans_model.calculate_path_loss(d_vec, 28.0, distance_unit="m", frequency_unit="GHz", mode="realization", seed=42)
        run2 = trans_model.calculate_path_loss(d_vec, 28.0, distance_unit="m", frequency_unit="GHz", mode="realization", seed=42)
        run3_diff_seed = trans_model.calculate_path_loss(d_vec, 28.0, distance_unit="m", frequency_unit="GHz", mode="realization", seed=999)

        np.testing.assert_allclose(run1, run2, err_msg="Identical seeds must yield exact identical trajectories.")
        assert not np.allclose(run1, run3_diff_seed)

    def test_transition_statistics_output(self):
        trans_model = StatisticalLoSNLoSTransitionModel(seed=42)
        d_vec = np.linspace(15.0, 300.0, 20)
        stats = trans_model.calculate_transition_statistics(d_vec, 28e9, num_monte_carlo=300, seed=42)

        assert "p_los" in stats
        assert "mean_pl_db" in stats
        assert "outage_pct" in stats
        assert np.all(stats["outage_pct"] >= 0.0)
        assert np.all(stats["outage_pct"] <= 100.0)


class TestAtmosphericAndBoundaryWarnings:
    """Verify oxygen 60 GHz resonance peak and parameter bounds warnings."""

    def test_oxygen_60ghz_absorption_peak(self):
        # Atmospheric absorption must exhibit sharp peak at 60 GHz
        gamma_28 = compute_atmospheric_absorption_db_per_km(28.0)
        gamma_60 = compute_atmospheric_absorption_db_per_km(60.0)
        gamma_90 = compute_atmospheric_absorption_db_per_km(90.0)

        assert gamma_60 > 10.0  # O2 resonance peak ~ 15 dB/km
        assert gamma_60 > gamma_28 * 10.0
        assert gamma_60 > gamma_90 * 5.0

    def test_out_of_range_warnings(self):
        umi = ThreeGPPUMiModel(mode="los")

        # Distance below 10 m triggers warning
        with pytest.warns(ModelRangeWarning):
            umi.calculate_path_loss(5.0, 28.0, distance_unit="m", frequency_unit="GHz", strict=False)

        # Distance above 5 km triggers warning
        with pytest.warns(ModelRangeWarning):
            umi.calculate_path_loss(6000.0, 28.0, distance_unit="m", frequency_unit="GHz", strict=False)

        # Frequency above 100 GHz triggers warning
        with pytest.warns(ModelRangeWarning):
            umi.calculate_path_loss(100.0, 150.0, distance_unit="m", frequency_unit="GHz", strict=False)

        # Strict mode raises InvalidParameterError
        with pytest.raises(InvalidParameterError):
            umi.calculate_path_loss(5.0, 28.0, distance_unit="m", frequency_unit="GHz", strict=True)
