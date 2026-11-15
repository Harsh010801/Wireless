"""
Close-In (CI), CIF, and Floating-Intercept (ABG) Path Loss Models.

References:
- Sun et al., "Investigation of Prediction Accuracy, Sensitivity, and Parameter Stability
  of Large-Scale Propagation Path Loss Models for 5G Wireless Communications", IEEE Trans. Antennas Propag., 2016 / arXiv:1603.04404
- Rappaport et al., "Wideband Millimeter-Wave Propagation Measurements and Channel Models for Future Wireless Communication System Design", IEEE Trans. Commun.
"""

from typing import Any, Dict, Optional, Tuple, Union
import numpy as np

from propagation.core.exceptions import InvalidParameterError
from propagation.core.units import SPEED_OF_LIGHT, to_hz, to_meters
from propagation.models.base import PropagationModel


class CloseInModel(PropagationModel):
    """
    Close-In (CI) Free-Space Reference Distance Path Loss Model.

    Formulation:
        PL_CI(f, d) = FSPL(f, 1m) + 10 * n * log10(d) + X_sigma
        FSPL(f, 1m) = 20 * log10(4 * pi * f / c)

    CIF Extension (Frequency-dependent path loss exponent):
        n(f) = n * (1 + b * (f - f0) / f0)
        PL_CIF(f, d) = FSPL(f, 1m) + 10 * n(f) * log10(d) + X_sigma
    """

    PRESETS = {
        "umi_los": {"n": 2.1, "sigma_db": 4.0},
        "umi_nlos": {"n": 3.19, "sigma_db": 8.2},
        "uma_los": {"n": 2.8, "sigma_db": 4.1},
        "uma_nlos": {"n": 3.0, "sigma_db": 6.8},
        "inh_los": {"n": 1.7, "sigma_db": 1.5},
        "inh_nlos": {"n": 2.6, "sigma_db": 8.3},
    }

    def __init__(
        self,
        n: float = 2.1,
        sigma_db: float = 4.0,
        d0_m: float = 1.0,
        preset: Optional[str] = None,
        use_cif: bool = False,
        b_cif: float = 0.0,
        f0_hz: float = 1e9,
        **kwargs: Any,
    ):
        if preset and preset.lower() in self.PRESETS:
            p = self.PRESETS[preset.lower()]
            n = p["n"]
            sigma_db = p["sigma_db"]
        elif "n_nlos" in kwargs:
            n = kwargs["n_nlos"]
            sigma_db = kwargs.get("sigma_nlos", 8.2)

        super().__init__(
            name="Close-In (CI) Model" if not use_cif else "Close-In Frequency-Dependent (CIF) Model",
            classification="Empirical mmWave / 5G Model",
            description="Close-In 1-meter free space reference distance model for 0.5 to 100 GHz channels.",
        )
        self.n = float(n)
        self.sigma_db = float(sigma_db)
        self.d0_m = float(d0_m)
        self.use_cif = use_cif
        self.b_cif = float(b_cif)
        self.f0_hz = float(f0_hz)

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (1.0, 5000.0),
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

        self.validate_parameters(strict=strict, distance_m=d_m, frequency_hz=f_hz)

        d_arr = np.asarray(d_m, dtype=np.float64)
        f_arr = np.asarray(f_hz, dtype=np.float64)

        # 1-meter Free Space Path Loss: 20*log10(4*pi*f/c)
        fspl_1m = 20.0 * np.log10(4.0 * np.pi * f_arr / SPEED_OF_LIGHT)

        # Path loss exponent (with optional CIF frequency dependence)
        ple = float(n if n is not None else self.n)
        if self.use_cif:
            ple = ple * (1.0 + self.b_cif * (f_arr - self.f0_hz) / self.f0_hz)

        d_ratio = np.maximum(d_arr / self.d0_m, 1.0)
        pl = fspl_1m + 10.0 * ple * np.log10(d_ratio)

        return float(pl) if (np.isscalar(pl) or np.ndim(pl) == 0) else pl


