from __future__ import annotations

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import EntityCategory

from ...api import ErdCodeType
from ...devices import ApplianceApi
from .bool_converter import BoolConverter
from .ge_erd_entity import GeErdEntity

_LOGGER = logging.getLogger(__name__)

class GeErdSwitch(GeErdEntity, SwitchEntity):
    """Switches for boolean ERD codes."""
    def __init__(
        self,
        api: ApplianceApi,
        erd_code: ErdCodeType,
        name: str,
        device_class: str = None,
        entity_category: str[EntityCategory] | None = EntityCategory.CONFIG,
        icon: str = None,
        bool_converter: BoolConverter = BoolConverter(),
    ) -> None:
        super().__init__(
            api=api,
            erd_code=erd_code,
            device_class=device_class,
            entity_category=entity_category,
            icon=icon,
            name=name,
        )
        self._converter = bool_converter

    @property
    def is_on(self) -> bool:
        """Return True if switch is on."""
        return self._converter.boolify(self.appliance.get_erd_value(self.erd_code))

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.debug(f"Turning on {self.unique_id}")
        await self.appliance.async_set_erd_value(self.erd_code, self._converter.true_value())

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.debug(f"Turning on {self.unique_id}")
        await self.appliance.async_set_erd_value(self.erd_code, self._converter.false_value())
