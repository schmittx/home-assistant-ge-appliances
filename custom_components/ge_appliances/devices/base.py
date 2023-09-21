import asyncio
import logging
from typing import Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..api import GeAppliance
from ..api.erd import ErdCode, ErdCodeType, ErdApplianceType
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ApplianceApi:
    """
    API class to represent a single physical device.

    Since a physical device can have many entities, we"ll pool common elements here
    """
    APPLIANCE_TYPE = None  # type: Optional[ErdApplianceType]

    def __init__(self, coordinator: DataUpdateCoordinator, appliance: GeAppliance):
        if not appliance.initialized:
            raise RuntimeError("Appliance not ready")
        self._appliance = appliance
        self._loop = appliance.client.loop
        self._hass = coordinator.hass
        self.coordinator = coordinator
        self.initial_update = False
        self._entities = {}  # type: Optional[Dict[str, Entity]]

    @property
    def hass(self) -> HomeAssistant:
        return self._hass

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        if self._loop is None:
            self._loop = self._appliance.client.loop
        return self._loop

    @property
    def appliance(self) -> GeAppliance:
        return self._appliance

    @appliance.setter
    def appliance(self, value: GeAppliance):
        self._appliance = value

    @property
    def available(self) -> bool:
        #Note - online will be there since we're using the GE coordinator
        #Didn't want to deal with the circular references to get the type hints
        #working.
        return self.appliance.available and self.coordinator.online

    @property
    def serial_number(self) -> str:
        return self.appliance.get_erd_value(ErdCode.SERIAL_NUMBER)

    @property
    def mac_addr(self) -> str:
        return self.appliance.mac_addr

    @property
    def serial_or_mac(self) -> str:
        def is_zero(val: str) -> bool:
            try:
                intVal = int(val)
                return intVal == 0
            except:
                return False
    
        if (self.serial_number and not 
            self.serial_number.isspace() and not 
            is_zero(self.serial_number)):
            return self.serial_number
        return self.mac_addr

    @property
    def model_number(self) -> str:
        return self.appliance.get_erd_value(ErdCode.MODEL_NUMBER)

    @property
    def appliance_sw_version(self) -> str:
        return self.try_get_erd_value(ErdCode.APPLIANCE_SW_VERSION)

    @property
    def wifi_module_sw_version(self) -> str:
        return self.try_get_erd_value(ErdCode.WIFI_MODULE_SW_VERSION)

    @property
    def name(self) -> str:
        appliance_type = self.appliance.appliance_type
        if appliance_type is None or appliance_type == ErdApplianceType.UNKNOWN:
            appliance_type = "Appliance"
        else:
            appliance_type = appliance_type.name.replace("_", " ").title()
        return f"{appliance_type} {self.serial_or_mac}"

    @property
    def device_info(self) -> DeviceInfo:
        """Device info dictionary."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.serial_or_mac)},
            manufacturer="GE",
            model=self.model_number,
            name=self.name,
            sw_version=self.appliance_sw_version,
#            hw_version=self.hw_version,
        )

    @property
    def entities(self) -> List[Entity]:
        return list(self._entities.values())

    def get_all_entities(self) -> List[Entity]:
        """Create Entities for this device."""
        return self.get_base_entities()

    def get_base_entities(self) -> List[Entity]:
        """Create base entities (i.e. common between all appliances)."""
        from ..entities import GeErdSensor, GeErdSwitch
        entities = [
            GeErdSensor(
                api=self,
                erd_code=ErdCode.CLOCK_TIME,
                name="Clock Time",
            ),
            GeErdSwitch(
                api=self,
                erd_code=ErdCode.SABBATH_MODE,
                name="Sabbath Mode",
            ),
        ]
        return entities        

    def build_entities_list(self) -> None:
        """Build the entities list, adding anything new."""
        from ..entities import GeErdEntity
        entities = [
            e for e in self.get_all_entities()
            if not isinstance(e, GeErdEntity) or e.erd_code in self.appliance.known_properties
        ]

        for entity in entities:
            if entity.unique_id not in self._entities:
                self._entities[entity.unique_id] = entity

    def try_get_erd_value(self, code: ErdCodeType):
        try:
            return self.appliance.get_erd_value(code)
        except:
            return None
    
    def has_erd_code(self, code: ErdCodeType):
        try:
            self.appliance.get_erd_value(code)
            return True
        except:
            return False
