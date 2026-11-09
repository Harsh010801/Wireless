"""
Free Space Path Loss (Friis) Model.

Mathematical Formulation:
    FSPL = (4 * pi * d / lambda)^2 = (4 * pi * d * f / c)^2
    In decibels:
    FSPL (dB) = 20 * log10(d) + 20 * log10(f) + 20 * log10(4 * pi / c)
              = 20 * log10(d_km) + 20 * log10(f_MHz) + 32.45
"""

import math
from typing import Any, Dict, Tuple, Union
import numpy as np

from propagation.core.units import SPEED_OF_LIGHT, to_hz, to_meters
from propagation.models.base import PropagationModel


class FreeSpacePathLoss(PropagationModel):
    """
    Theoretical Free Space Path Loss (Friis) Propagation Model.

    Assumes an idealized, unobstructed line-of-sight (LOS) channel in an infinite
    dielectric vacuum with no reflection, diffraction, absorption, or scattering.
    """

    def __init__(self):
        super().__init__(
            name="Free Space Path Loss (Friis)",
            classification="Theoretical",
            description="Idealized free-space line-of-sight propagation without obstructions or multipath reflections.",
        )
        # Constant: 20 * log10(4 * pi / c) ~= -147.552216695
        self._c_const_db = 20.0 * math.log10(4.0 * math.pi / SPEED_OF_LIGHT)

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        """
        Friis model is theoretically valid for any far-field distance d > 0 and f > 0.
        Practical physical engineering bounds: 0.1 m to 1,000,000 m (1,000 km), 1 MHz to 300 GHz.
        """
        return {
            "distance_m": (0.01, 1e8),
            "frequency_hz": (1e5, 3e11),
        }

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
        Calculate free space path loss in dB.

        Parameters:
            distance: Distance value or array.
            frequency: Carrier frequency value or array.
            distance_unit: 'm' or 'km'.
            frequency_unit: 'Hz', 'MHz', 'GHz', etc.
            strict: If True, validate parameters strictly.

        Returns:
            Path loss in dB.
        """
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)

        self.validate_parameters(distance_m=d_m, frequency_hz=f_hz, strict=strict)

        # Vectorized calculation: FSPL(dB) = 20*log10(d) + 20*log10(f) + 20*log10(4*pi/c)
        pl_db = 20.0 * np.log10(d_m) + 20.0 * np.log10(f_hz) + self._c_const_db

        return float(pl_db) if np.isscalar(distance) and np.isscalar(frequency) else pl_db
