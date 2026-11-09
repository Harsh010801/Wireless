"""
Simulation engine orchestrating distance sweeps, frequency sweeps, and multi-model evaluations.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

from propagation.core.exceptions import InvalidParameterError
from propagation.core.link_budget import LinkBudget
from propagation.models.base import PropagationModel
from propagation.models.cost231 import COST231HataModel
from propagation.models.free_space import FreeSpacePathLoss
from propagation.models.hata import HataModel
from propagation.models.log_distance import LogDistancePathLoss
from propagation.models.okumura import OkumuraModel
from propagation.models.shadowing import LogNormalShadowing
from propagation.models.two_ray import TwoRayGroundReflection
from propagation.simulation.scenario import ScenarioConfig


@dataclass
class SimulationResult:
    """Container holding multi-model numerical simulation results."""
    scenario_name: str
    sweep_type: str  # 'distance' or 'frequency'
    sweep_values: np.ndarray
    sweep_unit: str
    fixed_parameter_name: str
    fixed_parameter_value: float
    fixed_parameter_unit: str
    path_loss_db: Dict[str, np.ndarray]
    received_power_dbm: Dict[str, np.ndarray]
    link_budget: Dict[str, float]

    def to_dataframe(self) -> pd.DataFrame:
        """Export simulation results into a tidy Pandas DataFrame."""
        rows = []
        sweep_col = f"{self.sweep_type}_{self.sweep_unit}"

        for i, val in enumerate(self.sweep_values):
            for model_key in self.path_loss_db.keys():
                rows.append({
                    sweep_col: float(val),
                    "model": model_key,
                    "path_loss_db": float(self.path_loss_db[model_key][i]),
                    "received_power_dbm": float(self.received_power_dbm[model_key][i]),
                    "scenario": self.scenario_name,
                })
        return pd.DataFrame(rows)

    def to_wide_dataframe(self) -> pd.DataFrame:
        """Export simulation results into a wide DataFrame with models as columns."""
        sweep_col = f"{self.sweep_type}_{self.sweep_unit}"
        df = pd.DataFrame({sweep_col: self.sweep_values})
        for model_key, pl_arr in self.path_loss_db.items():
            df[f"PL_{model_key}_dB"] = pl_arr
            df[f"Pr_{model_key}_dBm"] = self.received_power_dbm[model_key]
        return df


class SimulationEngine:
    """
    Core engine managing model registries, parameter distribution, and numerical sweeps.
    """

    def __init__(self):
        self._model_classes: Dict[str, type] = {
            "fspl": FreeSpacePathLoss,
            "two_ray": TwoRayGroundReflection,
            "log_distance": LogDistancePathLoss,
            "okumura": OkumuraModel,
            "hata": HataModel,
            "cost231": COST231HataModel,
            "shadowing": LogNormalShadowing,
        }

    def get_registered_keys(self) -> List[str]:
        """Return list of supported model identifier keys."""
        return list(self._model_classes.keys())

    def create_model_instance(self, model_key: str, scenario: ScenarioConfig) -> PropagationModel:
        """Instantiate a propagation model with scenario-adapted defaults."""
        key = model_key.strip().lower()
        if key not in self._model_classes:
            raise InvalidParameterError(f"Unknown model key '{model_key}'. Available: {self.get_registered_keys()}")

        cls = self._model_classes[key]

        if key == "fspl":
            return cls()
        elif key == "two_ray":
            return cls(ht_default=scenario.ht, hr_default=scenario.hr)
        elif key == "log_distance":
            env = scenario.environment
            if scenario.path_loss_exponent is not None:
                return cls(n=scenario.path_loss_exponent)
            try:
                return cls(environment=env)
            except InvalidParameterError:
                return cls(environment="urban")
        elif key == "okumura":
            env = scenario.environment
            if env not in {"urban", "suburban", "open", "rural", "quasi_open"}:
                env = "urban"
            return cls(hte_default=scenario.ht, hre_default=scenario.hr, environment=env)
        elif key == "hata":
            env = scenario.environment
            if env not in {"urban_medium", "urban_large", "suburban", "rural"}:
                env = "urban_medium" if "urb" in env else ("suburban" if "sub" in env else "rural")
            return cls(hb_default=scenario.ht, hm_default=scenario.hr, environment=env)
        elif key == "cost231":
            env = "metropolitan" if "dense" in scenario.environment or "large" in scenario.environment else "medium_city"
            return cls(hb_default=scenario.ht, hm_default=scenario.hr, environment=env)
        elif key == "shadowing":
            n = scenario.path_loss_exponent if scenario.path_loss_exponent is not None else 3.0
            return cls(n=n, sigma_db=scenario.shadowing_std_db, seed=scenario.random_seed)

        return cls()

    def run_distance_sweep(self, scenario: ScenarioConfig) -> SimulationResult:
        """
        Execute a controlled distance sweep across all requested models.
        """
        # Generate distance sweep points
        if scenario.log_scale_distance:
            distances = np.geomspace(
                scenario.min_distance, scenario.max_distance, scenario.num_distance_points
            )
        else:
            distances = np.linspace(
                scenario.min_distance, scenario.max_distance, scenario.num_distance_points
            )

        budget = LinkBudget(
            tx_power_dbm=scenario.tx_power_dbm,
            tx_gain_dbi=scenario.tx_gain_dbi,
            rx_gain_dbi=scenario.rx_gain_dbi,
            system_loss_db=scenario.system_loss_db,
            rx_sensitivity_dbm=scenario.rx_sensitivity_dbm,
        )

        pl_results: Dict[str, np.ndarray] = {}
        pr_results: Dict[str, np.ndarray] = {}

        for model_key in scenario.models:
            model = self.create_model_instance(model_key, scenario)

            # Extra kwargs per model
            kwargs: Dict[str, Any] = {}
            if model_key == "two_ray":
                kwargs = {"ht": scenario.ht, "hr": scenario.hr}
            elif model_key in {"okumura", "hata", "cost231"}:
                kwargs = {"hb": scenario.ht, "hm": scenario.hr, "hte": scenario.ht, "hre": scenario.hr}
            elif model_key == "shadowing":
                kwargs = {"seed": scenario.random_seed}

            pl = model.calculate_path_loss(
                distance=distances,
                frequency=scenario.frequency,
                distance_unit=scenario.distance_unit,
                frequency_unit=scenario.frequency_unit,
                strict=False,
                **kwargs,
            )
            pl_arr = np.asarray(pl, dtype=np.float64)
            pr_arr = budget.calculate_received_power_dbm(pl_arr)

            pl_results[model_key] = pl_arr
            pr_results[model_key] = pr_arr

        return SimulationResult(
            scenario_name=scenario.name,
            sweep_type="distance",
            sweep_values=distances,
            sweep_unit=scenario.distance_unit,
            fixed_parameter_name="frequency",
            fixed_parameter_value=scenario.frequency,
            fixed_parameter_unit=scenario.frequency_unit,
            path_loss_db=pl_results,
            received_power_dbm=pr_results,
            link_budget={
                "tx_power_dbm": scenario.tx_power_dbm,
                "tx_gain_dbi": scenario.tx_gain_dbi,
                "rx_gain_dbi": scenario.rx_gain_dbi,
                "system_loss_db": scenario.system_loss_db,
                "eirp_dbm": budget.eirp_dbm,
                "rx_sensitivity_dbm": scenario.rx_sensitivity_dbm,
            },
        )

    def run_frequency_sweep(
        self,
        scenario: ScenarioConfig,
        min_freq_mhz: float = 150.0,
        max_freq_mhz: float = 3500.0,
        num_freq_points: int = 150,
        fixed_distance_km: float = 2.0,
    ) -> SimulationResult:
        """
        Execute a frequency sweep at a fixed distance across all requested models.
        """
        frequencies_mhz = np.linspace(min_freq_mhz, max_freq_mhz, num_freq_points)

        budget = LinkBudget(
            tx_power_dbm=scenario.tx_power_dbm,
            tx_gain_dbi=scenario.tx_gain_dbi,
            rx_gain_dbi=scenario.rx_gain_dbi,
            system_loss_db=scenario.system_loss_db,
            rx_sensitivity_dbm=scenario.rx_sensitivity_dbm,
        )

        pl_results: Dict[str, np.ndarray] = {}
        pr_results: Dict[str, np.ndarray] = {}

        for model_key in scenario.models:
            model = self.create_model_instance(model_key, scenario)

            kwargs: Dict[str, Any] = {}
            if model_key == "two_ray":
                kwargs = {"ht": scenario.ht, "hr": scenario.hr}
            elif model_key in {"okumura", "hata", "cost231"}:
                kwargs = {"hb": scenario.ht, "hm": scenario.hr, "hte": scenario.ht, "hre": scenario.hr}
            elif model_key == "shadowing":
                kwargs = {"seed": scenario.random_seed}

            pl = model.calculate_path_loss(
                distance=fixed_distance_km,
                frequency=frequencies_mhz,
                distance_unit="km",
                frequency_unit="MHz",
                strict=False,
                **kwargs,
            )
            pl_arr = np.asarray(pl, dtype=np.float64)
            pr_arr = budget.calculate_received_power_dbm(pl_arr)

            pl_results[model_key] = pl_arr
            pr_results[model_key] = pr_arr

        return SimulationResult(
            scenario_name=f"{scenario.name} (Frequency Sweep)",
            sweep_type="frequency",
            sweep_values=frequencies_mhz,
            sweep_unit="MHz",
            fixed_parameter_name="distance",
            fixed_parameter_value=fixed_distance_km,
            fixed_parameter_unit="km",
            path_loss_db=pl_results,
            received_power_dbm=pr_results,
            link_budget={
                "tx_power_dbm": scenario.tx_power_dbm,
                "tx_gain_dbi": scenario.tx_gain_dbi,
                "rx_gain_dbi": scenario.rx_gain_dbi,
                "system_loss_db": scenario.system_loss_db,
                "eirp_dbm": budget.eirp_dbm,
                "rx_sensitivity_dbm": scenario.rx_sensitivity_dbm,
            },
        )