class FloatingInterceptABGModel(PropagationModel):
    """
    Floating-Intercept / ABG (Alpha-Beta-Gamma) Path Loss Model.

    Formulation:
        PL_ABG(f, d) = 10 * alpha * log10(d) + beta + 10 * gamma * log10(fc) + X_sigma
        where fc is in GHz, d in meters, X_sigma ~ N(0, sigma^2).

    UMi Street-Canyon NLoS Standard Preset (matches 3GPP):
        alpha = 3.53, beta = 22.4, gamma = 2.13, sigma = 7.82 dB.
    """

    PRESETS = {
        "umi_nlos": {"alpha": 3.53, "beta": 22.4, "gamma": 2.13, "sigma_db": 7.82},
        "uma_nlos": {"alpha": 3.91, "beta": 13.54, "gamma": 2.0, "sigma_db": 6.0},
        "inh_nlos": {"alpha": 3.83, "beta": 17.30, "gamma": 2.49, "sigma_db": 8.03},
    }

    def __init__(
        self,
        alpha: float = 3.53,
        beta: float = 22.4,
        gamma: float = 2.13,
        sigma_db: float = 7.82,
        preset: Optional[str] = None,
    ):
        if preset and preset.lower() in self.PRESETS:
            p = self.PRESETS[preset.lower()]
            alpha = p["alpha"]
            beta = p["beta"]
            gamma = p["gamma"]
            sigma_db = p["sigma_db"]

        super().__init__(
            name="Floating-Intercept (ABG) Model",
            classification="Empirical Multi-Frequency Fit",
            description="Three-parameter Alpha-Beta-Gamma multi-frequency floating-intercept model.",
        )
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.gamma = float(gamma)
        self.sigma_db = float(sigma_db)

    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        return {
            "distance_m": (1.0, 5000.0),
            "frequency_hz": (0.5e9, 100.0e9),
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
        d_m = to_meters(distance, unit=distance_unit)
        f_hz = to_hz(frequency, unit=frequency_unit)
        fc_ghz = f_hz / 1e9

        self.validate_parameters(strict=strict, distance_m=d_m, frequency_hz=f_hz)

        d_arr = np.asarray(d_m, dtype=np.float64)
        d_safe = np.maximum(d_arr, 1.0)
        fc_safe = np.maximum(fc_ghz, 0.001)

        pl = (
            10.0 * self.alpha * np.log10(d_safe)
            + self.beta
            + 10.0 * self.gamma * np.log10(fc_safe)
        )
        return float(pl) if (np.isscalar(pl) or np.ndim(pl) == 0) else pl

    @classmethod
    def fit_from_data(
        cls,
        distances_m: np.ndarray,
        frequencies_hz: np.ndarray,
        measured_pl_db: np.ndarray,
    ) -> "FloatingInterceptABGModel":
        """
        Estimate optimal (alpha, beta, gamma, sigma_db) via Ordinary Least Squares (OLS).

        System:
            PL = [10*log10(d), 1, 10*log10(fc_ghz)] @ [alpha, beta, gamma]^T
        """
        d = np.asarray(distances_m, dtype=np.float64).flatten()
        f_ghz = np.asarray(frequencies_hz, dtype=np.float64).flatten() / 1e9
        y = np.asarray(measured_pl_db, dtype=np.float64).flatten()

        if len(d) != len(f_ghz) or len(d) != len(y) or len(d) < 3:
            raise InvalidParameterError("Fitting requires at least 3 matched data samples.")

        A = np.column_stack([
            10.0 * np.log10(np.maximum(d, 0.1)),
            np.ones_like(d),
            10.0 * np.log10(np.maximum(f_ghz, 0.1)),
        ])

        # Least squares solve
        params, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)
        alpha_est, beta_est, gamma_est = params

        y_pred = A @ params
        residuals_arr = y - y_pred
        sigma_est = float(np.std(residuals_arr, ddof=3 if len(y) > 3 else 0))

        return cls(
            alpha=float(alpha_est),
            beta=float(beta_est),
            gamma=float(gamma_est),
            sigma_db=max(0.1, sigma_est),
        )
