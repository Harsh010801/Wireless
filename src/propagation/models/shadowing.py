"""
Log-Normal Shadowing (Large-Scale Fading) Propagation Model.

Mathematical Formulation:
    PL(d) = PL(d0) + 10 * n * log10(d / d0) + X_sigma

Where:
    X_sigma ~ Normal(0, sigma^2) represents random shadow fading induced
    by clutter, terrain variations, buildings, and foliage.
    sigma: Shadowing standard deviation in dB (typically 4 dB to 12 dB).
"""

from typing import Any, Dict, Optional, Tuple, Union
import numpy as np
from scipy.special import erfc

from propagation.core.exceptions import InvalidParameterError
from propagation.core.units import to_hz, to_meters
from propagation.models.base import PropagationModel
from propagation.models.log_distance import LogDistancePathLoss


class LogNormalShadowing(PropagationModel):
    """
    Stochastic Log-Normal Shadowing Model.

    Parameters:
        n: Path loss exponent (default: 3.0 for urban environment).
        sigma_db: Shadowing standard deviation in dB (default: 6.0 dB).
        d0_m: Reference close-in distance in meters (default: 1.0 m).
        pl_d0_db: Path loss at reference distance d0 in dB (None -> computed via FSPL).
        seed: Default random seed for fully reproducible stochastic simulations.
    """

    def __init__(
        self,
        n: float = 3.0,
        sigma_db: float = 6.0,
        d0_m: float = 1.0,
        pl_d0_db: Optional[float] = None,
        seed: Optional[int] = 42,
    ):
        super().__init__(
            name="Log-Normal Shadowing",
            classification="Stochastic",
            description="Stochastic large-scale fading model combining distance decay with Gaussian shadow attenuation.",
        )
        if sigma_db < 0:
            raise InvalidParameterError(f"Shadowing standard deviation sigma must be non-negative, got: {sigma_db}")
        if d0_m <= 0:
            raise InvalidParameterError(f"Reference distance d0 must be strictly positive, got: {d0_m}")
        if n <= 0:
            raise InvalidParameterError(f"Path loss exponent n must be strictly positive, got: {n}")

        self.n = float(n)
        self.sigma_db = float(sigma_db)
        self.d0_m = float(d0_m)
        self.pl_d0_db = float(pl_d0_db) if pl_d0_db is not None else None
        self.default_seed = seed
        self._log_dist = LogDistancePathLoss(n=self.n, d0_m=self.d0_m, pl_d0_db=self.pl_d0_db)

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (self.d0_m, 100000.0),
            "frequency_hz": (1e5, 100e9),
            "sigma_db": (0.0, 20.0),
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
        Calculate path loss in dB.

        Supported kwargs:
            sigma: Override shadowing standard deviation in dB.
            seed: Seed for random generator (None or int). If seed is None and include_shadowing=False,
                  returns deterministic mean path loss.
            include_shadowing: bool (default: True). If False, returns purely the deterministic median.
        """
        include_shadowing = bool(kwargs.get("include_shadowing", True))
        sigma = float(kwargs.get("sigma", self.sigma_db))
        seed = kwargs.get("seed", self.default_seed)

        if sigma < 0:
            raise InvalidParameterError(f"Sigma must be non-negative, got: {sigma}")

        # Compute deterministic median path loss
        mean_pl = self._log_dist.calculate_path_loss(
            distance=distance,
            frequency=frequency,
            distance_unit=distance_unit,
            frequency_unit=frequency_unit,
            strict=strict,
            **kwargs,
        )

        if not include_shadowing or sigma == 0.0:
            return mean_pl

        # Generate Gaussian random shadow realization
        rng = np.random.default_rng(seed)
        if np.isscalar(mean_pl):
            shadow_noise = rng.normal(0.0, sigma)
            return float(mean_pl + shadow_noise)
        else:
            mean_arr = np.asarray(mean_pl, dtype=np.float64)
            shadow_noise = rng.normal(0.0, sigma, size=mean_arr.shape)
            return mean_arr + shadow_noise

    def generate_realizations(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        num_realizations: int = 100,
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        seed: Optional[int] = 42,
        **kwargs: Any,
    ) -> np.ndarray:
        """
        Generate multiple Monte Carlo realizations of shadowed path loss trajectories.

        Returns:
            2D NumPy array of shape (num_realizations, len(distance)).
        """
        if num_realizations <= 0:
            raise InvalidParameterError(f"num_realizations must be positive integer, got: {num_realizations}")

        rng = np.random.default_rng(seed)
        mean_pl = self._log_dist.calculate_path_loss(
            distance=distance,
            frequency=frequency,
            distance_unit=distance_unit,
            frequency_unit=frequency_unit,
            strict=False,
            **kwargs,
        )
        mean_arr = np.atleast_1d(np.asarray(mean_pl, dtype=np.float64))
        noise = rng.normal(0.0, self.sigma_db, size=(num_realizations, len(mean_arr)))
        return mean_arr + noise

    def calculate_bounds(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        confidence: float = 0.95,
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        **kwargs: Any,
    ) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray], Union[float, np.ndarray]]:
        """
        Compute deterministic median path loss and symmetric Gaussian confidence bounds.
        For 95% confidence, z ~= 1.95996; bounds are [mean - z*sigma, mean + z*sigma].

        Returns:
            Tuple of (mean_pl, lower_bound_pl, upper_bound_pl) in dB.
        """
        from scipy.stats import norm

        mean_pl = self._log_dist.calculate_path_loss(
            distance=distance,
            frequency=frequency,
            distance_unit=distance_unit,
            frequency_unit=frequency_unit,
            strict=False,
            **kwargs,
        )
        sigma = float(kwargs.get("sigma", self.sigma_db))
        z = norm.ppf((1.0 + confidence) / 2.0)
        margin = z * sigma

        lower_pl = mean_pl - margin
        upper_pl = mean_pl + margin
        return mean_pl, lower_pl, upper_pl

    def calculate_outage_probability(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        rx_sensitivity_dbm: float,
        tx_power_dbm: float = 30.0,
        tx_gain_dbi: float = 0.0,
        rx_gain_dbi: float = 0.0,
        system_loss_db: float = 0.0,
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        """
        Calculate analytical link outage probability:
            P_outage = P(P_r < P_threshold) = Q( (P_r_mean - P_threshold) / sigma )
                     = 0.5 * erfc( (P_r_mean - P_threshold) / (sqrt(2) * sigma) )

        Parameters:
            rx_sensitivity_dbm: Receiver minimum power threshold (gamma_th).
        """
        mean_pl = self._log_dist.calculate_path_loss(
            distance=distance,
            frequency=frequency,
            distance_unit=distance_unit,
            frequency_unit=frequency_unit,
            strict=False,
            **kwargs,
        )
        sigma = float(kwargs.get("sigma", self.sigma_db))
        if sigma <= 0:
            pr_mean = tx_power_dbm + tx_gain_dbi + rx_gain_dbi - mean_pl - system_loss_db
            return np.where(pr_mean < rx_sensitivity_dbm, 1.0, 0.0)

        pr_mean = tx_power_dbm + tx_gain_dbi + rx_gain_dbi - mean_pl - system_loss_db
        # Argument for Q-function: (pr_mean - gamma_th) / sigma
        arg = (pr_mean - rx_sensitivity_dbm) / (np.sqrt(2.0) * sigma)
        p_outage = 0.5 * erfc(arg)
        return float(p_outage) if np.isscalar(p_outage) and np.isscalar(distance) else p_outage

