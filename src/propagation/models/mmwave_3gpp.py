"""
3GPP TR 38.901 & IEEE Access 2026 mmWave / 6G Propagation Models.

Implements:
1. 3GPP TR 38.901 Urban Micro (UMi - Street Canyon) LoS and NLoS path loss models.
2. Statistical LoS-to-NLoS Transition model based on:
   Inam Ullah, Hesham El-Sayed, Alexis A. Dowhuszko, Jyri Hämäläinen,
   "Statistical Path Loss Modeling of LoS–NLoS Transitions for mmWave Communications
   in Urban Environments", IEEE Access, 2026. DOI: 10.1109/ACCESS.2026.3741615.
3. Close-In (CI) Free-Space Reference Distance mmWave propagation model.

Frequency Range: 0.5 GHz to 100 GHz (covering 5G mmWave FR2: 28 GHz, 39 GHz, 60 GHz,
and 6G sub-THz: 73 GHz, 95 GHz).
"""

import math
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import SPEED_OF_LIGHT, to_hz, to_meters
from propagation.models.base import PropagationModel


def calculate_3gpp_los_probability(
    distance_2d_m: Union[float, np.ndarray],
) -> Union[float, np.ndarray]:
    """
    Compute 3GPP TR 38.901 / ITU-R Line-of-Sight probability P_LoS(d_2D)
    for Urban Micro (UMi - Street Canyon).

    Formulation:
        For d_2D <= 18 m: P_LoS = 1.0
        For d_2D > 18 m:  P_LoS = (18 / d_2D) + exp(-d_2D / 36) * (1 - 18 / d_2D)
    """
    d = np.asarray(distance_2d_m, dtype=np.float64)
    # Vectorized computation
    p_los = np.ones_like(d)
    mask = d > 18.0
    if np.any(mask):
        d_sub = d[mask]
        p_los[mask] = (18.0 / d_sub) + np.exp(-d_sub / 36.0) * (1.0 - (18.0 / d_sub))
    p_los = np.clip(p_los, 0.0, 1.0)
    return float(p_los) if np.isscalar(distance_2d_m) else p_los


