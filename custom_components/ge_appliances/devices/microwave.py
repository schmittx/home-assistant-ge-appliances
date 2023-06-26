import logging
from typing import List

from homeassistant.helpers.entity import Entity
from gehomesdk import (
    ErdCode, 
    ErdApplianceType,
    ErdHoodFanSpeedAvailability,
    ErdHoodLightLevelAvailability,
    ErdOnOff
)

from .base import ApplianceApi
from ..entities import (
    GeHoodLightLevelSelect, 
    GeHoodFanSpeedSelect, 
    GeErdPropertySensor,
    GeErdPropertyBinarySensor,
    GeErdBinarySensor,
    GeErdTimerSensor
)

_LOGGER = logging.getLogger(__name__)


class MicrowaveApi(ApplianceApi):
    """API class for Microwave objects"""
    APPLIANCE_TYPE = ErdApplianceType.MICROWAVE

    def get_all_entities(self) -> List[Entity]:
        base_entities = super().get_all_entities()

        #get the availabilities
        fan_availability: ErdHoodFanSpeedAvailability = self.try_get_erd_value(ErdCode.HOOD_FAN_SPEED_AVAILABILITY)
        light_availability: ErdHoodLightLevelAvailability = self.try_get_erd_value(ErdCode.HOOD_LIGHT_LEVEL_AVAILABILITY)

        mwave_entities = [
            GeErdBinarySensor(self, ErdCode.MICROWAVE_REMOTE_ENABLE),
            GeErdPropertySensor(self, ErdCode.MICROWAVE_STATE, "status"),
            GeErdPropertyBinarySensor(self, ErdCode.MICROWAVE_STATE, "door_status", device_class_override="door"),
            GeErdPropertySensor(self, ErdCode.MICROWAVE_STATE, "cook_mode", icon_override="mdi:food-turkey"),
            GeErdPropertySensor(self, ErdCode.MICROWAVE_STATE, "power_level", icon_override="mdi:gauge"),
            GeErdPropertySensor(self, ErdCode.MICROWAVE_STATE, "temperature", icon_override="mdi:thermometer"),
            GeErdTimerSensor(self, ErdCode.MICROWAVE_COOK_TIMER),
            GeErdTimerSensor(self, ErdCode.MICROWAVE_KITCHEN_TIMER)
        ]

        if fan_availability and fan_availability.is_available:
            mwave_entities.append(GeHoodFanSpeedSelect(self, ErdCode.HOOD_FAN_SPEED))
        #for now, represent as a select
        if light_availability and light_availability.is_available:
            mwave_entities.append(GeHoodLightLevelSelect(self, ErdCode.HOOD_LIGHT_LEVEL))

        entities = base_entities + mwave_entities
        return entities
        
