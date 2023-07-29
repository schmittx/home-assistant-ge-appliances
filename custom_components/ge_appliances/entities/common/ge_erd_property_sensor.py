from __future__ import annotations

import magicattr
from typing import Optional

from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import EntityCategory

from ...api import ErdCode, ErdCodeType, ErdMeasurementUnits, ErdDataType
from ...devices import ApplianceApi
from .ge_erd_sensor import GeErdSensor


class GeErdPropertySensor(GeErdSensor):
    """GE Entity for sensors"""
    def __init__(   
        self,
        api: ApplianceApi,
        erd_code: ErdCodeType,
        erd_property: str,
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
            data_type=data_type,
            native_unit_of_measurement=native_unit_of_measurement,
            state_class=state_class,
        )
        self.erd_property = erd_property

    @property
    def unique_id(self) -> Optional[str]:
        return f"{super().unique_id}_{self.erd_property}"

    @property
    def native_value(self):
        try:
            value = magicattr.get(self.appliance.get_erd_value(self.erd_code), self.erd_property)

            # if it's a numeric data type, return it directly
            if self.data_type in [ErdDataType.INT, ErdDataType.FLOAT]:
                return value

            # otherwise, return a stringified version
            # TODO: perhaps enhance so that there's a list of variables available
            #       for the stringify function to consume...
            return self._stringify(value, temp_units=self._temp_units)
        except KeyError:
            return None