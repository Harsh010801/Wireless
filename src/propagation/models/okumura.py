"""
Okumura Propagation Model for Macrocellular Communication.

Based on Yoshihisa Okumura's classical extensive field measurements in Tokyo (1968).

Mathematical Formulation:
    PL (dB) = L_FSL + A_mu(f, d) - G(h_te) - G(h_re) - G_AREA

Valid Operating Ranges:
    Frequency (f): 150 MHz to 1920 MHz
    Distance (d): 1 km to 100 km
    Base station height (h_te): 30 m to 1000 m
    Mobile antenna height (h_re): 1 m to 10 m
"""

from typing import Any, Dict, Optional, Tuple, Union
import warnings
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import from_meters, to_hz, to_meters
from propagation.models.base import PropagationModel
from propagation.models.free_space import FreeSpacePathLoss


class OkumuraModel(PropagationModel):
    """
    Okumura Empirical Model for urban, suburban, and open macrocell propagation.

    Parameters:
        hte_default: Default base station antenna height in meters (default: 50.0 m).
        hre_default: Default mobile antenna height in meters (default: 1.5 m).
        environment: 'urban', 'suburban', 'quasi_open', or 'open'/'rural' (default: 'urban').
    """

    def __init__(
        self,
        hte_default: float = 50.0,
        hre_default: float = 1.5,
        environment: str = "urban",
    ):
        super().__init__(
            name="Okumura Model",
            classification="Empirical",
            description="Classical Japanese macrocellular propagation model based on extensive Tokyo drive tests.",
        )
        if hte_default <= 0 or hre_default <= 0:
            raise InvalidParameterError(f"Antenna heights must be strictly positive: hte={hte_default}, hre={hre_default}")

        self.hte_default = float(hte_default)
        self.hre_default = float(hre_default)

        valid_envs = {"urban", "suburban", "quasi_open", "open", "rural"}
        env_clean = environment.strip().lower()
        if env_clean not in valid_envs:
            raise InvalidParameterError(f"Unknown environment '{environment}'. Valid options: {valid_envs}")
        self.environment = "open" if env_clean == "rural" else env_clean
        self._fspl = FreeSpacePathLoss()

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        """Calibrated bounds established by Okumura (1968)."""
        return {
            "distance_m": (1000.0, 100000.0),      # 1 km to 100 km
            "frequency_hz": (150e6, 1920e6),        # 150 MHz to 1920 MHz
            "hte_m": (30.0, 1000.0),                # 30 m to 1000 m
            "hre_m": (1.0, 10.0),                   # 1 m to 10 m
        }

    def _calculate_a_mu(self, f_mhz: Union[float, np.ndarray], d_km: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Analytical fit for Okumura's median attenuation A_mu(f, d) relative to free space
        in an urban area with hte = 200 m and hre = 3 m.
        """
        # Hata-Delisle analytical parameterization of Okumura's urban baseline
        h_ref = 200.0
        log_f = np.log10(f_mhz)
        log_d = np.log10(d_km)
        log_href = np.log10(h_ref)

        urban_baseline = 69.55 + 26.16 * log_f - 13.82 * log_href + (44.9 - 6.55 * log_href) * log_d
        fspl_ref = 32.45 + 20.0 * log_f + 20.0 * log_d
        a_mu = urban_baseline - fspl_ref
        return np.maximum(a_mu, 0.0)

    def _calculate_g_area(self, f_mhz: Union[float, np.ndarray], env: str) -> Union[float, np.ndarray]:
        """Calculate environmental area gain G_AREA (dB)."""
        log_f = np.log10(f_mhz)
        if env == "urban":
            return 0.0
        elif env == "suburban":
            return 2.0 * ((np.log10(f_mhz / 28.0)) ** 2) + 5.4
        elif env == "quasi_open":
            return 4.78 * (log_f**2) - 18.33 * log_f + 35.94
        elif env in {"open", "rural"}:
            return 4.78 * (log_f**2) - 18.33 * log_f + 40.94
        return 0.0

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
        Calculate Okumura path loss in dB.

        Supported kwargs:
            hte: Base station effective antenna height in meters.
            hre: Mobile antenna effective height in meters.
            environment: Override environment ('urban', 'suburban', 'open', 'rural').
        """
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)

        hte = float(kwargs.get("hte", self.hte_default))
        hre = float(kwargs.get("hre", self.hre_default))
        env = str(kwargs.get("environment", self.environment)).lower()
        if env == "rural":
            env = "open"

        # Validate antenna heights
        if hte <= 0 or hre <= 0:
            raise InvalidParameterError(f"Antenna heights must be positive: hte={hte}, hre={hre}")

        ranges = self.get_valid_range()
        if hte < ranges["hte_m"][0] or hte > ranges["hte_m"][1]:
            msg = f"[Okumura] Base antenna height hte={hte}m is outside valid range {ranges['hte_m']}m."
            if strict:
                raise InvalidParameterError(msg)
            warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        if hre < ranges["hre_m"][0] or hre > ranges["hre_m"][1]:
            msg = f"[Okumura] Mobile antenna height hre={hre}m is outside valid range {ranges['hre_m']}m."
            if strict:
                raise InvalidParameterError(msg)
            warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        self.validate_parameters(distance_m=d_m, frequency_hz=f_hz, strict=strict)

        d_km = from_meters(d_m, to_unit="km")
        f_mhz = f_hz / 1e6

        # 1. Free Space Path Loss L_FSL
        l_fsl = self._fspl.calculate_path_loss(
            distance=d_m, frequency=f_hz, distance_unit="m", frequency_unit="Hz", strict=False
        )

        # 2. Median attenuation A_mu(f, d)
        a_mu = self._calculate_a_mu(f_mhz, d_km)

        # 3. Base station antenna height gain G(h_te)
        # G(h_te) = 20 * log10(h_te / 200) for 30m <= h_te <= 1000m
        g_hte = 20.0 * np.log10(hte / 200.0)

        # 4. Mobile station antenna height gain G(h_re)
        # G(h_re) = 10 * log10(h_re / 3) for h_re <= 3m; 20 * log10(h_re / 3) for 3m < h_re <= 10m
        if hre <= 3.0:
            g_hre = 10.0 * np.log10(hre / 3.0)
        else:
            g_hre = 20.0 * np.log10(hre / 3.0)

        # 5. Environment area gain G_AREA
        g_area = self._calculate_g_area(f_mhz, env)

        # Formula: PL = L_FSL + A_mu - G(h_te) - G(h_re) - G_AREA
        pl_db = l_fsl + a_mu - g_hte - g_hre - g_area
        pl_db = np.maximum(pl_db, 0.0)

        return float(pl_db) if np.isscalar(distance) and np.isscalar(frequency) else pl_db

