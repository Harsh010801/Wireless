"""
Abstract Base Class for Wireless Signal Propagation Models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Union
import warnings
import numpy as np

from propagation.core.exceptions import InvalidParameterError, ModelRangeWarning
from propagation.core.link_budget import LinkBudget
from propagation.core.units import to_hz, to_meters


class PropagationModel(ABC):
    """
    Abstract base class establishing the standard interface for all wireless
    signal propagation models in the framework.
    """

    def __init__(self, name: str, classification: str, description: str):
        self.name = name
        self.classification = classification
        self.description = description

    def get_model_name(self) -> str:
        """Return the descriptive name of the model."""
        return self.name

    def get_classification(self) -> str:
        """Return the category: Theoretical, Empirical, or Stochastic."""
        return self.classification

    def get_description(self) -> str:
        """Return a brief scientific summary of the model."""
        return self.description

    @abstractmethod
    def get_valid_range(self) -> Dict[str, Tuple[float, float]]:
        """
        Return recommended/calibrated parameter ranges as a dictionary:
        {
            'distance_m': (min_val, max_val),
            'frequency_hz': (min_val, max_val),
            ...
        }
        """
        pass

    def validate_parameters(
        self,
        distance_m: Union[float, np.ndarray],
        frequency_hz: Union[float, np.ndarray],
        strict: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Validate input parameters for physical viability and empirical calibration.

        Parameters:
            distance_m: Distance in meters.
            frequency_hz: Frequency in Hertz.
            strict: If True, raise InvalidParameterError when outside empirical bounds;
                    if False, emit ModelRangeWarning.
        """
        d = np.asarray(distance_m, dtype=np.float64)
        f = np.asarray(frequency_hz, dtype=np.float64)

        # Fundamental physics checks: strictly positive values
        if np.any(d <= 0):
            raise InvalidParameterError(f"Distance must be strictly positive (> 0 m). Received: {distance_m}")
        if np.any(f <= 0):
            raise InvalidParameterError(f"Frequency must be strictly positive (> 0 Hz). Received: {frequency_hz}")

        # Empirical calibration checks
        valid_ranges = self.get_valid_range()

        if "distance_m" in valid_ranges:
            d_min, d_max = valid_ranges["distance_m"]
            if np.any(d < d_min) or np.any(d > d_max):
                msg = (
                    f"[{self.name}] Distance ({np.min(d):.1f}m - {np.max(d):.1f}m) "
                    f"is outside calibrated bounds [{d_min:.1f}m, {d_max:.1f}m]."
                )
                if strict:
                    raise InvalidParameterError(msg)
                warnings.warn(msg, ModelRangeWarning, stacklevel=3)

        if "frequency_hz" in valid_ranges:
            f_min, f_max = valid_ranges["frequency_hz"]
            if np.any(f < f_min) or np.any(f > f_max):
                msg = (
                    f"[{self.name}] Frequency ({np.min(f)/1e6:.1f}MHz - {np.max(f)/1e6:.1f}MHz) "
                    f"is outside calibrated bounds [{f_min/1e6:.1f}MHz, {f_max/1e6:.1f}MHz]."
                )
                if strict:
                    raise InvalidParameterError(msg)
                warnings.warn(msg, ModelRangeWarning, stacklevel=3)

    @abstractmethod
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
        Calculate total median path loss in decibels (dB).

        Parameters:
            distance: Distance value or array.
            frequency: Frequency value or array.
            distance_unit: Unit of distance ('m', 'km', etc.).
            frequency_unit: Unit of frequency ('Hz', 'MHz', 'GHz', etc.).
            strict: If True, raise errors when parameters exceed calibration range.
            **kwargs: Model-specific arguments (e.g. antenna heights, environment).

        Returns:
            Path loss in dB (scalar float or NumPy ndarray matching distance array shape).
        """
        pass

    def calculate_received_power(
        self,
        distance: Union[float, np.ndarray],
        frequency: Union[float, np.ndarray],
        tx_power_dbm: float = 30.0,
        tx_gain_dbi: float = 0.0,
        rx_gain_dbi: float = 0.0,
        system_loss_db: float = 0.0,
        distance_unit: str = "m",
        frequency_unit: str = "Hz",
        strict: bool = False,
        **kwargs: Any,
    ) -> Union[float, np.ndarray]:
        """
        Calculate received power in dBm via link budget analysis.

        Parameters:
            distance: Distance value or array.
            frequency: Frequency value or array.
            tx_power_dbm: Transmit power in dBm (default: 30 dBm = 1 W).
            tx_gain_dbi: Transmitter antenna gain in dBi.
            rx_gain_dbi: Receiver antenna gain in dBi.
            system_loss_db: Miscellaneous hardware losses in dB.
            distance_unit: Distance unit ('m' or 'km').
            frequency_unit: Frequency unit ('Hz', 'MHz', or 'GHz').
            strict: Enforce strict parameter bounds.
            **kwargs: Extra model parameters.

        Returns:
            Received signal power in dBm.
        """
        pl_db = self.calculate_path_loss(
            distance=distance,
            frequency=frequency,
            distance_unit=distance_unit,
            frequency_unit=frequency_unit,
            strict=strict,
            **kwargs,
        )

        budget = LinkBudget(
            tx_power_dbm=tx_power_dbm,
            tx_gain_dbi=tx_gain_dbi,
            rx_gain_dbi=rx_gain_dbi,
            system_loss_db=system_loss_db,
        )
        return budget.calculate_received_power_dbm(pl_db)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', type='{self.classification}')>"

