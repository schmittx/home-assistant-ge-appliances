import logging
from typing import Type

from ..api.erd import ErdApplianceType

from .base import ApplianceApi
from .dishwasher import DishwasherApi

_LOGGER = logging.getLogger(__name__)


def get_appliance_api_type(appliance_type: ErdApplianceType) -> Type:
    """Get the appropriate appliance type"""
    _LOGGER.debug(f"Found device type: {appliance_type}")
    if appliance_type == ErdApplianceType.DISHWASHER:
        return DishwasherApi

    # Fallback
    return ApplianceApi
