from typing import Any

from .converters import *
from .erd_code_class import ErdCodeClass
from .erd_codes import ErdCode
from .erd_data_type import ErdDataType


class ErdConfigurationEntry:
    def __init__(
        self,
        erd_code: ErdCode,
        converter: ErdValueConverter,
        code_class: ErdCodeClass,
        data_type: ErdDataType = ErdDataType.STRING,
    ) -> None:
        super().__init__()
        self.erd_code = erd_code
        self.converter = converter
        self.code_class = code_class
        self.converter.erd_code = self.erd_code
        self.data_type = data_type

    @property
    def can_decode(self) -> bool:
        return self.converter.can_decode

    @property
    def can_encode(self) -> bool:
        return self.converter.can_encode

    def erd_decode(self, value: str) -> Any:
        return self.converter.erd_decode(value)

    def erd_encode(self, value: Any) -> str:
        return self.converter.erd_encode(value)

_configuration = [
    #Universal
    ErdConfigurationEntry(
        ErdCode.APPLIANCE_TYPE,
        ErdApplianceTypeConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.MODEL_NUMBER,
        ErdModelSerialConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.SERIAL_NUMBER,
        ErdModelSerialConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.SABBATH_MODE,
        ErdBoolConverter(),
        ErdCodeClass.SABBATH_CONTROL,
    ),
    ErdConfigurationEntry(
        ErdCode.USER_INTERFACE_LOCKED,
        ErdLockedBoolConverter(),
        ErdCodeClass.LOCK_CONTROL,
    ),
    ErdConfigurationEntry(
        ErdCode.ACM_UPDATING,
        ErdReadOnlyBoolConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.APPLIANCE_UPDATING,
        ErdReadOnlyBoolConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.LCD_UPDATING,
        ErdReadOnlyBoolConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.CLOCK_FORMAT,
        ErdClockFormatConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.SOUND_LEVEL,
        ErdSoundLevelConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.TEMPERATURE_UNIT,
        ErdMeasurementUnitsConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.APPLIANCE_SW_VERSION,
        ErdSoftwareVersionConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.APPLIANCE_SW_VERSION_AVAILABLE,
        ErdSoftwareVersionConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.LCD_SW_VERSION,
        ErdSoftwareVersionConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.LCD_SW_VERSION_AVAILABLE,
        ErdSoftwareVersionConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.WIFI_MODULE_UPDATING,
        ErdReadOnlyBoolConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.WIFI_MODULE_SW_VERSION,
        ErdSoftwareVersionConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.WIFI_MODULE_SW_VERSION_AVAILABLE,
        ErdSoftwareVersionConverter(),
        ErdCodeClass.GENERAL,
    ),
    ErdConfigurationEntry(
        ErdCode.UNIT_TYPE,
        ErdUnitTypeConverter(),
        ErdCodeClass.GENERAL,
    ),

    # Dishwasher
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_CYCLE_NAME,
        CycleNameConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_PODS_REMAINING_VALUE,
        ErdIntConverter(),
        ErdCodeClass.COUNTER,
        ErdDataType.INT,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_TIME_REMAINING,
        ErdReadOnlyTimeSpanConverter(),
        ErdCodeClass.TIMER,
        ErdDataType.TIMESPAN,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_CYCLE_STATE,
        ErdCycleStateConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_OPERATING_MODE,
        OperatingModeConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_REMINDERS,
        ErdRemindersSettingConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_DOOR_STATUS,
        ErdDishwasherDoorStatusConverter(),
        ErdCodeClass.DOOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_USER_SETTING,
        ErdUserSettingConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_DELAY_START_MINUTES,
        ErdTimeSpanConverter(),
        ErdCodeClass.TIMER,
        ErdDataType.TIMESPAN,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_CYCLE,
        ErdUserCycleSettingConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_CYCLE_COUNTS,
        ErdCycleCountSettingConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_TEMPERATURE,
        ErdUserTemperatureSettingConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_DRYING,
        ErdUserDryingSettingConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_WASH_ZONE,
        ErdUserZoneSettingConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_STEAM,
        ErdBoolConverter(),
        ErdDataType.BOOL,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_BOTTLE_JETS,
        ErdBoolConverter(),
        ErdDataType.BOOL,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_IS_CLEAN,
        ErdReadOnlyBoolConverter(),
        ErdDataType.BOOL,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_REMOTE_START_ENABLE,
        ErdReadOnlyBoolConverter(),
        ErdDataType.BOOL,
    ),
    ErdConfigurationEntry(
        ErdCode.DISHWASHER_ERROR,
        ErdErrorStateConverter(),
        ErdCodeClass.DISHWASHER_SENSOR,
    ),
]
