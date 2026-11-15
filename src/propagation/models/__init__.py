"""
Mathematical propagation models adhering to a common PropagationModel interface.
Includes classical VHF/UHF models, 3GPP TR 38.901 (Rel 16-19), CI/CIF, and ABG models.
"""

from propagation.models.base import PropagationModel
from propagation.models.free_space import FreeSpacePathLoss
from propagation.models.two_ray import TwoRayGroundReflection
from propagation.models.log_distance import LogDistancePathLoss, ENVIRONMENT_EXPONENTS
from propagation.models.okumura import OkumuraModel
from propagation.models.hata import HataModel
from propagation.models.cost231 import COST231HataModel
from propagation.models.shadowing import LogNormalShadowing
from propagation.models.three_gpp_tr38901 import (
    ThreeGPPTR38901Base,
    ThreeGPPUMiModel,
    ThreeGPPUMaModel,
    ThreeGPPInHOfficeModel,
    compute_atmospheric_absorption_db_per_km,
)
from propagation.models.ci_abg import (
    CloseInModel,
    FloatingInterceptABGModel,
)
from propagation.models.los_nlos_transition import (
    StatisticalLoSNLoSTransitionModel,
)
from propagation.models.mmwave_3gpp import (
    MMWave3GPPModel,
    CloseInMMWaveModel,
    calculate_3gpp_los_probability,
)

__all__ = [
    "PropagationModel",
    "FreeSpacePathLoss",
    "TwoRayGroundReflection",
    "LogDistancePathLoss",
    "ENVIRONMENT_EXPONENTS",
    "OkumuraModel",
    "HataModel",
    "COST231HataModel",
    "LogNormalShadowing",
    "ThreeGPPTR38901Base",
    "ThreeGPPUMiModel",
    "ThreeGPPUMaModel",
    "ThreeGPPInHOfficeModel",
    "compute_atmospheric_absorption_db_per_km",
    "CloseInModel",
    "FloatingInterceptABGModel",
    "StatisticalLoSNLoSTransitionModel",
    "MMWave3GPPModel",
    "CloseInMMWaveModel",
    "calculate_3gpp_los_probability",
]
