"""
Unit and integration tests for all 7 wireless propagation models.
"""

import warnings
import pytest
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import SPEED_OF_LIGHT, to_meters
from propagation.models import (
    FreeSpacePathLoss,
    TwoRayGroundReflection,
    LogDistancePathLoss,
    OkumuraModel,
    HataModel,
    COST231HataModel,
    LogNormalShadowing,
)


class TestFreeSpacePathLoss:
    """Tests for Friis Free Space Path Loss model."""

    def test_numerical_accuracy(self):
        model = FreeSpacePathLoss()
        # Known theoretical reference: d = 1 km, f = 900 MHz
        # FSPL = 20*log10(1000) + 20*log10(900e6) + 20*log10(4*pi / 299792458) ~= 91.53 dB
        pl = model.calculate_path_loss(1.0, 900.0, distance_unit="km", frequency_unit="MHz")
        assert pl == pytest.approx(91.53, abs=0.1)

    def test_vectorized_and_scaling(self):
        model = FreeSpacePathLoss()
        d_arr = np.array([100.0, 1000.0, 10000.0])  # decades of distance
        pl = model.calculate_path_loss(d_arr, 1.0, distance_unit="m", frequency_unit="GHz")
        # Each decade in free space adds exactly 20 dB
        assert pl[1] - pl[0] == pytest.approx(20.0, abs=1e-3)
        assert pl[2] - pl[1] == pytest.approx(20.0, abs=1e-3)

    def test_invalid_parameters(self):
        model = FreeSpacePathLoss()
        with pytest.raises(InvalidParameterError):
            model.calculate_path_loss(-50.0, 900.0)
        with pytest.raises(InvalidParameterError):
            model.calculate_path_loss(100.0, 0.0)


class TestTwoRayGroundReflection:
    """Tests for Two-Ray Ground Reflection model."""

    def test_crossover_distance_and_asymptote(self):
        model = TwoRayGroundReflection(ht_default=50.0, hr_default=2.0)
        f_hz = 900e6
        dc = model.crossover_distance(ht=50.0, hr=2.0, frequency_hz=f_hz)
        assert dc > 0

        # At far distance d >> dc (e.g. 20 km), exact and asymptotic should be very close
        pl_exact = model.calculate_path_loss(20.0, 900.0, distance_unit="km", frequency_unit="MHz", mode="exact")
        pl_asymp = model.calculate_path_loss(20.0, 900.0, distance_unit="km", frequency_unit="MHz", mode="asymptotic")
        assert abs(pl_exact - pl_asymp) < 1.5

    def test_height_effects(self):
        model = TwoRayGroundReflection()
        # Increasing transmitter height should reduce asymptotic path loss
        pl_h30 = model.calculate_path_loss(5.0, 900.0, distance_unit="km", frequency_unit="MHz", ht=30.0, mode="asymptotic")
        pl_h60 = model.calculate_path_loss(5.0, 900.0, distance_unit="km", frequency_unit="MHz", ht=60.0, mode="asymptotic")
        # Doubling ht reduces path loss by 20*log10(2) ~= 6.02 dB
        assert (pl_h30 - pl_h60) == pytest.approx(6.02, abs=0.1)


class TestLogDistancePathLoss:
    """Tests for Log-Distance model."""

    def test_environment_presets(self):
        m_urban = LogDistancePathLoss(environment="urban")
        m_free = LogDistancePathLoss(environment="free_space")
        assert m_urban.n == 3.0
        assert m_free.n == 2.0

    def test_distance_scaling(self):
        model = LogDistancePathLoss(n=3.0, d0_m=1.0, pl_d0_db=40.0)
        # d = 10 m -> 40 + 10 * 3 * log10(10) = 40 + 30 = 70 dB
        pl = model.calculate_path_loss(10.0, 1.0, distance_unit="m", frequency_unit="GHz")
        assert pl == pytest.approx(70.0, abs=1e-3)

    def test_sub_reference_warning(self):
        model = LogDistancePathLoss(d0_m=10.0)
        with pytest.warns(ModelRangeWarning):
            model.calculate_path_loss(5.0, 900.0, distance_unit="m", frequency_unit="MHz")


