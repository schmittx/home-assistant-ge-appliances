from __future__ import annotations

import logging
from typing import Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import EntityCategory

from ...api import ErdCodeType, ErdCodeClass
from ...api.erd.erd_data_type import ErdDataType
from .ge_erd_entity import GeErdEntity
from ...devices import ApplianceApi

_LOGGER = logging.getLogger(__name__)

class GeErdSensor(GeErdEntity, SensorEntity):
    """GE Entity for sensors"""

    def __init__(
        self, 
        api: ApplianceApi, 
        erd_code: ErdCodeType,
        name: str,
        device_class: str = None,
        entity_category: str[EntityCategory] | None = EntityCategory.DIAGNOSTIC,
        icon: str = None,
        data_type: ErdDataType = None,
        native_unit_of_measurement: str = None,
        state_class: str[SensorStateClass] | None = None,
    ) -> None:
        super().__init__(
            api=api,
            erd_code=erd_code,
            device_class=device_class,
            entity_category=entity_category,
            icon=icon,
            name=name,
        )
        self._data_type = data_type
        self._native_unit_of_measurement = native_unit_of_measurement
        self._state_class = state_class

    @property
    def native_value(self):
        try:
            value = self.appliance.get_erd_value(self.erd_code)

            # if it's a numeric data type, return it directly            
            if self.data_type in [ErdDataType.INT, ErdDataType.FLOAT]:
                return self._convert_numeric_value_from_device(value)

            # otherwise, return a stringified version
            # TODO: perhaps enhance so that there's a list of variables available
            #       for the stringify function to consume...
            return self._stringify(value, temp_units=self._temp_units)
        except KeyError:
            return None

    @property
    def data_type(self) -> ErdDataType:
        if self._data_type is not None:
            return self._data_type

        return self.appliance.get_erd_code_data_type(self.erd_code)

    @property
    def _temp_units(self) -> Optional[str]:
        #based on testing, all API values are in Fahrenheit, so we'll redefine
        #this property to be the configured temperature unit and set the native
        #unit differently
        return self.api.hass.config.units.temperature_unit

        #if self._measurement_system == ErdMeasurementUnits.METRIC:
        #    return TEMP_CELSIUS
        #return TEMP_FAHRENHEIT

    def _convert_numeric_value_from_device(self, value):
        """Convert to expected data type"""

        if self.data_type == ErdDataType.INT:
            return int(round(value))
        else:
            return value

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        return self._native_unit_of_measurement

    @property
    def state_class(self) -> Optional[str]:
        return self._state_class

    async def set_value(self, value):
        """Sets the ERD value, assumes that the data type is correct"""
        try:
            await self.appliance.async_set_erd_value(self.erd_code, value) 
        except:
            _LOGGER.warning(f"Could not set {self.name} to {value}")