class MMWave3GPPModel(PropagationModel):
    """
    3GPP TR 38.901 Urban Micro (UMi) mmWave / 6G Propagation Model.

    Supports:
      - mode='los': Line-of-Sight path loss
      - mode='nlos': Non-Line-of-Sight path loss
      - mode='transition': Statistical LoS-NLoS state transition (IEEE Access 2026)
    """

    def __init__(
        self,
        mode: str = "transition",
        hb_default: float = 10.0,
        hm_default: float = 1.5,
    ):
        mode_clean = mode.lower().strip()
        if mode_clean not in ["los", "nlos", "transition"]:
            raise InvalidParameterError(
                f"Mode must be 'los', 'nlos', or 'transition', got '{mode}'"
            )

        name_map = {
            "los": "3GPP TR 38.901 UMi LoS (mmWave)",
            "nlos": "3GPP TR 38.901 UMi NLoS (mmWave)",
            "transition": "3GPP / IEEE Access LoS-NLoS Transition (5G/6G mmWave)",
        }
        desc_map = {
            "los": "3GPP TR 38.901 Urban Micro (UMi) Line-of-Sight mmWave model (0.5–100 GHz).",
            "nlos": "3GPP TR 38.901 Urban Micro (UMi) Non-Line-of-Sight mmWave model (0.5–100 GHz).",
            "transition": "Statistical LoS–NLoS transition for mmWave urban microcells (Inam Ullah et al., IEEE Access 2026).",
        }

        super().__init__(
            name=name_map[mode_clean],
            classification="Empirical / 3GPP Standard",
            description=desc_map[mode_clean],
        )
        self.mode = mode_clean
        self.hb_default = hb_default
        self.hm_default = hm_default

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (10.0, 5000.0),
            "frequency_hz": (0.5e9, 100.0e9),  # 0.5 GHz to 100 GHz
            "hb_m": (4.0, 25.0),
            "hm_m": (1.0, 3.0),
        }

    def calculate_path_loss(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        hb: Optional[float] = None,
        hm: Optional[float] = None,
        mode_override: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        """
        Calculate mmWave path loss in dB.

        Formulas (3GPP TR 38.901 Table 7.4.1-1 UMi - Street Canyon):
            f_c in GHz, d_3D in meters:
            PL_LoS = 32.4 + 21.0 * log10(d_3D) + 20.0 * log10(f_c)
            PL_NLoS_prime = 22.4 + 35.3 * log10(d_3D) + 21.3 * log10(f_c)
            PL_NLoS = max(PL_LoS, PL_NLoS_prime)

            Transition (IEEE Access 2026):
            PL_trans = P_LoS * PL_LoS + (1 - P_LoS) * PL_NLoS
        """
        d_2d = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)
        f_ghz = f_hz / 1e9

        h_bs = float(hb if hb is not None else self.hb_default)
        h_ut = float(hm if hm is not None else self.hm_default)

        # Parameter checks
        if np.any(d_2d <= 0):
            raise InvalidParameterError("Distance must be strictly positive.")
        if np.any(f_ghz <= 0):
            raise InvalidParameterError("Frequency must be strictly positive.")

        self.validate_parameters(
            strict=strict,
            distance_m=d_2d,
            frequency_hz=f_hz,
            hb_m=h_bs,
            hm_m=h_ut,
        )

        # 3D propagation distance
        delta_h = h_bs - h_ut
        d_3d = np.sqrt(d_2d**2 + delta_h**2)
        d_3d_safe = np.maximum(d_3d, 1.0)

        # 1. LoS Path Loss
        pl_los = 32.4 + 21.0 * np.log10(d_3d_safe) + 20.0 * np.log10(f_ghz)

        # 2. NLoS Path Loss
        pl_nlos_prime = 22.4 + 35.3 * np.log10(d_3d_safe) + 21.3 * np.log10(f_ghz)
        pl_nlos = np.maximum(pl_los, pl_nlos_prime)

        active_mode = (mode_override or self.mode).lower().strip()

        if active_mode == "los":
            res = pl_los
        elif active_mode == "nlos":
            res = pl_nlos
        elif active_mode == "transition":
            p_los = calculate_3gpp_los_probability(d_2d)
            res = p_los * pl_los + (1.0 - p_los) * pl_nlos
        else:
            raise InvalidParameterError(f"Unknown mode: {active_mode}")

        return float(res) if np.isscalar(distance) else res


class CloseInMMWaveModel(PropagationModel):
    """
    Close-In (CI) Free-Space Reference Distance mmWave Propagation Model.

    Formulation (Rappaport et al. & Inam Ullah IEEE Access 2026):
        PL_CI(f, d) = FSPL(f, 1m) + 10 * n * log10(d)
        where FSPL(f, 1m) = 20 * log10(4 * pi * f / c) = 32.4 + 20 * log10(f_GHz)
    """

    def __init__(self, n: float = 2.1, d0_m: float = 1.0):
        super().__init__(
            name="Close-In (CI) mmWave Model",
            classification="Empirical mmWave Model",
            description="Close-In free-space reference distance model standard for 28/39/73 GHz channels.",
        )
        self.n = n
        self.d0_m = d0_m

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (1.0, 2000.0),
            "frequency_hz": (0.5e9, 100.0e9),
        }

    def calculate_path_loss(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        n: Optional[float] = None,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)
        f_ghz = f_hz / 1e9

        if np.any(d_m <= 0) or np.any(f_hz <= 0):
            raise InvalidParameterError("Distance and frequency must be positive.")

        self.validate_parameters(strict=strict, distance_m=d_m, frequency_hz=f_hz)

        path_loss_exp = n if n is not None else self.n
        # 1-meter free space reference loss
        fspl_1m = 32.44 + 20.0 * np.log10(f_ghz)
        d_ratio = np.maximum(d_m / self.d0_m, 1.0)
        pl = fspl_1m + 10.0 * path_loss_exp * np.log10(d_ratio)

        return float(pl) if np.isscalar(distance) else pl