class TestOkumuraModel:
    """Tests for classical Okumura model."""

    def test_environmental_hierarchy(self):
        model = OkumuraModel()
        # Urban should have highest path loss, then suburban, then rural/open
        pl_urb = model.calculate_path_loss(5.0, 900.0, distance_unit="km", frequency_unit="MHz", environment="urban")
        pl_sub = model.calculate_path_loss(5.0, 900.0, distance_unit="km", frequency_unit="MHz", environment="suburban")
        pl_rur = model.calculate_path_loss(5.0, 900.0, distance_unit="km", frequency_unit="MHz", environment="open")

        assert pl_urb > pl_sub
        assert pl_sub > pl_rur

    def test_out_of_range_warning(self):
        model = OkumuraModel()
        # Frequency 2.4 GHz is above Okumura's 1920 MHz limit
        with pytest.warns(ModelRangeWarning):
            model.calculate_path_loss(5.0, 2400.0, distance_unit="km", frequency_unit="MHz")


class TestHataModel:
    """Tests for Okumura-Hata model."""

    def test_environmental_ordering(self):
        model = HataModel(hb_default=30.0, hm_default=1.5)
        d_km = 5.0
        f_mhz = 900.0

        pl_urb = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="urban_medium")
        pl_sub = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="suburban")
        pl_rur = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="rural")

        assert pl_urb > pl_sub > pl_rur
        # In Hata 900 MHz, suburban correction is ~10 dB and rural is ~28-30 dB
        assert 8.0 < (pl_urb - pl_sub) < 13.0
        assert 25.0 < (pl_urb - pl_rur) < 35.0

    def test_range_warnings(self):
        model = HataModel()
        # Distance > 20 km triggers warning
        with pytest.warns(ModelRangeWarning):
            model.calculate_path_loss(30.0, 900.0, distance_unit="km", frequency_unit="MHz")


class TestCOST231HataModel:
    """Tests for COST-231 Hata model."""

    def test_metropolitan_correction(self):
        model = COST231HataModel(hb_default=50.0, hm_default=1.5)
        d_km = 3.0
        f_mhz = 1800.0

        pl_med = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="medium_city")
        pl_metro = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="metropolitan")

        # Metropolitan center adds exactly CM = 3 dB
        assert (pl_metro - pl_med) == pytest.approx(3.0, abs=1e-3)

    def test_frequency_range_warning(self):
        model = COST231HataModel()
        # 900 MHz is below COST-231 calibrated range (1500-2000 MHz)
        with pytest.warns(ModelRangeWarning):
            model.calculate_path_loss(5.0, 900.0, distance_unit="km", frequency_unit="MHz")


class TestLogNormalShadowing:
    """Tests for Log-Normal Shadowing model."""

    def test_reproducibility(self):
        model = LogNormalShadowing(n=3.0, sigma_db=8.0, seed=123)
        pl1 = model.calculate_path_loss(500.0, 1800.0, distance_unit="m", frequency_unit="MHz", seed=123)
        pl2 = model.calculate_path_loss(500.0, 1800.0, distance_unit="m", frequency_unit="MHz", seed=123)
        assert pl1 == pl2

    def test_deterministic_median(self):
        model = LogNormalShadowing(n=3.0, sigma_db=8.0)
        pl_no_shadow = model.calculate_path_loss(500.0, 1800.0, distance_unit="m", frequency_unit="MHz", include_shadowing=False)
        pl_zero_sigma = model.calculate_path_loss(500.0, 1800.0, distance_unit="m", frequency_unit="MHz", sigma=0.0)
        assert pl_no_shadow == pytest.approx(pl_zero_sigma)

    def test_outage_probability(self):
        model = LogNormalShadowing(n=3.0, sigma_db=6.0)
        # Strong signal: outage should be near 0
        p_out_strong = model.calculate_outage_probability(
            distance=100.0,
            frequency=1800.0,
            rx_sensitivity_dbm=-100.0,
            tx_power_dbm=40.0,
            distance_unit="m",
            frequency_unit="MHz",
        )
        assert p_out_strong < 0.01

        # Very weak signal (long distance, poor sensitivity): outage should approach 1.0
        p_out_weak = model.calculate_outage_probability(
            distance=50000.0,
            frequency=1800.0,
            rx_sensitivity_dbm=-40.0,
            tx_power_dbm=10.0,
            distance_unit="m",
            frequency_unit="MHz",
        )
        assert p_out_weak > 0.99

