"""
Exceptions and warning definitions for the wireless propagation framework.
"""

class PropagationError(Exception):
    """Base exception for all propagation-related errors."""
    pass


class InvalidParameterError(PropagationError, ValueError):
    """Raised when an impossible or unphysical parameter is provided (e.g. negative distance)."""
    pass


class UnitError(PropagationError, ValueError):
    """Raised when an unsupported unit is provided or unit conversion fails."""
    pass


class ModelRangeWarning(UserWarning):
    """Warning emitted when input parameters fall outside a model's empirical calibration boundaries."""
    pass

