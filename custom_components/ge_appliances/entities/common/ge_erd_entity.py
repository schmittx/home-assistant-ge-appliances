from __future__ import annotations

from datetime import timedelta
from typing import Optional

from homeassistant.const import EntityCategory

from ...api import ErdCode, ErdCodeType, ErdCodeClass, ErdMeasurementUnits
from ...const import DOMAIN
from ...devices import ApplianceApi
from .ge_entity import GeEntity


class GeErdEntity(GeEntity):
    """Parent class for GE entities tied to a specific ERD"""

    def __init__(
        self,
        api: ApplianceApi,
        erd_code: ErdCodeType,
        name: str,
        device_class: str = None,
        entity_category: str[EntityCategory] | None = None,
        icon: str = None,
    ) -> None:
        super().__init__(
            api=api,
        )
        self._device_class = device_class
        self._entity_category = entity_category
        self._erd_code = api.appliance.translate_erd_code(erd_code)
        self._erd_code_class = api.appliance.get_erd_code_class(self._erd_code)
        self._icon = icon
        self._name = name

        if not self._erd_code_class:
            self._erd_code_class = ErdCodeClass.GENERAL

    @property
    def erd_code(self) -> ErdCodeType:
        return self._erd_code

    @property
    def erd_code_class(self) -> ErdCodeClass:
        return self._erd_code_class

    @property
    def erd_string(self) -> str:
        erd_code = self.erd_code
        if isinstance(self.erd_code, ErdCode):
            return erd_code.name
        return erd_code

    @property
    def name(self) -> Optional[str]:
        return f"{self.device_info['name']} {self._name}"
#        return f"{self.serial_or_mac} {self._name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self.serial_or_mac}_{self.erd_string.lower()}"

    def _stringify(self, value: any, **kwargs) -> Optional[str]:
        """Stringify a value"""
        # perform special processing before passing over to the default method
        if self.erd_code == ErdCode.CLOCK_TIME:
            return value.strftime("%H:%M:%S") if value else None
        if self.erd_code_class == ErdCodeClass.RAW_TEMPERATURE:
            return f"{value}"
        if self.erd_code_class == ErdCodeClass.NON_ZERO_TEMPERATURE:
            return f"{value}" if value else ""
        if self.erd_code_class == ErdCodeClass.TIMER or isinstance(value, timedelta):
#            return str(value)[:-3] if value else "Off"
            return value
        if value is None:
            return None
        return self.appliance.stringify_erd_value(value, **kwargs)
#        return "_".join(self.appliance.stringify_erd_value(value, **kwargs).split()).lower()

    @property
    def _measurement_system(self) -> Optional[ErdMeasurementUnits]:
        """
        Get the measurement system this appliance is using.  For now, uses the
        temperature unit if available, otherwise assumes imperial.
        """
        try:
            value = self.appliance.get_erd_value(ErdCode.TEMPERATURE_UNIT)
        except KeyError:
            return ErdMeasurementUnits.Imperial
        return value

    def _get_icon(self):
        """Select an appropriate icon."""
        return self._icon

    def _get_device_class(self) -> Optional[str]:
        return self._device_class

    def _get_entity_category(self) -> str[EntityCategory]:
        return self._entity_category
