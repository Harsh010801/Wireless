"""
Log-Distance Path Loss Model.

Mathematical Formulation:
    PL(d) = PL(d0) + 10 * n * log10(d / d0)

Where:
    d0: Reference close-in distance (e.g., 1 m indoor, 1000 m outdoor macrocell)
    PL(d0): Path loss at reference distance (often computed via Free Space Friis)
    n: Path loss exponent capturing environment propagation characteristics
"""

from typing import Any, Dict, Optional, Tuple, Union
import warnings
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.units import SPEED_OF_LIGHT, to_hz, to_meters
from propagation.models.base import PropagationModel
from propagation.models.free_space import FreeSpacePathLoss


# Standard empirical path-loss exponents reported in wireless literature (Rappaport, Goldsmith)
ENVIRONMENT_EXPONENTS: Dict[str, float] = {
    "free_space": 2.0,
    "urban": 3.0,
    "urban_dense": 3.5,
    "suburban": 2.8,
    "rural": 2.2,
    "indoor_los": 1.7,
    "indoor_obstructed": 4.5,
    "shadowed_urban": 4.0,
}


class LogDistancePathLoss(PropagationModel):
    """
    Log-Distance Path Loss Model.

    Parameters:
        n: Path loss exponent (default: 2.0 for free space or look up via environment).
        d0_m: Reference close-in distance in meters (default: 1.0 m).
        pl_d0_db: Path loss at reference distance d0 in dB. If None, dynamically computed via FSPL.
        environment: Predefined environment preset ('urban', 'suburban', 'rural', 'indoor_los', etc.).
    """

    def __init__(
        self,
        n: Optional[float] = None,
        d0_m: float = 1.0,
        pl_d0_db: Optional[float] = None,
        environment: Optional[str] = None,
    ):
        super().__init__(
            name="Log-Distance Path Loss",
            classification="Empirical",
            description="Distance-dependent path loss model parameterized by reference distance and path loss exponent n.",
        )
        if d0_m <= 0:
            raise InvalidParameterError(f"Reference distance d0 must be strictly positive, got: {d0_m} m")

        self.d0_m = float(d0_m)
        self.pl_d0_db = float(pl_d0_db) if pl_d0_db is not None else None
        self._fspl_calc = FreeSpacePathLoss()

        if environment is not None:
            env_key = environment.strip().lower()
            if env_key in ENVIRONMENT_EXPONENTS:
                self.n = ENVIRONMENT_EXPONENTS[env_key]
                self.environment = env_key
            else:
                raise InvalidParameterError(
                    f"Unknown environment '{environment}'. Available presets: {list(ENVIRONMENT_EXPONENTS.keys())}"
                )
        else:
            self.n = float(n) if n is not None else 2.0
            self.environment = "custom"

        if self.n <= 0:
            raise InvalidParameterError(f"Path loss exponent n must be strictly positive (> 0), got: {self.n}")

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (self.d0_m, 100000.0),
            "frequency_hz": (1e5, 100e9),
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
        Calculate Log-Distance path loss in dB.

        Supported kwargs:
            n: Override path loss exponent.
            d0: Override reference distance in meters.
            pl_d0: Override reference path loss in dB.
        """
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)

        n_val = float(kwargs.get("n", self.n))
        d0_val = float(kwargs.get("d0", self.d0_m))
        pl_d0_val = kwargs.get("pl_d0", self.pl_d0_db)

        if d0_val <= 0:
            raise InvalidParameterError(f"Reference distance d0 must be positive, got: {d0_val}")
        if n_val <= 0:
            raise InvalidParameterError(f"Exponent n must be positive, got: {n_val}")

        self.validate_parameters(distance_m=d_m, frequency_hz=f_hz, strict=strict)

        d_arr = np.asarray(d_m, dtype=np.float64)

        if np.any(d_arr < d0_val):
            msg = f"Distance contains values smaller than reference distance d0 ({d0_val} m)."
            if strict:
                raise InvalidParameterError(msg)
            warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        # Determine reference path loss PL(d0)
        if pl_d0_val is None:
            # Standard procedure: compute FSPL at distance d0
            pl_d0 = self._fspl_calc.calculate_path_loss(
                distance=d0_val,
                frequency=f_hz,
                distance_unit="m",
                frequency_unit="Hz",
                strict=False,
            )
        else:
            pl_d0 = float(pl_d0_val)

        # Formula: PL(d) = PL(d0) + 10 * n * log10(d / d0)
        # For d < d0 in non-strict mode, prevent negative logarithmic drop below PL(d0)
        ratio = np.maximum(d_arr / d0_val, 1e-12)
        pl_db = pl_d0 + 10.0 * n_val * np.log10(ratio)

        return float(pl_db) if np.isscalar(distance) and np.isscalar(frequency) else pl_db
