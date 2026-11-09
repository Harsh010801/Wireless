"""
Two-Ray Ground Reflection Propagation Model.

Models line-of-sight (LOS) propagation combined with a single specular ground-reflected wave.

Formulation:
    Direct distance: d_dir = sqrt(d^2 + (h_t - h_r)^2)
    Reflected distance: d_ref = sqrt(d^2 + (h_t + h_r)^2)
    Phase difference: delta_phi = (2 * pi / lambda) * (d_ref - d_dir)
    Exact Received Power Ratio:
        | (lambda / 4pi) * ( exp(-j*k*d_dir)/d_dir + Gamma * exp(-j*k*d_ref)/d_ref ) |^2
    Asymptotic (large distance d >> 4*pi*h_t*h_r / lambda):
        PL (dB) = 40*log10(d) - 20*log10(h_t) - 20*log10(h_r)
"""

from typing import Any, Dict, Optional, Tuple, Union
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import SPEED_OF_LIGHT, to_hz, to_meters, wavelength
from propagation.models.base import PropagationModel


class TwoRayGroundReflection(PropagationModel):
    """
    Two-Ray Ground Reflection Model.

    Parameters:
        ht_default: Default transmitter antenna height in meters (default: 30.0 m).
        hr_default: Default receiver antenna height in meters (default: 1.5 m).
        ground_reflection_coeff: Specular ground reflection coefficient Gamma (default: -1.0).
        mode: Calculation mode: 'exact', 'asymptotic', or 'hybrid' (default: 'exact').
    """

    def __init__(
        self,
        ht_default: float = 30.0,
        hr_default: float = 1.5,
        ground_reflection_coeff: complex = -1.0 + 0.0j,
        mode: str = "exact",
    ):
        super().__init__(
            name="Two-Ray Ground Reflection",
            classification="Theoretical",
            description="Multipath ground reflection model combining direct LOS ray with specular earth-reflected ray.",
        )
        if ht_default <= 0 or hr_default <= 0:
            raise InvalidParameterError(f"Antenna heights must be strictly positive: ht={ht_default}, hr={hr_default}")

        self.ht_default = float(ht_default)
        self.hr_default = float(hr_default)
        self.ground_reflection_coeff = complex(ground_reflection_coeff)
        if mode.lower() not in {"exact", "asymptotic", "hybrid"}:
            raise InvalidParameterError(f"Mode must be 'exact', 'asymptotic', or 'hybrid', got '{mode}'")
        self.mode = mode.lower()

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        """Physical engineering range for macro/microcell ground reflection analysis."""
        return {
            "distance_m": (1.0, 100000.0),
            "frequency_hz": (1e6, 60e9),
            "ht_m": (1.0, 500.0),
            "hr_m": (0.5, 50.0),
        }

    def crossover_distance(self, ht: float, hr: float, frequency_hz: float) -> float:
        """
        Calculate asymptotic crossover distance:
            d_c = (4 * pi * ht * hr) / lambda
        Beyond d_c, signal decays strictly as d^-4 (40 dB/decade).
        """
        lam = SPEED_OF_LIGHT / frequency_hz
        return (4.0 * np.pi * ht * hr) / lam

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
        Calculate Two-Ray path loss in dB.

        Supported kwargs:
            ht: Transmitter antenna height in meters (overrides ht_default).
            hr: Receiver antenna height in meters (overrides hr_default).
            gamma: Ground reflection coefficient (overrides ground_reflection_coeff).
            mode: 'exact', 'asymptotic', or 'hybrid' (overrides self.mode).
        """
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)

        ht = float(kwargs.get("ht", self.ht_default))
        hr = float(kwargs.get("hr", self.hr_default))
        gamma = complex(kwargs.get("gamma", self.ground_reflection_coeff))
        calc_mode = str(kwargs.get("mode", self.mode)).lower()

        if ht <= 0 or hr <= 0:
            raise InvalidParameterError(f"Antenna heights must be positive (> 0 m): ht={ht}, hr={hr}")

        self.validate_parameters(distance_m=d_m, frequency_hz=f_hz, strict=strict)

        d_arr = np.asarray(d_m, dtype=np.float64)
        lam = SPEED_OF_LIGHT / np.asarray(f_hz, dtype=np.float64)
        k = 2.0 * np.pi / lam

        if calc_mode == "asymptotic":
            # Asymptotic large-distance formula: PL(dB) = 40*log10(d) - 20*log10(ht) - 20*log10(hr)
            pl_db = 40.0 * np.log10(d_arr) - 20.0 * np.log10(ht) - 20.0 * np.log10(hr)
            # Ensure path loss is non-negative
            pl_db = np.maximum(pl_db, 0.0)

        elif calc_mode == "exact":
            d_dir = np.sqrt(d_arr**2 + (ht - hr)**2)
            d_ref = np.sqrt(d_arr**2 + (ht + hr)**2)
            delta_phi = k * (d_ref - d_dir)

            # Complex field superposition: E_tot = exp(-j*k*d_dir)/d_dir + gamma * exp(-j*k*d_ref)/d_ref
            term_dir = np.exp(-1j * k * d_dir) / d_dir
            term_ref = gamma * np.exp(-1j * k * d_ref) / d_ref
            e_total = term_dir + term_ref

            power_ratio = ((lam / (4.0 * np.pi)) ** 2) * (np.abs(e_total) ** 2)
            # Guard against potential division by zero or numerical singularity
            power_ratio = np.maximum(power_ratio, 1e-25)
            pl_db = -10.0 * np.log10(power_ratio)

        elif calc_mode == "hybrid":
            # Below crossover distance, evaluate exact multipath oscillations.
            # Above crossover distance, smoothly follow the asymptotic d^-4 trend.
            d_c = (4.0 * np.pi * ht * hr) / lam
            exact_val = self.calculate_path_loss(
                distance=d_m, frequency=f_hz, ht=ht, hr=hr, gamma=gamma, mode="exact"
            )
            asymp_val = self.calculate_path_loss(
                distance=d_m, frequency=f_hz, ht=ht, hr=hr, gamma=gamma, mode="asymptotic"
            )
            pl_db = np.where(d_arr <= d_c, exact_val, asymp_val)

        else:
            raise InvalidParameterError(f"Unsupported mode: '{calc_mode}'. Use 'exact', 'asymptotic', or 'hybrid'.")

        return float(pl_db) if np.isscalar(distance) and np.isscalar(frequency) else pl_db

