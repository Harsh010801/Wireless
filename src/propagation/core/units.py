"""
Unit conversion utilities and fundamental electromagnetic constants.

Supports scalar values and NumPy arrays across:
- Frequency: Hz, kHz, MHz, GHz
- Distance: m, km, ft, mi
- Power: W, mW, dBm, dBW
"""

from typing import Union
import numpy as np

from propagation.core.exceptions import InvalidParameterError, UnitError

# Speed of light in vacuum (m/s) according to BIPM SI definition
SPEED_OF_LIGHT: float = 299792458.0


# ---------------------------------------------------------------------------
# Frequency Conversions
# ---------------------------------------------------------------------------

def to_hz(frequency: Union[float, np.ndarray], unit: str = "Hz") -> Union[float, np.ndarray]:
    """
    Convert frequency from specified unit to Hertz (Hz).

    Parameters:
        frequency: Frequency value or array.
        unit: Input unit ('hz', 'khz', 'mhz', 'ghz' - case insensitive).

    Returns:
        Frequency in Hz.
    """
    u = unit.strip().lower()
    val = np.asarray(frequency, dtype=np.float64)
    if np.any(val <= 0):
        raise InvalidParameterError(f"Frequency must be strictly positive (> 0), got: {frequency}")

    factors = {
        "hz": 1.0,
        "khz": 1e3,
        "mhz": 1e6,
        "ghz": 1e9,
    }
    if u not in factors:
        raise UnitError(f"Unsupported frequency unit '{unit}'. Valid options: {list(factors.keys())}")

    result = val * factors[u]
    return float(result) if np.isscalar(frequency) else result


def from_hz(frequency_hz: Union[float, np.ndarray], to_unit: str = "MHz") -> Union[float, np.ndarray]:
    """
    Convert frequency from Hertz (Hz) to target unit.

    Parameters:
        frequency_hz: Frequency in Hz.
        to_unit: Target unit ('hz', 'khz', 'mhz', 'ghz').

    Returns:
        Frequency in target unit.
    """
    u = to_unit.strip().lower()
    val = np.asarray(frequency_hz, dtype=np.float64)
    if np.any(val <= 0):
        raise InvalidParameterError(f"Frequency must be strictly positive (> 0), got: {frequency_hz}")

    divisors = {
        "hz": 1.0,
        "khz": 1e3,
        "mhz": 1e6,
        "ghz": 1e9,
    }
    if u not in divisors:
        raise UnitError(f"Unsupported frequency unit '{to_unit}'. Valid options: {list(divisors.keys())}")

    result = val / divisors[u]
    return float(result) if np.isscalar(frequency_hz) else result


def wavelength(frequency: Union[float, np.ndarray], unit: str = "Hz") -> Union[float, np.ndarray]:
    """
    Compute free-space electromagnetic wavelength lambda = c / f in meters.

    Parameters:
        frequency: Frequency value or array.
        unit: Unit of frequency ('hz', 'khz', 'mhz', 'ghz').

    Returns:
        Wavelength lambda in meters.
    """
    f_hz = to_hz(frequency, unit=unit)
    return SPEED_OF_LIGHT / f_hz


# ---------------------------------------------------------------------------
# Distance Conversions
# ---------------------------------------------------------------------------

def to_meters(distance: Union[float, np.ndarray], unit: str = "m") -> Union[float, np.ndarray]:
    """
    Convert distance from specified unit to meters (m).

    Parameters:
        distance: Distance value or array.
        unit: Input unit ('m', 'km', 'ft', 'mi' - case insensitive).

    Returns:
        Distance in meters.
    """
    u = unit.strip().lower()
    val = np.asarray(distance, dtype=np.float64)
    if np.any(val <= 0):
        raise InvalidParameterError(f"Distance must be strictly positive (> 0), got: {distance}")

    factors = {
        "m": 1.0,
        "km": 1000.0,
        "ft": 0.3048,
        "mi": 1609.344,
    }
    if u not in factors:
        raise UnitError(f"Unsupported distance unit '{unit}'. Valid options: {list(factors.keys())}")

    result = val * factors[u]
    return float(result) if np.isscalar(distance) else result


def from_meters(distance_m: Union[float, np.ndarray], to_unit: str = "km") -> Union[float, np.ndarray]:
    """
    Convert distance from meters (m) to target unit.

    Parameters:
        distance_m: Distance in meters.
        to_unit: Target unit ('m', 'km', 'ft', 'mi').

    Returns:
        Distance in target unit.
    """
    u = to_unit.strip().lower()
    val = np.asarray(distance_m, dtype=np.float64)
    if np.any(val <= 0):
        raise InvalidParameterError(f"Distance must be strictly positive (> 0), got: {distance_m}")

    divisors = {
        "m": 1.0,
        "km": 1000.0,
        "ft": 0.3048,
        "mi": 1609.344,
    }
    if u not in divisors:
        raise UnitError(f"Unsupported distance unit '{to_unit}'. Valid options: {list(divisors.keys())}")

    result = val / divisors[u]
    return float(result) if np.isscalar(distance_m) else result


# ---------------------------------------------------------------------------
# Power Conversions
# ---------------------------------------------------------------------------

def watts_to_dbm(power_w: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert power from Watts (W) to decibel-milliwatts (dBm).
    Formula: P_dBm = 10 * log10(P_W * 1000) = 10 * log10(P_W) + 30
    """
    val = np.asarray(power_w, dtype=np.float64)
    if np.any(val <= 0):
        raise InvalidParameterError(f"Power in Watts must be strictly positive (> 0), got: {power_w}")
    result = 10.0 * np.log10(val * 1000.0)
    return float(result) if np.isscalar(power_w) else result


def dbm_to_watts(power_dbm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert power from decibel-milliwatts (dBm) to Watts (W).
    Formula: P_W = 10^((P_dBm - 30) / 10)
    """
    val = np.asarray(power_dbm, dtype=np.float64)
    result = 10.0 ** ((val - 30.0) / 10.0)
    return float(result) if np.isscalar(power_dbm) else result


def mw_to_dbm(power_mw: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert milliwatts (mW) to dBm."""
    val = np.asarray(power_mw, dtype=np.float64)
    if np.any(val <= 0):
        raise InvalidParameterError(f"Power in mW must be strictly positive (> 0), got: {power_mw}")
    result = 10.0 * np.log10(val)
    return float(result) if np.isscalar(power_mw) else result


def dbm_to_mw(power_dbm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert dBm to milliwatts (mW)."""
    val = np.asarray(power_dbm, dtype=np.float64)
    result = 10.0 ** (val / 10.0)
    return float(result) if np.isscalar(power_dbm) else result


def dbw_to_dbm(power_dbw: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert dBW to dBm (P_dBm = P_dBW + 30)."""
    val = np.asarray(power_dbw, dtype=np.float64)
    result = val + 30.0
    return float(result) if np.isscalar(power_dbw) else result


def dbm_to_dbw(power_dbm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert dBm to dBW (P_dBW = P_dBm - 30)."""
    val = np.asarray(power_dbm, dtype=np.float64)
    result = val - 30.0
    return float(result) if np.isscalar(power_dbm) else result

