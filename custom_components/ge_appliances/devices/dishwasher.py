import logging
from typing import List

from homeassistant.helpers.entity import Entity
from gehomesdk.erd import ErdCode, ErdApplianceType

from .base import ApplianceApi
from ..entities import GeErdSensor, GeErdBinarySensor, GeErdPropertySensor

_LOGGER = logging.getLogger(__name__)


class DishwasherApi(ApplianceApi):
    """API class for dishwasher objects"""
    APPLIANCE_TYPE = ErdApplianceType.DISH_WASHER

    def get_all_entities(self) -> List[Entity]:
        base_entities = super().get_all_entities()

        dishwasher_entities = [
            #GeDishwasherControlLockedSwitch(self, ErdCode.USER_INTERFACE_LOCKED),
            GeErdSensor(self, ErdCode.DISHWASHER_CYCLE_NAME),
            GeErdSensor(self, ErdCode.DISHWASHER_CYCLE_STATE, icon_override="mdi:state-machine"),
            GeErdSensor(self, ErdCode.DISHWASHER_OPERATING_MODE),
            GeErdSensor(self, ErdCode.DISHWASHER_PODS_REMAINING_VALUE, uom_override="pods"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_REMINDERS, "add_rinse_aid", icon_override="mdi:shimmer"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_REMINDERS, "clean_filter", icon_override="mdi:dishwasher-alert"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_REMINDERS, "sanitized", icon_override="mdi:silverware-clean"),
            GeErdSensor(self, ErdCode.DISHWASHER_TIME_REMAINING),
            GeErdBinarySensor(self, ErdCode.DISHWASHER_DOOR_STATUS),
            GeErdBinarySensor(self, ErdCode.DISHWASHER_IS_CLEAN),
            GeErdBinarySensor(self, ErdCode.DISHWASHER_REMOTE_START_ENABLE),

            #User Setttings
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "mute", icon_override="mdi:volume-mute"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "lock_control", icon_override="mdi:lock"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "sabbath", icon_override="mdi:star-david"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "cycle_mode", icon_override="mdi:state-machine"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "presoak", icon_override="mdi:water"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "bottle_jet", icon_override="mdi:bottle-tonic-outline"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "wash_temp", icon_override="mdi:coolant-temperature"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "rinse_aid", icon_override="mdi:shimmer"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "dry_option", icon_override="mdi:fan"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "wash_zone", icon_override="mdi:dock-top"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_USER_SETTING, "delay_hours", icon_override="mdi:clock-fast"),

            #Cycle Counts
            GeErdPropertySensor(self, ErdCode.DISHWASHER_CYCLE_COUNTS, "started", icon_override="mdi:counter"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_CYCLE_COUNTS, "completed", icon_override="mdi:counter"),
            GeErdPropertySensor(self, ErdCode.DISHWASHER_CYCLE_COUNTS, "reset", icon_override="mdi:counter")
        ]
        entities = base_entities + dishwasher_entities
        return entities
        
