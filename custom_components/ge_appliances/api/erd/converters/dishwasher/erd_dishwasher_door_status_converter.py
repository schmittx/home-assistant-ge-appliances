import logging

from .....api.erd.converters.abstract import ErdReadOnlyConverter
from .....api.erd.converters.primitives import *
from .....api.erd.values.dishwasher import ErdDishwasherDoorStatus

_LOGGER = logging.getLogger(__name__)

class ErdDishwasherDoorStatusConverter(ErdReadOnlyConverter[ErdDishwasherDoorStatus]):
    def erd_decode(self, value: str) -> ErdDishwasherDoorStatus:
        """ Decodes the dishwasher door state """    
        try:  
            return ErdDishwasherDoorStatus(erd_decode_int(value))          
        except (ValueError, KeyError):
            return ErdDishwasherDoorStatus.NA
