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


DURATION_SCALING = {
    1: 0.0,
    2: 0.33,
    3: 0.66,
    4: 1.0,
    5: 1.0
}
