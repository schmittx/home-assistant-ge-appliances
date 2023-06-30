from __future__ import annotations

from typing import Optional
import magicattr

from homeassistant.const import EntityCategory

from ...api import ErdCodeType
from ...devices import ApplianceApi
from .ge_erd_binary_sensor import GeErdBinarySensor

class GeErdPropertyBinarySensor(GeErdBinarySensor):
    """GE Entity for property binary sensors"""
    def __init__(
        self,
        api: ApplianceApi,
        erd_code: ErdCodeType,
        erd_property: str,
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
        self.erd_property = erd_property

    @property
    def unique_id(self) -> Optional[str]:
        return f"{super().unique_id}_{self.erd_property}"

    @property
    def is_on(self) -> Optional[bool]:
        """Return True if entity is on."""
        try:
            value = magicattr.get(self.appliance.get_erd_value(self.erd_code), self.erd_property)
        except KeyError:
            return None
        if self._name:
            if "Enabled" in self._name:
                return bool(self._stringify(value) == "enable")
        return self._boolify(value)
