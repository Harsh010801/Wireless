"""
Scenario configuration loader, validator, and data structures.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml

from propagation.core.exceptions import InvalidParameterError


@dataclass
class ScenarioConfig:
    """Configuration container for a wireless propagation simulation scenario."""
    name: str
    description: str
    frequency: float
    frequency_unit: str = "MHz"
    min_distance: float = 0.1
    max_distance: float = 20.0
    num_distance_points: int = 200
    distance_unit: str = "km"
    log_scale_distance: bool = True
    tx_power_dbm: float = 43.0  # e.g., 20 Watts macrocell base station
    tx_gain_dbi: float = 15.0   # Sector antenna
    rx_gain_dbi: float = 0.0    # Mobile isotropic/omni dipole
    system_loss_db: float = 2.0 # Cable and connector attenuation
    rx_sensitivity_dbm: float = -100.0
    ht: float = 30.0            # Base station height in meters
    hr: float = 1.5             # Mobile station height in meters
    environment: str = "urban"
    path_loss_exponent: Optional[float] = None
    shadowing_std_db: float = 6.0
    random_seed: int = 42
    models: List[str] = field(default_factory=lambda: [
        "fspl", "two_ray", "log_distance", "okumura", "hata", "cost231", "shadowing"
    ])

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScenarioConfig":
        """Instantiate from a raw Python dictionary with validation."""
        valid_keys = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data.items() if k in valid_keys}

        if "frequency" not in filtered:
            raise InvalidParameterError("Scenario configuration must include 'frequency'.")
        if filtered.get("min_distance", 0.1) <= 0:
            raise InvalidParameterError("min_distance must be strictly positive.")
        if filtered.get("max_distance", 20.0) <= filtered.get("min_distance", 0.1):
            raise InvalidParameterError("max_distance must be strictly greater than min_distance.")

        return cls(**filtered)

    @classmethod
    def from_yaml(cls, yaml_path: Union[str, Path]) -> "ScenarioConfig":
        """Load scenario configuration from a YAML file."""
        p = Path(yaml_path)
        if not p.is_file():
            raise FileNotFoundError(f"Scenario configuration file not found at: {yaml_path}")
        with open(p, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def to_yaml(self, yaml_path: Union[str, Path]) -> None:
        """Persist scenario configuration to a YAML file."""
        p = Path(yaml_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        data = {k: getattr(self, k) for k in self.__dataclass_fields__.keys()}
        with open(p, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

