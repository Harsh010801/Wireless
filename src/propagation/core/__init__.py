"""Core mathematical utilities, physical constants, units, and link budget calculations."""

from propagation.core.exceptions import (
    PropagationError,
    InvalidParameterError,
    UnitError,
    ModelRangeWarning,
)
from propagation.core.units import (
    SPEED_OF_LIGHT,
    to_hz,
    from_hz,
    to_meters,
    from_meters,
    wavelength,
    watts_to_dbm,
    dbm_to_watts,
    mw_to_dbm,
    dbm_to_mw,
    dbw_to_dbm,
    dbm_to_dbw,
)
from propagation.core.link_budget import LinkBudget, LinkBudgetResult

__all__ = [
    "PropagationError",
    "InvalidParameterError",
    "UnitError",
    "ModelRangeWarning",
    "SPEED_OF_LIGHT",
    "to_hz",
    "from_hz",
    "to_meters",
    "from_meters",
    "wavelength",
    "watts_to_dbm",
    "dbm_to_watts",
    "mw_to_dbm",
    "dbm_to_mw",
    "dbw_to_dbm",
    "dbm_to_dbw",
    "LinkBudget",
    "LinkBudgetResult",
]
