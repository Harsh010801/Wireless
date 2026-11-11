"""Pydantic schemas for simulation API endpoints."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    frequency_mhz: float = Field(900.0, ge=10.0, le=100000.0, description="Carrier frequency in MHz")
    environment: str = Field("urban", description="urban | suburban | rural | indoor_obstructed")
    min_distance_km: float = Field(0.1, ge=0.001, le=50.0, description="Minimum distance in km")
    max_distance_km: float = Field(20.0, ge=0.1, le=200.0, description="Maximum distance in km")
    num_points: int = Field(100, ge=10, le=500, description="Number of distance points")
    tx_power_dbm: float = Field(43.0, ge=-10.0, le=80.0, description="Transmit power in dBm")
    tx_gain_dbi: float = Field(15.0, ge=-10.0, le=50.0, description="Tx antenna gain in dBi")
    rx_gain_dbi: float = Field(0.0, ge=-10.0, le=30.0, description="Rx antenna gain in dBi")
    system_loss_db: float = Field(3.0, ge=0.0, le=30.0, description="System cable/connector loss in dB")
    rx_sensitivity_dbm: float = Field(-100.0, ge=-150.0, le=0.0, description="Receiver sensitivity threshold in dBm")
    ht_m: float = Field(30.0, ge=1.0, le=500.0, description="Base station height in meters")
    hr_m: float = Field(1.5, ge=0.5, le=50.0, description="Mobile station height in meters")
    shadow_sigma_db: float = Field(6.0, ge=0.5, le=20.0, description="Shadowing standard deviation in dB")
    models: List[str] = Field(
        default=["fspl", "two_ray", "log_distance", "okumura", "hata", "cost231", "shadowing"],
        description="List of propagation model keys to evaluate",
    )


class LinkBudgetEvaluationRequest(BaseModel):
    target_distance_km: float = Field(3.0, ge=0.01, le=200.0)
    frequency_mhz: float = Field(900.0, ge=10.0, le=100000.0)
    environment: str = Field("urban")
    tx_power_dbm: float = Field(43.0)
    tx_gain_dbi: float = Field(15.0)
    rx_gain_dbi: float = Field(0.0)
    system_loss_db: float = Field(3.0)
    rx_sensitivity_dbm: float = Field(-100.0)
    ht_m: float = Field(30.0)
    hr_m: float = Field(1.5)

