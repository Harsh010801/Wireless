"""
Okumura-Hata Empirical Propagation Model.

Closed-form parametric equations developed by Hata (1980) from Okumura's graphical curves.

Valid Ranges:
    Frequency (f): 150 MHz to 1500 MHz
    Distance (d): 1 km to 20 km
    Base station height (h_b): 30 m to 200 m
    Mobile antenna height (h_m): 1 m to 10 m
"""

from typing import Any, Dict, Optional, Tuple, Union
import warnings
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import from_meters, to_hz, to_meters
from propagation.models.base import PropagationModel


class HataModel(PropagationModel):
    """
    Standard Okumura-Hata Propagation Model.

    Parameters:
        hb_default: Base station antenna height in meters (default: 30.0 m).
        hm_default: Mobile antenna height in meters (default: 1.5 m).
        environment: 'urban_medium', 'urban_large', 'suburban', or 'rural'/'open' (default: 'urban_medium').
    """

    def __init__(
        self,
        hb_default: float = 30.0,
        hm_default: float = 1.5,
        environment: str = "urban_medium",
    ):
        super().__init__(
            name="Okumura-Hata Model",
            classification="Empirical",
            description="Empirical closed-form cellular path loss model for macrocellular environments up to 1.5 GHz.",
        )
        if hb_default <= 0 or hm_default <= 0:
            raise InvalidParameterError(f"Antenna heights must be strictly positive: hb={hb_default}, hm={hm_default}")

        self.hb_default = float(hb_default)
        self.hm_default = float(hm_default)

        env_norm = self._normalize_environment(environment)
        self.environment = env_norm

    def _normalize_environment(self, env: str) -> str:
        e = env.strip().lower()
        if e in {"urban", "urban_medium", "medium_city", "small_city"}:
            return "urban_medium"
        elif e in {"urban_large", "large_city", "metropolitan"}:
            return "urban_large"
        elif e in {"suburban"}:
            return "suburban"
        elif e in {"rural", "open", "open_rural"}:
            return "rural"
        raise InvalidParameterError(
            f"Unsupported environment '{env}'. Use 'urban_medium', 'urban_large', 'suburban', or 'rural'."
        )

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        """Calibrated empirical limits of Hata (1980)."""
        return {
            "distance_m": (1000.0, 20000.0),    # 1 km to 20 km
            "frequency_hz": (150e6, 1500e6),    # 150 MHz to 1500 MHz
            "hb_m": (30.0, 200.0),               # 30 m to 200 m
            "hm_m": (1.0, 10.0),                 # 1 m to 10 m
        }

    def mobile_antenna_correction(
        self, hm: float, f_mhz: Union[float, np.ndarray], city_type: str = "urban_medium"
    ) -> Union[float, np.ndarray]:
        """
        Calculate mobile antenna height correction factor a(h_m) in dB.

        Parameters:
            hm: Mobile station antenna height in meters.
            f_mhz: Carrier frequency in MHz.
            city_type: 'urban_medium' or 'urban_large'.
        """
        log_f = np.log10(f_mhz)
        if city_type == "urban_large":
            # For large cities:
            # f <= 300 MHz: a(hm) = 8.29 * (log10(1.54 * hm))^2 - 1.1
            # f > 300 MHz: a(hm) = 3.2 * (log10(11.75 * hm))^2 - 4.97
            if np.all(f_mhz <= 300.0):
                return 8.29 * ((np.log10(1.54 * hm)) ** 2) - 1.1
            elif np.all(f_mhz > 300.0):
                return 3.2 * ((np.log10(11.75 * hm)) ** 2) - 4.97
            else:
                cond = f_mhz <= 300.0
                low = 8.29 * ((np.log10(1.54 * hm)) ** 2) - 1.1
                high = 3.2 * ((np.log10(11.75 * hm)) ** 2) - 4.97
                return np.where(cond, low, high)
        else:
            # Small and medium-sized city standard equation:
            # a(hm) = (1.1 * log10(f) - 0.7) * hm - (1.56 * log10(f) - 0.8)
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
        Calculate Okumura-Hata path loss in dB.

        Supported kwargs:
            hb: Base station antenna height in meters.
            hm: Mobile antenna height in meters.
            environment: Override environment ('urban_medium', 'urban_large', 'suburban', 'rural').
        """
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)

        hb = float(kwargs.get("hb", self.hb_default))
        hm = float(kwargs.get("hm", self.hm_default))
        env = self._normalize_environment(kwargs.get("environment", self.environment))

        if hb <= 0 or hm <= 0:
            raise InvalidParameterError(f"Antenna heights must be strictly positive: hb={hb}, hm={hm}")

        ranges = self.get_valid_range()
        if hb < ranges["hb_m"][0] or hb > ranges["hb_m"][1]:
            msg = f"[Hata] Base antenna height hb={hb}m is outside valid range {ranges['hb_m']}m."
            if strict:
                raise InvalidParameterError(msg)
            warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        if hm < ranges["hm_m"][0] or hm > ranges["hm_m"][1]:
            msg = f"[Hata] Mobile antenna height hm={hm}m is outside valid range {ranges['hm_m']}m."
            if strict:
                raise InvalidParameterError(msg)
            warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        self.validate_parameters(distance_m=d_m, frequency_hz=f_hz, strict=strict)

        d_km = from_meters(d_m, to_unit="km")
        f_mhz = f_hz / 1e6

        log_f = np.log10(f_mhz)
        log_hb = np.log10(hb)
        log_d = np.log10(d_km)

        # Mobile antenna correction
        city_type = "urban_large" if env == "urban_large" else "urban_medium"
        a_hm = self.mobile_antenna_correction(hm, f_mhz, city_type=city_type)

        # Urban Path Loss baseline:
        # PL_urban = 69.55 + 26.16*log10(f) - 13.82*log10(hb) - a(hm) + [44.9 - 6.55*log10(hb)]*log10(d)
        pl_urban = 69.55 + 26.16 * log_f - 13.82 * log_hb - a_hm + (44.9 - 6.55 * log_hb) * log_d

        if env in {"urban_medium", "urban_large"}:
            pl_db = pl_urban
        elif env == "suburban":
            # PL_suburban = PL_urban - 2 * [log10(f / 28)]^2 - 5.4
            pl_db = pl_urban - 2.0 * ((np.log10(f_mhz / 28.0)) ** 2) - 5.4
        elif env == "rural":
            # PL_rural = PL_urban - 4.78 * (log10(f))^2 + 18.33 * log10(f) - 40.94
            pl_db = pl_urban - 4.78 * (log_f**2) + 18.33 * log_f - 40.94
        else:
            pl_db = pl_urban

        pl_db = np.maximum(pl_db, 0.0)
        return float(pl_db) if np.isscalar(distance) and np.isscalar(frequency) else pl_db

