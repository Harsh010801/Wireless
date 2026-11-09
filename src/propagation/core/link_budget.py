"""
Link budget calculations and radio frequency power budget analysis.

Formulas implemented:
    P_r (dBm) = P_t (dBm) + G_t (dBi) + G_r (dBi) - PL (dB) - L_sys (dB)
    EIRP (dBm) = P_t (dBm) + G_t (dBi) - L_tx (dB)
    Fade Margin (dB) = P_r (dBm) - Receiver_Sensitivity (dBm)
"""

from dataclasses import dataclass
from typing import Optional, Union, Dict, Any
import numpy as np

from propagation.core.exceptions import InvalidParameterError
from propagation.core.units import dbm_to_watts, watts_to_dbm


@dataclass
class LinkBudgetResult:
    """Structured container holding detailed link budget analysis outputs."""
    tx_power_dbm: float
    tx_gain_dbi: float
    rx_gain_dbi: float
    path_loss_db: Union[float, np.ndarray]
    system_loss_db: float
    eirp_dbm: float
    rx_power_dbm: Union[float, np.ndarray]
    rx_power_watts: Union[float, np.ndarray]
    fade_margin_db: Optional[Union[float, np.ndarray]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert scalar or summarized budget to dictionary."""
        return {
            "tx_power_dbm": self.tx_power_dbm,
            "tx_gain_dbi": self.tx_gain_dbi,
            "rx_gain_dbi": self.rx_gain_dbi,
            "path_loss_db": float(np.mean(self.path_loss_db)) if isinstance(self.path_loss_db, np.ndarray) else self.path_loss_db,
            "system_loss_db": self.system_loss_db,
            "eirp_dbm": self.eirp_dbm,
            "rx_power_dbm": float(np.mean(self.rx_power_dbm)) if isinstance(self.rx_power_dbm, np.ndarray) else self.rx_power_dbm,
            "rx_power_watts": float(np.mean(self.rx_power_watts)) if isinstance(self.rx_power_watts, np.ndarray) else self.rx_power_watts,
            "fade_margin_db": float(np.mean(self.fade_margin_db)) if (self.fade_margin_db is not None and isinstance(self.fade_margin_db, np.ndarray)) else self.fade_margin_db,
        }


class LinkBudget:
    """
    Standard RF Link Budget analyzer.

    Parameters:
        tx_power_dbm: Transmit power in dBm. If given in Watts, convert via watts_to_dbm().
        tx_gain_dbi: Transmitter antenna gain in dBi (default: 0.0 dBi).
        rx_gain_dbi: Receiver antenna gain in dBi (default: 0.0 dBi).
        system_loss_db: Miscellaneous hardware losses (cables, connectors, mispointing) in dB (default: 0.0 dB).
        rx_sensitivity_dbm: Receiver detection sensitivity threshold in dBm (optional, for fade margin).
    """

    def __init__(
        self,
        tx_power_dbm: float = 30.0,
        tx_gain_dbi: float = 0.0,
        rx_gain_dbi: float = 0.0,
        system_loss_db: float = 0.0,
        rx_sensitivity_dbm: Optional[float] = None,
    ):
        if system_loss_db < 0:
            raise InvalidParameterError(f"System loss must be non-negative, got: {system_loss_db} dB")

        self.tx_power_dbm = float(tx_power_dbm)
        self.tx_gain_dbi = float(tx_gain_dbi)
        self.rx_gain_dbi = float(rx_gain_dbi)
        self.system_loss_db = float(system_loss_db)
        self.rx_sensitivity_dbm = float(rx_sensitivity_dbm) if rx_sensitivity_dbm is not None else None

    @property
    def eirp_dbm(self) -> float:
        """Effective Isotropic Radiated Power (dBm) = P_tx + G_tx."""
        return self.tx_power_dbm + self.tx_gain_dbi

    def calculate_received_power_dbm(
        self, path_loss_db: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        """
        Calculate received signal power in dBm given the path loss.

        Formula:
            P_r = P_t + G_t + G_r - PL - L_sys
        """
        pl = np.asarray(path_loss_db, dtype=np.float64)
        if np.any(pl < 0):
            raise InvalidParameterError(f"Path loss must be non-negative, got: {path_loss_db}")

        pr = self.tx_power_dbm + self.tx_gain_dbi + self.rx_gain_dbi - pl - self.system_loss_db
        return float(pr) if np.isscalar(path_loss_db) else pr

    def calculate_received_power_watts(
        self, path_loss_db: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        """Calculate received signal power in Watts."""
        pr_dbm = self.calculate_received_power_dbm(path_loss_db)
        return dbm_to_watts(pr_dbm)

    def calculate_fade_margin(
        self, path_loss_db: Union[float, np.ndarray]
    ) -> Optional[Union[float, np.ndarray]]:
        """
        Calculate link fade margin in dB relative to receiver sensitivity threshold.

        Formula:
            Fade Margin = P_r (dBm) - Sensitivity (dBm)
        """
        if self.rx_sensitivity_dbm is None:
            return None
        pr_dbm = self.calculate_received_power_dbm(path_loss_db)
        return pr_dbm - self.rx_sensitivity_dbm

    def compute(self, path_loss_db: Union[float, np.ndarray]) -> LinkBudgetResult:
        """Execute complete link budget calculation and return LinkBudgetResult."""
        rx_dbm = self.calculate_received_power_dbm(path_loss_db)
        rx_watts = dbm_to_watts(rx_dbm)
        fade_margin = self.calculate_fade_margin(path_loss_db)

        return LinkBudgetResult(
            tx_power_dbm=self.tx_power_dbm,
            tx_gain_dbi=self.tx_gain_dbi,
            rx_gain_dbi=self.rx_gain_dbi,
            path_loss_db=path_loss_db,
            system_loss_db=self.system_loss_db,
            eirp_dbm=self.eirp_dbm,
            rx_power_dbm=rx_dbm,
            rx_power_watts=rx_watts,
            fade_margin_db=fade_margin,
        )

