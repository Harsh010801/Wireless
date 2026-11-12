"""
Unit tests for 3GPP TR 38.901 and IEEE Access 2026 mmWave / 6G Propagation Models.
"""

import numpy as np
import pytest

from propagation.core.exceptions import InvalidParameterError
from propagation.models.mmwave_3gpp import (
    MMWave3GPPModel,
    CloseInMMWaveModel,
    calculate_3gpp_los_probability,
)


class TestMMWave3GPP:
    def test_los_probability_boundary(self):
        # d <= 18 m must have P_LoS == 1.0
        assert calculate_3gpp_los_probability(10.0) == 1.0
        assert calculate_3gpp_los_probability(18.0) == 1.0

        # d > 18 m must strictly decay
        p_50 = calculate_3gpp_los_probability(50.0)
        p_100 = calculate_3gpp_los_probability(100.0)
        p_500 = calculate_3gpp_los_probability(500.0)

        assert 0.0 < p_500 < p_100 < p_50 < 1.0

    def test_vectorized_los_probability(self):
        d_arr = np.array([5.0, 18.0, 50.0, 200.0, 1000.0])
        p_arr = calculate_3gpp_los_probability(d_arr)
        assert len(p_arr) == 5
        assert p_arr[0] == 1.0
        assert p_arr[1] == 1.0
        assert np.all(np.diff(p_arr[1:]) < 0)  # monotonically decreasing

    def test_los_vs_nlos_ordering(self):
        model_los = MMWave3GPPModel(mode="los")
        model_nlos = MMWave3GPPModel(mode="nlos")
        model_trans = MMWave3GPPModel(mode="transition")

        # Evaluate at 28 GHz (standard 5G mmWave FR2 band) over 100 m
        pl_los = model_los.calculate_path_loss(100.0, 28.0, distance_unit="m", frequency_unit="GHz")
        pl_nlos = model_nlos.calculate_path_loss(100.0, 28.0, distance_unit="m", frequency_unit="GHz")
        pl_trans = model_trans.calculate_path_loss(100.0, 28.0, distance_unit="m", frequency_unit="GHz")

        # LoS path loss must be strictly lower than NLoS
        assert pl_los < pl_nlos
        # Transition must lie between LoS and NLoS
        assert pl_los <= pl_trans <= pl_nlos

    def test_ghz_frequency_scaling(self):
        model = MMWave3GPPModel(mode="los")
        # 28 GHz vs 73 GHz (6G sub-THz)
        pl_28 = model.calculate_path_loss(100.0, 28.0, distance_unit="m", frequency_unit="GHz")
        pl_73 = model.calculate_path_loss(100.0, 73.0, distance_unit="m", frequency_unit="GHz")

        # Higher frequency experiences strictly higher path loss (Friis / 20 log10(fc) rule)
        expected_diff = 20.0 * np.log10(73.0 / 28.0)
        assert pl_73 > pl_28
        assert abs((pl_73 - pl_28) - expected_diff) < 0.1

    def test_close_in_mmwave_model(self):
        ci_los = CloseInMMWaveModel(n=2.0)
        ci_nlos = CloseInMMWaveModel(n=3.2)

        pl_los = ci_los.calculate_path_loss(100.0, 28.0, distance_unit="m", frequency_unit="GHz")
        pl_nlos = ci_nlos.calculate_path_loss(100.0, 28.0, distance_unit="m", frequency_unit="GHz")

        assert pl_los < pl_nlos
        assert pl_los > 50.0  # reasonable attenuation at 100m for 28 GHz

    def test_invalid_parameters_raise(self):
        model = MMWave3GPPModel(mode="los")
        with pytest.raises(InvalidParameterError):
            model.calculate_path_loss(-10.0, 28.0, distance_unit="m", frequency_unit="GHz")
        with pytest.raises(InvalidParameterError):
            model.calculate_path_loss(100.0, -5.0, distance_unit="m", frequency_unit="GHz")

