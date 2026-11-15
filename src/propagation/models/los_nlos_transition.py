"""
Statistical LoS-NLoS State Transition & Hybrid Channel Model.

References:
- Ullah, El-Sayed, Dowhuszko, Hamalainen, "Statistical Path Loss Modeling of
  LoS-NLoS Transitions for mmWave Communications in Urban Environments,"
  IEEE Access, 2026, doi:10.1109/ACCESS.2026.3741615
- 3GPP TR 38.901 Rel-17/19 Channel Model for frequencies 0.5 to 100 GHz
"""

from typing import Any, Dict, Optional, Tuple, Union
import numpy as np

from propagation.core.exceptions import InvalidParameterError
from propagation.core.units import to_hz, to_meters
from propagation.models.base import PropagationModel
from propagation.models.three_gpp_tr38901 import ThreeGPPUMiModel, ThreeGPPUMaModel


class StatisticalLoSNLoSTransitionModel(PropagationModel):
    """
    Probabilistic / Hybrid LoS-NLoS Channel Model with Monte Carlo State Transitions.

    Implements:
    1. Analytical expectation:
       PL_mean(d) = P_LoS(d) * PL_LoS(d) + (1 - P_LoS(d)) * PL_NLoS(d)
    2. Monte Carlo state drawing (seed-controlled):
       State S in {LoS, NLoS} ~ Bernoulli(P_LoS(d))
       PL_realized(d) = PL_LoS + X_sigma_LoS  if S == LoS else  PL_NLoS + X_sigma_NLoS
    3. Analytical composite variance and outage probabilities across distance.
    """

    def __init__(
        self,
        environment: str = "umi",
        seed: int = 42,
        hbs_default: float = 10.0,
        hut_default: float = 1.5,
        sigma_los_db: float = 4.0,
        sigma_nlos_db: float = 7.82,
        **kwargs: Any,
    ):
        super().__init__(
            name="LoS-NLoS Statistical Transition (IEEE Access 2026)",
            classification="Stochastic Transition Model",
            description="Statistical transition and mixed-state channel model for 5G/6G mmWave (Inam Ullah et al. 2026).",
        )
        self.environment = environment.lower().strip()
        self.seed = int(seed)
        self.hbs_default = float(kwargs.get("h_bs", kwargs.get("hbs", hbs_default)))
        self.hut_default = float(kwargs.get("h_ut", kwargs.get("hut", hut_default)))
        self.sigma_los_db = float(sigma_los_db)
        self.sigma_nlos_db = float(sigma_nlos_db)

        self._umi_los = ThreeGPPUMiModel(mode="los", hbs_default=self.hbs_default, hut_default=self.hut_default)
        self._umi_nlos = ThreeGPPUMiModel(mode="nlos", hbs_default=self.hbs_default, hut_default=self.hut_default)

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (10.0, 5000.0),
            "frequency_hz": (0.5e9, 100.0e9),
        }

    def get_los_probability(self, distance_2d_m: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Compute LoS probability using 3GPP UMi formulation."""
        return ThreeGPPUMiModel.calculate_los_probability(distance_2d_m)

    def calculate_path_loss(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        mode: str = "expectation",  # 'expectation' or 'realization'
        seed: Optional[int] = None,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        """
        Calculate path loss:
          - mode='expectation': analytical smooth transition
          - mode='realization': Monte Carlo single-run realization with Bernoulli state
        """
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)

        self.validate_parameters(strict=strict, distance_m=d_m, frequency_hz=f_hz)

        pl_los = self._umi_los.calculate_path_loss(d_m, f_hz, distance_unit="m", frequency_unit="Hz", strict=False, **kwargs)
        pl_nlos = self._umi_nlos.calculate_path_loss(d_m, f_hz, distance_unit="m", frequency_unit="Hz", strict=False, **kwargs)
        p_los = self.get_los_probability(d_m)

        if mode == "expectation":
            res = p_los * pl_los + (1.0 - p_los) * pl_nlos
            return float(res) if np.isscalar(distance) else res

        # Monte Carlo realization
        rng = np.random.default_rng(self.seed if seed is None else seed)
        d_arr = np.atleast_1d(d_m)
        p_arr = np.atleast_1d(p_los)

        u = rng.uniform(0.0, 1.0, size=len(d_arr))
        is_los = u < p_arr

        # Shadow fading draws
        x_los = rng.normal(0.0, self.sigma_los_db, size=len(d_arr))
        x_nlos = rng.normal(0.0, self.sigma_nlos_db, size=len(d_arr))

        pl_los_arr = np.atleast_1d(pl_los)
        pl_nlos_arr = np.atleast_1d(pl_nlos)

        realized = np.where(is_los, pl_los_arr + x_los, pl_nlos_arr + x_nlos)
        return float(realized[0]) if np.isscalar(distance) else realized

    def calculate_transition_statistics(
        self,
        distance_m: Union[float, np.ndarray],
        frequency_hz: Union[float, np.ndarray],
        num_monte_carlo: int = 1000,
        seed: Optional[int] = None,
        rx_sensitivity_dbm: float = -100.0,
        tx_power_dbm: float = 30.0,
        tx_gain_dbi: float = 15.0,
        rx_gain_dbi: float = 0.0,
        system_loss_db: float = 2.0,
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Run repeated Monte Carlo state transitions across distance vector,
        evaluating mean, std dev, and outage probability.
        """
        d_m = to_meters(distance_m, unit=distance_unit)
        f_hz = to_hz(frequency_hz, unit=frequency_unit)
        rng = np.random.default_rng(self.seed if seed is None else seed)
        d_arr = np.asarray(d_m, dtype=np.float64)
        p_los = np.asarray(self.get_los_probability(d_arr), dtype=np.float64)

        pl_los = np.asarray(self._umi_los.calculate_path_loss(d_arr, f_hz, distance_unit="m", frequency_unit="Hz", strict=False))
        pl_nlos = np.asarray(self._umi_nlos.calculate_path_loss(d_arr, f_hz, distance_unit="m", frequency_unit="Hz", strict=False))

        eirp = tx_power_dbm + tx_gain_dbi - system_loss_db + rx_gain_dbi
        threshold_pl = eirp - rx_sensitivity_dbm

        realizations = np.zeros((num_monte_carlo, len(d_arr)), dtype=np.float64)
        for i in range(num_monte_carlo):
            u = rng.uniform(0.0, 1.0, size=len(d_arr))
            is_los = u < p_los
            x_los = rng.normal(0.0, self.sigma_los_db, size=len(d_arr))
            x_nlos = rng.normal(0.0, self.sigma_nlos_db, size=len(d_arr))
            realizations[i, :] = np.where(is_los, pl_los + x_los, pl_nlos + x_nlos)

        mean_pl = np.mean(realizations, axis=0)
        std_pl = np.std(realizations, axis=0)
        outage_prob = np.mean(realizations > threshold_pl, axis=0) * 100.0

        return {
            "distance_m": d_arr,
            "p_los": p_los,
            "mean_pl_db": mean_pl,
            "std_pl_db": std_pl,
            "outage_pct": outage_prob,
            "threshold_pl_db": np.full_like(d_arr, threshold_pl),
        }

    def generate_transition_realizations(
        self,
        distance_m: np.ndarray,
        frequency_hz: float,
        num_realizations: int = 5,
        seed: Optional[int] = None,
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
    ) -> np.ndarray:
        """Generate discrete Monte Carlo realization traces of LoS-NLoS channel transitions."""
        d_m = to_meters(distance_m, unit=distance_unit)
        f_hz = to_hz(frequency_hz, unit=frequency_unit)
        d_arr = np.asarray(d_m, dtype=np.float64)
        p_los = np.asarray(self.get_los_probability(d_arr), dtype=np.float64)
        pl_los = np.asarray(self._umi_los.calculate_path_loss(d_arr, f_hz, distance_unit="m", frequency_unit="Hz", strict=False))
        pl_nlos = np.asarray(self._umi_nlos.calculate_path_loss(d_arr, f_hz, distance_unit="m", frequency_unit="Hz", strict=False))

        rng = np.random.default_rng(self.seed if seed is None else seed)
        reals = np.zeros((num_realizations, len(d_arr)), dtype=np.float64)
        for i in range(num_realizations):
            u = rng.uniform(0.0, 1.0, size=len(d_arr))
            is_los = u < p_los
            x_los = rng.normal(0.0, self.sigma_los_db, size=len(d_arr))
            x_nlos = rng.normal(0.0, self.sigma_nlos_db, size=len(d_arr))
            reals[i, :] = np.where(is_los, pl_los + x_los, pl_nlos + x_nlos)
        return reals
