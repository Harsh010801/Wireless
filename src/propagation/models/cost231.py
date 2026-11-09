"""
COST-231 Hata Empirical Propagation Model.

European Cooperative for Scientific and Technical Research (COST) extension
of the Hata model to higher cellular frequencies (1500 MHz to 2000 MHz).

Mathematical Formulation:
    PL (dB) = 46.3 + 33.9 * log10(f) - 13.82 * log10(hb) - a(hm) +
              (44.9 - 6.55 * log10(hb)) * log10(d) + C_M

Where:
    f: Carrier frequency in MHz (1500 to 2000 MHz)
    d: Distance in km (1 to 20 km)
    hb: Base station antenna height in meters (30 to 200 m)
    hm: Mobile antenna height in meters (1 to 10 m)
    C_M: Constant correction factor (0 dB for medium cities/suburban, 3 dB for metropolitan centers)
"""

from typing import Any, Dict, Optional, Tuple, Union
import warnings
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import from_meters, to_hz, to_meters
from propagation.models.base import PropagationModel


class COST231HataModel(PropagationModel):
    """
    COST-231 Hata Model for 1.5 GHz to 2.0 GHz macrocellular propagation.

    Parameters:
        hb_default: Base station antenna height in meters (default: 30.0 m).
        hm_default: Mobile antenna height in meters (default: 1.5 m).
        environment: 'medium_city', 'suburban', or 'metropolitan'/'urban_dense' (default: 'medium_city').
    """

    def __init__(
        self,
        hb_default: float = 30.0,
        hm_default: float = 1.5,
        environment: str = "medium_city",
    ):
        super().__init__(
            name="COST-231 Hata Model",
            classification="Empirical",
            description="European extension of Okumura-Hata for PCS/cellular bands from 1.5 GHz to 2.0 GHz.",
        )
        if hb_default <= 0 or hm_default <= 0:
            raise InvalidParameterError(f"Antenna heights must be positive: hb={hb_default}, hm={hm_default}")

        self.hb_default = float(hb_default)
        self.hm_default = float(hm_default)

        env_norm, cm = self._parse_environment(environment)
        self.environment = env_norm
        self.cm_default = cm

    def _parse_environment(self, env: str) -> Tuple[str, float]:
        e = env.strip().lower()
        if e in {"metropolitan", "urban_dense", "dense_urban", "large_city"}:
            return "metropolitan", 3.0
        elif e in {"medium_city", "urban_medium", "urban", "suburban", "suburban_center"}:
            return "medium_city", 0.0
        raise InvalidParameterError(
            f"Unsupported environment '{env}'. Use 'medium_city', 'suburban', or 'metropolitan'."
        )

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        """Calibrated empirical limits of COST-231."""
        return {
            "distance_m": (1000.0, 20000.0),    # 1 km to 20 km
            "frequency_hz": (1500e6, 2000e6),   # 1500 MHz to 2000 MHz
            "hb_m": (30.0, 200.0),               # 30 m to 200 m
            "hm_m": (1.0, 10.0),                 # 1 m to 10 m
        }

    def mobile_antenna_correction(
        self, hm: float, f_mhz: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        """
        Calculate COST-231 mobile antenna height correction factor a(h_m) in dB.
        Formula:
            a(hm) = (1.1 * log10(f) - 0.7) * hm - (1.56 * log10(f) - 0.8)
        """
        log_f = np.log10(f_mhz)
        return (1.1 * log_f - 0.7) * hm - (1.56 * log_f - 0.8)

    def calculate_path_loss(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        """
        Calculate COST-231 Hata path loss in dB.

        Supported kwargs:
            hb: Base station antenna height in meters.
            hm: Mobile antenna height in meters.
            environment: Override environment ('medium_city', 'suburban', 'metropolitan').
            cm: Explicitly override correction factor C_M in dB (0 or 3 dB).
        """
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)

        hb = float(kwargs.get("hb", self.hb_default))
        hm = float(kwargs.get("hm", self.hm_default))

        if "environment" in kwargs:
            env, cm_from_env = self._parse_environment(kwargs["environment"])
            cm = float(kwargs.get("cm", cm_from_env))
        else:
            env = self.environment
            cm = float(kwargs.get("cm", self.cm_default))

        if hb <= 0 or hm <= 0:
            raise InvalidParameterError(f"Antenna heights must be strictly positive: hb={hb}, hm={hm}")

        ranges = self.get_valid_range()
        if hb < ranges["hb_m"][0] or hb > ranges["hb_m"][1]:
            msg = f"[COST-231] Base antenna height hb={hb}m is outside valid range {ranges['hb_m']}m."
            if strict:
                raise InvalidParameterError(msg)
            warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        if hm < ranges["hm_m"][0] or hm > ranges["hm_m"][1]:
            msg = f"[COST-231] Mobile antenna height hm={hm}m is outside valid range {ranges['hm_m']}m."
            if strict:
                raise InvalidParameterError(msg)
            warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        self.validate_parameters(distance_m=d_m, frequency_hz=f_hz, strict=strict)

        d_km = from_meters(d_m, to_unit="km")
        f_mhz = f_hz / 1e6

        log_f = np.log10(f_mhz)
        log_hb = np.log10(hb)
        log_d = np.log10(d_km)

        a_hm = self.mobile_antenna_correction(hm, f_mhz)

        # Formula:
        # PL = 46.3 + 33.9*log10(f) - 13.82*log10(hb) - a(hm) + [44.9 - 6.55*log10(hb)]*log10(d) + CM
        pl_db = 46.3 + 33.9 * log_f - 13.82 * log_hb - a_hm + (44.9 - 6.55 * log_hb) * log_d + cm

        pl_db = np.maximum(pl_db, 0.0)
        return float(pl_db) if np.isscalar(distance) and np.isscalar(frequency) else pl_db

