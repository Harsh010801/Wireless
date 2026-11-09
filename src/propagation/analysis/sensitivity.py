"""
Sensitivity analysis module: parameter sweeps across antenna heights, frequencies, and fading variance.
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from propagation.models.cost231 import COST231HataModel
from propagation.models.free_space import FreeSpacePathLoss
from propagation.models.hata import HataModel
from propagation.models.log_distance import LogDistancePathLoss
from propagation.models.okumura import OkumuraModel
from propagation.models.shadowing import LogNormalShadowing
from propagation.models.two_ray import TwoRayGroundReflection


class SensitivityAnalyzer:
    """
    Executes controlled sensitivity sweeps over single parameters while fixing others.
    """

    @staticmethod
    def sweep_tx_antenna_height(
        min_ht_m: float = 20.0,
        max_ht_m: float = 200.0,
        num_points: int = 50,
        distance_km: float = 5.0,
        frequency_mhz: float = 900.0,
        mobile_height_m: float = 1.5,
        environment: str = "urban_medium",
    ) -> pd.DataFrame:
        """
        Evaluate path loss variation as base station antenna height ht increases.
        """
        ht_values = np.linspace(min_ht_m, max_ht_m, num_points)

        two_ray = TwoRayGroundReflection(mode="asymptotic")
        okumura = OkumuraModel(environment="urban")
        hata = HataModel(environment=environment)

        pl_two_ray = []
        pl_okumura = []
        pl_hata = []

        for ht in ht_values:
            pl_two_ray.append(
                two_ray.calculate_path_loss(
                    distance=distance_km, frequency=frequency_mhz, distance_unit="km", frequency_unit="MHz",
                    ht=ht, hr=mobile_height_m
                )
            )
            pl_okumura.append(
                okumura.calculate_path_loss(
                    distance=distance_km, frequency=frequency_mhz, distance_unit="km", frequency_unit="MHz",
                    hte=ht, hre=mobile_height_m
                )
            )
            pl_hata.append(
                hata.calculate_path_loss(
                    distance=distance_km, frequency=frequency_mhz, distance_unit="km", frequency_unit="MHz",
                    hb=ht, hm=mobile_height_m
                )
            )

        return pd.DataFrame({
            "tx_height_m": ht_values,
            "PL_TwoRay_dB": np.array(pl_two_ray),
            "PL_Okumura_dB": np.array(pl_okumura),
            "PL_Hata_dB": np.array(pl_hata),
        })

    @staticmethod
    def sweep_rx_antenna_height(
        min_hm_m: float = 1.0,
        max_hm_m: float = 10.0,
        num_points: int = 50,
        distance_km: float = 5.0,
        frequency_mhz: float = 900.0,
        base_height_m: float = 30.0,
        environment: str = "urban_medium",
    ) -> pd.DataFrame:
        """
        Evaluate path loss variation as mobile antenna height hm increases.
        """
        hm_values = np.linspace(min_hm_m, max_hm_m, num_points)

        two_ray = TwoRayGroundReflection(mode="asymptotic")
        okumura = OkumuraModel(environment="urban")
        hata = HataModel(environment=environment)

        pl_two_ray = []
        pl_okumura = []
        pl_hata = []

        for hm in hm_values:
            pl_two_ray.append(
                two_ray.calculate_path_loss(
                    distance=distance_km, frequency=frequency_mhz, distance_unit="km", frequency_unit="MHz",
                    ht=base_height_m, hr=hm
                )
            )
            pl_okumura.append(
                okumura.calculate_path_loss(
                    distance=distance_km, frequency=frequency_mhz, distance_unit="km", frequency_unit="MHz",
                    hte=base_height_m, hre=hm
                )
            )
            pl_hata.append(
                hata.calculate_path_loss(
                    distance=distance_km, frequency=frequency_mhz, distance_unit="km", frequency_unit="MHz",
                    hb=base_height_m, hm=hm
                )
            )

        return pd.DataFrame({
            "rx_height_m": hm_values,
            "PL_TwoRay_dB": np.array(pl_two_ray),
            "PL_Okumura_dB": np.array(pl_okumura),
            "PL_Hata_dB": np.array(pl_hata),
        })

    @staticmethod
    def generate_2d_heatmap_grid(
        model_name: str = "cost231",
        distances_km: Optional[np.ndarray] = None,
        frequencies_mhz: Optional[np.ndarray] = None,
        hb: float = 30.0,
        hm: float = 1.5,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate a 2D meshgrid of Path Loss over Distance and Frequency.

        Returns:
            (D_grid, F_grid, PL_grid)
        """
        if distances_km is None:
            distances_km = np.linspace(1.0, 15.0, 50)
        if frequencies_mhz is None:
            frequencies_mhz = np.linspace(1500.0, 2000.0, 50)

        D, F = np.meshgrid(distances_km, frequencies_mhz)
        model = COST231HataModel(hb_default=hb, hm_default=hm)

        # Vectorized evaluation over flattened grid
        pl_flat = model.calculate_path_loss(
            distance=D.ravel(),
            frequency=F.ravel(),
            distance_unit="km",
            frequency_unit="MHz",
            strict=False,
            hb=hb,
            hm=hm,
        )
        PL = pl_flat.reshape(D.shape)
        return D, F, PL

