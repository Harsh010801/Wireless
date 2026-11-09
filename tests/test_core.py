"""
Unit tests for core mathematics, unit conversions, and link budget module.
"""

import math
import pytest
import numpy as np

from propagation.core.exceptions import InvalidParameterError, UnitError
from propagation.core.units import (
    SPEED_OF_LIGHT,
    to_hz,
    from_hz,
    to_meters,
    from_meters,
    wavelength,
    watts_to_dbm,
    dbm_to_watts,
    mw_to_dbm,
    dbm_to_mw,
    dbw_to_dbm,
    dbm_to_dbw,
)
from propagation.core.link_budget import LinkBudget


class TestUnitConversions:
    """Tests for frequency, distance, and power conversions."""

    def test_frequency_conversions(self):
        assert to_hz(1.0, "GHz") == pytest.approx(1e9)
        assert to_hz(900.0, "MHz") == pytest.approx(900e6)
        assert to_hz(150.0, "kHz") == pytest.approx(150e3)
        assert to_hz(1e6, "Hz") == pytest.approx(1e6)

        assert from_hz(1.8e9, "GHz") == pytest.approx(1.8)
        assert from_hz(900e6, "MHz") == pytest.approx(900.0)

    def test_wavelength_calculation(self):
        # f = 300 MHz -> lambda = 299792458 / 300e6 ~= 0.9993 m
        wl = wavelength(300.0, "MHz")
        assert wl == pytest.approx(SPEED_OF_LIGHT / 300e6, rel=1e-5)

    def test_distance_conversions(self):
        assert to_meters(1.0, "km") == pytest.approx(1000.0)
        assert to_meters(500.0, "m") == pytest.approx(500.0)
        assert from_meters(2500.0, "km") == pytest.approx(2.5)

    def test_power_conversions(self):
        # 1 W = 30 dBm
        assert watts_to_dbm(1.0) == pytest.approx(30.0)
        # 10 W = 40 dBm
        assert watts_to_dbm(10.0) == pytest.approx(40.0)
        # 0.001 W = 1 mW = 0 dBm
        assert watts_to_dbm(0.001) == pytest.approx(0.0)
        assert mw_to_dbm(1.0) == pytest.approx(0.0)
        assert mw_to_dbm(100.0) == pytest.approx(20.0)

        # Inverses
        assert dbm_to_watts(30.0) == pytest.approx(1.0)
        assert dbm_to_mw(20.0) == pytest.approx(100.0)
        assert dbw_to_dbm(0.0) == pytest.approx(30.0)
        assert dbm_to_dbw(30.0) == pytest.approx(0.0)

    def test_invalid_parameters(self):
        with pytest.raises(InvalidParameterError):
            to_hz(-10.0, "MHz")

        with pytest.raises(InvalidParameterError):
            to_hz(0.0, "Hz")

        with pytest.raises(InvalidParameterError):
            to_meters(-5.0, "m")

        with pytest.raises(InvalidParameterError):
            watts_to_dbm(-1.0)

        with pytest.raises(UnitError):
            to_hz(100.0, "lightyears")

        with pytest.raises(UnitError):
            to_meters(100.0, "furlongs")

    def test_vectorized_conversions(self):
        freqs_mhz = np.array([100.0, 900.0, 1800.0, 2400.0])
        freqs_hz = to_hz(freqs_mhz, "MHz")
        assert isinstance(freqs_hz, np.ndarray)
        assert np.allclose(freqs_hz, freqs_mhz * 1e6)

        dists_km = np.array([0.5, 1.0, 5.0, 10.0])
        dists_m = to_meters(dists_km, "km")
        assert isinstance(dists_m, np.ndarray)
        assert np.allclose(dists_m, dists_km * 1000.0)


class TestLinkBudget:
    """Tests for link budget calculations."""

    def test_basic_link_budget(self):
        budget = LinkBudget(
            tx_power_dbm=30.0,  # 1 W
            tx_gain_dbi=15.0,
            rx_gain_dbi=3.0,
            system_loss_db=2.0,
            rx_sensitivity_dbm=-90.0,
        )

        assert budget.eirp_dbm == pytest.approx(45.0)

        # PL = 100 dB
        # Pr = 30 + 15 + 3 - 100 - 2 = -54 dBm
        pr_dbm = budget.calculate_received_power_dbm(100.0)
        assert pr_dbm == pytest.approx(-54.0)

        # Fade margin = -54 - (-90) = 36 dB
        fade_margin = budget.calculate_fade_margin(100.0)
        assert fade_margin == pytest.approx(36.0)

        pr_w = budget.calculate_received_power_watts(100.0)
        assert pr_w == pytest.approx(dbm_to_watts(-54.0))

    def test_vectorized_link_budget(self):
        budget = LinkBudget(tx_power_dbm=33.0, tx_gain_dbi=10.0, rx_gain_dbi=0.0)
        path_losses = np.array([80.0, 90.0, 100.0, 110.0])
        expected_rx = 33.0 + 10.0 - path_losses
        rx_dbm = budget.calculate_received_power_dbm(path_losses)
        assert isinstance(rx_dbm, np.ndarray)
        assert np.allclose(rx_dbm, expected_rx)

    def test_invalid_system_loss(self):
        with pytest.raises(InvalidParameterError):
            LinkBudget(system_loss_db=-1.0)

