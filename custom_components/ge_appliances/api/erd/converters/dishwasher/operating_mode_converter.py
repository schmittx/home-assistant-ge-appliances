import logging

from .....api.erd.converters.abstract import ErdReadOnlyConverter
from .....api.erd.converters.primitives import *
from .....api.erd.values.dishwasher import ErdOperatingMode, OperatingMode, OPERATING_MODE_MAP

_LOGGER = logging.getLogger(__name__)

class OperatingModeConverter(ErdReadOnlyConverter[OperatingMode]):
    def erd_decode(self, value: str) -> OperatingMode:
        """Decode the dishwasher operating state """
        try:
            operating_mode = ErdOperatingMode(erd_decode_int(value))
            _LOGGER.debug(f'raw operating mode value: {operating_mode}')
#            return OPERATING_MODE_MAP[om]
            return operating_mode
        except (KeyError, ValueError):
            return ErdOperatingMode.INVALID
