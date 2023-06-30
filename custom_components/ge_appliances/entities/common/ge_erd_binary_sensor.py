from __future__ import annotations

from typing import Optional

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import EntityCategory

from ...api import ErdCode, ErdCodeType, ErdCodeClass
from ...devices import ApplianceApi
from .ge_erd_entity import GeErdEntity


class GeErdBinarySensor(GeErdEntity, BinarySensorEntity):
    """GE Entity for binary sensors"""
    def __init__(
        self,
        api: ApplianceApi,
        erd_code: ErdCodeType,
        name: str,
        device_class: str = None,
        entity_category: str[EntityCategory] | None = EntityCategory.DIAGNOSTIC,
        icon: str = None, 
    ) -> None:
        super().__init__(
            api=api,
            erd_code=erd_code,
            device_class=device_class,
            entity_category=entity_category,
            icon=icon,
            name=name,
        )

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self._boolify(self.appliance.get_erd_value(self.erd_code))
