"""
3GPP TR 38.901 (Release 16–19) Propagation Models for 0.5 to 100 GHz.

Implements standard 3GPP channel models:
1. Urban Micro (UMi) Street Canyon (LoS, NLoS, Breakpoint distance d'BP)
2. Urban Macro (UMa) (LoS, NLoS, Breakpoint distance d'BP)
3. Indoor Hotspot (InH) Office (LoS, NLoS)
4. Atmospheric absorption (ITU-R P.676 approximation including 60 GHz O2 resonance)
5. Vehicle and human blockage attenuation

References:
- 3GPP TR 38.901 V17.0.0 (and Rel-19 study enhancements for 6G):
  "Study on channel model for frequencies from 0.5 to 100 GHz"
- Poddar et al., "Overview of 3GPP Release 19 Study on Channel Modeling Enhancements to TR 38.901 for 6G", arXiv:2507.19266
"""

import math
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import SPEED_OF_LIGHT, to_hz, to_meters
from propagation.models.base import PropagationModel


def compute_atmospheric_absorption_db_per_km(fc_ghz: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    ITU-R P.676 empirical approximation for specific attenuation gamma (dB/km)
    due to atmospheric oxygen (O2) and water vapor from 0.5 to 100 GHz at standard
    sea-level pressure (1013.25 hPa) and 15°C temperature.

    Key physical characteristic:
        Sharp resonant oxygen peak centered at 60 GHz (~15 dB/km).
    """
    f = np.asarray(fc_ghz, dtype=np.float64)
    # Oxygen resonance peak model approximation
    # Baseline dry air absorption
    gamma_o2 = (
        (7.2 * f**2 / (f**2 + 0.36)) * 1e-3
        + (3.6 * (f - 60)**2 / ((f - 60)**2 + 1.2**2) * 0.05 + 15.0 / (1.0 + ((f - 60) / 2.5)**2))
        * (f >= 50.0) * (f <= 70.0)
    )
    # Water vapor baseline (22.2 GHz line)
    gamma_h2o = 0.001 * f**1.8 / (1.0 + ((f - 22.2) / 3.0)**2)

    total_gamma = np.maximum(0.005, gamma_o2 + gamma_h2o)
    return float(total_gamma) if np.isscalar(fc_ghz) else total_gamma


class ThreeGPPTR38901Base(PropagationModel):
    """
    Abstract base class for 3GPP TR 38.901 family models (UMi, UMa, InH).
    """

    def __init__(self, name: str, scenario_type: str, description: str):
        super().__init__(
            name=name,
            classification="Empirical / 3GPP Standard",
            description=description,
        )
        self.scenario_type = scenario_type

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (10.0, 5000.0),
            "frequency_hz": (0.5e9, 100.0e9),  # 0.5 GHz to 100 GHz (3GPP standard range)
        }


class ThreeGPPUMiModel(ThreeGPPTR38901Base):
    """
    3GPP TR 38.901 Urban Micro (UMi - Street Canyon) Path Loss Model.

    Formulation (3GPP TR 38.901 Table 7.4.1-1):
        fc in GHz, distances in meters, c = SPEED_OF_LIGHT.
        Effective environment height hE = 1.0 m.
        h'BS = hBS - hE,  h'UT = hUT - hE.
        Breakpoint distance:
            d'BP = 4 * h'BS * h'UT * (fc * 1e9) / c

        LoS Path Loss:
            For 10 m <= d2D <= d'BP:
                PL1 = 32.4 + 21.0 * log10(d3D) + 20.0 * log10(fc)
            For d'BP < d2D <= 5000 m:
                PL2 = 32.4 + 40.0 * log10(d3D) + 20.0 * log10(fc)
                      - 9.5 * log10((d'BP)^2 + (hBS - hUT)^2)
            Shadow fading: sigma_SF = 4.0 dB.

        NLoS Path Loss:
            PL'_NLoS = 35.3 * log10(d3D) + 22.4 + 21.3 * log10(fc) - 0.3 * (hUT - 1.5)
            PL_NLoS = max(PL_LoS, PL'_NLoS)
            Shadow fading: sigma_SF = 7.82 dB.

        LoS Probability:
            P_LoS = 1.0                                      for d2D <= 18 m
            P_LoS = 18/d2D + exp(-d2D/36) * (1 - 18/d2D)     for d2D > 18 m
    """

    def __init__(
        self,
        mode: str = "los",
        hbs_default: float = 10.0,
        hut_default: float = 1.5,
        include_atmospheric_loss: bool = False,
        blockage_loss_db: float = 0.0,
    ):
        super().__init__(
            name=f"3GPP TR 38.901 UMi ({mode.upper()})",
            scenario_type="umi",
            description=f"3GPP TR 38.901 Urban Micro Street Canyon {mode.upper()} model (0.5–100 GHz).",
        )
        self.mode = mode.lower().strip()
        self.hbs_default = hbs_default
        self.hut_default = hut_default
        self.include_atmospheric_loss = include_atmospheric_loss
        self.blockage_loss_db = blockage_loss_db

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (10.0, 5000.0),
            "frequency_hz": (0.5e9, 100.0e9),
            "hbs_m": (4.0, 25.0),
            "hut_m": (1.0, 3.0),
        }

    @staticmethod
    def calculate_los_probability(distance_2d_m: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """3GPP UMi Street Canyon LoS Probability formula."""
        d = np.asarray(distance_2d_m, dtype=np.float64)
        p = np.ones_like(d)
        mask = d > 18.0
        if np.any(mask):
            d_sub = d[mask]
            p[mask] = (18.0 / d_sub) + np.exp(-d_sub / 36.0) * (1.0 - (18.0 / d_sub))
        p = np.clip(p, 0.0, 1.0)
        return float(p) if np.isscalar(distance_2d_m) else p

    def calculate_path_loss(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        hbs: Optional[float] = None,
        hut: Optional[float] = None,
        mode: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        d2d = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)
        fc_ghz = f_hz / 1e9

        h_bs = float(hbs if hbs is not None else kwargs.get("ht", self.hbs_default))
        h_ut = float(hut if hut is not None else kwargs.get("hr", self.hut_default))

        self.validate_parameters(
            strict=strict,
            distance_m=d2d,
            frequency_hz=f_hz,
            hbs_m=h_bs,
            hut_m=h_ut,
        )

        d2d_arr = np.asarray(d2d, dtype=np.float64)
        delta_h = h_bs - h_ut
        d3d = np.sqrt(d2d_arr**2 + delta_h**2)
        d3d_safe = np.maximum(d3d, 1.0)

        # Breakpoint distance d'BP (effective environment height hE = 1.0 m)
        h_prime_bs = max(1.0, h_bs - 1.0)
        h_prime_ut = max(0.1, h_ut - 1.0)
        dbp_prime = 4.0 * h_prime_bs * h_prime_ut * (fc_ghz * 1e9) / SPEED_OF_LIGHT

        # 1. LoS Calculation
        # PL1 for d2D <= d'BP
        pl1 = 32.4 + 21.0 * np.log10(d3d_safe) + 20.0 * np.log10(fc_ghz)
        # PL2 for d2D > d'BP
        pl2 = (
            32.4
            + 40.0 * np.log10(d3d_safe)
            + 20.0 * np.log10(fc_ghz)
            - 9.5 * np.log10(dbp_prime**2 + delta_h**2)
        )
        pl_los = np.where(d2d_arr <= dbp_prime, pl1, pl2)

        # 2. NLoS Calculation
        pl_nlos_prime = 35.3 * np.log10(d3d_safe) + 22.4 + 21.3 * np.log10(fc_ghz) - 0.3 * (h_ut - 1.5)
        pl_nlos = np.maximum(pl_los, pl_nlos_prime)

        active_mode = (mode or self.mode).lower().strip()
        if active_mode in ["los", "umi_los"]:
            res = pl_los
        elif active_mode in ["nlos", "umi_nlos"]:
            res = pl_nlos
        elif active_mode in ["transition", "hybrid"]:
            p_los = self.calculate_los_probability(d2d_arr)
            res = p_los * pl_los + (1.0 - p_los) * pl_nlos
        else:
            res = pl_los

        # Add atmospheric absorption if enabled
        if self.include_atmospheric_loss or kwargs.get("include_atmospheric_loss", False):
            d_km = d2d_arr / 1000.0
            gamma = compute_atmospheric_absorption_db_per_km(fc_ghz)
            res = res + gamma * d_km

        # Add blockage loss if specified
        blockage = kwargs.get("blockage_loss_db", self.blockage_loss_db)
        if blockage > 0:
            res = res + blockage

        return float(res) if np.isscalar(distance) else res


class ThreeGPPUMaModel(ThreeGPPTR38901Base):
    """
    3GPP TR 38.901 Urban Macro (UMa) Path Loss Model.

    Formulation (3GPP TR 38.901 Table 7.4.1-1):
        fc in GHz, distances in meters.
        Defaults: hBS = 25.0 m, hUT = 1.5 m.
        Effective environment height hE = 1.0 m (nominal).
        h'BS = hBS - hE,  h'UT = hUT - hE.
        Breakpoint distance:
            d'BP = 4 * h'BS * h'UT * (fc * 1e9) / c

        LoS Path Loss:
            For 10 m <= d2D <= d'BP:
                PL1 = 28.0 + 22.0 * log10(d3D) + 20.0 * log10(fc)
            For d'BP < d2D <= 5000 m:
                PL2 = 28.0 + 40.0 * log10(d3D) + 20.0 * log10(fc)
                      - 9.5 * log10((d'BP)^2 + (hBS - hUT)^2)
            Shadow fading: sigma_SF = 4.0 dB.

        NLoS Path Loss:
            PL'_NLoS = 13.54 + 39.08 * log10(d3D) + 20.0 * log10(fc) - 0.6 * (hUT - 1.5)
            PL_NLoS = max(PL_LoS, PL'_NLoS)
            Shadow fading: sigma_SF = 6.0 dB.

        LoS Probability:
            P_LoS = 1.0                                       for d2D <= 18 m
            P_LoS = (18/d2D + exp(-d2D/63)*(1 - 18/d2D)) * [1 + C'(hUT)*(5/4)*(d2D/100)^3 * exp(-d2D/150)]
            (For hUT <= 13 m, C'(hUT) = 0, so the second bracket is 1.0).
    """

    def __init__(
        self,
        mode: str = "los",
        hbs_default: float = 25.0,
        hut_default: float = 1.5,
        include_atmospheric_loss: bool = False,
        blockage_loss_db: float = 0.0,
    ):
        super().__init__(
            name=f"3GPP TR 38.901 UMa ({mode.upper()})",
            scenario_type="uma",
            description=f"3GPP TR 38.901 Urban Macro {mode.upper()} model (0.5–100 GHz).",
        )
        self.mode = mode.lower().strip()
        self.hbs_default = hbs_default
        self.hut_default = hut_default
        self.include_atmospheric_loss = include_atmospheric_loss
        self.blockage_loss_db = blockage_loss_db

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (10.0, 5000.0),
            "frequency_hz": (0.5e9, 100.0e9),
            "hbs_m": (10.0, 150.0),
            "hut_m": (1.5, 22.5),
        }

    @staticmethod
    def calculate_los_probability(
        distance_2d_m: Union[float, np.ndarray], hut: float = 1.5
    ) -> Union[float, np.ndarray]:
        """3GPP UMa LoS Probability formula."""
        d = np.asarray(distance_2d_m, dtype=np.float64)
        p = np.ones_like(d)
        mask = d > 18.0
        if np.any(mask):
            d_sub = d[mask]
            p_base = (18.0 / d_sub) + np.exp(-d_sub / 63.0) * (1.0 - (18.0 / d_sub))
            if hut <= 13.0:
                c_prime = 0.0
            else:
                c_prime = ((hut - 13.0) / 10.0)**1.5
            height_factor = 1.0 + c_prime * (5.0 / 4.0) * (d_sub / 100.0)**3 * np.exp(-d_sub / 150.0)
            p[mask] = p_base * height_factor
        p = np.clip(p, 0.0, 1.0)
        return float(p) if np.isscalar(distance_2d_m) else p

    def calculate_path_loss(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        hbs: Optional[float] = None,
        hut: Optional[float] = None,
        mode: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        d2d = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)
        fc_ghz = f_hz / 1e9

        h_bs = float(hbs if hbs is not None else kwargs.get("ht", self.hbs_default))
        h_ut = float(hut if hut is not None else kwargs.get("hr", self.hut_default))

        self.validate_parameters(
            strict=strict,
            distance_m=d2d,
            frequency_hz=f_hz,
            hbs_m=h_bs,
            hut_m=h_ut,
        )

        d2d_arr = np.asarray(d2d, dtype=np.float64)
        delta_h = h_bs - h_ut
        d3d = np.sqrt(d2d_arr**2 + delta_h**2)
        d3d_safe = np.maximum(d3d, 1.0)

        # Breakpoint distance d'BP for UMa (nominal hE = 1.0 m)
        h_prime_bs = max(1.0, h_bs - 1.0)
        h_prime_ut = max(0.1, h_ut - 1.0)
        dbp_prime = 4.0 * h_prime_bs * h_prime_ut * (fc_ghz * 1e9) / SPEED_OF_LIGHT

        # 1. LoS Calculation
        pl1 = 28.0 + 22.0 * np.log10(d3d_safe) + 20.0 * np.log10(fc_ghz)
        pl2 = (
            28.0
            + 40.0 * np.log10(d3d_safe)
            + 20.0 * np.log10(fc_ghz)
            - 9.5 * np.log10(dbp_prime**2 + delta_h**2)
        )
        pl_los = np.where(d2d_arr <= dbp_prime, pl1, pl2)

        # 2. NLoS Calculation
        pl_nlos_prime = 13.54 + 39.08 * np.log10(d3d_safe) + 20.0 * np.log10(fc_ghz) - 0.6 * (h_ut - 1.5)
        pl_nlos = np.maximum(pl_los, pl_nlos_prime)

        active_mode = (mode or self.mode).lower().strip()
        if active_mode in ["los", "uma_los"]:
            res = pl_los
        elif active_mode in ["nlos", "uma_nlos"]:
            res = pl_nlos
        elif active_mode in ["transition", "hybrid"]:
            p_los = self.calculate_los_probability(d2d_arr, hut=h_ut)
            res = p_los * pl_los + (1.0 - p_los) * pl_nlos
        else:
            res = pl_los

        if self.include_atmospheric_loss or kwargs.get("include_atmospheric_loss", False):
            d_km = d2d_arr / 1000.0
            gamma = compute_atmospheric_absorption_db_per_km(fc_ghz)
            res = res + gamma * d_km

        blockage = kwargs.get("blockage_loss_db", self.blockage_loss_db)
        if blockage > 0:
            res = res + blockage

        return float(res) if np.isscalar(distance) else res


class ThreeGPPInHOfficeModel(ThreeGPPTR38901Base):
    """
    3GPP TR 38.901 Indoor Hotspot (InH) Office Path Loss Model.

    Formulation (3GPP TR 38.901 Table 7.4.1-1):
        fc in GHz, distances in meters.
        Valid: 1 m <= d3D <= 150 m, 0.5 <= fc <= 100 GHz.

        LoS Path Loss:
            PL_InH_LoS = 32.4 + 17.3 * log10(d3D) + 20.0 * log10(fc)
            Shadow fading: sigma_SF = 3.0 dB.

        NLoS Path Loss:
            PL'_InH_NLoS = 38.3 * log10(d3D) + 17.30 + 24.9 * log10(fc)
            PL_InH_NLoS = max(PL_InH_LoS, PL'_InH_NLoS)
            Shadow fading: sigma_SF = 8.03 dB (mixed office) / 8.29 dB.
    """

    def __init__(
        self,
        mode: str = "los",
        hbs_default: float = 3.0,
        hut_default: float = 1.0,
    ):
        super().__init__(
            name=f"3GPP TR 38.901 InH ({mode.upper()})",
            scenario_type="inh",
            description=f"3GPP TR 38.901 Indoor Hotspot Office {mode.upper()} model (0.5–100 GHz).",
        )
        self.mode = mode.lower().strip()
        self.hbs_default = hbs_default
        self.hut_default = hut_default

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (1.0, 150.0),
            "frequency_hz": (0.5e9, 100.0e9),
        }

    def calculate_path_loss(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        hbs: Optional[float] = None,
        hut: Optional[float] = None,
        mode: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        d2d = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)
        fc_ghz = f_hz / 1e9

        h_bs = float(hbs if hbs is not None else kwargs.get("ht", self.hbs_default))
        h_ut = float(hut if hut is not None else kwargs.get("hr", self.hut_default))

        self.validate_parameters(strict=strict, distance_m=d2d, frequency_hz=f_hz)

        d2d_arr = np.asarray(d2d, dtype=np.float64)
        delta_h = h_bs - h_ut
        d3d = np.sqrt(d2d_arr**2 + delta_h**2)
        d3d_safe = np.maximum(d3d, 1.0)

        # InH LoS
        pl_los = 32.4 + 17.3 * np.log10(d3d_safe) + 20.0 * np.log10(fc_ghz)

        # InH NLoS
        pl_nlos_prime = 38.3 * np.log10(d3d_safe) + 17.30 + 24.9 * np.log10(fc_ghz)
        pl_nlos = np.maximum(pl_los, pl_nlos_prime)

        active_mode = (mode or self.mode).lower().strip()
        if active_mode in ["los", "inh_los"]:
            res = pl_los
        else:
            res = pl_nlos

        return float(res) if np.isscalar(distance) else res
