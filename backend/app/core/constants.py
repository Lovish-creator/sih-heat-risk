"""
SIH26083 Platform Domain Constants and Enumerations.
"""

from enum import Enum


class AppEnv(str, Enum):
    DEVELOPMENT = "development"
    DEMO = "demo"
    TESTING = "testing"
    PRODUCTION = "production"


class DataMode(str, Enum):
    LIVE = "live"
    DEMO = "demo"
    HYBRID = "hybrid"


class AlertLevel(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    RED = "RED"


class ProviderStatus(str, Enum):
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    TIER_2_INTERFACE = "TIER_2_INTERFACE"


MODEL_VERSION = "1.0.0-prototype"

# Multi-criteria composite risk weights (sum to 1.0)
HAZARD_WEIGHT = 0.55
VULNERABILITY_WEIGHT = 0.30
DURATION_WEIGHT = 0.15

# Hazard subcomponent weights (sum to 1.0)
HAZARD_SUBWEIGHT_UTCI = 0.60
HAZARD_SUBWEIGHT_WBGT = 0.25
HAZARD_SUBWEIGHT_HEAT_INDEX = 0.15

# Vulnerability subcomponent weights (sum to 1.0)
VULN_SUBWEIGHT_ELDERLY = 0.40        # Age >= 60
VULN_SUBWEIGHT_OUTDOOR_WORKER = 0.35 # Cultivators, Ag Laborers, Informal Outdoor Workers
VULN_SUBWEIGHT_DENSITY = 0.25        # Population density per km²

# Alert classification thresholds (Relative Risk score [0, 100])
ALERT_THRESHOLD_GREEN_MAX = 25.0
ALERT_THRESHOLD_YELLOW_MAX = 50.0
ALERT_THRESHOLD_ORANGE_MAX = 75.0

DURATION_SCALING = {
    1: 0.0,
    2: 0.33,
    3: 0.66,
    4: 1.0,
    5: 1.0
}
