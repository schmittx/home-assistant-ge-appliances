import logging
from typing import List

from homeassistant.const import UnitOfTime
from homeassistant.helpers.entity import Entity
from ..api.erd import ErdCode, ErdApplianceType

from .base import ApplianceApi
from ..entities import (
    GeErdBinarySensor,
    GeErdSensor,
    GeErdPropertyBinarySensor,
    GeErdPropertySensor,
)

_LOGGER = logging.getLogger(__name__)


class DishwasherApi(ApplianceApi):
    """API class for dishwasher objects"""
    APPLIANCE_TYPE = ErdApplianceType.DISHWASHER

    def get_all_entities(self) -> List[Entity]:
        base_entities = super().get_all_entities()

        dishwasher_entities = [
#            GeDishwasherControlLockedSwitch(
#                api=self,
#                ErdCode.USER_INTERFACE_LOCKED,
#            ),
            GeErdSensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_CYCLE_NAME,
                name="Cycle Name",
            ),
            GeErdSensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_CYCLE_STATE,
#                icon="mdi:state-machine",
                name="Cycle State",
            ),
            GeErdSensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_OPERATING_MODE,
                name="Operating Mode",
            ),
            GeErdSensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_PODS_REMAINING_VALUE,
                name="Remaining Pods",
                native_unit_of_measurement="pods",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_REMINDERS,
                erd_property="add_rinse_aid",
#                icon="mdi:shimmer",
                name="Rinse Aid Needed",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_REMINDERS,
                erd_property="clean_filter",
#                icon="mdi:dishwasher-alert",
                name="Filter Dirty",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_REMINDERS,
                erd_property="sanitized",
#                icon="mdi:silverware-clean",
                name="Sanitization Complete",
            ),
            GeErdSensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_TIME_REMAINING,
                name="Cycle Time Remaining",
                native_unit_of_measurement=UnitOfTime.MINUTES,
            ),
            GeErdBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_DOOR_STATUS,
                name="Door Status",
            ),
            GeErdBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_IS_CLEAN,
                name="Cleaning Complete",
            ),
            GeErdBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_REMOTE_START_ENABLE,
                name="Remote Start Enabled",
            ),

            #User Setttings
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="mute",
#                icon="mdi:volume-mute",
                name="Mute Enabled",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="lock_control",
#                icon="mdi:lock",
                name="Control Lock Enabled",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="sabbath",
#                icon="mdi:star-david",
                name="Sabbath Mode Enabled",
            ),
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="cycle_mode",
#                icon="mdi:state-machine",
                name="Cycle Mode",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="presoak",
#                icon="mdi:water",
                name="Presoak Enabled",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="bottle_jet",
#                icon="mdi:bottle-tonic-outline",
                name="Bottle Jet Enabled",
            ),
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="wash_temp",
#                icon="mdi:coolant-temperature",
                name="Wash Temp",
            ),
            GeErdPropertyBinarySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="rinse_aid",
#                icon="mdi:shimmer",
                name="Rinse Aid Enabled",
            ),
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="dry_option",
#                icon="mdi:fan",
                name="Dry Option",
            ),
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="wash_zone",
#                icon="mdi:dock-top",
                name="Wash Zone",
            ),
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_USER_SETTING,
                erd_property="delay_hours",
#                icon="mdi:clock-fast",
                name="Delay Start",
                native_unit_of_measurement=UnitOfTime.HOURS,
            ),

            #Cycle Counts
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_CYCLE_COUNTS,
                erd_property="started",
#                icon="mdi:counter",
                name="Cycles Started",
                native_unit_of_measurement="cycles",
            ),
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_CYCLE_COUNTS,
                erd_property="completed",
#                icon="mdi:counter",
                name="Cycles Completed",
                native_unit_of_measurement="cycles",
            ),
            GeErdPropertySensor(
                api=self,
                erd_code=ErdCode.DISHWASHER_CYCLE_COUNTS,
                erd_property="reset",
#                icon="mdi:counter",
                name="Cycles Reset",
                native_unit_of_measurement="cycles",
            )
        ]
        entities = base_entities + dishwasher_entities
        return entities
        
